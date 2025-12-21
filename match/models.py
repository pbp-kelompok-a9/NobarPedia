from django.db import models
from homepage.models import NobarSpot
import uuid


def player_logo_image_path(instance, filename):
    return 'images/player_logos/{0}'.format(instance.id)


class Player(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    logo = models.URLField(null=True, blank=True)
    established_date = models.DateField()
    is_defunct = models.BooleanField(default=False, blank=True)


def competition_logo_image_path(instance, filename):
    return 'images/player_logos/{0}'.format(instance.id)


class Competition(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    logo = models.URLField(null=True, blank=True)
    begin_date = models.DateField()
    end_date = models.DateField()


class Match(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    competition = models.ForeignKey(to=Competition, on_delete=models.CASCADE)
    players = models.ManyToManyField(to=Player)
    shownAt = models.ManyToManyField(to=NobarSpot)
    begin_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
