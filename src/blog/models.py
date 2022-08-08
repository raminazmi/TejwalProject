from django.db import models
from accounts.models import Profile
from home.images import image_resize
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField 
# Create your models here.

order = ( (1,1),(2,2),(3,3),(4,4),(5,5),(6,6),(7,7),(8,8),(9,9))

category_blog = [
    ('advices','نصائح'),
    ('suggestions','اقتراحات'),
    ('public','عامه'),
    ('learning','محتوى تعليمي'),
    ]
class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    def __str__(self):
        return self.name
    
class Post(models.Model):
    class Meta:
        ordering = ["-publish_date"]

    title = models.CharField(max_length=255, unique=True)
    subtitle = models.TextField(max_length=500, blank=True)
    category = models.CharField(max_length=100 , choices=category_blog)
    slug = models.SlugField(max_length=255, unique=True)
    meta_description = models.CharField(max_length=400, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    publish_date = models.DateTimeField(blank=True, null=True)
    published = models.BooleanField(default=False)
    background = models.ImageField(upload_to = 'BackgroundPost/')
    body =  RichTextUploadingField(blank=True,null=True)
    source = models.CharField(max_length=100)
    author = models.ForeignKey(Profile, on_delete=models.PROTECT)
    tags = models.ManyToManyField(Tag, blank=True )
    
    def save(self , commit=True,*args , **kwargs):
        if commit:
            image_resize(self.background, 900 , 900)
            super().save(*args, **kwargs)
        return super(Post,self).save(*args, **kwargs)
    def __str__(self):
        return self.title
    
class PartsPost(models.Model):
    class Meta:
        ordering = ["order"]
        
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    title = models.CharField(max_length=250 , null=True , blank= True)
    body = RichTextField()
    image = models.ImageField(upload_to='ImagesPartsPost/',null=True , blank= True)
    alt_image = models.CharField(max_length=200 , null=True , blank= True)
    order = models.IntegerField(choices = order)
    
    def __str__(self):
        return self.title
    
    def save(self , commit=True,*args , **kwargs):
        if self.image != None:
            if commit:
                image_resize(self.image, 600 , 600)
                super().save(*args, **kwargs)
        return super(PartsPost,self).save(*args, **kwargs)



    