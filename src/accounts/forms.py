from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from accounts.models import Plans
from accounts.models import Profile

class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name','last_name', 'username','email','password1','password2']
 
class UserCreateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [ 'first_name','last_name', 'username','email','password']

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name','last_name','email','username']

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['brithdate','gender','country','person_image']


