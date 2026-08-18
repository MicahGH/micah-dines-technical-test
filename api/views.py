"""Stores the views used in the API."""

from datetime import UTC, datetime

from rest_framework import generics, status
from rest_framework.request import Request
from rest_framework.response import Response

from api.errors import PaymentIntentFailureError
from api.models import Payment, Tab, TabItem
from api.serializers import (
    PaymentSerializer,
    TabCreateSerializer,
    TabItemCreateSerializer,
    TabRetrieveSerializer,
)
from api.services.payment import MockPaymentGatewayService
from api.services.tab import TabService


class TabCreateView(generics.CreateAPIView):
    """View used to create a new tab."""

    queryset = Tab.objects.all()
    serializer_class = TabCreateSerializer


class TabRetrieveView(generics.RetrieveAPIView):
    """View used to retrieve data for an existing tab."""

    queryset = Tab.objects.all()
    serializer_class = TabRetrieveSerializer


class TabItemCreateView(generics.CreateAPIView):
    """View used to add a tab item to an existing tab."""

    queryset = TabItem.objects.all()
    serializer_class = TabItemCreateSerializer

    def perform_create(self, serializer: TabItemCreateSerializer) -> None:
        """Add a tab item to a tab and recalculate the tab's totals."""
        tab_id: int = self.kwargs["pk"]

        tab = TabService.get_open_tab_or_raise(tab_id=tab_id)

        serializer.save(tab_id=tab_id)  # type: ignore[reportUnknownMemberType]
        tab.recalculate_and_save()


class PaymentIntentCreateView(generics.CreateAPIView):
    """Create a payment intent for a tab."""

    def post(self, _request: Request, pk: int) -> Response:
        """Create a payment intent for a tab."""
        tab = TabService.get_open_tab_or_raise(tab_id=pk)

        res = MockPaymentGatewayService().create_payment_intent(amount_p=tab.total_p)

        payment = Payment.objects.create(
            tab=tab,
            payment_intent_id=res["id"],
            client_secret=res["client_secret"],
            status=res["status"],
            amount_p=tab.total_p,
        )

        if res["status"] == Payment.Status.FAILED.value:
            msg = f"Payment for tab: {pk} failed."
            raise PaymentIntentFailureError(msg)

        serializer = PaymentSerializer(payment)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class PaymentConfirmCreateView(generics.CreateAPIView):
    """Create a payment confirmation for a tab (Idempotent)."""

    def post(self, _request: Request, pk: int) -> Response:
        """Confirm a payment intent for a tab."""
        tab = TabService.get_open_tab_or_raise(tab_id=pk)

        if tab.status == Tab.Status.PAID.value:
            return Response(
                {"status": "Payment successful.", "note": "Already processed."},
                status=status.HTTP_200_OK,
            )

        payment = Payment.objects.filter(
            status=Payment.Status.PENDING, tab_id=tab.id
        ).last()

        if payment is None:
            return Response(
                {"error": "No pending payment intent found for this tab."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        res = MockPaymentGatewayService().confirm_payment_intent(
            intent_id=payment.payment_intent_id
        )

        payment.status = res["status"]
        payment.save(update_fields=["status"])

        if res["status"] == Payment.Status.COMPLETED.value:
            tab.status = Tab.Status.PAID
            tab.closed_at = datetime.now(tz=UTC)
            tab.save(update_fields=["status", "closed_at"])

            return Response(
                {"status": "Payment successful."},
                status=status.HTTP_200_OK,
            )

        return Response(
            {"error": "Payment has failed."},
            status=status.HTTP_402_PAYMENT_REQUIRED,
        )
