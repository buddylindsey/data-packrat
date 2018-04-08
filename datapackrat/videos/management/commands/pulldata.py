import subprocess

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from videos.models import Video, VideoCategory

from utils.dates import can_run_task

class Command(BaseCommand):
    help = 'Pull data down from the internet based on what is in the database'

    # def add_arguments(self, parser):
    #     parser.add_argument('poll_id', nargs='+', type=int)

    def check_folders(self):
        for category in VideoCategory.objects.all():
            print(category.slug)
            subprocess.run([
                'mkdir', '-p', settings.DOWNLOAD_FOLDER.format(category=category.slug)
            ])

    def handle(self, *args, **options):
        self.check_folders()
        if not can_run_task():
            return

        command = ['youtube-dl', '-f', 'bestvideo+bestaudio',
                   '--youtube-include-dash-manifest', '-o']

        for video in Video.objects.filter(status=Video.IN_QUEUE):
            if not can_run_task:
                break
            run_command = command.copy()
            location = [
                settings.DOWNLOAD_LOCATION.format(category=video.category.slug),
                video.target
            ]
            result = subprocess.run(command + location)
            if result.returncode == 0:
                video.status = Video.COMPLETED
            else:
                video.status = Video.ERROR

            video.save()