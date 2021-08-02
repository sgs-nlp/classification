from django.db import models
import logging
import os


def get_upload_to(instance, file_name):
    from uuid import uuid4

    _uuid = uuid4()
    _uuid2 = uuid4()
    ext = file_name.split('.')[-1]
    return "files/{}.{}".format(str(_uuid), str(_uuid2), ext)


class Word(models.Model):
    string = models.CharField(
        max_length=64,
        null=False,
        blank=False,
    )
    code = models.CharField(
        max_length=32,
        null=False,
        blank=False,
    )

    def __iter__(self):
        yield 'pk', self.pk
        yield 'string', self.string
        yield 'code', self.code


class StopWord(models.Model):
    word = models.ForeignKey(
        to=Word,
        on_delete=models.CASCADE,
    )
    reference = models.ForeignKey(
        to='Reference',
        on_delete=models.CASCADE,
    )

    def __iter__(self):
        yield 'pk', self.pk
        yield 'word', dict(self.word)
        yield 'reference', dict(self.reference)


class Reference(models.Model):
    title = models.CharField(
        max_length=128,
        blank=False,
        null=False,
    )
    load_complate_flag = models.BooleanField(
        default=False,
    )
    length = models.IntegerField(
        default=0,
    )
    stopwords_list = models.JSONField(
        blank=True,
        null=True,
    )
    categories_list = models.JSONField(
        blank=True,
        null=True,
    )
    titr_string_flag = models.BooleanField(
        default=False,
    )
    titr_string_code_flag = models.BooleanField(
        default=False,
    )
    titr_words_flag = models.BooleanField(
        default=False,
    )
    titr_words_code_flag = models.BooleanField(
        default=False,
    )
    titr_words_without_stopword_flag = models.BooleanField(
        default=False,
    )
    titr_words_without_stopword_code_flag = models.BooleanField(
        default=False,
    )
    content_string_flag = models.BooleanField(
        default=False,
    )
    content_string_code_flag = models.BooleanField(
        default=False,
    )
    content_words_flag = models.BooleanField(
        default=False,
    )
    content_words_code_flag = models.BooleanField(
        default=False,
    )
    content_words_without_stopword_flag = models.BooleanField(
        default=False,
    )
    content_words_without_stopword_code_flag = models.BooleanField(
        default=False,
    )
    category_flag = models.BooleanField(
        default=False,
    )
    vector_flag = models.BooleanField(
        default=False,
    )
    keywords_flag = models.BooleanField(
        default=False,
    )

    def __iter__(self):
        yield 'pk', self.pk
        yield 'title', self.title
        yield 'length', self.length
        yield 'stopwords_list', dict(self.stopwords_list)
        yield 'categories_list', dict(self.categories_list)
        yield 'titr_string_flag', self.titr_string_flag
        yield 'titr_string_code_flag', self.titr_string_code_flag
        yield 'titr_words_flag', self.titr_words_flag
        yield 'titr_words_code_flag', self.titr_words_code_flag
        yield 'titr_words_without_stopword_flag', self.titr_words_without_stopword_flag
        yield 'titr_words_without_stopword_code_flag', self.titr_words_without_stopword_code_flag
        yield 'content_string_flag', self.content_string_flag
        yield 'content_string_code_flag', self.content_string_code_flag
        yield 'content_words_flag', self.content_words_flag
        yield 'content_words_code_flag', self.content_words_code_flag
        yield 'content_words_without_stopword_flag', self.content_words_without_stopword_flag
        yield 'content_words_without_stopword_code_flag', self.content_words_without_stopword_code_flag
        yield 'category_flag', self.category_flag
        yield 'vector_flag', self.vector_flag
        yield 'keywords_flag', self.keywords_flag


