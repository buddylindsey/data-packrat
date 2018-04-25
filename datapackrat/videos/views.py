from django.views.generic import ListView, CreateView, UpdateView
from django.urls import reverse_lazy

from .models import Video
from .forms import VideoForm, PlaylistForm


class VideoDownloadsView(ListView):
    model = Video
    context_object_name = 'videos'
    template_name = 'videos/downloads.html'
    ordering = ('-id')


class AddVideoView(CreateView):
    model = Video
    template_name = 'videos/add_video.html'
    success_url = reverse_lazy('video_downloads')
    form_class = VideoForm


class UpdateVideoView(UpdateView):
    model = Video
    template_name = 'videos/add_video.html'
    success_url = reverse_lazy('video_downloads')
    form_class = VideoForm


class AddPlaylistView(CreateView):
    model = Video
    template_name = 'videos/add_playlist.html'
    success_url = reverse_lazy('video_downloads')
    form_class = PlaylistForm


class UpdatePlaylistView(UpdateView):
    model = Video
    template_name = 'videos/add_playlist.html'
    success_url = reverse_lazy('video_downloads')
    form_class = PlaylistForm
