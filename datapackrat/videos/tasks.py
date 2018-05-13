import requests
import youtube_dl

from django.conf import settings
from celery import shared_task

from videos.models import Video, VideoCategory
from .models import  Channel, Video


class GetSingleVideo:
    def __init__(self, video_id, force=False):
        self.video = Video.objects.get(id=video_id)
        self.force = force

    def get_location(self):
        location = settings.DOWNLOAD_FOLDER.format(
            category=self.video.category.slug)

        if self.video.playlist:
            location += '{}/'.format(self.video.playlist.slug)

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

        ydl_opts['outtmpl'] = self.get_location()

        try:
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download([self.video.target])
            self.video.status = Video.COMPLETED
        except:
            self.video.status = Video.ERROR
        self.video.save()

@shared_task
def get_single_video(video_id, force=False):
    gsv = GetSingleVideo(video_id, force)
    gsv.run()


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
    def run(self):
        for video in Video.objects.filter(status=Video.IN_QUEUE):
            get_single_video.delay(video.id)


@shared_task
def pull_video_data():
    pvd = PullVideoData()
    pvd.run()