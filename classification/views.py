from django.shortcuts import render
from django.http import HttpRequest


def sample_view(request: HttpRequest):
    return render(
        request,
        'ai_index.html',
        context={},
    )
