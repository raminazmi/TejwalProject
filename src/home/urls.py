from django.contrib import admin
from django.urls import path ,include
from . import views
from place.views import Events , EventView
from country.views import get_cities
urlpatterns = [
    path('' , views.homeView , name ='MainPage'),
    path('events/' , Events, name ='events'),
    path('events/<str:slug>' , EventView, name ='event_view'),
    path('search-special/' , views.search , name ='search-special'),
    path('cities/' , get_cities , name ='cities'),
    path('ajax/load-cities/', views.load_cities, name='ajax_load_cities'),
    path('search'  ,views.GeneralSearch , name='general_search'),
]