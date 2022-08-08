from datetime import datetime
from django.core.files import File
from pathlib import Path
from PIL import Image
from io import BytesIO
from django.db import models
from country.models import City
from django.utils.text import slugify
from multiselectfield import MultiSelectField
from django.contrib.auth.models import User
# Create your models here.
order = ((0,0),(1,1),(2,2),(3,3),(4,4),(5,5))
place_category =[
    ('فن وثقافة',(
        ('historical','تاريخ وآثار'),
        ('Architectural','هندسة المعمارية'),
        ('museums_galleries','متاحف ومعارض فنية'),
        ('arts_crafts','فنون وحرف يدويه'),
    )),
    ('beach',(
        ('beach',' شواطئ'),
        ('lake','بحيرات وشلالات'),
        ('resort','منتجعات'),
        ('island','جزر'),
        ('Harbor','مؤانى'),
    )),
    ('الطبيعة والمتزهات',(
        ('park',' حدائق'),
        ('air',' أنشطة الهواءالطلق'),
        ('Sanctuaries_zoos',' محميات و حدائق حيوانات '),
        ('forests',' غابات'),
    )),
    ('المغامرات والترفيه',(
        ('theaters','مسارح'),
        ('amusement','ملاهي '),
        ('stadium','ملاعب'),
        ('gyms','صالات رياضيه'),
    )),
      (' التسوق والاستجمام',(
        ('shopping_centers',' مراكز تسوق'),
        ('traditional_markets',' أسواق شعبية'),
        ('recreation_centers','منتجع صحي '),
      )),
    ('معالم دينيه',(
        ('mosques',' مساجد'),
        ('house_worship','دور عباده'),
        ('Holy_places','أماكن مقدسه '),
    )),
]
activtiy_category =[
    ('sea_activity','أنشطة البحار'),
    ('adventures',' مغامرات'),
    ('sport',' رياضه'),
    ('control','قياده وتحكم'),
    ('family_activity',' نشاط عائلي'),
    ('marketing',' تسوق'),
]

features =[
    ('families','مناسب للعائلات'),
    ('Children','مناسب للأطفال'),
    ('couples','مناسب للأطفال'),
    ('groups','مناسب للمجموعات'),
    ('Internet','إنترنت مجاني'),
    ('free',' مجاني'),
    ('delivery','توصيل '),
    ('parking',' موقف سيارات متاح'),
    ('Indoor_yards','ساحات داخليه '),
    ('outdoor_yards','ساحات خارجيه'),
    ('green_yards','ساحات خضراء'),
] 

events_category = [
    ('religious','ديني'),
    ('sport','الرياضه'),
    ('art','فن وثقافة'),
    ('festival','مهرجانات'),
    ('entertainment','ترفيه'),
    ('gallery','معارض'),
    ('conspiracy','مؤتمرات'),
    ('marketing','التسوق')
]

events_audience = [
    ('public','عام'),
    ('private','خاص')
    ]

image_types = {
    "jpg": "JPEG",
    "jpeg": "JPEG",
    "png": "PNG",
    "gif": "GIF",
    "tif": "TIFF",
    "tiff": "TIFF",
}
# to define folder to save image and rename image when save
def upload_image_background(instance,filename):
    imagename , extenstion = filename.split(".")
    return "BackgroundPlace/%s.%s"%(imagename, extenstion)
# rename image that background to activtiy
def upload_image_activity(instance, filename):
    imagename ,extention = filename.split(".")
    return "BackgroundActivity/%s.%s"%(instance.id,extention)

def upload_image_event(instance, filename):
    imagename ,extention = filename.split(".")
    return "BackgroundEvent/%s.%s"%(instance.id,extention)

def image_resize(image, width, height):
    # Open the image using Pillow
    img = Image.open(image)
    # check if either the width or height is greater than the max
    if img.width > width or img.height > height:
        output_size = (width, height)
        # Create a new resized “thumbnail” version of the image with Pillow
        img.thumbnail(output_size)
        # Find the file name of the image
        img_filename = Path(image.file.name).name
        # Spilt the filename on “.” to get the file extension only
        img_suffix = Path(image.file.name).name.split(".")[-1]
        # Use the file extension to determine the file type from the image_types dictionary
        img_format = image_types[img_suffix]
        # Save the resized image into the buffer, noting the correct file type
        buffer = BytesIO()
        img.save(buffer, format=img_format)
        # Wrap the buffer in File object
        file_object = File(buffer)
        # Save the new resized file as usual, which will save to S3 using django-storages
        image.save(img_filename, file_object)
        
