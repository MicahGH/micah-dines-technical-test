"""Stores permission logic for the API."""

import os

from rest_framework.permissions import BasePermission
from rest_framework.request import Request


class HasAPIKey(BasePermission):
    """Check if the API Key is valid."""

    def has_permission(self, request: Request, _view: object) -> bool:  # type: ignore[reportIncompatibleMethodOverride]
        """Check if the provided API key matches the valid one."""
        return request.headers.get("X-API-Key") == os.environ["API_KEY"]
