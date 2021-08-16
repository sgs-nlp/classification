from django.http import HttpRequest, JsonResponse
from django.shortcuts import render
from django.conf import settings
from .controller import news_classification, prerequisites
from .models import reference2db
import redis
import pickle
from pathlib import Path


def index(request: HttpRequest):
    from extra_settings.models import File
    file = File()
    file.save(Path('staticfiles', 'HamshahriData.xlsx'))
    res, header = file.load(file_name='HamshahriData.xlsx', to_be_continued=False, from_which_row=8, up_to_which_row=10)
    print(res)
    return render(
        request,
        'ai_index.html',
        context={},
    )


# def prerequisites(request: HttpRequest):
#     # logging.info('Started storing dataset in the database.')
#     # file_name = Path('staticfiles', 'HamshahriData.xlsx')
#     # add2database(file_name)
#     # logging.info('Data storage in the database is complete.')
#     # logging.info('Started classification analys.')
#     # clss = classification()
#     # logging.info('Classification analys complate.')
#     # from statistical_pnc.models import news2db
#     # file_name = Path('staticfiles', 'HamshahriData.xlsx')
#     # add2database(file_name)
#     # s = news2db(titr_string=titr_string, content_string=content_string, category_title=category_title)
#     return render(
#         request,
#         'ai_index.html',
#         context={'word2vec_word_embeding__svm__accuracy_score': 1},  # clss,
#     )


def sample(request: HttpRequest):
    return render(request, 'index.html', context={})


def classification(request: HttpRequest):
    response = {}
    # content = request.POST['content_text_for_classify']
    # titr = request.POST['titr_text_for_classify']
    #
    # if content is None or len(content) == 0:
    #     response['TEXT'] = False
    #     response['ERROR_MESSAGE'] = 'Please enter the news you want to categorize in this section.'
    #     return JsonResponse(response)
    #
    # response['TEXT'] = True
    # reference = reference2db('HamshahriData.xlsx')
    # category = news_classification(reference=reference, content=content, titr=titr)
    # response['CATEGORY_TITLE'] = category.title
    return JsonResponse(response)


def preprocessing(request: HttpRequest):
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

# 0790160000000000774260366

# 09151712846
