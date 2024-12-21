from rest_framework.response import Response
from rest_framework.exceptions import APIException


class CustomBaseResponse(APIException):
    def __init__(self, message=None):
        self.message = message if message else self.default_detail
        super().__init__(detail=self.message)

    def get_response(self):
        return Response({'message': self.message}, status=self.status_code)


class SuccessResponse(CustomBaseResponse):
    status_code = 200
    default_detail = 'Success'
    default_code = 'success'


class CreatedResponse(CustomBaseResponse):
    status_code = 201
    default_detail = 'Created'
    default_code = 'created'


class BadRequestError(CustomBaseResponse):
    status_code = 400
    default_detail = 'Bad request'
    default_code = 'bad_request'


class UnauthorizedError(CustomBaseResponse):
    status_code = 401
    default_detail = 'Unauthorized'
    default_code = 'unauthorized'


class ForbiddenError(CustomBaseResponse):
    status_code = 403
    default_detail = 'Forbidden'
    default_code = 'forbidden'


class NotFoundError(CustomBaseResponse):
    status_code = 404
    default_detail = 'Not Found'
    default_code = 'not_found'


class InternalServerError(CustomBaseResponse):
    status_code = 500
    default_detail = 'Internal Server Error'
    default_code = 'internal_server_error'
