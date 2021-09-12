import logging

from django.db import models

from classification.settings import BASE_DICT
from nvd.extractor import Keywords
from nvd.hasher import string_hash
from nvd.pre_processing import normilizer, tokenizer

NORMILIZER = normilizer
WORD_TOKENIZER = tokenizer
KEYWORDS = Keywords(fre=True)
KEYWORDS_EXTRACTOR = KEYWORDS.by_frequency


class Reference(models.Model):
    title = models.CharField(
        max_length=64,
        blank=False,
        null=False,
        unique=True,
    )
    load_symbols_list = models.BooleanField(
        default=False,
    )
    load_stopwords_list = models.BooleanField(
        default=False,
    )
    load_complate = models.BooleanField(
        default=False,
    )

    def __str__(self):
        return self.title


def reference2db(title: str) -> Reference:
    ref_key = {'type': 'Reference', 'title': title}
    ref = BASE_DICT.get_item(ref_key)
    if ref is None:
        ref = Reference.objects.filter(title=title).first()
        if ref is None:
            ref = Reference(title=title)
            ref.save()
        BASE_DICT.set_item(ref_key, ref)
    logging.info(f'Reference title: {title} -> Available in memory.')
    return ref


class Word(models.Model):
    string = models.CharField(
        max_length=32,
        blank=False,
        null=False,
        unique=True,
    )
    _number_of_repetitions = models.PositiveIntegerField(
        default=0,
    )
    _hash_code = models.CharField(
        max_length=256,
        null=True,
        blank=True,
    )

    @property
    def hash_code(self):
        if self._hash_code is not None:
            return self._hash_code
        self._hash_code = string_hash(self.string)
        return self._hash_code

    @property
    def number_of_repetitions(self):
        return self._number_of_repetitions

    @property
    def code(self):
        return str(self.pk)

    def __str__(self):
        return self.string


def word2db(string: str) -> Word:
    word_key = {'type': 'Word', 'string': string}
    word = BASE_DICT.get_item(word_key)
    if word is None:
        word = Word.objects.filter(string=string).first()
        if word is None:
            word = Word(string=string)
            word.hash_code
            word.save()
        BASE_DICT.set_item(word_key, word)
    logging.info(f'Word String: {string} -> Available in memory.')
    return word


class StatisticalWordCategory(models.Model):
    word = models.ForeignKey(
        to='Word',
        on_delete=models.CASCADE,
        null=False,
        blank=False,
    )
    category = models.ForeignKey(
        to='Category',
        on_delete=models.CASCADE,
        null=False,
        blank=False,
    )
    all_docs_frequency = models.JSONField(
        null=True,
        blank=True,
    )
    docs_frequency_mean = models.FloatField(
        null=True,
        blank=True,
    )
    docs_frequency_stdev = models.FloatField(
        null=True,
        blank=True,
    )

    def __str__(self):
        return str(self.pk)


class Category(models.Model):
    reference = models.ForeignKey(
        to='Reference',
        on_delete=models.CASCADE,
    )
    title = models.CharField(
        max_length=64,
        null=False,
        blank=False,
    )
    _number_of_subcategories = models.PositiveIntegerField(
        default=0,
    )

    @property
    def vector(self):
        swcs = StatisticalWordCategory.objects.filter(category=self).all()
        word_dict_len = Word.objects.last()
        word_dict_len = word_dict_len.pk
        vector = [0] * word_dict_len
        for swc in swcs:
            vector[swc.word.pk] = swc.docs_frequency_mean
        return vector

    @property
    def number_of_subcategories(self):
        return self._number_of_subcategories

    @property
    def code(self):
        return str(self.pk)

    def __str__(self):
        return self.title


def category2db(title: str, reference: Reference) -> Category:
    cat_key = {'type': 'Category', 'reference': reference, 'title': title}
    category = BASE_DICT.get_item(cat_key)
    if category is None:
        category = Category.objects.filter(reference=reference).filter(title=title).first()
        if category is None:
            category = Category(reference=reference, title=title)
            category.save()
        BASE_DICT.set_item(cat_key, category)
    logging.info(f'Category title: {title} -> Available in memory.')
    return category


class Content(models.Model):
    string = models.TextField()
    words = models.ManyToManyField(
        to='Word',
    )

    _hash_code = models.CharField(
        max_length=256,
        null=True,
        blank=True,
    )

    @property
    def hash_code(self):
        if self._hash_code is not None:
            return self._hash_code
        self._hash_code = string_hash(self.string)
        return self._hash_code

    @property
    def code(self):
        return str(self.pk)

    def __str__(self):
        return self.string


