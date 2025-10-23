from django.forms import ModelForm
from django.utils.html import strip_tags
from django.core.exceptions import ValidationError
from . import models


class PlayerForm(ModelForm):
    class Meta:
        model = models.Player
        fields = ["name", "logo", "established_date", "is_defunct"]

    def clean_name(self):
        return strip_tags(self.cleaned_data["name"])


class MatchForm(ModelForm):
    class Meta:
        model = models.Match
        fields = ["competition", "players", "begin_datetime", "end_datetime"] # shownAt

    def clean(self):
        super().clean()
        begin_datetime = self.cleaned_data["begin_datetime"]
        end_datetime = self.cleaned_data["end_datetime"]

        if (begin_datetime > end_datetime):
            raise ValidationError("End match time must be greater than or equal begin match time")


class CompetitionForm(ModelForm):
    class Meta:
        model = models.Competition
        fields = ["name", "logo", "begin_date", "end_date"]

    def clean_name(self):
        return strip_tags(self.cleaned_data["name"])

    def clean(self):
        super().clean()

        begin_date = self.cleaned_data["begin_date"]
        end_date = self.cleaned_data["end_date"]

        if (begin_date >= end_date):
            raise ValidationError("End date must be greater than or equal begin date")
