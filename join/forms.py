from django import forms
from django.forms import ModelForm
from django.utils.html import strip_tags
from join.models import Join_List

class JoinForm(ModelForm):
    class Meta:
        model = Join_List
        fields = ["status"]
        widgets = {
            'status': forms.Select(attrs={'class': 'bg-black text-white p-2 rounded w-full'})
        }
