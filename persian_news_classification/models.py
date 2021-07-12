from django.db import models


class Reference(models.Model):
    title = models.CharField(
        max_length=128,
        blank=False,
        null=False,
    )


class Category(models.Model):
    title = models.CharField(
        max_length=128,
        blank=False,
        null=False,
    )
    reference = models.ForeignKey(
        to=Reference,
        on_delete=models.CASCADE,
        blank=False,
        null=False,
    )


class News(models.Model):
    titr_string = models.CharField(
        max_length=512,
        blank=False,
        null=False,
    )
    titr_words = models.JSONField(
        blank=False,
        null=False,
    )
    titr_words_without_stopword = models.JSONField(
        blank=False,
        null=False,
    )
    content_string = models.TextField(
        blank=False,
        null=False,
    )
    content_words = models.JSONField(
        blank=False,
        null=False,
    )
    content_words_without_stopword = models.JSONField(
        blank=False,
        null=False,
    )
    category = models.ForeignKey(
        to=Category,
        on_delete=models.CASCADE,
        blank=False,
        null=False,
    )
    vector = models.JSONField(
        blank=True,
        null=True,
    )
    reference = models.ForeignKey(
        to=Reference,
        on_delete=models.CASCADE,
        blank=False,
        null=False,
    )


def add_category(category_title: str, reference_id: int):
    category = Category()
    category.title = category_title
    category.reference_id = reference_id
    category.save()
    return category.pk


def add_reference(reference_title: str):
    reference = Reference()
    reference.title = reference_title
    reference.save()
    return reference.pk


def add_news(
        titr_string: str,
        titr_words: dict,
        titr_words_without_stopword: dict,
        content_string: str,
        content_words: dict,
        content_words_without_stopword: dict,
        category_id: int,
        reference_id: int,
        vector: dict = None
):
    news = News()
    news.titr_string = titr_string
    news.titr_words = titr_words
    news.titr_words_without_stopword = titr_words_without_stopword
    news.content_string = content_string
    news.content_words = content_words
    news.content_words_without_stopword = content_words_without_stopword
    news.category_id = category_id
    if vector:
        news.vector = vector
    news.reference_id = reference_id
    news.save()
    return news.pk


def update_news(
        news_id: int,
        titr_string: str = None,
        titr_words: dict = None,
        titr_words_without_stopword: dict = None,
        content_string: str = None,
        content_words: dict = None,
        content_words_without_stopword: dict = None,
        category_id: int = None,
        reference_id: int = None,
        vector: dict = None
):
    news = News.objects.get(pk=news_id)
    if news is None:
        return False

    if titr_string:
        news.titr_string = titr_string

    if titr_words:
        news.titr_words = titr_words

    if titr_words_without_stopword:
        news.titr_words_without_stopword = titr_words_without_stopword

    if content_string:
        news.content_string = content_string

    if content_words:
        news.content_words = content_words

    if content_words_without_stopword:
        news.content_words_without_stopword = content_words_without_stopword

    if category_id:
        news.category_id = category_id

    if reference_id:
        news.reference_id = reference_id

    if vector:
        news.vector = vector

    news.save()
    return True
