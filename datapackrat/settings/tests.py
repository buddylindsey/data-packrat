from django.test import TestCase


from .models import DownloadTemplate, Attribute, TemplateAttribute

class DownloadTemplateTest(TestCase):
    def test_template(self):

        ta1 = TemplateAttribute.objects.create(
            name='upload_date', code='%(upload_date)s', datatype='s')
        ta2 = TemplateAttribute.objects.create(
            name='playlist_index', code='%(playlist_index)d', datatype='d')
        ta3 = TemplateAttribute.objects.create(
            name='uploader', code='%(uploader)s', datatype='s')

        dt = DownloadTemplate.objects.create(title='base')

        Attribute.objects.create(
            template=dt, template_attribute=ta1, order=2, end_joiner=' - ')
        Attribute.objects.create(template=dt, template_attribute=ta2, order=4)
        Attribute.objects.create(
            template=dt, template_attribute=ta3, order=1, end_joiner='/')
        Attribute.objects.create(
            template=dt, template_attribute=ta3, order=3, end_joiner=' - ')


        self.assertEqual(
            dt.template(),
            '%(uploader)s/%(upload_date)s - %(uploader)s - %(playlist_index)d')