from rest_framework.views import exception_handler
from rest_framework.exceptions import APIException


def core_exception_handler(exc, context):
    response = exception_handler(exc, context)
    handlers = {
        'ValidationError': _handle_generic_error,
        'ProfileDoesNotExist': _handle_generic_error,
        'EmailDoesNotExist': _handle_generic_error,
        'PostAlreadyLiked': _handle_generic_error,
        'PostWasntLiked': _handle_generic_error,
    }
    exception_class = exc.__class__.__name__

    if exception_class in handlers:
        return handlers[exception_class](exc, context, response)

    return response


def _handle_generic_error(exc, context, response):
    response.data = {
        'errors': response.data
    }

    return response


class ProfileDoesNotExist(APIException):
    status_code = 400
    default_detail = 'The requested profile does not exist.'


class EmailDoesNotExist(APIException):
    status_code = 400
    default_detail = 'The email you submitted is not valid.'


class PostAlreadyLiked(APIException):
    status_code = 400
    default_detail = 'You have already liked this post.'


class PostWasntLiked(APIException):
    status_code = 400
    default_detail = 'You can not unlike this post since you have never liked it at first.'
