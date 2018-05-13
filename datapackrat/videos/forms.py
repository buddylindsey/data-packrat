from django import forms

from .models import Video, Playlist
from .tasks import get_single_video


class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ['status', 'target', 'target_type', 'category', 'title']


class PlaylistForm(forms.ModelForm):
    class Meta:
        model = Playlist
        fields = ['status', 'target', 'target_type', 'category', 'title']


class ForceDownloadForm(forms.Form):
    video_id = forms.IntegerField(required=True, widget=forms.HiddenInput)

    def force_download(self):
        get_single_video.delay(self.cleaned_data['video_id'], True)