from audioop import reverse
from locale import currency
from random import choices
from django.db import models
from django.contrib.auth.models import User
from django.forms import ImageField
from django.utils.text import slugify
from home.images import image_resize

continent = [
    ('asia','اسيا'),
    ('africa','أفريقيا'),
    ('europe','أوروبا'),
    ('north_america','أمريكا الشمالية'),
    ('south_america','أمريكا الجنوبية'),
    ('australia','أستراليا'),
]

food_category = [
    ('meat','لحوم'),
    ('vegetarian','مأكولات نباتية'),
    ('Seafood','وجبات بحرية'),
    ('Candy','حلويات'),
    ('fastfood','وجبات سريعة'),
    ('fastfood2','بقوليات'),
    ('fastfood3','وجبات'),
    ]
order = ( (1,1),(2,2),(3,3),(4,4),(5,5),(6,6),(7,7),(8,8),(9,9))

# function to change name file with upload on DB in City
def ImageUploadCity(instance , filename):
    imagename , extension = filename.split('.')
    return "Background/%s.%s"%(instance.city_id,extension);

# function to change name file with upload on DB in Country
def ImageUploadCountry(instance , filename):
    imagename , extension = filename.split('.')
    return "Background/%s.%s"%(instance.country_id,extension);

def ImageUploadRegion(instance , filename):
    imagename , extension = filename.split('.')
    return "Region/%s.%s"%(instance.region_id,extension);

# function to change name file with upload on DB in ImagesCity
def ImageUpload(instance , filename):
    imagename , extension = filename.split('.')
    return "city/%s/%s%s.%s"%( instance.city, instance.city.city_id , instance.id_image ,extension)

class Country(models.Model):
    country_id     = models.CharField(max_length=10 , primary_key=True)
    name_country   = models.CharField(max_length=30 , null=False)
    formal_country = models.CharField(max_length=100 , null = True)
    info           = models.TextField(max_length=1000 , null=False)
    capital        = models.CharField(max_length = 50 , null=False)
    formal_lang    = models.CharField(max_length=50  , null=False)
    currency       = models.CharField(max_length=50 , null=False)
    area_country   = models.DecimalField(decimal_places=2 , null = False , max_digits = 12)
    continent      = models.CharField(max_length=20 , choices = continent , null=False)
    cost_living    = models.DecimalField(max_digits=20 , decimal_places=2 , null =True , blank=True)
    police         = models.CharField(max_length=8,null=True , blank=True)
    ambulance      = models.CharField(max_length=8,null=True , blank=True)
    firefighting   = models.CharField(max_length=8,null=True , blank=True)
    order          = models.PositiveSmallIntegerField(default=1)
    slug           = models.SlugField(blank=True , null = False)
    image          = models.ImageField(upload_to = ImageUploadCountry , null=True , blank=True)
    meta_description = models.TextField(max_length=500,null=True, blank=True)
    published = models.BooleanField(default=False)

    # def save(self , *args , **kwargs):
    #     self.slug = slugify(self.name_country , allow_unicode=True)
    #     super(Country,self).save(*args, **kwargs)
    def save(self , commit=True,*args , **kwargs):
        if commit:
            image_resize(self.image, 1200 , 800)
            super().save(*args, **kwargs)
        return super(Country,self).save(*args, **kwargs)  
        
    def delete(self,*agrs , **kwargs):
        self.image.delete()
        return super(Country,self).delete(*agrs ,**kwargs)
    
    def __str__(self):
        return self.slug
    class Meta:
        ordering = ['order']
