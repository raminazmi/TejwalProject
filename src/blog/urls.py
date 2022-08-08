from django.contrib import admin
from django.urls import include , path
from . import views
urlpatterns = [
    path(''   ,   views.Articles     ,name='articles'),
    path('<str:slug>'   ,   views.GetArticle     ,name='article_view')
]