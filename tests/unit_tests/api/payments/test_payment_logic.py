import uuid

import pytest

from api.errors import PaymentIntentFailureError
from api.mock_payment_gateway import MockPaymentGateway
from api.models import Payment, Tab


@pytest.mark.django_db
def test_create_payment_intent_failure() -> None:
    tab = Tab.objects.create(table_number=1, covers=2)

    gateway = MockPaymentGateway()
    amount_p = gateway.FAILURE_VALUE_FOR_DEMO
    res = gateway.create_payment_intent(amount_p=amount_p)

    assert res["status"] == Payment.Status.FAILED.value

    with pytest.raises(PaymentIntentFailureError):
        raise PaymentIntentFailureError(f"Payment for tab {tab.id} failed.")  # type: ignore[reportAttributeAccessIssue]


@pytest.mark.django_db
def test_take_payment_idempotency() -> None:
    tab = Tab.objects.create(table_number=1, covers=2)
    payment_intent_id = uuid.uuid4()
    Payment.objects.create(
        tab=tab,
        payment_intent_id=payment_intent_id,
        client_secret=uuid.uuid4(),
        amount_p=1000,
        status=Payment.Status.PENDING,
    )

    res1 = MockPaymentGateway().confirm_payment_intent(payment_intent_id)
    Payment.objects.filter(tab=tab, payment_intent_id=payment_intent_id).update(
        status=res1["status"]
    )
    tab.refresh_from_db()

    res2 = MockPaymentGateway().confirm_payment_intent(payment_intent_id)
    Payment.objects.filter(tab=tab, payment_intent_id=payment_intent_id).update(
        status=res2["status"]
    )
    tab.refresh_from_db()

    assert tab.status in [Tab.Status.OPEN, Tab.Status.PAID]
