from django.contrib import admin
from .models import Tag , Post , PartsPost
# Register your models here.
@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    model = Tag
    
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    model = Post
    
    list_display = (
        "id",
        "title",
        "publish_date",
        "published",
        'category',
    )
    list_filter = (
        "published",
        "publish_date",
    )
    list_editable = (
        'category',
    )
    search_fields = (
        "title",
    )
    prepopulated_fields = {
        "slug": (
            "title",
        )
    }
    date_hierarchy = "publish_date"
    save_on_top = True
    
@admin.register(PartsPost)
class PartsPostAdmin(admin.ModelAdmin):
    model = PartsPost
    