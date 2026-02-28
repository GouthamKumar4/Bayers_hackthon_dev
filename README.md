# Booking Ticket Service (Two App Modes)

This repo now contains **two maintained FastAPI implementations**:

1. **Modular app** (`app/`) — layered architecture (models/repository/service/routes).
2. **Simple app** (`simple_app/`) — single-file app for fast development/testing.

## Why two folders?

- `app/` is for production-style structure and long-term maintainability.
- `simple_app/` is for quick experiments and easy onboarding (everything in one file).

Both are kept side-by-side and each has separate Docker and CI entry points.

## Folder layout

```text
app/                    # modular/class-oriented structure
simple_app/             # single-file non-class service layer style
tests/                  # tests for modular app
tests_simple/           # tests for simple app
Dockerfile              # container for modular app
Dockerfile.simple       # container for simple app
.github/workflows/ci-devsecops.yml      # modular app pipeline
.github/workflows/simple-app-ci.yml     # simple app DevSecOps pipeline (tests+sonar+trivy+owasp+sbom)
```

## Modular app run

```bash
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

## Simple app run

```bash
python -m uvicorn simple_app.main:app --host 127.0.0.1 --port 8010
```

## Tests

Modular app tests:

```bash
python -m unittest discover -s tests -v
```

Simple app tests:

```bash
python -m unittest discover -s tests_simple -v
```

## Docker

Modular app image:

```bash
docker build -f Dockerfile -t booking-modular .
docker run --rm -p 8000:8000 booking-modular
```

Simple app image:

```bash
docker build -f Dockerfile.simple -t booking-simple .
docker run --rm -p 8010:8010 booking-simple
```

## TODO roadmap

Cloud-native TODO items (DB/auth/cache/observability) are tracked in `docs/TODO.md` and inline comments in both app implementations.
