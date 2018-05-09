import requests

from django.conf import settings
from celery import shared_task

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
