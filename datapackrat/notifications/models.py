from django.db import models

from django_extensions.db.models import TimeStampedModel


class Message(TimeStampedModel):
    message = models.CharField(max_length=255)
    UNREAD = 'unread'
    READ = 'read'
    STATUS_CHOICES = (
        (UNREAD, 'Unread'),
        (READ, 'Read')
    )
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default=UNREAD)

    def __str__(self):
        return '{} - {}'.format(self.status, self.message)