import uuid
from typing import TypedDict

from api.models import Payment


class PaymentIntentResponse(TypedDict):
    """TypedDict for the response of a payment intent."""

    id: str
    client_secret: str
    status: str


class MockPaymentGateway:
    """Class for a mock payment gateway used in the API."""

    FAILURE_VALUE_FOR_DEMO = 13

    def create_payment_intent(self, amount_p: int) -> PaymentIntentResponse:
        """Create a dummy payment intent."""
        payment_intent_id = str(uuid.uuid4())
        client_secret = str(uuid.uuid4())

        status = (
            Payment.Status.FAILED.value
            if amount_p == self.FAILURE_VALUE_FOR_DEMO
            else Payment.Status.PENDING.value
        )

        return {
            "id": payment_intent_id,
            "client_secret": client_secret,
            "status": status,
        }

    def confirm_payment_intent(
        self, intent_id: uuid.UUID | str
    ) -> PaymentIntentResponse:
        """Create a dummy payment confirmation."""
        return {
            "id": str(intent_id),
            "status": Payment.Status.COMPLETED.value,
            "client_secret": str(uuid.uuid4()),
        }
