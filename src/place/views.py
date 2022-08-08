from unicodedata import category
from django.shortcuts import render , redirect
from .models import Place  ,Review  ,Favorite , Event
from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Count
from django.core.paginator import Paginator
from .filters import TitlePlaceFilter , CategoryPlaceFilter , FeaturesPlaceFilter
from django.urls import reverse
from country.models import Country , City
from accounts.models import Profile
from django.http import JsonResponse
# Create your views here.
    
def PlaceList(request):
    places = Place.objects.all()
    # use filter in website 
    # filter to title place 
    title_place_filter = TitlePlaceFilter(request.GET , queryset=places)
    places = title_place_filter.qs
    #filter to category 
    category_filter  = CategoryPlaceFilter(request.GET , queryset=places)
    places = category_filter.qs
    paginator = Paginator(places,12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context ={'objects'               :  page_obj ,
              'title_place_filter'    :  title_place_filter ,
              'category_place_filter' :category_filter }
    return render(request , 'place/places.html' , context)

def PlaceListAsCity(request,slug):
    places = Place.objects.filter(city__slug = slug)
    # use filter in website 
    # filter to title place 
    title_place_filter = TitlePlaceFilter(request.GET , queryset=places)
    places = title_place_filter.qs
    #filter to category 
    category_filter  = CategoryPlaceFilter(request.GET , queryset=places)
    places = category_filter.qs
    paginator = Paginator(places,12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context ={'objects'               :  page_obj ,
              'title_place_filter'    :  title_place_filter ,
              'category_place_filter' :category_filter }
    return render(request , 'place/beach.html' , context)

def PlaceDetail(request,slug):
    place_object = Place.objects.get(slug = slug)
    comment = Review.objects.filter(place__slug=slug)
    rate = Review.objects.filter(place__slug = slug).aggregate(Avg('rate'))
    count = Review.objects.filter(place__slug = slug).aggregate(Count('rate'))
    similer_place = Place.objects.filter(category = place_object.category)
    features = place_object.get_features_display
    if rate['rate__avg'] != None:
        rate3 = round(rate['rate__avg'],2)
    else:
        rate3 = 0.0
    context = {'object'  :place_object,
               'rate'          :rate3 , 
               'comments'       :comment,
               'count'         :count,
               'similer_objects':similer_place,
               'features': features} 
    return render(request , 'place/place_view.html' , context)

def SearchPlace(request):
    if request.method == 'GET':
        text_search = request.GET.get('text_search')
        place = Place.objects.filter(title_place__icontains = text_search)
        return render(request, 'place/places.html',{'objects':place})
# function to review and comment V 1.0
@login_required
def ReviewPlace(request):
    if request.method == 'GET':
        place_id = request.GET.get('place_id')
        place = Place.objects.get(id = place_id)
        user = request.user
        profile = Profile.objects.get(user = user)
        comment = request.GET.get('comment')
        rate = request.GET.get('rate')
        if rate is None:
            rate = 5
        Review(user = profile  ,place = place, comment = comment ,rate = rate).save();
        return redirect('place_view' , id = place_id)
    
@login_required
def AddFavorite(request):
    place_id = request.GET.get('place_id')
    place = Place.objects.get(id=place_id)
    users = Favorite.objects.filter(place = place,user = request.user)
    if len(users) > 0:
        place = users.get(user=request.user)
        place.delete()
        data ={'success':False}
    else:
        Favorite(user = request.user , place = place).save();
        data ={'success':True}
        
    return JsonResponse(data)

def Beach(request , slug):
    is_beach = True
    country = Country.objects.filter(slug=slug).values('name_country','slug')
    country = country[0]
    places = Place.objects.filter(category__in=['Beach','lakes','resorts','Islands'],city__country__slug = slug)
    context = {'places':places , 'destination':country, 'type_destination':'country' ,'is_beach':is_beach}
    return render(request, 'place/beach_category.html',context)

def NatureCategory(request , slug):
    country = Country.objects.filter(slug=slug).values('name_country','slug')
    country = country[0]
    places = Place.objects.filter(category__in=['park','air','Sanctuaries_zoos','forests'],city__country__slug = slug)
    is_nature = True
    context = {'places':places , 'destination':country,'is_nature':is_nature}
    return render(request , 'place/nature_category.html',context)

def CultureCategory(request , slug):
    country = Country.objects.filter(slug=slug).values('name_country','slug')
    country = country[0]
    places = Place.objects.filter(category__in=['historical','Architectural','museums_galleries','arts_crafts'],city__country__slug = slug)

    is_culture = True
    context = {'places':places , 
               'destination':country,
               'is_culture':is_culture}
    return render(request , 'place/culture_category.html',context)

def AdventuresCategory(request , slug):
    country = Country.objects.filter(slug=slug).values('name_country','slug')
    country = country[0]
    places = Place.objects.filter(category__in=['theaters','amusement','stadium','gyms'],city__country__slug = slug)
    is_adventures = True
    context = {'places':places , 'destination':country,'is_adventures':is_adventures}
    return render(request , 'place/adventures_category.html',context)
 
def MarketingCategory(request , slug):
    country = Country.objects.filter(slug=slug).values('name_country','slug')
    country = country[0]
    places = Place.objects.filter(category__in=['shopping_centers','traditional_markets','recreation_centers'],city__country__slug = slug)
    is_market = True
    type_destination = 'Country'
    context = {'places':places , 'destination':country,'is_market':is_market}
    return render(request , 'place/market_category.html',context)

def BeachCity(request , slug):
    is_beach = True
    city = City.objects.filter(slug=slug).values('city_id','name_city','slug')
    city = city[0]
    places = Place.objects.filter(category__in=['beach','lake','resort','island'],city__slug = slug)
    context = {'places':places ,
               'destination':city ,
               'type_destination':'city',
               'is_beach':is_beach}
    return render(request, 'place/city/beach_category.html',context)

def NatureCity(request , slug):
    city = City.objects.filter(slug=slug).values('city_id','name_city','slug')
    city = city[0]
    places = Place.objects.filter(category__in=['park','air','Sanctuaries_zoos','forests'],city__slug = slug)
    is_nature = True
    context = {'places':places ,
               'destination':city ,
               'type_destination':'city',
               'is_nature':is_nature}
    return render(request , 'place/city/nature_category.html',context)

def CultureCity(request , slug):
    city = City.objects.filter(slug=slug).values('city_id','name_city','slug')
    city = city[0]
    places = Place.objects.filter(category__in=['historical','Architectural','museums_galleries','arts_crafts'],city__slug = slug)
    myfilter = FeaturesPlaceFilter(request.GET , queryset=places)
    places =  myfilter.qs
    is_culture = True
    
    context = {'places':places ,
               'destination':city ,
               'type_destination':'city',
               'feature_filter':myfilter,
               'is_culture':is_culture}
    return render(request , 'place/city/culture_category.html',context)

def AdventuresCity(request , slug):
    city = City.objects.filter(slug=slug).values('city_id','name_city','slug')
    city = city[0]
    places = Place.objects.filter(category__in=['theaters','amusement','stadium','gyms'],city__slug = slug)
    is_adventures = True
    context = {'places':places ,
               'destination':city ,
               'type_destination':'city',
               'is_adventures':is_adventures}
    return render(request , 'place/city/adventures_category.html',context)
 
def MarketingCity(request , slug):
    city = City.objects.filter(slug=slug).values('city_id','name_city','slug')
    city = city[0]
    places = Place.objects.filter(category__in=['shopping_centers','traditional_markets','recreation_centers'],city__slug = slug)
    is_market = True
    context = {'places':places ,
               'destination':city ,
               'type_destination':'city',
               'is_market':is_market}
    return render(request , 'place/city/market_category.html',context)
 
def Events(request):
    events = Event.objects.all()
    context = {'events':events}
    return render(request,'place/events.html',context)
 
def EventView(request , slug):
    event = Event.objects.get(slug=slug)
    # popular_events = Event.object.filter(city__id = event.city.id)
    context = {
        'event':event,
        # 'popular_events':popular_events
    }
    return render(request , 'place/event.html',context)