# Generated by Django 2.0.4 on 2018-06-03 18:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('settings', '0002_auto_20180525_2207'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attribute',
            name='end_joiner',
            field=models.CharField(blank=True, max_length=5),
        ),
        migrations.AlterField(
            model_name='attribute',
            name='start_joiner',
            field=models.CharField(blank=True, max_length=5),
        ),
    ]
