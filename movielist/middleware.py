from django.conf import settings


class RequestCountMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.request_count = 0

    def __call__(self, request):
        settings.request_count += 1
        response = self.get_response(request)
        return response