from django.views.generic import TemplateView

from videos.models import Video


class IndexView(TemplateView):
    template_name = 'home/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['latest_downloaded_videos'] = Video.objects.filter(
            status=Video.COMPLETED).order_by('-modified')[:10]
        context['video_completed'] = Video.objects.filter(status=Video.COMPLETED).count()
        context['video_in_queue'] = Video.objects.filter(status=Video.IN_QUEUE).count()
        context['video_errored'] = Video.objects.filter(status=Video.ERROR).count()
        return context
