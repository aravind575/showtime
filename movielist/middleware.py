import os


class RequestCountMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        os.environ['request_count'] = '0'

    def __call__(self, request):
        req = os.environ['request_count']
        os.environ['request_count'] = str(int(req) + 1)
        response = self.get_response(request)
        return response