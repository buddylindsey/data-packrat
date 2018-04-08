import subprocess

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from videos.models import Video

from utils.dates import can_run_task

class Command(BaseCommand):
    help = 'Pull data down from the internet based on what is in the database'

    # def add_arguments(self, parser):
    #     parser.add_argument('poll_id', nargs='+', type=int)

    def handle(self, *args, **options):
        if not can_run_task():
            return

        command = ['youtube-dl', '-f', 'bestvideo+bestaudio',
                   '--youtube-include-dash-manifest', '-o',
                   settings.DOWNLOAD_LOCATION]

        for video in Video.objects.filter(status=Video.IN_QUEUE):
            if not can_run_task:
                break
            run_command = command.copy()
            result = subprocess.run(command + [video.target])
            if result.returncode == 0:
                video.status = Video.COMPLETED
            else:
                video.status = Video.ERROR

            video.save()