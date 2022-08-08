import django_filters
from .models import Place , Activity 

class TitlePlaceFilter(django_filters.FilterSet):
    title_place = django_filters.CharFilter(lookup_expr='icontains')
    class Meta:
        model = Place
        fields = ['title_place']

class CategoryPlaceFilter(django_filters.FilterSet):
    class Meta:
        model = Place
        fields = ['category']

class FeaturesPlaceFilter(django_filters.FilterSet):
    class Meta:
        model = Place
        fields = ['features']
                
class PlaceFilter(django_filters.FilterSet):
    class Meta:
        model = Place
        fields = ['title_place','category','city','order']
class ActvityFilter(django_filters.FilterSet):
    class Meta:
        model = Activity
        fields = ['title','category']