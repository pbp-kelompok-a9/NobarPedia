from django.forms import ModelForm
from review.models import reviewers

class ReviewForm(ModelForm):
    class Meta:
        model = reviewers
        fields =["comment", "stars"]