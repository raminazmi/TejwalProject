from django.shortcuts import render , redirect

from country.models import Country
from .forms import SignupForm
from django.contrib.auth import  login
from .models import Profile , Plans
from place.models import Favorite , Review
from django.contrib.auth.decorators import login_required
from place.views import Place
from .forms import SignupForm , UserForm , ProfileForm , UserCreateForm
# Create your views here.
def signup(request):
    if request.method == 'POST':
        user_form = SignupForm(request.POST)
        if user_form.is_valid():
            user = user_form.save()
            login(request, user)
            return redirect('MainPage')
    return render(request , 'registration/signup.html') 
        
@login_required
def Profilee(request):
    profile = Profile.objects.get(user = request.user)
    num_place = Place.objects.all().count()
    favorite = Favorite.objects.filter(user = request.user)
    reviews = Review.objects.filter(user__user = request.user)
    context = {'profile':profile,
               'favorite':favorite,
               'reviews':reviews}
    return render(request,'accounts/profile.html',context)

@login_required
def ProfileComment(request):
    profile = Profile.objects.get(user = request.user)
    num_place = Place.objects.all().count()
    comment = Review.objects.filter(user = request.user)
    if(profile.auth_user == 1):
        return render(request,'accounts/profile_data.html',{'profile':profile,'count_place':num_place})
    else:
        return render(request,'accounts/profile_comment.html',{'user':profile,'comment':comment})

@login_required
def ProfileInfo(request):
    profile = Profile.objects.get(user = request.user)
    num_place = Place.objects.all().count()
    if(profile.auth_user == 1):
        return render(request,'accounts/profile_data.html',{'profile':profile,'count_place':num_place})
    else:
        return render(request,'accounts/profile_info.html',{'profile':profile})

@login_required
def CreatePlan(request):
    if request.method == 'POST':
        user = request.user;
        title = request.POST.get('title')
        country_id = request.POST.get('country')
        country = Country.objects.get(country_id = country_id)
        tour_type = request.POST.get('tour_type')
        lunch_date = request.POST.get('lunch_date')
        budget = request.POST.get('budget')
        Plans(user = user , title = title , country = country , launch_date = lunch_date , budget=budget , tour_type = tour_type).save();
        return render(request, 'home/plan-board.html')

@login_required
def EditProfile(request):
    profile = Profile.objects.get(user = request.user)
    if request.method == 'POST':
        myuser = UserForm(request.POST , instance=request.user)
        myprofile = ProfileForm(request.POST ,request.FILES, instance=profile)
        if myuser.is_valid() or myprofile.is_valid():
            myuser.save()
            myprofile.save(commit=False)
            myprofile.user = request.user
            myprofile.save()  
            return redirect('accounts:profile_user')
        return redirect('accounts:profile_user')
    else:
        userform = UserForm(instance=request.user)
        profileform = ProfileForm(instance=profile)
        context = {'userform':userform,'profileform':profileform}
        return render(request,'accounts/edit_profile.html',context)

   