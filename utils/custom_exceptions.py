from rest_framework.exceptions import APIException

class InvalidCredentialsError(APIException):
    status_code = 401
    default_detail = "Invalid credentials."
    default_code = "invalid_credentials"