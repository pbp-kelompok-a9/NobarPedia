from django.db import models
import uuid
from django.contrib.auth.models import User
#from... import NobarSpot
#from... import Account
# Create your models here.

#Placeholder
class NobarSpot(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    address = models.TextField()
    stars = models.SmallIntegerField()
    host = models.ForeignKey(User, on_delete=models.CASCADE, null = True)
    time = models.TimeField()
    date = models.DateField()
    
class reviewers(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    comment = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, null = True)
    created_at = models.DateTimeField(auto_now_add=True)
    stars = models.SmallIntegerField()