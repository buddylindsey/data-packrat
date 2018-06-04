from django.test import TestCase
from model_mommy import mommy

from .tasks import GetSingleVideo
from .models import Video

class GetSingleVideoTests(TestCase):

    def test_get_location_with_category(self):
        name_template = mommy.make('settings.DownloadTemplate')

        mommy.make(
            'settings.Attribute', template=name_template,
            template_attribute__code='{category}', order=1, end_joiner='/')
        mommy.make(
            'settings.Attribute', template=name_template,
            template_attribute__code='%(uploader)s', order=2, end_joiner='/')
        vc = mommy.make('videos.VideoCategory', name='Firearms')
        video = mommy.make(
            'videos.Video', name_template=name_template,
            target_type=Video.TARGET_VIDEO, category=vc)

        gsv = GetSingleVideo(video.id)

        with self.settings(DOWNLOAD_BASE='/dir/'):
            self.assertEqual(gsv.get_location(), '/dir/firearms/%(uploader)s/')

    def test_get_location_with_playlist(self):
        name_template = mommy.make('settings.DownloadTemplate')
        playlist = mommy.make(
            'videos.Playlist', title='something',
            target_type=Video.TARGET_VIDEO)

        mommy.make(
            'settings.Attribute', template=name_template,
            template_attribute__code='{category}', order=1, end_joiner='/')
        mommy.make(
            'settings.Attribute', template=name_template,
            template_attribute__code='{playlist_slug}', order=2, end_joiner='/')
        mommy.make(
            'settings.Attribute', template=name_template,
            template_attribute__code='%(uploader)s', order=3, end_joiner='/')

        vc = mommy.make('videos.VideoCategory', name='Firearms')
        video = mommy.make(
            'videos.Video', name_template=name_template,
            target_type=Video.TARGET_VIDEO, category=vc, playlist=playlist)

        gsv = GetSingleVideo(video.id)

        with self.settings(DOWNLOAD_BASE='/dir/'):
            self.assertEqual(
                gsv.get_location(), '/dir/firearms/something/%(uploader)s/')