class Activity(models.Model):
    id             = models.AutoField(primary_key=True)
    title          = models.CharField(max_length=80)
    info           = models.TextField(max_length=500,null=True)
    category       = models.CharField(max_length=80 , null=True ,choices= activtiy_category)
    image          = models.ImageField(upload_to= upload_image_activity , null=True)
    recommended    = models.BooleanField(default=False)
    city = models.ForeignKey(City, default=None,null=True, blank=False ,on_delete=models.CASCADE)
    
    def __str__(self):
        return self.title
    
    def save(self ,commit=True, *args , **kwargs):
        if commit:
            image_resize(self.image, 800 , 800)
            super().save(*args, **kwargs)

class Place(models.Model):
    class Meta:
        ordering = ["created_at"]
    id          = models.AutoField(primary_key=True)
    title_place = models.CharField(max_length=100,null=False , blank=False)
    info        = models.TextField(max_length=1200 , null=False, blank=False)
    city        = models.ForeignKey(City , on_delete=models.CASCADE , null=False, blank=False)
    category    = models.CharField(max_length=50 , null=False, blank=False,choices=tuple(place_category))
    features    = MultiSelectField(choices=features)
    short_info  = models.CharField(max_length=40,default='None')
    location    = models.TextField(max_length=800 , default='None')
    order       = models.IntegerField(null=True, blank=True , choices=order)    
    slug        = models.SlugField(max_length=255 , unique=True) 
    background  = models.ImageField(upload_to = upload_image_background)
    website     = models.URLField(null=True, blank=True)
    created_at = models.DateTimeField(null=True, blank=True,auto_now_add=True)

    def __str__(self):
        return self.title_place
    
    def save(self ,commit=True, *args , **kwargs):
        if commit:
            image_resize(self.background, 600 , 600)
            super().save(*args, **kwargs)
        return super(Place,self).save(*args, **kwargs)

    class Meta:
        ordering = ['order']

class Favorite(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User , on_delete=models.CASCADE)
    place = models.ForeignKey(Place , on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

# لتحديد المجلد لحفظ الصوره واعادة التسمية 
def upload_image(instance,filename):
    image_name , extenstion = filename.split('.')
    return "Place/%s/%s.%s"%(instance.place.city.city_id,instance.place.id,extenstion)

class ImagePlace(models.Model):
    place     = models.ForeignKey(Place , on_delete=models.CASCADE)
    image     = models.ImageField(upload_to = upload_image)
    describe  = models.CharField(max_length=80 , null =True , blank=True)
    
    def delete(self,*agrs , **kwargs):
        self.image.delete()
        return super(ImagePlace,self).delete(*agrs ,**kwargs)
    
    def save(self ,commit=True, *args , **kwargs):
        self.describe = self.place.title_place
        if commit:
            image_resize(self.image, 600 , 600)
            super().save(*args, **kwargs)
        return super(ImagePlace,self).save(*args, **kwargs)
         
class Review(models.Model):
    user       =models.ForeignKey("accounts.Profile" , on_delete=models.CASCADE)
    place      = models.ForeignKey(Place , on_delete=models.CASCADE)
    comment    = models.TextField(max_length=500)
    rate       = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username
    
class Event(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    category = models.CharField(max_length=50 ,choices=events_category)
    audience = models.CharField(max_length=50 ,choices=events_audience)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    info = models.TextField(max_length=500)
    fees = models.BooleanField(default=False)
    link_ticket = models.URLField(max_length=300)
    start_date = models.DateField()
    end_date   = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    background = models.ImageField(upload_to = upload_image_event)
    slug = models.SlugField(max_length=300 , blank=True ,null = False)
    
    def __str__(self):
        return self.title
    
    def save(self ,commit=True, *args , **kwargs):
        if commit:
            image_resize(self.background, 700 , 700)
            super().save(*args, **kwargs)
        return super(Event,self).save(*args, **kwargs)
    
