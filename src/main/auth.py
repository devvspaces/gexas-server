from django.conf import settings
from django.http.request import HttpRequest
from django.utils.crypto import constant_time_compare


def validate_request(request: HttpRequest):
    # Extract X-API-KEY from request
    api_key = request.headers.get("X-API-KEY")
    if not api_key:
        return False
    return constant_time_compare(api_key, settings.API_KEY)
