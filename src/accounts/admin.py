from django.contrib import admin
from .models import Profile , Plans , PlansPlaces
# Register your models here.

admin.site.register(Profile)
admin.site.register(Plans)
admin.site.register(PlansPlaces)