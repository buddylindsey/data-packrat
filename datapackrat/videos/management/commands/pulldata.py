import subprocess

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from videos.models import Video, VideoCategory

from utils.dates import can_run_task

class Command(BaseCommand):
    help = 'Pull data down from the internet based on what is in the database'

    # def add_arguments(self, parser):
    #     parser.add_argument('poll_id', nargs='+', type=int)

    def get_location(self, video):
        location = settings.DOWNLOAD_FOLDER.format(category=video.category.slug)

        if video.playlist:
            location += '{}/'.format(video.playlist.slug)

        location += settings.DOWNLOAD_FILE_FORMAT

        return location

    def handle(self, *args, **options):
        if not can_run_task():
            return

        command = ['/usr/local/bin/youtube-dl', '-f', 'bestvideo+bestaudio',
                   '--youtube-include-dash-manifest','--ffmpeg-location',
                   '/usr/local/bin/ffmpeg', '--recode-video', 'mp4', '-o']

        for video in Video.objects.filter(status=Video.IN_QUEUE):
            if not can_run_task:
                break
            run_command = command.copy()

            location = [ self.get_location(video), '{}'.format(video.target) ]

            result = subprocess.run(command + location)
            if result.returncode == 0:
                video.status = Video.COMPLETED
            else:
                video.status = Video.ERROR

            video.save()
