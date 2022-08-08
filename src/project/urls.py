
from django.contrib import admin
from django.urls import path , include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('account/' , include('accounts.urls',namespace='accounts')),
    path('admin/', admin.site.urls),
    path('ckeditor/', include('ckeditor_uploader.urls')), 
    path('' , include('home.urls')),
    path('destinations/' , include('country.urls')),
    path('place/', include('place.urls')),
    path('articles/', include('blog.urls')),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = "project.views.handler_404"
