from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.Match)
admin.site.register(models.Competition)
admin.site.register(models.Player)
