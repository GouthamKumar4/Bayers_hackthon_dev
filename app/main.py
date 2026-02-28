from fastapi import FastAPI

from app.api.routes import router as booking_router

app = FastAPI(
    title="Booking Ticket Service",
    version="0.1.0",
    description="Simple modular microservice to create and view ticket bookings.",
)

app.include_router(booking_router)


# TODO(observability): Add Azure Monitor OpenTelemetry instrumentation and export.
# TODO(auth): Integrate Microsoft Entra ID (Azure AD) JWT authn/authz middleware.
# TODO(database): Move persistence to Azure managed database instance.


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=False)
