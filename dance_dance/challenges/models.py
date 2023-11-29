from django.db import models

from dance_dance.users.models import User


class PlatformType(models.Model):
    name = models.CharField(max_length=16)
    description = models.CharField(max_length=32, null=True)

    def __str__(self):
        return str(self.name)


class OriginalVideo(models.Model):
    platform_type_id = models.ForeignKey(PlatformType, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=128)
    youtube_video_url = models.CharField(max_length=512)
    channel_name = models.CharField(max_length=128)
    thumbnail_image_url = models.CharField(max_length=512)
    uploaded_at = models.DateTimeField()

    hits = models.IntegerField(default=0)
    motion_data_path = models.CharField(max_length=512, null=True)
    video_file_path = models.CharField(max_length=512, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.title)


class UserVideo(models.Model):
    platform_type_id = models.ForeignKey(PlatformType, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=128)
    youtube_video_url = models.CharField(max_length=512)
    channel_name = models.CharField(max_length=128)
    thumbnail_image_url = models.CharField(max_length=512)
    uploaded_at = models.DateTimeField()

    score = models.FloatField(null=True)
    score_list = models.TextField(null=True)
    is_rank = models.BooleanField(default=False)
    likes = models.ManyToManyField(User, related_name="like_videos")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    tags = models.TextField(null=True)

    def __str__(self):
        return str(self.title)


class Tag(models.Model):
    name = models.CharField(max_length=64)
    parent_tag_id = models.ForeignKey("self", on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return str(self.name)


class OriginalVideoTag(models.Model):
    original_video_id = models.ForeignKey(OriginalVideo, on_delete=models.CASCADE, related_name="original_video_id")
    tag_id = models.ForeignKey(Tag, on_delete=models.CASCADE, related_name="original_video_tag")

    def __str__(self):
        return "[" + str(self.tag_id) + "]_" + str(self.original_video_id)


class UserVideoTag(models.Model):
    user_video_id = models.ForeignKey(UserVideo, on_delete=models.CASCADE, related_name="user_video_id")
    tag_id = models.ForeignKey(Tag, on_delete=models.CASCADE, related_name="user_video_tag")

    def __str__(self):
        return "[" + str(self.tag_id) + "]_" + str(self.user_video_id)


class OriginalVideoLikesLog(models.Model):
    original_video_id = models.ForeignKey(OriginalVideo, on_delete=models.CASCADE)
    is_liked = models.BooleanField(null=False)
    updated_at = models.DateTimeField(auto_now=True)


class UserVideoLikesLog(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    user_video_id = models.ForeignKey(OriginalVideo, on_delete=models.CASCADE)
    is_liked = models.BooleanField(null=False)
    updated_at = models.DateTimeField(auto_now=True)
