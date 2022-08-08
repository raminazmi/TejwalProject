from django.contrib import admin
from django.urls import path ,include
from . import views

urlpatterns = [
    path('<str:slug>' , views.PlaceDetail , name='place_view'),
    path('<str:slug>', views.PlaceListAsCity , name='place_list_as_city'),
    path('review/' , views.ReviewPlace , name ='review'),
    path('search/' , views.SearchPlace , name ='place_search'),
    path('addfavorite/' , views.AddFavorite , name="add_favorite"),
    path('nature/' , views.NatureCategory , name="nature_view"),
] 