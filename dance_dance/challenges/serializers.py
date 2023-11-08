from rest_framework import serializers

from dance_dance.challenges.models import OriginalVideo, UserVideo, Tag


class OriginalVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = OriginalVideo
        fields = "__all__"


class UserVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserVideo
        fields = "__all__"


class TagCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = "__all__"