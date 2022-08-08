from django.contrib import admin 
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
app_name = 'accounts'

urlpatterns =[
    path('signup/' , views.signup    , name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name ='login'),
    path('logout/', auth_views.LogoutView.as_view(), name ='logout'),
    path('profile/'                  ,views.Profilee   , name='profile_user'),
    path('settings/edit-profile'     ,views.EditProfile   , name='edit_profile'),
    path('settings/chanaePassword', auth_views.PasswordChangeView.as_view(template_name = 'registration/profile.html') , name='change_password'),
    path('settings/changePassword/Done', auth_views.PasswordChangeView.as_view(template_name = 'registration/profile.html') , name='Done_change_password'),


]