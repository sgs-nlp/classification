from .views import index, prerequisites
from django.urls import path, include

app_name = 'statistical_pnc'
urlpatterns = [
    path('', prerequisites),
    path('index', index, name='index'),
]
