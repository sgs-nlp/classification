from django.urls import path, include

from .views import *

app_name = 'statistical_pnc'
urlpatterns = [
    path('', index_view, name='index'),
    path('classification', classification_view, name='classification'),
    path('classification/feedback', classification_feedback_view, name='classification_feedback'),
    path('preprocessing', preprocessing_view, name='preprocessing'),
]
