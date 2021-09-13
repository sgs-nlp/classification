from django.urls import path, include

from .views import *

app_name = 'statistical_pnc'
urlpatterns = [
    path('news-classification', classification_index_view, name='news_classification_index'),
    path('news-classification/classification', classification_view, name='news_classification_classification'),
    path('news-classification/feedback', classification_feedback_view, name='news_classification_feedback'),
    path('news-classification/preprocessing', classification_preprocessing_view,
         name='news_classification_preprocessing'),

    path('keywords-extraction', keywords_extraction_view, name='keywords_extraction_index'),
    path('text-similarity', text_similarity_view, name='text_similarity_index'),
]
