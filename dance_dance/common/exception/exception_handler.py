from datetime import datetime
from typing import Optional, Union

from rest_framework.exceptions import APIException
from rest_framework.response import Response

from config.settings import logger
from dance_dance.common.base.exception import BaseAPIException
from dance_dance.common.exception.exceptions import UnknownServerException
from dance_dance.common.response import create_response


def default_exception_handler(exc: Exception, context: dict) -> Union[Response, None]:
    logger.error("[EXCEPTION_HANDLER]")
    logger.error(f"[{datetime.now()}]")
    logger.error("> exc")
    logger.error(f"{exc}")
    logger.error("> context")
    logger.error(f"{context}")

    response = handle_api_exception(exc, context)

    if response:
        return response

    return handle_api_exception(UnknownServerException(), context)


def handle_api_exception(exc: Exception, context: dict) -> Optional[Response]:
    if not isinstance(exc, APIException):
        return None

    message = getattr(exc, "detail")
    status_code = getattr(exc, "status_code")
    code = getattr(exc, "code", BaseAPIException.code)

    return create_response(code=code, message=message, status_code=status_code)
