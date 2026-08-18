# Café EPOS — Technical Test

A small slice of a café EPOS system built for a technical test.  
Powered by Django, Django REST Framework, PostgreSQL, uv, and Docker.

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

The application setup and execution are fully containerized with Docker Compose. Build and start the services with a single command:

```bash
docker compose up --build
```

### What it does:

1. **Database Readiness:** Launches PostgreSQL 16 and waits for health checks to pass.
2. **Container Build:** Builds the Django container using `uv` for multi-stage dependency installation.
3. **Database Setup:** Applies database migrations automatically inside the container.
4. **Data Seeding:** Seeds initial menu items into the database for testing.

Once running, the API will be available at [http://127.0.0.1:8000/api/](http://127.0.0.1:8000/api/).

---

### Useful Commands

* **View real-time logs:**
  ```bash
  docker compose logs -f
  ```

* **Stop containers:**
  ```bash
  docker compose down
  ```

* **Reset environment and database:**
  ```bash
  docker compose down -v
  ```

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