# Base imports
import logging
import traceback
from typing import Optional, Iterable, Union

# Django imports
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

# Third-party imports
from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework.serializers import ValidationError as SerializerValidationError


LOGGER = logging.getLogger(__name__)


ExceptionType = Union[
    APIException,
    BaseException,
    ValidationError,
    SerializerValidationError
]


def log_error_traceback(
    exception: ExceptionType,
    level: Optional[int] = logging.ERROR
) -> Iterable[str]:
    """
    Logs and then returns the traceback lines of a BaseException instance.
    """
    traceback_lines = []

    exc_traceback = traceback.format_exception(
        exception.__class__,
        exception,
        exception.__traceback__
    )

    for line in [line.rstrip('\n') for line in exc_traceback]:
        traceback_lines.extend(line.splitlines())

    LOGGER.log(level, traceback_lines.__str__())

    return traceback_lines


def _build_payload(
    http_status: int,
    exception: Optional[ExceptionType] = None,
    custom_message: Optional[str] = None,
    environment: Optional[str] = settings.ENVIRONMENT_MODE
) -> dict:
    payload = {'status': http_status}

    if exception:
        payload.update({
            'error': exception.__class__.__name__,
        })

        if isinstance(exception, APIException):
            payload.update({
                'description': exception.__dict__()
                if callable(exception.__dict__) else exception.__dict__,
            })
        elif isinstance(exception, (ValidationError, SerializerValidationError)):
            payload.update({
                'validation_errors': exception.error_list
            })
        else:
            payload.update({
                'description': str(exception),
            })

        # Logs the exception traceback if the server is in development mode
        if environment == 'dev':
            payload.update({
                'traceback': log_error_traceback(exception)
            })

    if custom_message:
        payload.update({
            'message': _(custom_message),
        })

    return payload


def _generate_response(
    http_status: int,
    custom_message: Optional[str] = None,
    environment: Optional[str] = settings.ENVIRONMENT_MODE,
    exception: Optional[ExceptionType] = None,
) -> Response:
    """
    Generates an HTTP REST response, with a customized payload.
    """
    payload = _build_payload(
        http_status=http_status,
        exception=exception,
        custom_message=custom_message,
        environment=environment
    )

    return Response(payload, http_status)


def not_found_response(
    exception: Optional[ExceptionType] = None,
    custom_message: Optional[str] = None,
    environment: Optional[str] = settings.ENVIRONMENT_MODE
) -> Response:
    """
    Generates a HTTP 404 response.
    """
    return _generate_response(
        status.HTTP_404_NOT_FOUND,
        custom_message,
        environment,
        exception
    )


def bad_request_response(
    exception: Optional[ExceptionType] = None,
    custom_message: Optional[str] = None,
    environment: Optional[str] = settings.ENVIRONMENT_MODE
) -> Response:
    """
    Generates a HTTP 400 response.
    """
    return _generate_response(
        status.HTTP_400_BAD_REQUEST,
        custom_message,
        environment,
        exception
    )


def internal_server_error_response(
    exception: ExceptionType,
    custom_message: Optional[str] = None,
    environment: Optional[str] = settings.ENVIRONMENT_MODE
) -> Response:
    """
    Generates a HTTP 500 response.
    """
    return _generate_response(
        status.HTTP_500_INTERNAL_SERVER_ERROR,
        custom_message,
        environment,
        exception
    )


def api_exception_response(
    exception: ExceptionType,
    custom_message: Optional[str] = None,
    http_status: Optional[str] = None,
    environment: Optional[str] = settings.ENVIRONMENT_MODE
) -> Response:
    if isinstance(exception, APIException):
        status_code = exception.status_code
    else:
        status_code = http_status if http_status else status.HTTP_500_INTERNAL_SERVER_ERROR

    return _generate_response(
        status_code,
        custom_message,
        environment,
        exception
    )
