# Generated by Django 4.2.7 on 2023-11-09 11:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('challenges', '0008_rename_motion_data_url_originalvideo_motion_data_path'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='originalvideo',
            table='original_video',
        ),
    ]