from rest_framework import status


class BaseException(Exception):
    status_code: int
    message: str
    detail_info: str | bool = False


class NotRequiredData(Exception):
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    message = "Not all necessary data provided"
    detail_info = True


class FetchingFailuresError(Exception):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    message = "An error occurred while fetching data"


class EnoughtFailures(Exception):
    status_code = status.HTTP_409_CONFLICT
    message = "Too much messages about this failure"
