from django.db import models


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


class StopWord(models.Model):
    word = models.ForeignKey(
        to=Word,
        on_delete=models.CASCADE,
    )
    reference = models.ForeignKey(
        to='Reference',
        on_delete=models.CASCADE,
    )


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


def add_word(string: str) -> int:
    word = Word.objects.filter(string=string).first()
    if word:
        return word.pk
    from datetime import datetime
    now = datetime.utcnow()
    # todo tedade raghamashu say kon yeki koni masalan mahe 6 ro bokon mahe 06
    code = f'{now.year}{now.month}{now.day}{now.hour}{now.minute}{now.second}{now.microsecond}'
    code = int(code)
    word = Word()
    word.string = string
    word.code = code
    word.save()
    return word.pk


def add_stopword(string: str, reference_id: int) -> int:
    stopword = StopWord.objects.filter(reference_id=reference_id).filter(word__string=string).first()
    if stopword:
        return stopword.pk
    word_id = add_word(string)
    stopword = StopWord()
    stopword.word_id = word_id
    stopword.reference_id = reference_id
    stopword.save()
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
    title_code = word2code(category_title)
    category = Category()
    category.title = category_title
    category.title_code = title_code
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
        content_string: str,
        category_id: int,
        reference_id: int,
        vector: dict = None
):
    from nvd.pre_processing import normilizer, tokenizer, without_stopword
    titr_words = tokenizer(titr_string)
    titr_words_without_stopword = []
    for sent in titr_words:
        titr_words_without_stopword.append(without_stopword(sent))
    content_words = tokenizer(content_string)
    content_words_without_stopword = []
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
