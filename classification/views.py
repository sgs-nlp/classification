from django.shortcuts import render
from django.http import HttpRequest


def home_page_view(request: HttpRequest):
    return render(
        request,
        'home.html',
        context={},
    )


def sample_page_view(request: HttpRequest):
    return render(
        request,
        'sample.html',
        context={},
    )
