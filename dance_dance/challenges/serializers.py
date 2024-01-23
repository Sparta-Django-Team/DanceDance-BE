from rest_framework import serializers

from dance_dance.challenges.models import OriginalVideo, Tag, UserVideo


class OriginalVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = OriginalVideo
        fields = "__all__"


class UserVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserVideo
        fields = "__all__"
        read_only_fields = ["likes"]


class TagCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = "__all__"
