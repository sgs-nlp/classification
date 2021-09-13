from django.shortcuts import render
from django.http import HttpRequest


def home_page_view(request: HttpRequest):
    return render(
        request,
        'home.html',
        context={},
    )


def about_me_page_view(request: HttpRequest):
    return render(
        request,
        'statics_pages/about.html',
        context={},
    )


def contact_me_page_view(request: HttpRequest):
    return render(
        request,
        'statics_pages/contact.html',
        context={},
    )


def sample_page_view(request: HttpRequest):
    return render(
        request,
        'sample.html',
        context={},
    )
