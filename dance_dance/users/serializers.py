from rest_framework import serializers

from dance_dance.common.exception.exceptions import ValidationErrorException
from dance_dance.users.models import Follow, User
from dance_dance.users.validations import nickname_validator, password_validator


class SignupSerializer(serializers.ModelSerializer):
    repassword = serializers.CharField(
        error_messages={
            "required": "re_password is required.",
            "blank": "re_password is blank.",
            "write_only": True,
        }
    )

    class Meta:
        model = User
        fields = (
            "email",
            "nickname",
            "password",
            "repassword",
            "is_agree_marketing",
        )

        extra_kwargs = {
            "nickname": {
                "error_messages": {
                    "required": "nickname is required.",
                    "blank": "nickname is blank.",
                }
            },
            "password": {
                "write_only": True,
                "error_messages": {
                    "required": "password is required.",
                    "blank": "password is blank.",
                },
            },
            "email": {
                "error_messages": {
                    "required": "email is required.",
                    "invalid": "email is invalid.",
                    "blank": "email is blank.",
                }
            },
        }

    def validate(self, data):
        nickname = data.get("nickname")
        password = data.get("password")
        repassword = data.get("repassword")

        if nickname_validator(nickname):
            raise ValidationErrorException("nickname is 3 to 10 characters long and cannot contain special characters.")

        if password != repassword:
            raise ValidationErrorException("password and repassword do not match.")

        if password_validator(password):
            raise ValidationErrorException(
                "password is 8 to 16 characters long and must contain at least one number, one lowercase letter, and one special character."
            )

        return data

    def create(self, validated_data):
        nickname = validated_data["nickname"]
        email = validated_data["email"]

        user = User(
            nickname=nickname,
            email=email,
        )
        user.set_password(validated_data["password"])
        user.save()

        return user


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "nickname",
            "thumbnail_image_url",
        )
        read_only_fields = ("id",)


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "nickname",
            "thumbnail_image_url",
        )


class KakaoInputSerializer(serializers.Serializer):
    code = serializers.CharField(required=False)
    error = serializers.CharField(required=False)


class KakaoOutputSerializer(serializers.Serializer):
    access_token = serializers.CharField()
    refresh_token = serializers.CharField()


class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = ("id", "follower", "following", "is_followed", "updated_at")
