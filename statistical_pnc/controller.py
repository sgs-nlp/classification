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
    logging.info('Started classification analys.')
    # clss = classification()
    logging.info('Classification analys complate.')
    return