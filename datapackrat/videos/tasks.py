import requests
import youtube_dl

from django.conf import settings
from celery import shared_task

from videos.models import Video, VideoCategory
from .models import  Channel, Video


class LatestChannelVideo:
    def run(self):
        for channel in Channel.objects.filter(paused=False).iterator():
            if channel.target_type != Channel.TARGET_YOUTUBE:
                continue

            url = settings.YOUTUBE_CHANNEL_URL.format(
                channel_id=channel.target, api_key=settings.YOUTUBE_API_KEY)

            response = requests.get(url)

            data = response.json()

            for v in data['items']:
                if v['id']['kind'] != "youtube#video":
                    continue

                video, created = Video.objects.get_or_create(target=v['id']['videoId'])

                if (created):
                    video.status = Video.IN_QUEUE
                    video.target_type = Video.TARGET_YOUTUBE
                    video.category = channel.category
                    video.title = v['snippet']['title']
                    video.save()

@shared_task
def find_latest_channel_videos():
    lcv = LatestChannelVideo()
    lcv.run()


class PullVideoData:
    def get_location(self, video):
        location = settings.DOWNLOAD_FOLDER.format(category=video.category.slug)

        if video.playlist:
            location += '{}/'.format(video.playlist.slug)

        location += settings.DOWNLOAD_FILE_FORMAT

        return location

    def run(self):

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

            ydl_opts['outtmpl'] = self.get_location(video)

            try:
                with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([video.target])
                video.status = Video.COMPLETED
            except:
                video.status = Video.ERROR
            video.save()

@shared_task
def pull_video_data():
    pvd = PullVideoData()
    pvd.run()