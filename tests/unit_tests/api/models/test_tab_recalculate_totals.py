import pytest

from api.models import MenuItem, Tab, TabItem


@pytest.mark.django_db
def test_tab_recalculate_totals() -> None:
    # Given a tab with two items
    tab = Tab.objects.create(table_number=1, covers=2)
    coffee = MenuItem.objects.create(
        name="Coffee", unit_price_p=350, vat_rate_percent=20.0
    )
    croissant = MenuItem.objects.create(
        name="Croissant", unit_price_p=280, vat_rate_percent=0.0
    )

    TabItem.objects.create(
        tab=tab,
        menu_item=coffee,
        qty=2,
        unit_price_p=350,
        vat_rate_percent=20.0,
        line_total_p=700,
        vat_p=140,
    )
    TabItem.objects.create(
        tab=tab,
        menu_item=croissant,
        qty=1,
        unit_price_p=280,
        vat_rate_percent=0.0,
        line_total_p=280,
        vat_p=0,
    )

    # When we recalculate the totals
    tab.recalculate_and_save()

    # Then the totals are as expected
    assert tab.subtotal_p == 980
    assert tab.service_charge_p == 98
    assert tab.vat_total_p == 140
    assert tab.total_p == 980 + 98 + 140
