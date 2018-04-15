import subprocess

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from videos.models import Playlist, Video, VideoCategory

from utils.dates import can_run_task

class Command(BaseCommand):
    help = 'Pull data down from the internet based on what is in the database'

    # def add_arguments(self, parser):
    #     parser.add_argument('poll_id', nargs='+', type=int)

    def handle(self, *args, **options):
        if not can_run_task():
            return

        command = ['/usr/local/bin/youtube-dl', '-f', 'bestvideo+bestaudio',
                   '--youtube-include-dash-manifest','--ffmpeg-location',
                   '/usr/local/bin/ffmpeg', '--recode-video', 'mp4',
                   '--download-archive', 'downloaded.txt', '-o']

        for playlist in Playlist.objects.filter(status=Playlist.IN_QUEUE):
            if not can_run_task:
                break
            run_command = command.copy()
            full_location = settings.DOWNLOAD_FOLDER.format(category=playlist.category.slug) + '{}/'.format(playlist.slug) + settings.DOWNLOAD_FILE_FORMAT
            location = [full_location, '{}'.format(playlist.target)]
            result = subprocess.run(command + location)
            if result.returncode == 0:
                playlist.status = Video.COMPLETED

            playlist.save()
