from django.db import models
import uuid
from django.contrib.auth.models import User

# Create your models here.
class NobarSpot(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name=models.CharField(max_length=255)
    home_team = models.CharField(max_length=50)
    away_team = models.CharField(max_length=50)
    date = models.DateField()
    time = models.TimeField()
    city = models.CharField(max_length=200)
    address = models.TextField()
    host = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name