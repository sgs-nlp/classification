from django.shortcuts import render, redirect
from django.http import HttpRequest, JsonResponse
from .dataset2database import add2database
import logging
from django.contrib import messages


def prerequisites():
    from pathlib import Path
    from datetime import datetime
    logging.info('Started storing dataset in the database.')
    corpus_file_path = Path('staticfiles', 'HamshahriData.xlsx')
    add2database(corpus_file_path)
    logging.info('Data storage in the database is complete.')


def news_classification(reference: Reference, content: str, titr: str = None) -> Category:
    news = news2db(
        content_string=content,
        titr_string=titr,
    )
    # news = News.objects.get(pk=3)
    news_vector = news2vector(news)
    cats_list = categories_list(reference=reference, vector=True)
    print(cats_list)
    distances_list = []
    for cat in cats_list:
        distances_list.append(cosine(news_vector, cat))
    print(sorted(distances_list))
    return min(distances_list)


def news2vector(news: News) -> list:
    vector_len = Word.objects.last()
    vector_len = int(vector_len.pk)
    vector = [0] * vector_len
    kwrds = Keyword.objects.filter(news=news).all()
    for kw in kwrds:
        vector[int(kw.word.pk)] = kw.frequency
    return vector
