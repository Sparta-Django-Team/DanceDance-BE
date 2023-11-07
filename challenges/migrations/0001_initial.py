# Generated by Django 4.2.7 on 2023-11-07 09:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='OriginalVideo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=32)),
                ('youtube_video_id', models.CharField(max_length=512)),
                ('channel_name', models.CharField(max_length=16)),
                ('thumbnail_image_url', models.CharField(max_length=512)),
                ('motion_data_url', models.CharField(max_length=512)),
                ('uploaded_at', models.DateTimeField()),
                ('hits', models.IntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='PlatformType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=16)),
                ('description', models.CharField(max_length=32, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('parent_tag_id', models.IntegerField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserVideo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=32)),
                ('youtube_video_id', models.CharField(max_length=512)),
                ('channel_name', models.CharField(max_length=16)),
                ('thumbnail_image_url', models.CharField(max_length=512)),
                ('uploaded_at', models.DateTimeField()),
                ('score', models.IntegerField()),
                ('score_list', models.TextField()),
                ('is_rank', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserVideoTag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_video_tag', to='challenges.tag')),
                ('user_video_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_video_id', to='challenges.uservideo')),
            ],
        ),
        migrations.CreateModel(
            name='UserVideoLikesLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_liked', models.BooleanField()),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user_video_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='challenges.originalvideo')),
            ],
        ),
        migrations.CreateModel(
            name='OriginalVideoTag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('original_video_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='original_video_id', to='challenges.originalvideo')),
                ('tag_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='original_video_tag', to='challenges.tag')),
            ],
        ),
        migrations.CreateModel(
            name='OriginalVideoLikesLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_liked', models.BooleanField()),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('original_video_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='challenges.originalvideo')),
            ],
        ),
    ]
