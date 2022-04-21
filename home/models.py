
from django.db import models
from accounts.models import User
from embed_video.fields import EmbedVideoField

# Create your models here.


class Property(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True, blank=True)
    name = models.CharField(max_length=50)
    image = models.ImageField( upload_to="property")
    description = models.TextField()
    price = models.DecimalField( max_digits=10, decimal_places=2)
    location = models.CharField(max_length=50)
    property_type = models.CharField(max_length=50)
    area = models.CharField(max_length=50)
    beds = models.CharField(max_length=50)
    baths = models.CharField(max_length=50)
    garage = models.CharField(max_length=50)
    video = EmbedVideoField(blank= True, null=True)
    date_added = models.DateField(auto_now_add=True)
    is_publish = models.BooleanField(default=False)

    class Meta:
        ordering = ('-date_added',)
        
    def __str__(self):
        return self.name


class Slider(models.Model):
    image = models.ImageField( upload_to="slider/")
    property = models.ForeignKey(Property, on_delete= models.CASCADE)

    def __str__(self):
        return self.property.name

class Inquary(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank = True, null= True)
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=254)
    phone = models.CharField(max_length = 26, null = True, blank = True)
    message = models.TextField()