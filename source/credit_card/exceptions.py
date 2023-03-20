from rest_framework import status
from rest_framework.exceptions import APIException


class DateFormatException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "date is formatted wrong"
