# forms.py

from django import forms
from .models import Profile, Song, Price, PortfolioPicture, PortfolioVideo

class ArtistProfileForm(forms.ModelForm):
    profile_picture = forms.ImageField(required=False)

    class Meta:
        model = Profile
        fields = ['profile_picture']

class PricingForm(forms.ModelForm):
    class Meta:
        model = Price
        fields = ['price']

class PortfolioPictureForm(forms.ModelForm):
    class Meta:
        model = PortfolioPicture
        fields = ['image']

class PortfolioVideoForm(forms.ModelForm):
    class Meta:
        model = PortfolioVideo
        fields = ['video']

class SongForm(forms.ModelForm):
    class Meta:
        model = Song
        fields = ['title', 'file']