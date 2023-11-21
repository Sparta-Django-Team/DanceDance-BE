from typing import Type

from rest_framework import serializers


######################################################
# API serializers utils
######################################################
def create_serializer_class(name: str, fields: dict) -> Type[serializers.Serializer]:
    class Meta:
        ref_name = None

    return type(name, (serializers.Serializer,), {**fields, "Meta": Meta})


def inline_serializer(*, fields: dict, data: dict | None = None, **kwargs) -> serializers.Serializer:
    serializer_class = create_serializer_class(name="inline_serializer", fields=fields)
    if data is not None:
        return serializer_class(data=data, **kwargs)

    return serializer_class(**kwargs)
