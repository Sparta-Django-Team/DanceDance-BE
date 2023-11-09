# Generated by Django 4.2.7 on 2023-11-08 15:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('challenges', '0004_originalvideo_challenge_name_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='originalvideo',
            name='challenge_name',
        ),
        migrations.RemoveField(
            model_name='originalvideo',
            name='video_route',
        ),
        migrations.AlterField(
            model_name='originalvideo',
            name='hits',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='originalvideo',
            name='motion_data_url',
            field=models.CharField(max_length=512, null=True),
        ),
    ]