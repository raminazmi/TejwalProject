from django.contrib import admin
from django.urls import include , path
from . import views
from place.views import Beach , NatureCategory , CultureCategory , AdventuresCategory , MarketingCategory , BeachCity , NatureCity , AdventuresCity , CultureCity ,MarketingCity


urlpatterns = [
    path(''          , views.CountryList   ,      name='CountryList'),
    path('filter/<str:continent>' , views.CountryFilter ,      name='country_filter'),
    path('review/'                , views.AddReviewCity ,      name ='review_city'),
    path('<str:slug>'             ,views.get_country_detail,   name="country"),
    path('<str:slug>/cities'      ,views.CitiesFilter ,        name="city_filter"),
    path('<str:slug>/foods'       ,views.get_more_food,        name='more_food'),
    path('<str:slug>/place'       ,views.get_more_place,       name='more_place'),
    path('city/<str:slug>'        ,views.get_city_detail ,     name="city"),
    path('<str:slug>/restaurant'  ,views.Restaurant,           name='restaurants_view'),
    path('<str:slug>/beach'       , Beach ,                    name = 'beach_view'),
    path('<str:slug>/nature'      , NatureCategory ,           name = 'nature_view'),
    path('<str:slug>/culture'     , CultureCategory ,          name = 'culture_view'),
    path('<str:slug>/adventures'  , AdventuresCategory ,       name = 'adventures_view'),
    path('<str:slug>/market'      , MarketingCategory ,        name = 'market_view'),
    path('city/<str:slug>/nature'  , NatureCity ,              name = 'nature_city'),
    path('city/<str:slug>/culture'  , CultureCity ,            name = 'culture_city'),
    path('city/<str:slug>/adventures'  , AdventuresCity ,      name = 'adventures_city'),
    path('city/<str:slug>/beach'  , BeachCity ,                name = 'beach_city'),
    path('city/<str:slug>/market'  , MarketingCity ,           name = 'market_city'),
    
]    