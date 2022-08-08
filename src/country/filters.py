import django_filters
from .models import City , Country

class TitleCityFilter(django_filters.FilterSet):
    name_city = django_filters.CharFilter(lookup_expr='icontains')
    class Meta:
        model = City
        fields = ['name_city']
        
class ContinentCountry(django_filters.FilterSet):
    class Meta:
        model = Country
        fields = ['continent']
class CityFilter(django_filters.FilterSet):
    class Meta:
        model = City
        fields = ['name_city','country']