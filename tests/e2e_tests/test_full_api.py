import os
from typing import cast

import pytest
from rest_framework.response import Response
from rest_framework.test import APIClient

from api.models import MenuItem, Tab


@pytest.mark.django_db
def test_full_api_flow() -> None:
    client = APIClient()
    client.credentials(HTTP_X_API_KEY=os.environ["API_KEY"])

    tab = Tab.objects.create(table_number=1, covers=2)

    coffee = MenuItem.objects.create(
        name="Coffee", unit_price_p=350, vat_rate_percent=20.0
    )
    croissant = MenuItem.objects.create(
        name="Croissant", unit_price_p=280, vat_rate_percent=0.0
    )

    client.post(
        f"/api/tabs/{tab.id}/items/", {"menu_item": coffee.id, "qty": 2}, format="json"
    )
    client.post(
        f"/api/tabs/{tab.id}/items/",
        {"menu_item": croissant.id, "qty": 1},
        format="json",
    )

    res_pi = cast("Response", client.post(f"/api/tabs/{tab.id}/payment_intent/"))
    assert res_pi.status_code == 201

    res_payment = cast("Response", client.post(f"/api/tabs/{tab.id}/take_payment/"))
    assert res_payment.status_code == 200
    tab.refresh_from_db()
    assert tab.status == Tab.Status.PAID
