import logging
from pathlib import Path
from scipy.spatial.distance import cosine

from .dataset2database import add2database
from .models import Category, news2db, News, Word, Keyword, categories_list, Reference


def prerequisites():
    logging.info('Started storing dataset in the database.')
    corpus_file_path = Path('staticfiles', 'HamshahriData.xlsx')
    add2database(corpus_file_path)
    logging.info('Data storage in the database is complete.')


def news_classification(reference: Reference, content: str, titr: str = None) -> Category:
    news = news2db(
        content_string=content,
        titr_string=titr,
    )
    news_vector = news2vector(news)
    cats_list = categories_list(reference=reference, vector=True)
    minimum_value = 100
    minimum_index = ''
    for cat_key, cat_val in cats_list.items():
        dist = cosine(news_vector, cat_val)
        if minimum_value > dist:
            minimum_value = dist
            minimum_index = cat_key
    near_category = Category.objects.get(pk=minimum_index)
    return near_category


def news2vector(news: News) -> list:
    vector_len = Word.objects.last()
    vector_len = int(vector_len.pk)
    vector = [0] * (vector_len + 1)
    kwrds = Keyword.objects.filter(news=news).all()
    for kw in kwrds:
        vector[int(kw.word.pk)] = kw.frequency
    return vector
