from django.db import models
import uuid
from django.contrib.auth.models import User


class NobarSpot(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name=models.CharField(max_length=255)
    thumbnail = models.URLField(blank=True, null=True)
    home_team = models.CharField(max_length=50)
    away_team = models.CharField(max_length=50)
    date = models.DateField()
    time = models.TimeField()
    city = models.CharField(max_length=200)
    address = models.TextField()
    host = models.ForeignKey(User, on_delete=models.CASCADE, related_name='homepage_spots',null=True)

    def __str__(self):
        return self.name

class Join_List(models.Model):
    status_options = [
        ("pasti", "Pasti"),
        ("mungkin", "Mungkin"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    nobar_place = models.ForeignKey(NobarSpot, on_delete=models.CASCADE, null=True)
    status = models.TextField(choices=status_options, default="50%")
    created_at = models.DateTimeField(auto_now_add=True)


