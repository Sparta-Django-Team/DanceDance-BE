from django.db import models


# Create your models here.
class OriginalVideo(models.Model):
    # platform_type_id = models.ForeignKeY(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=32)
    youtube_video_id = models.CharField(max_length=512)
    channel_name = models.CharField(max_length=16)
    thumbnail_image_url = models.CharField(max_length=512)
    motion_data_url = models.CharField(max_length=512)
    uploaded_at = models.DateTimeField()
    hits = models.IntegerField()
    # likes = models.ManyToManyField(User, related_name="like_videos")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.title)


class UserVideo(models.Model):
    # platform_type_id = models.ForeignKeY(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=32)
    youtube_video_id = models.CharField(max_length=512)
    channel_name = models.CharField(max_length=16)
    thumbnail_image_url = models.CharField(max_length=512)
    uploaded_at = models.DateTimeField()
    score = models.IntegerField()
    score_list = models.TextField()
    is_rank = models.BooleanField(default=False)
    # likes = models.ManyToManyField(User, related_name="like_videos")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.title)


class PlatformType(models.Model):
    name = models.CharField(max_length=16)
    description = models.CharField(max_length=32, null=True)


class Tag(models.Model):
    name = models.CharField(max_length=64)
    parent_tag_id = models.IntegerField(null=True)


class OriginalVideoTag(models.Model):
    original_video_id = models.ForeignKey(OriginalVideo, on_delete=models.CASCADE, related_name="original_video_id")
    tag_id = models.ForeignKey(Tag, on_delete=models.CASCADE, related_name="original_video_tag")


class UserVideoTag(models.Model):
    user_video_id = models.ForeignKey(UserVideo, on_delete=models.CASCADE, related_name="user_video_id")
    tag_id = models.ForeignKey(Tag, on_delete=models.CASCADE, related_name="user_video_tag")


class OriginalVideoLikesLog(models.Model):
    # user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    original_video_id = models.ForeignKey(OriginalVideo, on_delete=models.CASCADE)
    is_liked = models.BooleanField(null=False)
    updated_at = models.DateTimeField(auto_now=True)


class UserVideoLikesLog(models.Model):
    # user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    user_video_id = models.ForeignKey(OriginalVideo, on_delete=models.CASCADE)
    is_liked = models.BooleanField(null=False)
    updated_at = models.DateTimeField(auto_now=True)
