from pydantic import BaseModel, Field


class BookingCreate(BaseModel):
    customer_name: str = Field(..., min_length=1, max_length=120)
    event_name: str = Field(..., min_length=1, max_length=120)
    seats: int = Field(..., ge=1, le=10)


class Booking(BaseModel):
    booking_id: int
    customer_name: str
    event_name: str
    seats: int
