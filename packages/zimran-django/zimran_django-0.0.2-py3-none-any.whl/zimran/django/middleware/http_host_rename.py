from typing import Callable

from django.http import HttpRequest


class HttpHostRenameMiddleware:
    def __init__(self, get_response: Callable) -> None:
        self.get_response = get_response

    def __call__(self, request: HttpRequest):
        self.rename_http_host(request)
        return self.get_response(request)

    @staticmethod
    def rename_http_host(request: HttpRequest) -> None:
        if request.META.get('HTTP_HOST'):
            request.META['HTTP_HOST'] = request.META['HTTP_HOST'].replace('_', '-')
