# Booking Microservice TODOs

## Platform and architecture
- [ ] Add containerized deployment artifacts for Azure Container Apps / AKS.
- [ ] Add environment-based config module (`dev`, `test`, `prod`).
- [ ] Add API versioning (`/api/v1`) and backward compatibility policy.

## Persistence
- [ ] Replace in-memory repository with Azure Database for PostgreSQL (managed instance).
- [ ] Add SQLAlchemy models and Alembic migrations.
- [ ] Add optimistic locking and audit fields (`created_at`, `updated_at`).

## Security and access control
- [ ] Integrate Microsoft Entra ID JWT validation.
- [ ] Add role-based authorization (admin, support, customer).
- [ ] Add rate limiting and API key support for trusted internal services.

## Caching and performance
- [ ] Integrate Azure Cache for Redis for hot reads.
- [ ] Add idempotency key support for booking creation.

## Observability
- [ ] Add OpenTelemetry traces, metrics, and logs.
- [ ] Export telemetry to Azure Monitor / Application Insights.
- [ ] Add correlation IDs and structured logging fields.

## Quality engineering
- [ ] Add unit tests for repository and service layers.
- [ ] Add integration test profile with testcontainers.
- [ ] Enforce linting and type checks in CI.
