from django.db import models
import uuid
from django.contrib.auth.models import User
#from... import NobarSpot
# Create your models here.

#Placeholder
class NobarSpot(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    address = models.TextField()
    stars = models.SmallIntegerField()
    host = models.ForeignKey(User, on_delete=models.CASCADE, related_name='hosted_nobars_review')
    time = models.TimeField()
    date = models.DateField()
    
class reviewers(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    stars = models.SmallIntegerField()
    nobar_spot = models.ForeignKey(NobarSpot, on_delete=models.CASCADE, null = True )