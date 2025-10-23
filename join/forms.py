from django.forms import ModelForm
from django.utils.html import strip_tags
from join.models import Join_List

class JoinForm(ModelForm):
    class Meta:
        model = Join_List
        fields = ["status"]

    # def clean_title(self):
    #     title = self.cleaned_data["title"]
    #     return strip_tags(title)