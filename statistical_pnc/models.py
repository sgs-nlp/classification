from django.db import models
from nvd.pre_processing import normilizer, tokenizer
from nvd.extractor import Keywords

NORMILIZER = normilizer
WORD_TOKENIZER = tokenizer
KEYWORDS = Keywords(fre=True)
KEYWORDS_EXTRACTOR = KEYWORDS.by_frequency


class Reference(models.Model):
    title = models.CharField(
        max_length=32,
        blank=False,
        null=False,
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


def reference2db(title: str) -> Reference:
    ref = Reference.objects.filter(title=title).first()
    if ref is None:
        ref = Reference(title=title)
        ref.save()
    return ref


class Word(models.Model):
    string = models.CharField(
        max_length=32,
        blank=False,
        null=False,
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


def word2db(string: str) -> Word:
    word = Word.objects.filter(string=string).first()
    if word is not None:
        return word
    word = Word()
    word.string = string
    word.save()
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


def category2db(title: str, reference: Reference = None, reference_title: str = None) -> Category:
    category = Category.objects.filter(title=title).first()
    if category is not None:
        return category
    if reference is None:
        if reference_title is None:
            raise Exception('Refrence(or reference title) is not define... .')
        reference = reference2db(reference_title)
    category = Category(reference=reference)
    category.title = title
    category.save()
    return category


class Content(models.Model):
    string = models.TextField()
    words = models.ManyToManyField(
        to='Word',
    )

    @property
    def code(self):
        return str(self.pk)


def content2db(string: str) -> Content:
    content = Content.objects.filter(string=string).first()
    if content is not None:
        return content

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
    return content


class Titr(models.Model):
    string = models.TextField()
    words = models.ManyToManyField(
        to='Word',
    )

    @property
    def code(self):
        return str(self.pk)


def titr2db(string: str) -> Titr:
    titr = Titr.objects.filter(string=string).first()
    if titr is not None:
        return titr

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
    symbol = Symbol(reference=reference, word=word)
    symbol.save()
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
    stopword = StopWord(reference=reference, word=word)
    stopword.save()
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
        return _obj
    from statistics import mean, stdev
    tmp = list(_obj.all_docs_frequency)
    tmp.append(docs_frequency)
    _obj.all_docs_frequency = tmp
    _obj.docs_frequency_mean = mean(tmp)
    _obj.docs_frequency_stdev = stdev(tmp)
    _obj.save()
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

# ALL_NEWS = get_all_news()
