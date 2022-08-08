from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from country.models import Country
from place.models import Place
# Create your models here.
user_auth = [(0,0),(1,1)]
country_list = [('PS','PS'),
                ('JAD','الأردن'),
                ('EGY','مصر'),
                ('AUS','السعودية'),
                ('EUS','الامارات '),
                ('AJZ','الجزائر'),
                ]
gender = [('Male','ذكر'),('Female', 'انثى')]

tour_type = [('worship','عبادة '),
             ('romantic-tourism','قضاء شهر العسل'),
             ('family','عائلتي'),
             ('friends','أصدقائي'),
             ('Safari','سفاري'),
             ('medical','علاجية')]
class Profile(models.Model):
    user = models.OneToOneField(User , on_delete=models.CASCADE)
    country = models.CharField(max_length=40 , choices=country_list)
    brithdate = models.DateField(null=True ,blank=True)
    gender = models.CharField(max_length=10 , choices = gender)
    person_image = models.ImageField(upload_to='UserImages/')
    auth_user = models.IntegerField(default=0)
    
    def __str__(self):
        return self.user.username 
    
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

class Plans(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=80)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    budget = models.IntegerField(default=0)
    launch_date = models.DateField()
    tour_type = models.CharField(max_length=30 , choices=tour_type)
    
class PlansPlaces(models.Model):
    id = models.AutoField(primary_key=True)
    plan = models.ForeignKey(Plans, on_delete=models.CASCADE)
    place = models.ForeignKey(Place, on_delete=models.CASCADE)
