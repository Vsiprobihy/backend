from rest_framework.views import exception_handler

from utils.custom_exceptions import CustomBaseResponse


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if isinstance(exc, CustomBaseResponse):
        response.data = {'message': exc.message}
        response.status_code = exc.status_code
    return response
