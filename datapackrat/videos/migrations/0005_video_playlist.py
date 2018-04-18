# Generated by Django 2.0.4 on 2018-04-17 21:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0004_auto_20180415_2034'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='playlist',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='videos', to='videos.Playlist'),
        ),
    ]