def content2db(string: str) -> Content:
    string = NORMILIZER(string)
    cntnt_key = {'type': 'Content', 'string': string}
    cntnt = BASE_DICT.get_item(cntnt_key)
    if cntnt is None:
        cntnt = Content.objects.filter(_hash_code=string_hash(string)).first()
        if cntnt is None:
            cntnt = Content()
            cntnt.string = string
            cntnt.hash_code
            cntnt.save()
            words_string = WORD_TOKENIZER(string)
            for sent in words_string:
                for word_string in sent:
                    word = word2db(word_string)
                    word._number_of_repetitions += 1
                    word.save()
                    cntnt.words.add(word)
            cntnt.save()
    logging.info(f'Content String: {string} -> Available in memory.')
    return cntnt


class Titr(models.Model):
    string = models.TextField()
    words = models.ManyToManyField(
        to='Word',
    )

    _hash_code = models.CharField(
        max_length=256,
        null=True,
        blank=True,
    )

    @property
    def hash_code(self):
        if self._hash_code is not None:
            return self._hash_code
        self._hash_code = string_hash(self.string)
        return self._hash_code

    @property
    def code(self):
        return str(self.pk)

    def __str__(self):
        return self.string


def titr2db(string: str) -> Titr:
    string = NORMILIZER(string)
    ttr_key = {'type': 'Titr', 'string': string}
    ttr = BASE_DICT.get_item(ttr_key)
    if ttr is None:
        ttr = Titr.objects.filter(_hash_code=string_hash(string)).first()
        if ttr is None:
            ttr = Titr()
            ttr.string = string
            ttr.hash_code
            ttr.save()
            words_string = WORD_TOKENIZER(string)
            for sent in words_string:
                for word_string in sent:
                    word = word2db(word_string)
                    word._number_of_repetitions += 1
                    word.save()
                    ttr.words.add(word)
            ttr.save()
    logging.info(f'Titr string: {string} -> Available in memory.')
    return ttr


