from django.shortcuts import render,redirect
from django.http import HttpRequest, JsonResponse
from .dataset2database import add2database


def prerequisites(request: HttpRequest):
    from pathlib import Path
    file_name = Path('statics_files', 'HamshahriData.xlsx')
    add2database(file_name)
    return redirect('persian_news_classification:index')


def index(request: HttpRequest):
    return render(request, 'test.html', context={})
