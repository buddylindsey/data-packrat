from django.contrib import admin

from .models import Channel, Playlist, Video, VideoCategory


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'target', 'status', 'target_type', 'get_playlist')
    list_filter = ('status', 'target_type')

    def get_playlist(self, obj):
        if obj.playlist:
            return obj.playlist.title
    get_playlist.short_description = 'Playlist'


@admin.register(VideoCategory)
class VideoCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Playlist)
class PlaylistAdmin(admin.ModelAdmin):
    list_display = ('title', 'target', 'status', 'target_type', 'download_status')
    list_filter = ('status', 'target_type')

    def download_status(self, obj):
        status = []
        status

        for video in obj.videos.all():
            status.append(video.status == Video.COMPLETED)

        if all(status):
            return 'Completed'

        if obj.videos.filter(status=Video.ERROR):
            return 'Errored'

        return 'In Queue'


@admin.register(Channel)
class ChannelAdmin(admin.ModelAdmin):
    pass