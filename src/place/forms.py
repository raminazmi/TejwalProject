from dataclasses import fields
from django import forms
from .models import  ImagePlace , Place , Activity

class PlaceForm(forms.ModelForm):
    class Meta:
        model = Place
        fields = ['title_place','info','city','category','short_info','order','background','website','location']

class ImagePlaceForm(forms.ModelForm):
    class Meta:
        model = ImagePlace
        fields = ['place','image']
# class ActivityForm(forms.ModelForm):
#     class Meta:
#         model = Activity
#         fields = ['title','info','category','image','alert']