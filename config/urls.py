"""URLs for the Django app."""

from django.urls import path

from api.views import (
    PaymentConfirmCreateView,
    PaymentIntentCreateView,
    TabCreateView,
    TabItemCreateView,
    TabRetrieveView,
)

BASE_API_PATH = "api/"
BASE_TABS_PATH = "tabs/"

urlpatterns = [
    path(BASE_API_PATH + BASE_TABS_PATH, TabCreateView.as_view()),
    path(
        BASE_API_PATH + BASE_TABS_PATH + "<int:pk>/items/", TabItemCreateView.as_view()
    ),
    path(BASE_API_PATH + BASE_TABS_PATH + "<int:pk>/", TabRetrieveView.as_view()),
    path(
        BASE_API_PATH + BASE_TABS_PATH + "<int:pk>/payment_intent/",
        PaymentIntentCreateView.as_view(),
    ),
    path(
        BASE_API_PATH + BASE_TABS_PATH + "<int:pk>/take_payment/",
        PaymentConfirmCreateView.as_view(),
    ),
]
