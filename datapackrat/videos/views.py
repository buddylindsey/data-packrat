from django.views.generic import ListView, CreateView, UpdateView, FormView
from django.urls import reverse_lazy

from .tasks import get_single_video

from .models import Video
from .forms import VideoForm, PlaylistForm, ForceDownloadForm


class VideoDownloadsView(ListView):
    model = Video
    context_object_name = 'videos'
    template_name = 'videos/downloads.html'
    ordering = ('-id')
    paginate_by = 50


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
    context_object_name = 'video'


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


class ForceDownloadView(FormView):
    success_url = reverse_lazy('video_downloads')
    form_class = ForceDownloadForm

    def form_valid(self, form):
        form.force_download()
        return super().form_valid(form)
