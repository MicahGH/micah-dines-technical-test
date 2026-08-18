"""Utility functions for the API."""

from django.shortcuts import get_object_or_404

from api.errors import TabClosedError
from api.models import Tab


def check_valid_tab(tab_id: int) -> Tab:
    """Check if the tab with the ID provided exists and is open."""
    tab = get_object_or_404(Tab, id=tab_id)
    if tab.status == Tab.Status.PAID.value:
        msg = f"Tab with ID: {tab_id} already closed."
        raise TabClosedError(msg)
    return tab
