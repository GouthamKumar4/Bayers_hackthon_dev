from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field

app = FastAPI(
    title="Booking Ticket Service - Simple",
    version="0.1.0",
    description="Single-file FastAPI app for faster development and experiments.",
)


class BookingCreate(BaseModel):
    customer_name: str = Field(..., min_length=1, max_length=120)
    event_name: str = Field(..., min_length=1, max_length=120)
    seats: int = Field(..., ge=1, le=10)


class Booking(BaseModel):
    booking_id: int
    customer_name: str
    event_name: str
    seats: int


BOOKINGS: dict[int, Booking] = {}
NEXT_ID = 1


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "booking-ticket-service-simple"}


@app.post("/bookings", response_model=Booking, status_code=status.HTTP_201_CREATED)
def create_booking(payload: BookingCreate) -> Booking:
    global NEXT_ID
    booking = Booking(booking_id=NEXT_ID, **payload.model_dump())
    BOOKINGS[NEXT_ID] = booking
    NEXT_ID += 1

    # TODO(database): move BOOKING store to Azure managed DB.
    # TODO(auth): add Microsoft Entra ID authN/authZ checks.
    # TODO(cache): add Azure Redis for read-heavy endpoints.
    # TODO(observability): add OpenTelemetry export to Azure Monitor.
    return booking


@app.get("/bookings", response_model=list[Booking])
def list_bookings() -> list[Booking]:
    return list(BOOKINGS.values())


@app.get("/bookings/{booking_id}", response_model=Booking)
def get_booking(booking_id: int) -> Booking:
    booking = BOOKINGS.get(booking_id)
    if not booking:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Booking {booking_id} not found",
        )
    return booking


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("simple_app.main:app", host="127.0.0.1", port=8010, reload=False)
