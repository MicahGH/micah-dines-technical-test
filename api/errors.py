"""Stores custom errors for the API."""

from rest_framework.exceptions import APIException


class TabClosedError(APIException):
    """Error for when a tab is closed."""

    status_code = 400
    default_detail = "Tab is already closed."
    default_code = "tab_closed"


class MenuItemNotFoundError(APIException):
    """Error for when a menu item is not found."""

    status_code = 400
    default_detail = "Menu item not found."
    default_code = "menu_item_not_found"


class PaymentIntentFailureError(APIException):
    """Error for when a payment intent fails."""

    status_code = 400
    default_detail = "Payment intent failed."
    default_code = "payment_failed"


class TabNotFoundError(APIException):
    """Error for when a tab is not found."""

    status_code = 404
    default_detail = "Tab not found."
    default_code = "tab_not_found"
