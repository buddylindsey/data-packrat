from django.views.generic import ListView

from .models import Video


class VideoHistoryView(ListView):
    model = Video
    context_object_name = 'videos'
    template_name = 'videos/history.html'