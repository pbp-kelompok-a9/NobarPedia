from django.db import models
import uuid
from django.contrib.auth.models import User
# from ... import nobar_place

# placeholder, remove if implemented by homepage app
class Nobar_Place(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.TextField()
    made_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    location = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

# Create your models here.
class Join_List(models.Model):
    status_options = [
        ("100%", "Pasti join"),
        ("50", "Mungkin join"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    nobar_place = models.ForeignKey(Nobar_Place, on_delete=models.CASCADE, null=True)
    status = models.TextField(choices=status_options, default="50%")
    created_at = models.DateTimeField(auto_now_add=True)


