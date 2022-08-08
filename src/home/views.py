from django.shortcuts import render
from country.models import Country ,City
from place.models import Place , Event , Activity
from blog.models import Post
# Create your views here.
def homeView(request):
    country = Country.objects.filter(published = True)
    place = Place.objects.filter(order=1)[:6]
    city = City.objects.filter(order_city=1 , published = True)[:6]
    event = Event.objects.all()[:6]
    activity = Activity.objects.filter(recommended = True)[:6]
    posts = Post.objects.filter(published = True)[:4]
    main_post = posts
    context = {'country_list':country,
               'places':place,
               'cities':city,
               'events':event ,
               'activities':activity,
               'posts':posts,
               'main_post':main_post
               }
    return render(request,'home/index02.html',context)

def load_cities(request):
    country2 = request.GET.get('country')
    object_coun = Country.objects.get(country_id=country2)
    cities = City.objects.filter(country=object_coun)
    return render(request, 'home/city_dropdown_list_options.html', {'cities': cities})

def search(request):
    if request.method == 'GET':
        country = request.GET.get('country_id')
        city = request.GET.get('city_id')
        if city =='no':
            object_country = Country.objects.get(country_id=country)
            context={'object':object_country}
            return render(request, 'country/country.html' , context)
        else:
            object_city = City.objects.get(city_id = city)
            place = Place.objects.filter(city__slug = object_city.slug)
            context = {'object':object_city ,'places_object':place}
            return render(request, 'country/city.html' , context)

def discover_city(request):
    return render(request , 'home/discover.html')

def GeneralSearch(request):
    text = request.GET.get('search-text')
    country = Country.objects.filter(name_country__contains = text,published = True)
    city =  City.objects.filter(name_city__contains = text,published = True)
    place =  Place.objects.filter(title_place__contains = text)
    count_result = len(country) + len(city) + len(place)
    result = False
    if count_result == 0:
        result = True
    
    context={'country_objects': country,
             'result':result,
             'city_objects':city,
             'place_objects':place}
    return render(request, 'home/search-result.html',context)

