from django.contrib.auth.models import BaseUserManager

from dance_dance.common.constants import (
    USER_SOCIAL_PROVIDER_EMAIL,
    USER_SOCIAL_PROVIDER_KAKAO,
)
from dance_dance.common.exception.exceptions import ValidationErrorException


class UserManager(BaseUserManager):
    def create_user(self, email: str, password: str, nickname: str, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            nickname=nickname,
            user_social_provider_id=USER_SOCIAL_PROVIDER_EMAIL,
            **extra_fields,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_social_user(self, email: str, social_id: str, nickname: str, thumbnail_image_url: str, **extra_fields):
        email = self.normalize_email(email)
        if self.filter(email=email).exists():
            raise ValidationErrorException("Already exists user with this email.")

        if self.filter(social_id=social_id).exists():
            raise ValidationErrorException("Already exists user with this social id.")

        user = self.model(
            email=email,
            social_id=social_id,
            nickname=nickname,
            thumbnail_image_url=thumbnail_image_url,
            user_social_provider_id=USER_SOCIAL_PROVIDER_KAKAO,
            **extra_fields,
        )
        user.save(using=self._db)
        return user

    def create_superuser(self, email: str, password: str, nickname: str, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            nickname=nickname,
            is_admin=True,
            user_social_provider_id=USER_SOCIAL_PROVIDER_EMAIL,
            **extra_fields,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
