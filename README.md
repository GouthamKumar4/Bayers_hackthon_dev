# Booking Ticket Microservice (FastAPI)

This repository now contains a **simple modular FastAPI microservice** for storing booking tickets in-memory and viewing booked information.

## What is implemented now

- In-memory ticket booking storage (single service process)
- Create booking API
- List bookings API
- Get single booking API
- Health endpoint
- Modular structure (API routes, service layer, repository layer, models)

## API endpoints

- `GET /health` - service health
- `POST /bookings` - create booking
- `GET /bookings` - list all bookings
- `GET /bookings/{booking_id}` - retrieve one booking

### Example create request

```json
{
  "customer_name": "Alex",
  "event_name": "Concert",
  "seats": 2
}
```

## Project structure

```text
app/
  api/routes.py
  core/dependencies.py
  models/booking.py
  repositories/booking_repository.py
  services/booking_service.py
  main.py
docs/
  TODO.md
tests/
  test_app.py
```

## Planned cloud-native integration points

Code TODO blocks are included for:

- Database integration with Azure managed database
- Authentication + authorization via Microsoft Entra ID
- Redis cache via Azure Cache for Redis
- Observability with OpenTelemetry + Azure Monitor

See `docs/TODO.md` for detailed task backlog.

## Run locally

```bash
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## Run tests

```bash
python -m unittest discover -s tests -v
```
