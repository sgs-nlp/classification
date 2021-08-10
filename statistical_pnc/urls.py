from .views import index, prerequisites, classification
from django.urls import path, include

app_name = 'statistical_pnc'
urlpatterns = [
    path('', prerequisites, name='prerequisites'),
    path('index', index, name='index'),
    path('classification', classification, name='classification'),
]
