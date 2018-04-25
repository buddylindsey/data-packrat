from django import forms

from .models import Video, Playlist


class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ['status', 'target', 'target_type', 'category', 'title']


class PlaylistForm(forms.ModelForm):
    class Meta:
        model = Playlist
        fields = ['status', 'target', 'target_type', 'category', 'title']
