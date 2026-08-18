"""Stores the views used in the API."""

from datetime import UTC, datetime
from typing import cast
from urllib.request import Request

from rest_framework import generics
from rest_framework.response import Response

from api.errors import PaymentIntentFailureError
from api.models import Payment, Tab, TabItem
from api.serializers import (
    PaymentSerializer,
    TabCreateSerializer,
    TabItemCreateSerializer,
    TabRetrieveSerializer,
)
from api.services.payments import MockPaymentGateway
from api.utils import check_valid_tab


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

        check_valid_tab(tab_id=tab_id)

        tab_item = cast("TabItem", serializer.save(tab_id=tab_id))
        tab_item.tab.recalculate_and_save()


class PaymentIntentCreateView(generics.CreateAPIView):
    """Create a payment intent for a tab."""

    def post(self, _request: Request, pk: int) -> Response:
        tab = check_valid_tab(pk)

        res = MockPaymentGateway().create_payment_intent(amount_p=tab.total_p)

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
        return Response(serializer.data, status=201)


class PaymentConfirmCreateView(generics.CreateAPIView):
    """Create a payment confirmation for a tab."""

    def post(self, _request: Request, pk: int) -> Response:
        tab = check_valid_tab(pk)
        payment: Payment = tab.payments.filter(status=Payment.Status.PENDING).last()  # type: ignore[reportAttributeAccessIssue]
        if not payment:
            return Response({"error": "No payment to confirm."}, status=400)

        res = MockPaymentGateway().confirm_payment_intent(
            intent_id=payment.payment_intent_id
        )
        payment.status = res["status"]
        payment.save()

        if res["status"] == Payment.Status.COMPLETED.value:
            tab.status = Tab.Status.PAID
            tab.closed_at = datetime.now(tz=UTC)
            tab.save()
            return Response({"status": "Payment successful."}, status=200)
        return Response({"error": "Payment has failed."}, status=402)
