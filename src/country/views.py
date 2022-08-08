from django.shortcuts import get_object_or_404, render , redirect
from django.views.generic import ListView , DetailView
from django.core.paginator import Paginator
from place.models import Place , Activity , Event
from .models import Country , City , ReviewCity , Food , PopularQuestion
from django.core.paginator import Paginator
from accounts.views import Profile
from django.contrib.auth.decorators import login_required
def GetTemperature(request , destination):
    api_url = "https://api.openweathermap.org./data/2.5/weather?appid=0c42f7f6b53b244c78a418f4f181282a&q="
    destination = destination
    url = api_url + destination
    response = requests.get(url)
    content = response.json()
    weather = {
        'temperature':content['main']['temp'], 
        'icon':content['weather'][0]['icon']
    }
    return weather

def CountryList(request):
    country_list = Country.objects.filter(published = True)
    
    # continenty_filter = ContinentCountry(request.GET , queryset=country_list)
    # country_list = continenty_filter.qs
    
    context = {'destinations':country_list,
               }
    return render(request , 'country/destinations.html',context)

def CountryFilter(request , continent):
    country_list = Country.objects.filter(continent=continent)
    context = {'destinations':country_list}
    return render(request , 'country/destinations.html',context)

class CountryDetail(DetailView):
    model = Country
    template_name = 'country/destination.html'
    
    def get_object(self):
        slug_ = self.kwargs.get('slug')
        context_object_name = 'object'
        return get_object_or_404(Country, slug=slug_)
        
def get_country_detail(request , slug):
    country_object = Country.objects.get(slug = slug)
    city = City.objects.filter(country__slug = country_object.slug,published = True)[:8]
    activities = Activity.objects.filter(city__country__slug = country_object.slug)[:6]
    questions = PopularQuestion.objects.filter(country__slug = country_object.slug)[:10]
    events = Event.objects.filter(city__country__slug = country_object.slug)
    place = Place.objects.filter(city__country__slug = slug , order = 1)[:10]
    context = {'destination':country_object,
               'cities_objects':city,
               'questions':questions,
               'activities':activities,
               'places':place,
               'events':events,
               'type_destination':'country'}
    return render(request, 'country/destination.html',context)

def get_city_detail(request , slug):
    city_object = City.objects.get(slug = slug)
    country = Country.objects.get(slug = city_object.country.slug)
    cities = City.objects.filter(country = country,published = True)[:6]
    place = Place.objects.filter(city__slug = city_object.slug)[:12]
    activities = Activity.objects.filter(city__slug = slug)[:10]
    questions = PopularQuestion.objects.filter(country__slug = country.slug)[:12]
    events = Event.objects.filter(city__country__slug = country.slug)
    
    context = { 'destination':city_object,
                'places':place,
                'cities':cities,
                'events':events,
                'activities' : activities,
                'questions' : questions,
                'type_destination':'city'}
    
    return render(request, 'country/city.html',context)

def get_cities(request):
    cities = City.objects.all();
    paginator = Paginator(cities,9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context ={'objects':page_obj }
    return render(request,'country/city_list.html',context)

def CitiesFilter(request , slug):
    country = Country.objects.get(slug = slug)
    cities = City.objects.filter(country=country);
    title_city_filter = TitleCityFilter(request.GET , queryset=cities)
    cities = title_city_filter.qs
    
    paginator = Paginator(cities,9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context ={'objects':page_obj ,'city_filter':title_city_filter}
    return render(request,'country/city_list.html',context)

def get_more_food(request,slug):
    food = Food.objects.filter(country__slug = slug)
    context = {'objects':food}
    return render(request , 'food/food.html' ,context)
    

def get_more_place(request,slug):
    place = Place.objects.filter(city__country__slug = slug)
    paginator = Paginator(place, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'objects':page_obj}
    return render(request , 'place/places.html' ,context)

@login_required
def AddReviewCity(request):
    if request.method == 'GET':
        city_id = request.GET.get('city_id')
        city = City.objects.get(city_id = city_id)
        user = request.user
        profile = Profile.objects.get(user = user)
        comment = request.GET.get('comment')
        rate = request.GET.get('rate')
        ReviewCity(user = user  ,profile = profile, city=city, comment=comment ,rate = rate).save();
        return redirect('city',slug = city.slug)
    else:
        return render(request, 'home/index.html')
    
def Restaurant(request , slug):
    food = Food.objects.filter(country__slug = slug)
    country = Country.objects.get(slug = slug)
    is_restaurant = True
    context = {
        'foods':food,
        'destination':country
    }
    return render(request, 'place/restaurants.html',context) 


