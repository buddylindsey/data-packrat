from django.views.generic import ListView

from .models import Video


class VideoDownloadsView(ListView):
    model = Video
    context_object_name = 'videos'
    template_name = 'videos/downloads.html'
    ordering = ('-id')