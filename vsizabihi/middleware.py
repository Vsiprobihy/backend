from django.utils.deprecation import MiddlewareMixin


class DisableCSRF(MiddlewareMixin):
    def process_request(self, request):  # noqa
        setattr(request, '_dont_enforce_csrf_checks', True)
