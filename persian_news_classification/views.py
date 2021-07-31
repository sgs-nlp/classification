from django.shortcuts import render, redirect
from django.http import HttpRequest, JsonResponse
from .dataset2database import add2database
from .controller import classification as classification


def prerequisites(request: HttpRequest):
    from pathlib import Path
    from datetime import datetime
    file_name = Path('staticfiles', 'HamshahriData.xlsx')
    start = datetime.utcnow()
    add2database(file_name)
    print(f'create database run time = {datetime.utcnow() - start}')
    start = datetime.utcnow()
    scores = classification()
    print(f'create machine learning model run time = {datetime.utcnow() - start}')
    return render(
        request,
        'ai_index.html',
        context={
            'scores': scores,
        },
    )


def index(request: HttpRequest):
    return render(request, 'test.html', context={})
