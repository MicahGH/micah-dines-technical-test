"""Stores authentication logic used in the API."""

import os
from urllib.request import Request

from django.contrib.auth.models import AnonymousUser
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed


class APIKeyAuthentication(BaseAuthentication):
    """Authentication class with custom logic for the technical test."""

    def authenticate(self, request: Request) -> tuple[AnonymousUser, None]:
        """Authenticate the request using the provided key."""
        key = request.headers.get("X-API-Key")
        if key != os.environ["API_KEY"]:
            msg = f"Invalid API Key: {key}"
            raise AuthenticationFailed(msg)
        return (AnonymousUser(), None)
