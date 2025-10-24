from homepage.models import NobarSpot
from django import forms
from django.utils import timezone

class NobarSpotForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        today = timezone.localdate().isoformat()
        self.fields['date'].widget.attrs['min'] = today
        
    class Meta:
        model = NobarSpot
        fields = ["name", "thumbnail","home_team","away_team","date","time","city","address"]
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'w-full'}),
            'time': forms.TimeInput(attrs={'type': 'time', 'class': 'w-full'}),
            'address': forms.Textarea(attrs={'rows': 3, 'class': 'w-full'}),
        }