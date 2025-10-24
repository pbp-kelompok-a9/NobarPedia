from django.db import models
import uuid
from django.contrib.auth.models import User
from homepage.models import NobarSpot

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


