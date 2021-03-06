# Generated by Django 2.0.4 on 2018-06-03 18:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('settings', '0003_auto_20180603_1813'),
        ('videos', '0007_auto_20180514_2120'),
    ]

    operations = [
        migrations.AddField(
            model_name='playlist',
            name='name_template',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='settings.DownloadTemplate'),
        ),
        migrations.AddField(
            model_name='video',
            name='name_template',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='settings.DownloadTemplate'),
        ),
        migrations.AlterField(
            model_name='playlist',
            name='status',
            field=models.CharField(choices=[('in-queue', 'In Queue'), ('completed', 'Completed'), ('skip', 'Skip'), ('error', 'Errored')], default='in-queue', max_length=25),
        ),
        migrations.AlterField(
            model_name='video',
            name='status',
            field=models.CharField(choices=[('in-queue', 'In Queue'), ('completed', 'Completed'), ('skip', 'Skip'), ('error', 'Errored')], default='in-queue', max_length=25),
        ),
    ]
