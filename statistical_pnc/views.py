from django.http import HttpRequest, JsonResponse
from django.shortcuts import render

from .controller import *


def classification_index_view(request: HttpRequest):
    res = index_default_data()
    return render(
        request,
        'news_classification.html',
        context=res,
    )


def classification_preprocessing_view(request: HttpRequest):
    res = prerequisites()
    return JsonResponse(res)


def classification_view(request: HttpRequest):
    content = request.POST['content_text_for_classify']
    titr = request.POST['titr_text_for_classify']
    res = classification_result(content, titr)
    return JsonResponse(res)


def classification_feedback_view(request: HttpRequest):
    classification_feedback_view(news_id=request.POST['news_pk'], category_id=request.POST['category_radios'])
    return JsonResponse({})


def keywords_extraction_view(request: HttpRequest):
    return render(
        request,
        'keywords_extraction.html',
        context={},
    )


def text_similarity_view(request: HttpRequest):
    return render(
        request,
        'text_similarity.html',
        context={},
    )
