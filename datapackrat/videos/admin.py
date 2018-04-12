from django.contrib import admin

from .models import Video, VideoCategory

@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'target', 'status', 'target_type')
    list_filter = ('status', 'target_type')

@admin.register(VideoCategory)
class VideoCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)