class Region(models.Model):
    region_id    = models.AutoField(primary_key=True)
    name_regio   = models.CharField(max_length=30 , null=False)
    info         = models.TextField(max_length=500 , null=False)
    formal_lang  = models.CharField(max_length=50  , null=False)
    country      = models.ForeignKey(Country, blank=True , on_delete=models.CASCADE , null=False)
    cost_living    = models.DecimalField(max_digits=20 , decimal_places=2 , null =True , blank=True)
    order          = models.PositiveSmallIntegerField(default=1)
    slug         = models.SlugField(blank=True ,null = False , allow_unicode=True)
    image        = models.ImageField(upload_to = ImageUploadRegion,null=False , blank=False)
    
    def __str__(self):
        return self.name_regio
    class Meta:
        ordering = ['order']
        
    def save(self , commit=True,*args , **kwargs):
        if commit:
            image_resize(self.image, 1200 , 800)
            super().save(*args, **kwargs)
        return super(City,self).save(*args, **kwargs) 
     
class City(models.Model):
    city_id      = models.CharField(max_length=10 , primary_key=True)
    name_city    = models.CharField(max_length=30 , null=False)
    info         = models.TextField(max_length=800 , null=False)
    formal_lang  = models.CharField(max_length=50  , null=False)
    country      = models.ForeignKey(Country, blank=True , on_delete=models.CASCADE , null=False)
    region       = models.ForeignKey(Region , on_delete=models.SET_NULL , null=True , blank=True )
    slug         = models.SlugField (max_length=100,null=False)
    order_city   = models.IntegerField(choices=order , null=True)
    image        = models.ImageField(upload_to = ImageUploadCity,null=False , blank=False)
    published = models.BooleanField(default=False)


    def __str__(self):
        return self.name_city
    
    def save(self , commit=True,*args , **kwargs):
        if commit:
            image_resize(self.image, 800 , 800)
            super().save(*args, **kwargs)
        return super(City,self).save(*args, **kwargs)        


    def delete(self,*agrs , **kwargs):
        self.image.delete()
        return super(City,self).delete(*agrs ,**kwargs)
    class Meta:
        ordering = ['order_city']
        
class ImageCity(models.Model):
     id_image  = models.AutoField(primary_key=True)
     city      = models.ForeignKey(City , blank=False , null = False , on_delete = models.CASCADE)
     Image     = models.ImageField(upload_to = ImageUpload)
     
     def save(self , commit=True,*args , **kwargs):
        if commit:
            image_resize(self.Image, 600 , 600)
            super().save(*args, **kwargs)
        return super(ImageCity,self).save(*args, **kwargs) 
    
     def delete(self , *args , **kwargs):
        self.Image.delete()
        return super(ImageCity,self).delete(*args,**kwargs)
    
     def __str__(self):
            return str(self.id_image)

class ReviewCity(models.Model):
    user       = models.ForeignKey(User , on_delete=models.CASCADE)
    profile    = models.ForeignKey('accounts.Profile' , on_delete=models.CASCADE ,null=True, blank=True)
    city       = models.ForeignKey(City , on_delete=models.CASCADE)
    comment    = models.TextField(max_length=500)
    rate       = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.user.username
    
class PopularQuestion(models.Model):
    id = models.AutoField(primary_key=True)
    question = models.CharField(max_length=300)
    answer = models.TextField(max_length=500)
    country = models.ForeignKey(Country, null=True ,blank=False,on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
    

def upload_food(instance,filename):
    filename , extension = filename.rsplit('.')
    return "BackgroundFood/%s.%s"%(instance.id,extension)
    
class Food(models.Model):
    id         = models.AutoField(primary_key=True)
    title_food = models.CharField(max_length=50)
    info       = models.TextField(max_length=800)
    country    = models.ForeignKey(Country,on_delete=models.PROTECT)
    category   = models.CharField(max_length=30,choices=food_category)
    image      = models.ImageField(upload_to=upload_food)

    class Meta:
        pass

    def save(self , commit=True,*args , **kwargs):
        if commit:
            image_resize(self.image, 800 , 800)
            super().save(*args, **kwargs)
        return super(Food,self).save(*args, **kwargs) 
    
    def __str__(self):
        return self.title_food
 
    