from dataclasses import fields
from django import forms
from .models import City , ImageCity ,Region

class CityForm(forms.ModelForm):
    class Meta:
        model = City
        fields = ['city_id','name_city','info','country','order_city','image']

class ImageCityForm(forms.ModelForm):
    class Meta:
        model = ImageCity
        fields = ['city','Image']

class RegionForm(forms.ModelForm):
    class Meta:
        model = Region
        fields =['name_regio','info','formal_lang','country','order','slug','cost_living','image']