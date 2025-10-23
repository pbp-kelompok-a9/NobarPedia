from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile

class CustomUserCreationForm(UserCreationForm):
    # email = forms.EmailField(required=True)
    fullname = forms.CharField(max_length=100, required=True)
    bio = forms.CharField(widget=forms.Textarea, required=False)
    profile_picture = forms.ImageField(required=False) 
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'fullname', 'bio', 'profile_picture']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']  # Store email ke model user
        if commit:
            user.save()
            # Bikin object Profile baru, store data profil disana, sambungkan sama model user tadi
            profile = Profile.objects.create(
                user=user,
                fullname=self.cleaned_data.get('fullname'),
                bio=self.cleaned_data.get('bio'),
                profile_picture=self.cleaned_data.get('profile_picture', None) 
            )
            profile.save()
        return user


class CustomUserEditForm(forms.ModelForm):
    email = forms.EmailField(required=True)
    fullname = forms.CharField(max_length=100, required=True)
    bio = forms.CharField(widget=forms.Textarea, required=False)
    profile_picture = forms.ImageField(required=False) 

    class Meta:
        model = User
        fields = ['username', 'email', 'fullname', 'bio', 'profile_picture']  # Mengambil field dari model User

    def __init__(self, *args, **kwargs):
        super(CustomUserEditForm, self).__init__(*args, **kwargs)
        # Isi field dari model Profile jika ada
        if self.instance and hasattr(self.instance, 'profile'):
            self.fields['username'].initial = self.instance.username
            self.fields['email'].initial = self.instance.email
            self.fields['fullname'].initial = self.instance.profile.fullname
            self.fields['bio'].initial = self.instance.profile.bio
            self.fields['profile_picture'].initial = self.instance.profile.profile_picture

    def save(self, commit=True):
        user = super(CustomUserEditForm, self).save(commit=False)
        if commit:
            user.save()
            profile, _ = Profile.objects.get_or_create(user=user)
            profile.fullname = self.cleaned_data.get('fullname') or ''
            profile.bio = self.cleaned_data.get('bio') or ''
            # Only set profile_picture if present in cleaned_data
            pic = self.cleaned_data.get('profile_picture')
            if pic is not None:
                profile.profile_picture = pic
            profile.save()
        return user