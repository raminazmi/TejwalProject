from django.contrib import admin
from .models import Country ,City , ImageCity , ReviewCity , Region , PopularQuestion , Food
from import_export.admin import ImportExportModelAdmin
# Register your models here.


admin.site.register(ImageCity)
admin.site.register(ReviewCity)
admin.site.register(Region)
admin.site.register(Food)
admin.site.site_header = "TEJWAL -FKR Comp."

@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    model = Country
    
    list_display = (
        "country_id",
        "name_country",
        "published",
        
    )
    list_filter = (
        "published",
    )
    list_editable= (
        'published',
    )
    search_fields = (
        "name_country",
    )
    
@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    model = City
    
    list_display = (
        "city_id",
        "name_city",
        "country",
        'order_city',
        'published'
        
    )
    list_filter = (
        "country",
        'published',
        "order_city",
    )
    list_editable= (
        'order_city',
        'published',
    )
    search_fields = (
        "title_place",
    )
    
@admin.register(PopularQuestion)
class PopularQuestionAdmin(admin.ModelAdmin):
    model = PopularQuestion
    
    list_display = (
        "question",
        "created_at",
    )
    list_filter = (
        "country",
    )
    search_fields = (
        "question",
        "answer",
    )


