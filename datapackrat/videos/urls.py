from django.urls import path

from .views import (
    VideoDownloadsView,
    AddVideoView,
    UpdateVideoView,
    AddPlaylistView,
    UpdatePlaylistView
)

urlpatterns = [
    path('downloads/', VideoDownloadsView.as_view(), name='video_downloads'),
    path('add/', AddVideoView.as_view(), name='video_add'),
    path('edit/<int:pk>/', UpdateVideoView.as_view(), name='video_edit'),
    path('add/playlist/', AddPlaylistView.as_view(), name='playlist_add'),
    path('edit/playlist/<int:pk>', UpdatePlaylistView.as_view(), name='playlist_edit')
]