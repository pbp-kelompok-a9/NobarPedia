from django.db import models
from django.contrib.auth.models import User

# Proxy model buat data diri user
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_admin = models.BooleanField(default=False)
    fullname = models.CharField(max_length=100)
    email = models.EmailField()
    
    def __str__(self):
        return self.user.username
    