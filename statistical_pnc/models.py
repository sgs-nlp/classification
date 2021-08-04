from django.db import models
from hazm import Normalizer, WordTokenizer

NORMILIZER = Normalizer()
WORD_TOKENIZER = WordTokenizer()


# todo ; keywords extractor tarif shavad

class KEYWORDS_EXTRACTOR:
    def __init__(self, string: str):
        pass


class Word(models.Model):
    string = models.CharField(
        max_length=32,
        blank=False,
        null=False,
    )
    number_of_repetitions = models.PositiveIntegerField(
        default=0,
    )

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
    title = models.CharField(
        max_length=64,
        null=False,
        blank=False,
    )
    number_of_subcategories = models.PositiveIntegerField(
        default=0,
    )

    @property
    def code(self):
        return str(self.pk)


def category2db(title: str) -> Category:
    category = Category.objects.filter(title=title).first()
    if category is not None:
        return category
    category = Category()
    category.title = title
    category.save()
    return category


class Context(models.Model):
    string = models.TextField()
    words = models.ManyToManyField(
        to='Word',
    )

    @property
    def code(self):
        return str(self.pk)


def context2db(string: str) -> Context:
    context = Context.objects.filter(string=string).first()
    if context is not None:
        return context

    context = Context()
    string = NORMILIZER.normalize(string)
    context.string = string
    context.save()

    words_string = WORD_TOKENIZER.tokenize(string)
    for word_string in words_string:
        word = word2db(word_string)
        word.number_of_repetitions += 1
        word.save()
        context.words.add(word)
    context.save()
    return context


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
    string = NORMILIZER.normalize(string)
    titr.string = string
    titr.save()

    words_string = WORD_TOKENIZER.tokenize(string)
    for word_string in words_string:
        word = word2db(word_string)
        word.number_of_repetitions += 1
        word.save()
        titr.words.add(word)
    titr.save()
    return titr


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
    obj = StatisticalWordCategory.objects.filter(word=word).filter(category=category).first()
    if obj is None:
        obj = StatisticalWordCategory()
        obj.word = word
        obj.category = category
        obj.all_docs_frequency = [docs_frequency]
        obj.docs_frequency_mean = docs_frequency
        obj.docs_frequency_stdev = 0
        obj.save()
        return obj
    from statistics import mean, stdev
    tmp = list(obj.all_docs_frequency)
    tmp = tmp.append(docs_frequency)
    obj.all_docs_frequency = tmp
    obj.docs_frequency_mean = mean(tmp)
    obj.docs_frequency_stdev = stdev(tmp)
    obj.save()
    return obj


class News(models.Model):
    string = models.TextField()
    words_tokenize = models.ManyToManyField(
        to='Word'
    )
    context = models.ForeignKey(
        to='Context',
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
    )


def news2db(titr_string: str, context_string: str, category_title: str) -> News:
    news = News()
    news.titr = titr2db(titr_string)
    news.context = context2db(context_string)
    news.string = f'{news.titr.string} {news.context.string}'

    category = category2db(category_title)
    category.number_of_subcategories += 1
    category.save()

    news.category = category
    news.save()
    words = news.titr.words.all() + news.context.words.all()
    news.words_tokenize.add(words)
    news.save()
    keywords = KEYWORDS_EXTRACTOR(news.string)
    for keyword in keywords:
        word = word2db(keyword['string'])
        news.keywords.add(word)
        statistical_word_category2db(word, category, docs_frequency=keyword['frequency'])
    news.save()

    return news


def get_all_news() -> list:
    objs = News.objects.all()
    news = []
    for obj in objs:
        new = []
        for word in obj.words_tokenize.all():
            new.append(word.code)
        news.append(new)
    return news


ALL_NEWS = get_all_news()
