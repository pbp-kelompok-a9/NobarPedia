from django.db import models
import uuid
from django.contrib.auth.models import User
from homepage.models import NobarSpot

    
class reviewers(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    comment = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, null = True)
    nobar_place = models.ForeignKey(NobarSpot, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    stars = models.SmallIntegerField()
