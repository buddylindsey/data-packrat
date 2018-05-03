import subprocess

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from videos.models import Video, VideoCategory

from utils.dates import can_run_task

import youtube_dl

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

        ydl_opts = {
            'format': 'bestvideo+bestaudio',
            'writesubtitles': True,
            'subtitlesformat': 'srt',
            'ffmpeg_location': settings.FFMPEG_LOCATION,
            'prefer_ffmpeg': True,
            'postprocessors': [
                { 'key': 'FFmpegVideoConvertor', 'preferedformat': 'mp4' },
                { 'key': 'FFmpegMetadata' }
            ],
        }

        for video in Video.objects.filter(status=Video.IN_QUEUE):
            if not can_run_task():
                break

            ydl_opts['outtmpl'] = self.get_location(video)

            try:
                with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([video.target])
                video.status = Video.COMPLETED
            except:
                video.status = Video.ERROR
            video.save()
