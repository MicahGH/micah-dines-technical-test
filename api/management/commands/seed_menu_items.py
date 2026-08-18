from django.core.management.base import BaseCommand

from api.models import MenuItem

MENU_ITEMS = [
    {"name": "Flat White", "unit_price_p": 350, "vat_rate_percent": 20.0},
    {"name": "Croissant", "unit_price_p": 280, "vat_rate_percent": 0.0},
    {"name": "Iced Tea", "unit_price_p": 300, "vat_rate_percent": 20.0},
    {"name": "Kids Meal", "unit_price_p": 700, "vat_rate_percent": 5.0},
]


class Command(BaseCommand):
    help = "Seed menu items for the café EPOS."

    def handle(self, *args, **kwargs) -> None:
        for item in MENU_ITEMS:
            obj, created = MenuItem.objects.get_or_create(
                name=item["name"],
                defaults={
                    "unit_price_p": item["unit_price_p"],
                    "vat_rate_percent": item["vat_rate_percent"],
                },
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"Created: {obj.name}"))
            else:
                self.stdout.write(f"Exists: {obj.name}")

        self.stdout.write(self.style.SUCCESS("Menu items seeded successfully!"))