class Category(models.Model):
    title = models.CharField(
        max_length=128,
        blank=False,
        null=False,
    )
    title_code = models.CharField(
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

    def __iter__(self):
        yield 'pk', self.pk
        yield 'title', self.title
        yield 'title_code', self.title_code
        yield 'reference', dict(self.reference)


class News(models.Model):
    titr_string = models.TextField(
        blank=False,
        null=False,
    )
    titr_string_code = models.TextField(
        blank=False,
        null=False,
    )
    titr_words = models.JSONField(
        blank=False,
        null=False,
    )
    titr_words_code = models.JSONField(
        blank=False,
        null=False,
    )
    titr_words_without_stopword = models.JSONField(
        blank=False,
        null=False,
    )
    titr_words_without_stopword_code = models.JSONField(
        blank=False,
        null=False,
    )
    content_string = models.TextField(
        blank=False,
        null=False,
    )
    content_string_code = models.TextField(
        blank=False,
        null=False,
    )
    content_words = models.JSONField(
        blank=False,
        null=False,
    )
    content_words_code = models.JSONField(
        blank=False,
        null=False,
    )
    content_words_without_stopword = models.JSONField(
        blank=False,
        null=False,
    )
    content_words_without_stopword_code = models.JSONField(
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
    keywords = models.JSONField(
        blank=True,
        null=True,
    )

    def __iter__(self):
        yield 'titr_string', self.titr_string
        yield 'titr_string_code', self.titr_string_code
        yield 'titr_words', dict(self.titr_words)
        yield 'titr_words_code', dict(self.titr_words_code)
        yield 'titr_words_without_stopword', dict(self.titr_words_without_stopword)
        yield 'titr_words_without_stopword_code', dict(self.titr_words_without_stopword_code)
        yield 'content_string', self.content_string
        yield 'content_string_code', self.content_string_code
        yield 'content_words', dict(self.content_words)
        yield 'content_words_code', dict(self.content_words_code)
        yield 'content_words_without_stopword', dict(self.content_words_without_stopword)
        yield 'content_words_without_stopword_code', dict(self.content_words_without_stopword_code)
        yield 'category', dict(self.category)
        yield 'vector', dict(self.vector)
        yield 'reference', dict(self.reference)


class File(models.Model):
    title = models.CharField(
        max_length=32,
        null=False,
        blank=False,
    )
    ftype = models.CharField(
        max_length=32,
        null=False,
        blank=False,
    )
    file = models.FileField(
        # upload_to=get_upload_to,
    )


def add_word(string: str) -> int:
    word = Word.objects.filter(string=string).first()
    if word is not None:
        logging.warning(f'String \"{string}\" is available in the database with ID {word.pk}.')
        return word.pk
    from datetime import datetime
    now = datetime.utcnow()
    # code = f'{now.year}{now.month}{now.day}{now.hour}{now.minute}{now.second}{now.microsecond}'
    code = int(str(now).replace('-', '').replace(':', '').replace(' ', '').replace('.', ''))
    code = int(code)
    word = Word()
    word.string = string
    word.code = code
    word.save()
    logging.info(f'String {string} with ID {word.pk} is stored in the database.')
    return word.pk


def add_stopword(string: str, reference_id: int) -> int:
    stopword = StopWord.objects.filter(reference_id=reference_id).filter(word__string=string).first()
    if stopword:
        logging.warning(f'String \"{string}\" is available in the database with ID {stopword.pk}.')
        return stopword.pk
    word_id = add_word(string)
    stopword = StopWord()
    stopword.word_id = word_id
    stopword.reference_id = reference_id
    stopword.save()
    logging.info(f'String {string} with ID {stopword.pk} is stored in the database.')
    return stopword.pk


def word2code(string: str) -> str:
    word = Word.objects.filter(string=string).first()
    if word is None:
        word_id = add_word(string)
        word = Word.objects.get(pk=word_id)
    return word.code


def code2word(code: str) -> str:
    code = int(code.rsplit('_', 1)[1])
    word = Word.objects.filter(code=code).first()
    if word:
        return word.string
    return None


def add_category(category_title: str, reference_id: int):
    category = Category.objects.filter(reference_id=reference_id).filter(title=category_title).first()
    if category:
        logging.warning(f'Category title \"{category_title}\" is available in the database with ID {category.pk}.')
        return category.pk
    title_code = word2code(category_title)
    category = Category()
    category.title = category_title
    category.title_code = title_code
    category.reference_id = reference_id
    category.save()
    logging.info(f'Category title {category_title} with ID {category.pk} is stored in the database.')
    return category.pk


def add_reference(reference_title: str):
    reference = Reference.objects.filter(title=reference_title).first()
    if reference:
        logging.warning(f'Reference title \"{reference_title}\" is available in the database with ID {reference.pk}.')
        return reference.pk
    reference = Reference()
    reference.title = reference_title
    reference.save()
    logging.info(f'Reference title {reference_title} with ID {reference.pk} is stored in the database.')
    return reference.pk


def add_news(
        titr_string: str,
        content_string: str,
        category_id: int,
        reference_id: int,
        vector: dict = None
):
    from nvd.pre_processing import normilizer, tokenizer, without_stopword
    logging.info(f'Titr Tokenizer.')
    titr_words = tokenizer(titr_string)
    titr_words_without_stopword = []
    logging.info(f'Titr without stopwords.')
    for sent in titr_words:
        titr_words_without_stopword.append(without_stopword(sent))

    logging.info(f'Content Tokenizer.')
    content_words = tokenizer(content_string)
    content_words_without_stopword = []
    logging.info(f'Content without stopwords.')
    for sent in content_words:
        content_words_without_stopword.append(without_stopword(sent))
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

    # coding
    # ->
    tmp = _lists_coding(titr_words)
    news.titr_string_code = _string_coding(tmp)
    news.titr_words_code = tmp
    news.titr_words_without_stopword_code = _lists_coding(titr_words_without_stopword)
    tmp = _lists_coding(content_words)
    news.content_string_code = _string_coding(tmp)
    news.content_words_code = tmp
    news.content_words_without_stopword_code = _lists_coding(content_words_without_stopword)
    # <-
    news.save()
    logging.info(f'News with ID {news.pk} is stored in the database.')
    return news.pk


def update_news(
        news_id: int,
        titr_string: str = None,
        content_string: str = None,
        category_id: int = None,
        reference_id: int = None,
        vector: dict = None
):
    from nvd.pre_processing import normilizer, tokenizer, without_stopword

    news = News.objects.get(pk=news_id)
    if news is None:
        logging.warning(f'News with ID {news_id} is not exist in the database.')
        return False

    if titr_string:
        news.titr_string = titr_string
        titr_words = tokenizer(titr_string)
        titr_words_without_stopword = []
        for sent in titr_words:
            titr_words_without_stopword.append(without_stopword(sent))
        news.titr_words = titr_words
        news.titr_words_without_stopword = titr_words_without_stopword
        tmp = _lists_coding(titr_words)
        news.titr_string_code = _string_coding(tmp)
        news.titr_words_code = tmp
        news.titr_words_without_stopword_code = _lists_coding(titr_words_without_stopword)

    if content_string:
        news.content_string = content_string
        content_words = tokenizer(content_string)
        content_words_without_stopword = []
        for sent in content_words:
            content_words_without_stopword.append(without_stopword(sent))
        news.content_words = content_words
        news.content_words_without_stopword = content_words_without_stopword
        tmp = _lists_coding(content_words)
        news.content_string_code = _string_coding(content_words)
        news.content_words_code = tmp
        news.content_words_without_stopword_code = _lists_coding(content_words_without_stopword)

    if category_id:
        news.category_id = category_id

    if reference_id:
        news.reference_id = reference_id

    if vector:
        news.vector = vector

    news.save()
    logging.info('News updated.')
    return True


def _string_coding(string: list) -> str:
    _string = ''
    for s in string:
        for w in s:
            _string += w
            _string += ' '
        _string += '\n'
    return _string


def list_coding(words_list: list) -> list:
    _words_list = []
    for word in words_list:
        _words_list.append(word2code(word))
    return _words_list


def _lists_coding(words_lists: list) -> list:
    _words_lists = []
    for sent in words_lists:
        _words_lists.append(list_coding(sent))
    return _words_lists
