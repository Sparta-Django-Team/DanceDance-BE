from rest_framework import status

from dance_dance.common.base.exception import BaseAPIException


class UnknownServerException(BaseAPIException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = "Unknown server error"
    code = 1000


class InvalidParameterFormatException(BaseAPIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Invalid parameter format"
    code = 1001