class Symbol(models.Model):
    reference = models.ForeignKey(
        to='Reference',
        on_delete=models.CASCADE,
    )
    word = models.ForeignKey(
        to='Word',
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return str(self.word)


def symbol2db(reference: Reference, word: Word) -> Symbol:
    sym_typ = {'type': 'Symbol', 'reference': reference, 'word': word}
    symbol = BASE_DICT.get_item(sym_typ)
    if symbol is None:
        symbol = Symbol.objects.filter(reference=reference).filter(word=word).first()
        if symbol is None:
            symbol = Symbol(reference=reference, word=word)
            symbol.save()
        BASE_DICT.set_item(sym_typ, symbol)
    logging.info(f'Symbol : {symbol} -> Available in memory.')
    return symbol


class StopWord(models.Model):
    reference = models.ForeignKey(
        null=True,
        blank=True,
        to='Reference',
        on_delete=models.CASCADE,
    )
    word = models.ForeignKey(
        to='Word',
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return str(self.word)


def stopword2db(word: Word, reference: Reference = None) -> StopWord:
    stpwrd_key = {'type': 'StopWord', 'reference': reference, 'word': word}
    stopword = BASE_DICT.get_item(stpwrd_key)
    if stopword is None:
        stopword = StopWord.objects.filter(reference=reference).filter(word=word).first()
        if stopword is None:
            stopword = StopWord(reference=reference, word=word)
            stopword.save()
        BASE_DICT.set_item(stpwrd_key, stopword)
    logging.info(f'Stop word : {stopword} -> Available in memory.')
    return stopword


def statistical_word_category2db(word: Word, category: Category, docs_frequency: int = None) -> StatisticalWordCategory:
    swc_key = {'type': 'StatisticalWordCategory', 'word': word, 'category': category}
    swc = BASE_DICT.get_item(swc_key)
    if swc is None:
        swc = StatisticalWordCategory.objects.filter(word=word).filter(category=category).first()
        if swc is None:
            swc = StatisticalWordCategory()
            swc.word = word
            swc.category = category
            swc.all_docs_frequency = [docs_frequency]
            swc.docs_frequency_mean = docs_frequency
            swc.docs_frequency_stdev = 0
            swc.save()
            logging.info(f'Statical-word::category-: {word.string}::{category.title} -> Stored in bata base.')
            BASE_DICT.set_item(swc_key, swc)
            return swc
    from statistics import mean, stdev
    tmp = list(swc.all_docs_frequency)
    tmp.append(docs_frequency)
    swc.all_docs_frequency = tmp
    swc.docs_frequency_mean = mean(tmp)
    swc.docs_frequency_stdev = stdev(tmp)
    swc.save()
    logging.info(f'Statical-word::category-: {word.string}::{category.title} -> Available in memory.')
    BASE_DICT.set_item(swc_key, swc)
    return swc


class News(models.Model):
    reference = models.ForeignKey(
        to='Reference',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    string = models.TextField()
    words = models.ManyToManyField(
        to='Word',
        related_name='sn_words'
    )
    words_tokenize = models.ManyToManyField(
        to='Word',
        related_name='sn_words_tokenize'
    )
    content = models.ForeignKey(
        to='Content',
        on_delete=models.CASCADE,
        blank=False,
        null=False,
    )
    titr = models.ForeignKey(
        to='Titr',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    category = models.ForeignKey(
        to='Category',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )

    _vector = models.JSONField(
        null=True,
        blank=True,
    )

    @property
    def vector(self):
        word_dict_len = Word.objects.last()
        word_dict_len = word_dict_len.pk
        if len(self._vector) == word_dict_len:
            return self._vector

        self.vector = self._vector + [0] * (word_dict_len - len(self._vector))
        return self._vector

    @vector.setter
    def vector(self, value):
        self._vector = value

    _hash_code = models.CharField(
        max_length=256,
        null=True,
        blank=True,
    )

    @property
    def hash_code(self):
        if self._hash_code is not None:
            return self._hash_code
        self._hash_code = string_hash(self.string)
        return self._hash_code

    def __str__(self):
        return str(self.string)


class Keyword(models.Model):
    news = models.ForeignKey(
        to='News',
        on_delete=models.CASCADE,
        blank=False,
        null=False,
    )
    word = models.ForeignKey(
        to='Word',
        on_delete=models.CASCADE,
        blank=False,
        null=False,
    )
    frequency = models.FloatField(
        blank=False,
        null=False,
    )

    def __str__(self):
        return str(self.word)


def keyword2db(news: News, word: Word, frequency: float) -> Keyword:
    kw_key = {'type': 'Keyword', 'news': news, 'word': word}
    kywrd = BASE_DICT.get_item(kw_key)
    if kywrd is None:
        kywrd = Keyword.objects.filter(news=news).filter(word=word).first()
        if kywrd is None:
            kywrd = Keyword(news=news, word=word, frequency=frequency)
            kywrd.save()
        BASE_DICT.set_item(kw_key, kywrd)
    logging.info(f'Stop word : {kywrd} -> Available in memory.')
    return kywrd


def news2db(content_string: str, titr_string: str = None, category: Category = None,
            reference: Reference = None) -> News:
    if titr_string is not None and content_string is not None:
        string = NORMILIZER(str(titr_string) + str(content_string))
    elif titr_string is None and content_string is not None:
        string = NORMILIZER(str(content_string))
    elif titr_string is not None and content_string is None:
        string = NORMILIZER(str(titr_string))
    else:
        string = NORMILIZER('Empty String')
    nws_key = {'type': 'News', 'string': string}
    nws = BASE_DICT.get_item(nws_key)
    if nws is None:
        nws = News.objects.filter(_hash_code=string_hash(string)).first()
        if nws is None:
            nws = News()
            nws.content = content2db(content_string)
            if reference is not None:
                nws.reference = reference
            if titr_string is not None:
                nws.titr = titr2db(titr_string)
                nws.string = f'{nws.titr.string} {nws.content.string}'
            else:
                nws.string = f'{nws.content.string}'
            if category is not None:
                category._number_of_subcategories += 1
                category.save()
                nws.category = category
            nws.hash_code
            nws.save()
            if titr_string is not None:
                for wrd in nws.titr.words.all():
                    nws.words_tokenize.add(wrd)
            for wrd in nws.content.words.all():
                nws.words_tokenize.add(wrd)
            for wrd in nws.words_tokenize.all():
                if wrd not in nws.words.all():
                    nws.words.add(wrd)

            doc = WORD_TOKENIZER(nws.string)
            keywords = KEYWORDS_EXTRACTOR(document=doc, stopword=1, sents=1)
            nws_vector = [0]
            for keyword in keywords:
                word = word2db(keyword['word'])
                keyword2db(news=nws, word=word, frequency=keyword['frequency'])
                if len(nws_vector) < word.pk:
                    nws_vector = nws_vector + [0] * (word.pk - len(nws_vector) + 1)
                    nws_vector[word.pk] = keyword['frequency']
                if category is not None:
                    statistical_word_category2db(word, category, docs_frequency=keyword['frequency'])
            nws.vector = nws_vector
            nws.save()
    return nws


def news_update(news_id: int, content_string: str = None, titr_string: str = None, category_id: int = None,
                reference_id: int = None) -> News:
    news = News.objects.filter(pk=news_id).first()
    if news is None:
        return None
    if content_string is not None:
        news.content_string = content_string
    if titr_string is not None:
        news.titr_string = titr_string
    if category_id is not None:
        category = Category.objects.filter(pk=category_id).first()
        if category is not None:
            news.category = category
    if reference_id is not None:
        reference = Reference.objects.filter(pk=reference_id).first()
        if reference is not None:
            news.reference = reference
    news.save()
    return news


def get_all_news() -> list:
    _objs = News.objects.all()
    news = []
    for _obj in _objs:
        new = []
        for word in _obj.words_tokenize.all():
            new.append(word.code)
        news.append(new)
    return news


def stopwords_list(reference: Reference) -> list:
    swl_key = {'type': 'stopwords_list', 'reference': reference}
    stpwrds_list = BASE_DICT.get_item(swl_key)
    if stpwrds_list is None:
        stpwrds = StopWord.objects.filter(reference=reference).all()
        if stpwrds is None:
            return []
        stpwrds_list = []
        for stpwrd in stpwrds:
            stpwrds_list.append(stpwrd.word.string)
    return stpwrds_list


def symbols_list(reference: Reference) -> list:
    syml_key = {'type': 'symbols_list', 'reference': reference}
    syms_list = BASE_DICT.get_item(syml_key)
    if syms_list is None:
        syms = Symbol.objects.filter(reference=reference).all()
        syms_list = []
        for sym in syms:
            syms_list.append(sym.word.string)
        BASE_DICT.set_item(syml_key, syms_list)
    return syms_list


def categories_list(reference: Reference = None, vector: bool = False):
    if reference is None:
        if vector is False:
            cats_key = {'type': 'categories_list', 'reference': reference, 'vector': False}
            cats_list = BASE_DICT.get_item(cats_key)
            if cats_list is None:
                cats = Category.objects.all()
                cats_list = {}
                for cat in cats:
                    cats_list[cat.pk] = cat.title
                BASE_DICT.set_item(cats_key, cats_list)
            elif len(cats_list) == 0:
                cats = Category.objects.all()
                cats_list = {}
                for cat in cats:
                    cats_list[cat.pk] = cat.title
                BASE_DICT.set_item(cats_key, cats_list)
        else:
            vector_len = Word.objects.last()
            vector_len = int(vector_len.pk)
            cats_key = {'type': 'categories_list', 'reference': reference, 'vector': vector_len}
            cats_list = BASE_DICT.get_item(cats_key)
            if cats_list is None:
                cats = Category.objects.all()
                cats_list = {}
                for cat in cats:
                    cats_list[cat.pk] = cat.vector
                BASE_DICT.set_item(cats_key, cats_list)
            elif len(cats_list) == 0:
                cats = Category.objects.all()
                cats_list = {}
                for cat in cats:
                    cats_list[cat.pk] = cat.title
                BASE_DICT.set_item(cats_key, cats_list)
        return cats_list
    else:
        if vector is False:
            cats_key = {'type': 'categories_list', 'reference': reference, 'vector': False}
            cats_list = BASE_DICT.get_item(cats_key)
            if cats_list is None:
                cats = Category.objects.filter(reference=reference).all()
                cats_list = {}
                for cat in cats:
                    cats_list[cat.pk] = cat.title
                BASE_DICT.set_item(cats_key, cats_list)
            elif len(cats_list) == 0:
                cats = Category.objects.all()
                cats_list = {}
                for cat in cats:
                    cats_list[cat.pk] = cat.title
                BASE_DICT.set_item(cats_key, cats_list)
        else:
            vector_len = Word.objects.last()
            vector_len = int(vector_len.pk)
            cats_key = {'type': 'categories_list', 'reference': reference, 'vector': vector_len}
            cats_list = BASE_DICT.get_item(cats_key)
            if cats_list is None:
                cats = Category.objects.filter(reference=reference).all()
                cats_list = {}
                for cat in cats:
                    cats_list[cat.pk] = cat.vector
                BASE_DICT.set_item(cats_key, cats_list)
            elif len(cats_list) == 0:
                cats = Category.objects.all()
                cats_list = {}
                for cat in cats:
                    cats_list[cat.pk] = cat.title
                BASE_DICT.set_item(cats_key, cats_list)
        return cats_list
