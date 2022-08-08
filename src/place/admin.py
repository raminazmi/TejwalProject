from django.contrib import admin
from .models import Place , ImagePlace ,Activity , Review , Favorite , Event
from import_export.admin import ImportExportModelAdmin
# Register your models here.
# admin.site.register(Place)
admin.site.register(Activity)
admin.site.register(Review)
admin.site.register(Favorite)
admin.site.register(Event)
# class PlaceAdmin(ImportExportModelAdmin):
#     pass

@admin.register(ImagePlace)
class ImagePlaceAdmin(ImportExportModelAdmin):
    pass

@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    model = Place
    
    list_display = (
        "id",
        "title_place",
        "category",
        "city",
        'order',
    )
    list_filter = (
        'city',
        "order",
    )
    list_editable = (
        "category",
    )
    search_fields = (
        "title_place",
    )
    prepopulated_fields = {
        "slug": (
            "title_place",
    )
    }
    save_on_top = True
    




