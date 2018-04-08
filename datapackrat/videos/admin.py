from django.contrib import admin

from .models import Video

@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('target', 'status', 'target_type')
    list_filter = ('status', 'target_type')