from django.db import models

from django_extensions.db.models import TimeStampedModel
from django_extensions.db.fields import AutoSlugField

import requests
from bs4 import BeautifulSoup

class VideoCategory(TimeStampedModel):
    name = models.CharField(max_length=25)
    slug = AutoSlugField(populate_from=['name'])

    def __str__(self):
        return self.name

class Video(TimeStampedModel):
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
    target_choices = (
        ('video', 'Video'),
        ('youtube', 'YouTube'),
        ('full30', 'Full 30')
    )
    target_type = models.CharField(max_length=25, choices=target_choices)
    category = models.ForeignKey(VideoCategory, on_delete=models.SET_NULL, null=True)

    title = models.CharField(max_length=500, blank=True, help_text='Should Auto-populate if you don\'t fill it in.')

    def __str__(self):
        return self.target

    def save(self, *args, **kwargs):

        if self.target_type == 'video' or not self.target.startswith('http'):
            return super().save(*args, **kwargs)

        if not self.title:
            response = requests.get(self.target)
            soup = BeautifulSoup(response.content, 'html.parser')

            self.title = soup.find('title').contents[0]

        return super().save(*args, **kwargs)
