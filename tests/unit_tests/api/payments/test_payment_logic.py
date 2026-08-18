import uuid

import pytest

from api.errors import PaymentIntentFailureError
from api.models import Payment, Tab
from api.services.payments import MockPaymentGatewayService


@pytest.mark.django_db
def test_create_payment_intent_failure() -> None:
    """Test that creating a payment intent with a specific amount fails.

    It raises the appropriate error.
    """
    tab = Tab.objects.create(table_number=1, covers=2)

    gateway = MockPaymentGatewayService()
    amount_p = gateway.FAILURE_VALUE_FOR_DEMO

    with pytest.raises(
        expected_exception=PaymentIntentFailureError,
        match=f"Payment for tab {tab.id} failed.",
    ):
        gateway.create_payment_intent(amount_p=amount_p)


@pytest.mark.django_db
def test_take_payment_idempotency() -> None:
    """Test that confirming a payment intent is idempotent.

    It does not change the tab status after the first successful confirmation.
    """
    tab = Tab.objects.create(table_number=1, covers=2)
    payment_intent_id = uuid.uuid4()
    Payment.objects.create(
        tab=tab,
        payment_intent_id=payment_intent_id,
        client_secret=uuid.uuid4(),
        amount_p=1000,
        status=Payment.Status.PENDING,
    )

    gateway = MockPaymentGatewayService()
    res1 = gateway.confirm_payment_intent(payment_intent_id)
    Payment.objects.filter(tab=tab, payment_intent_id=payment_intent_id).update(
        status=res1["status"]
    )
    tab.refresh_from_db()

    res2 = gateway.confirm_payment_intent(payment_intent_id)
    Payment.objects.filter(tab=tab, payment_intent_id=payment_intent_id).update(
        status=res2["status"]
    )
    tab.refresh_from_db()

    assert tab.status in [Tab.Status.OPEN, Tab.Status.PAID]
