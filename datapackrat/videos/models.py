from django.db import models
from django.conf import settings

from django_extensions.db.models import TimeStampedModel
from django_extensions.db.fields import AutoSlugField

import requests
from bs4 import BeautifulSoup


class VideoCategory(TimeStampedModel):
    name = models.CharField(max_length=25)
    slug = AutoSlugField(populate_from=['name'])

    def __str__(self):
        return self.name


class DownloadBase(TimeStampedModel):
    IN_QUEUE = 'in-queue'
    COMPLETED = 'completed'
    ERROR = 'error'
    target_status = (
        (IN_QUEUE, 'In Queue'),
        (COMPLETED, 'Completed'),
        (ERROR, 'Errored')
    )
    status = models.CharField(
        max_length=25, choices=target_status, default=IN_QUEUE)
    target = models.CharField(max_length=1000)
    TARGET_YOUTUBE = 'youtube'
    TARGET_VIDEO = 'video'
    target_choices = (
        (TARGET_VIDEO, 'Video'),
        (TARGET_YOUTUBE, 'YouTube')
    )
    target_type = models.CharField(max_length=25, choices=target_choices)
    category = models.ForeignKey(
        VideoCategory, on_delete=models.SET_NULL, null=True)

    title = models.CharField(
        max_length=500, blank=True,
        help_text='Should Auto-populate if you don\'t fill it in.')

    class Meta:
        abstract = True


class Video(DownloadBase):
    playlist = models.ForeignKey(
        'videos.Playlist', null=True, blank=True, on_delete=models.SET_NULL,
        related_name='videos')

    def __str__(self):
        return self.target

    def save(self, *args, **kwargs):

        if self.target_type != 'youtube' and not self.target.startswith('http'):
            return super().save(*args, **kwargs)

        if not self.title:
            response = requests.get(
                settings.YOUTUBE_VIDEO_URL.format(
                    id=self.target, api_key=settings.YOUTUBE_API_KEY))
            self.title = response.json()['items'][0]['snippet']['title']

        return super().save(*args, **kwargs)


class Playlist(DownloadBase):
    slug = AutoSlugField(populate_from=['title'])

    def get_playlist_videos(self, page=None):
        videos = []

        url = settings.YOUTUBE_PLAYLIST_URL.format(
            id=self.target, api_key=settings.YOUTUBE_API_KEY)
        if page:
            url += "&pageToken={page}".format(page=page)
            print(url)

        response = requests.get(url)

        data = response.json()

        if 'nextPageToken' in data:
            videos += self.get_playlist_videos(page=data['nextPageToken'])

        return videos + data['items']

    def save(self, *args, **kwargs):
        if self.id:
            super().save(*args, **kwargs)
            return

        super().save(*args, **kwargs)

        for item in self.get_playlist_videos():
            video = Video.objects.create(
                title=item['snippet']['title'],
                target=item['snippet']['resourceId']['videoId'],
                category=self.category,
                target_type=self.target_type,
                status=self.status)
            self.videos.add(video)


class Channel(TimeStampedModel):
    target = models.CharField(max_length=1000)
    TARGET_YOUTUBE = 'youtube'
    target_choices = (
        (TARGET_YOUTUBE, 'YouTube'),
    )
    target_type = models.CharField(max_length=25, choices=target_choices)
    slug = AutoSlugField(populate_from=['title'])
    category = models.ForeignKey(
        VideoCategory, on_delete=models.SET_NULL, null=True)
    title = models.CharField(
        max_length=500, blank=True,
        help_text='Should Auto-populate if you don\'t fill it in.')
    paused = models.BooleanField(default=False)

    def __str__(self):
        return self.title