from rest_framework import serializers

from challenges.models import OriginalVideo, UserVideo


class OriginalVideoListSerializer(serializers.ModelSerializer):
    class Meta:
        model = OriginalVideo
        fields = "__all__"


class UserVideoListSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserVideo
        fields = "__all__"
