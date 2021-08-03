from django.shortcuts import render, redirect
from django.http import HttpRequest, JsonResponse
from .dataset2database import add2database
from .controller import classification as classification
import logging


def prerequisites(request: HttpRequest):
    from pathlib import Path
    from datetime import datetime

    logging.info('Started storing dataset in the database.')
    file_name = Path('staticfiles', 'HamshahriData.xlsx')
    add2database(file_name)
    logging.info('Data storage in the database is complete.')
    logging.info('Started classification analys.')
    clss = classification()
    logging.info('Classification analys complate.')
    return render(
        request,
        'ai_index.html',
        context=clss,
    )


def index(request: HttpRequest):
    return render(request, 'index.html', context={})
