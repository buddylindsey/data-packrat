from django.db import models

from django_extensions.db.models import TimeStampedModel, TitleSlugDescriptionModel


class DownloadTemplate(TimeStampedModel, TitleSlugDescriptionModel):
    attributes = models.ManyToManyField(
        'settings.TemplateAttribute', through='Attribute',
        through_fields=('template', 'template_attribute'))

    def __str__(self):
        return self.title

    def template(self):
        template = ''

        attrs = self.attribute_set.all().order_by('order')

        for attr in attrs:
            template += "{}{}{}".format(
                attr.start_joiner, attr.template_attribute.code, attr.end_joiner)

        return template


class Attribute(TimeStampedModel):
    template = models.ForeignKey(
        'settings.DownloadTemplate', on_delete=models.CASCADE)
    template_attribute = models.ForeignKey(
        'settings.TemplateAttribute', on_delete=models.CASCADE)
    order = models.IntegerField()
    start_joiner = models.CharField(max_length=5, blank=True)
    end_joiner = models.CharField(max_length=5, blank=True)

    def __str__(self):
        return "{} - {} - {}{}{}".format(
            self.template.title,
            self.order,
            self.start_joiner,
            self.template_attribute.code,
            self.end_joiner
        )


class TemplateAttribute(TimeStampedModel):
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=60)
    description = models.TextField()

    def __str__(self):
        return '{} - {}'.format(self.name, self.code)
