from .views import index, sample, classification, preprocessing
from django.urls import path, include

app_name = 'statistical_pnc'
urlpatterns = [
    path('', index, name='index'),
    path('sample', sample, name='sample'),
    path('classification', classification, name='classification'),
    path('preprocessing', preprocessing, name='preprocessing'),
]
