from .views import index, prerequisites
from django.urls import path, include

app_name = 'persian_news_classification'
urlpatterns = [
    path('', prerequisites),
    path('index', index, name='index'),
]
