from django.middleware.csrf import CsrfViewMiddleware
from django.conf import settings
from django.http import HttpResponseForbidden
from urllib.parse import urlparse

class CustomCsrfMiddleware(CsrfViewMiddleware):
    def _get_trusted_origins(self):
        # You could get trusted origins from settings
        return getattr(settings, 'CSRF_TRUSTED_ORIGINS', [])

    def process_request(self, request):
        trusted_origins = self._get_trusted_origins()
        origin = request.META.get('HTTP_ORIGIN')

        if origin and any(origin.startswith(trusted_origin) for trusted_origin in trusted_origins):
            # Exempt CSRF protection for requests from trusted origins
            request.csrf_processing_done = True
            return None

        return super().process_request(request)