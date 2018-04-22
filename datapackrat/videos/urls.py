from django.urls import path

from .views import VideoDownloadsView

urlpatterns = [
    path('downloads/', VideoDownloadsView.as_view(), name='video_downloads')
]