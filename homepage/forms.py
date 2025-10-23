from django.forms import ModelForm
from homepage.models import NobarSpot

class NobarSpotForm(ModelForm):
    class Meta:
        model = NobarSpot
        fields = ["name", "home_team","away_team","date","time","city","address"]