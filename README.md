# Café EPOS — Technical Test

A small slice of a café EPOS system built for a technical test.  
Powered by Django, Django REST Framework, PostgreSQL, Poetry, and Docker.

## Features

- Create tabs and add menu items  
- Automatic calculation of subtotal, service charge, VAT, and total  
- Mock payment intents and confirmations  
- API key authentication for endpoints

## Stack

- Python 3.13  
- Django 5.x, Django REST Framework 3.x  
- PostgreSQL 16 (Docker)  
- uv for dependency management  
- pytest + pytest-django for testing  

## Setup

The setup is fully automated via a bash script; run it in a bash shell:

```
sh scripts/setup.sh
```

What it does:

1. Starts PostgreSQL in Docker
2. Installs dependencies with uv  
3. Runs Django migrations
4. Seeds some menu items for testing 

After doing this, you can run the server with this command:

```
uv run python manage.py runserver
```

Your API will be available at http://127.0.0.1:8000/api/.

## API Overview

- Endpoints:

Endpoint | Method | Description
-------- | ------ | -----------
/api/tabs/ | POST | Create a tab
/api/tabs/:id/ | GET | Retrieve tab details
/api/tabs/:id/items/ | POST | Add a menu item to a tab
/api/tabs/:id/payment_intent/ | POST | Create a mock payment intent
/api/tabs/:id/take_payment/ | POST | Confirm the payment

## Business Rules

- Service charge: 10% of subtotal, rounded to pence  
- VAT per line: round_to_pence(line_total * vat_rate_percent / 100)  
- Total = subtotal + service charge + VAT  
- Money stored in pence (integers)  

## Testing

Run all tests with:

```
uv run pytest
```

Tests include:

- Unit tests for total calculations for a tab
- Payment idempotency 
- Full end-to-end flow: Open tab → Add items → Create payment intent → Take payment → Tab marked PAID

## Notes
I implemented this little café EPOS as part of a technical test. At the time of writing, I am not a Django fella at all, as I have much more experience with FastAPI. However, I really took the time to learn what I did here. Basically, I used AI very sparingly to create this which I'm sure will help me become a more robust Django (and Python) dev.