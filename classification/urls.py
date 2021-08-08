from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
                  # path('', include('persian_news_classification.urls')),
                  path('', include('statistical_pnc.urls')),
                  path('home', views.home_page_view, name='home'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
