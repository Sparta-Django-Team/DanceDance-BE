from django.contrib.auth.models import AbstractBaseUser
from django.db import models

from dance_dance.common.base.models import BaseModel, SimpleModel
from dance_dance.users.managers import UserManager


class User(AbstractBaseUser, BaseModel):
    email = models.EmailField(unique=True)
    social_id = models.CharField(max_length=128, null=True, unique=True)
    nickname = models.CharField(max_length=16)
    thumbnail_image_url = models.CharField(max_length=512, null=True)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True)
    is_agree_privacy = models.BooleanField(default=True)
    is_agree_marketing = models.BooleanField(default=False)
    user_social_provider = models.ForeignKey(
        "UserSocialProvider",
        on_delete=models.SET_NULL,
        null=True,
        related_name="users",
    )
    follow = models.ForeignKey(
        "Follow",
        on_delete=models.SET_NULL,
        null=True,
        related_name="users",
    )

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["nickname"]

    def __str__(self):
        return f"[{self.id}]: {self.email}"

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin

    class Meta:
        db_table = "users"


class UserSocialProvider(SimpleModel):
    def __str__(self):
        return f"[{self.id}]: {self.name}"

    class Meta:
        db_table = "user_social_provider"


class Follow(BaseModel):
    follower = models.ForeignKey("User", related_name="following", on_delete=models.CASCADE)
    following = models.ForeignKey("User", related_name="followers", on_delete=models.CASCADE)
    is_followed = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.follower} is following {self.following}"

    class Meta:
        db_table = "follow"
