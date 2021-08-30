from django.http import HttpRequest, JsonResponse
from django.shortcuts import render


def index(request: HttpRequest):
    from .models import categories_list
    return render(
        request,
        'ai_index.html',
        context={'categories_list_name': categories_list()},
    )


def sample(request: HttpRequest):
    return render(request, 'index.html', context={})


def preprocessing(request: HttpRequest):
    from .controller import prerequisites
    prerequisites()
    response = {
        'RESULT': True,
        'word2vec_word_embeding__svm__precision_score': 1,
        'word2vec_word_embeding__svm__recall_score': 2,
        'word2vec_word_embeding__svm__accuracy_score': 3,

        'word2vec_word_embeding__mlp__precision_score': 4,
        'word2vec_word_embeding__mlp__recall_score': 5,
        'word2vec_word_embeding__mlp__accuracy_score': 6,

        'word2vec_word_embeding__mnb__precision_score': 7,
        'word2vec_word_embeding__mnb__recall_score': 8,
        'word2vec_word_embeding__mnb__accuracy_score': 9,

        'one_hot_encoding_word_embeding__svm__precision_score': 10,
        'one_hot_encoding_word_embeding__svm__recall_score': 11,
        'one_hot_encoding_word_embeding__svm__accuracy_score': 12,

        'one_hot_encoding_word_embeding__mlp__precision_score': 13,
        'one_hot_encoding_word_embeding__mlp__recall_score': 14,
        'one_hot_encoding_word_embeding__mlp__accuracy_score': 15,

        'one_hot_encoding_word_embeding__mnb__precision_score': 16,
        'one_hot_encoding_word_embeding__mnb__recall_score': 17,
        'one_hot_encoding_word_embeding__mnb__accuracy_score': 18,
    }
    return JsonResponse(response)


def classification(request: HttpRequest):
    from .controller import NewsClassification
    response = {}
    content = request.POST['content_text_for_classify']
    titr = request.POST['titr_text_for_classify']

    if content is None or len(content) == 0:
        response['TEXT'] = False
        response['ERROR_MESSAGE'] = 'Please enter the news you want to categorize in this section.'
        return JsonResponse(response)
    response['TEXT'] = True

    cn = NewsClassification()
    category = cn.classification(content, titr)

    response['CATEGORY_TITLE'] = category.title
    response['CATEGORY_PK'] = category.pk
    response['NEWS_PK'] = cn.news_for_classification.pk

    return JsonResponse(response)


def feedback(request: HttpRequest):
    from .controller import feedback as cfb
    cfb(news_id=request.POST['news_pk'], category_id=request.POST['category_radios'])

    return JsonResponse({})
