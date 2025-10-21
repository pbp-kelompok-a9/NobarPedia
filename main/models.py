from django.db import models


# Create your models here.
class NobarLocation(models.Model):
    name = models.CharField(max_length=255)
    latitude = models.DecimalField(max_digits=8, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    maps_url = models.URLField()
    stars = models.SmallIntegerField()
    
