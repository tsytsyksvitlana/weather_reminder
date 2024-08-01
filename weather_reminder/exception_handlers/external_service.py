from rest_framework import status

from weather_reminder.exception_handlers.base import BaseException


class ExternalServiceError(BaseException):
    status_code = status.HTTP_503_SERVICE_UNAVAILABLE
    message = "Error on external weather API service"
