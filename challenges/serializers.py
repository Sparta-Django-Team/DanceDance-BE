from rest_framework import serializers

from challenges.models import OriginalVideo, UserVideo


class OriginalVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = OriginalVideo
        fields = "__all__"


class UserVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserVideo
        fields = "__all__"
