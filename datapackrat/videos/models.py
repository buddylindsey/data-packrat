from django.db import models

from django_extensions.db.models import TimeStampedModel

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

    def __str__(self):
        return self.target
