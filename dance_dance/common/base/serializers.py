from rest_framework import serializers

from dance_dance.common.exception.exceptions import InvalidParameterFormatException


class BaseSerializer(serializers.Serializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if "data" in kwargs and not self.is_valid():
            raise InvalidParameterFormatException()

    class Meta:
        ref_name = None


class BaseModelSerializer(serializers.ModelSerializer):
    class Meta:
        ref_name = None


class BaseResponseSerializer(serializers.Serializer):
    code = serializers.IntegerField()
    success = serializers.BooleanField()
    message = serializers.CharField()

    def __init__(self, *args, **kwargs):
        data_serializer = kwargs.pop("data_serializer", None)
        super().__init__(*args, **kwargs)

        if data_serializer is not None:
            self.fields["data"] = data_serializer()

    class Meta:
        ref_name = None
