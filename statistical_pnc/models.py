import logging

from django.db import models
from nvd.pre_processing import normilizer, tokenizer
from nvd.extractor import Keywords
from classification.settings import BASE_DICT

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
            word.save()
        BASE_DICT.set_item(word_key, word)
    logging.info(f'Word String: {string} -> Available in memory.')
    return word


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

    @property
    def code(self):
        return str(self.pk)

    def __str__(self):
        return self.string


def content2db(string: str) -> Content:
    content = Content()
    string = NORMILIZER(string)
    content.string = string
    content.save()
    words_string = WORD_TOKENIZER(string)
    for sent in words_string:
        for word_string in sent:
            word = word2db(word_string)
            word._number_of_repetitions += 1
            word.save()
            content.words.add(word)
    content.save()
    logging.info(f'Content String: {string} -> Available in memory.')
    return content


class Titr(models.Model):
    string = models.TextField()
    words = models.ManyToManyField(
        to='Word',
    )

    @property
    def code(self):
        return str(self.pk)

    def __str__(self):
        return self.string


def titr2db(string: str) -> Titr:
    titr = Titr()
    string = NORMILIZER(string)
    titr.string = string
    titr.save()
    words_string = WORD_TOKENIZER(string)
    for sent in words_string:
        for word_string in sent:
            word = word2db(word_string)
            word._number_of_repetitions += 1
            word.save()
            titr.words.add(word)
    titr.save()
    logging.info(f'Titr string: {string} -> Available in memory.')
    return titr


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

def symbol2db(reference: Reference = None, reference_title: str = None, word: Word = None,
              string: str = None) -> Symbol:
    if reference is None:
        if reference_title is None:
            raise Exception('Refrence(or reference title) is not define... .')
        reference = reference2db(reference_title)
    if word is None:
        if string is None:
            raise Exception('Word(or string) is not define... .')
        word = word2db(string)
    symbol = Symbol.objects.filter(reference=reference).filter(word=word).first()
    if symbol is None:
        symbol = Symbol(reference=reference, word=word)
        symbol.save()
        logging.info(f'Symbol string: {string} -> Stored in bata base.')
    logging.info(f'Symbol string: {string} -> Available in memory.')
    return symbol


class StopWord(models.Model):
    reference = models.ForeignKey(
        to='Reference',
        on_delete=models.CASCADE,
    )
    word = models.ForeignKey(
        to='Word',
        on_delete=models.CASCADE,
    )


def stopword2db(reference: Reference = None, reference_title: str = None, word: Word = None,
                string: str = None) -> StopWord:
    if reference is None:
        if reference_title is None:
            raise Exception('Refrence(or reference title) is not define... .')
        reference = reference2db(reference_title)
    if word is None:
        if string is None:
            raise Exception('Word(or string) is not define... .')
        word = word2db(string)
    stopword = StopWord.objects.filter(reference=reference).filter(word=word).first()
    if stopword is None:
        stopword = StopWord(reference=reference, word=word)
        stopword.save()
        logging.info(f'Stop word string: {string} -> Stored in bata base.')
    logging.info(f'Stop word string: {string} -> Available in memory.')
    return stopword


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


def statistical_word_category2db(word: Word, category: Category, docs_frequency: int = None) -> StatisticalWordCategory:
    _obj = StatisticalWordCategory.objects.filter(word=word).filter(category=category).first()
    if _obj is None:
        _obj = StatisticalWordCategory()
        _obj.word = word
        _obj.category = category
        _obj.all_docs_frequency = [docs_frequency]
        _obj.docs_frequency_mean = docs_frequency
        _obj.docs_frequency_stdev = 0
        _obj.save()
        logging.info(f'Statical-word::category-: {word.string}::{category.title} -> Stored in bata base.')
        return _obj
    from statistics import mean, stdev
    tmp = list(_obj.all_docs_frequency)
    tmp.append(docs_frequency)
    _obj.all_docs_frequency = tmp
    _obj.docs_frequency_mean = mean(tmp)
    _obj.docs_frequency_stdev = stdev(tmp)
    _obj.save()
    logging.info(f'Statical-word::category-: {word.string}::{category.title} -> Available in memory.')
    return _obj


class News(models.Model):
    reference = models.ForeignKey(
        to='Reference',
        on_delete=models.CASCADE,
        blank=False,
        null=False,
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
    )
    titr = models.ForeignKey(
        to='Titr',
        on_delete=models.CASCADE,
    )
    category = models.ForeignKey(
        to='Category',
        on_delete=models.CASCADE,
    )
    keywords = models.ManyToManyField(
        to='Word',
        related_name='sn_keywords',
    )


def news2db(titr_string: str, content_string: str, category_title: str, reference: Reference = None,
            reference_title: str = None) -> News:
    if reference is None:
        if reference_title is None:
            raise Exception('Refrence(or reference title) is not define... .')
        reference = reference2db(reference_title)
    news = News()
    news.reference = reference
    news.titr = titr2db(titr_string)
    news.content = content2db(content_string)
    news.string = f'{news.titr.string} {news.content.string}'

    category = category2db(title=category_title, reference=reference)
    category._number_of_subcategories += 1
    category.save()

    news.category = category
    news.save()
    for wrd in news.titr.words.all():
        news.words_tokenize.add(wrd)
    for wrd in news.content.words.all():
        news.words_tokenize.add(wrd)
    for wrd in news.words_tokenize.all():
        if wrd not in news.words.all():
            news.words.add(wrd)

    doc = WORD_TOKENIZER(news.string)
    keywords = KEYWORDS_EXTRACTOR(document=doc, stopword=1, sents=1)
    for keyword in keywords:
        word = word2db(keyword['word'])
        news.keywords.add(word)
        statistical_word_category2db(word, category, docs_frequency=keyword['frequency'])
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


def stopwords_list(reference: Reference = None, reference_title: str = None) -> list:
    if reference is None:
        if reference_title is None:
            raise Exception('Refrence(or reference title) is not define... .')
        reference = reference2db(reference_title)
    stpwrds = StopWord.objects.filter(reference=reference).all()
    if stpwrds is None:
        return []
    stpwrds_list = []
    for stpwrd in stpwrds:
        stpwrds_list.append(stpwrd.word.string)
    return stpwrds_list


def symbols_list(reference: Reference = None, reference_title: str = None) -> list:
    if reference is None:
        if reference_title is None:
            raise Exception('Refrence(or reference title) is not define... .')
        reference = reference2db(reference_title)
    syms = Symbol.objects.filter(reference=reference).all()
    if syms is None:
        return []
    syms_list = []
    for sym in syms:
        syms_list.append(sym.word.string)
    return syms_list


def categories_list(reference: Reference = None, reference_title: str = None, vector: bool = False):
    if reference is None:
        if reference_title is None:
            raise Exception('Refrence(or reference title) is not define... .')
        reference = reference2db(reference_title)
    cats = Category.objects.filter(reference=reference).all()
    if not vector:
        cats_list = {}
        for cat in cats:
            cats_list[cat.pk] = cat.title
        return cats_list
    vector_len = Word.objects.last()
    vector_len = vector_len.pk
    cats_list = {}
    for cat in cats:
        vector = [0] * vector_len
        cat_statistical = StatisticalWordCategory.objects.filter(category=cat).all()
        for cs in cat_statistical:
            vector[int(cs.word.pk)] = cs.docs_frequency_mean
        cats_list[cat.pk] = vector
    return cats_list
# ALL_NEWS = get_all_news()
