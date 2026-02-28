from dataclasses import dataclass

try:
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

except ModuleNotFoundError:

    @dataclass
    class BookingCreate:
        customer_name: str
        event_name: str
        seats: int

        def __post_init__(self) -> None:
            if not self.customer_name or len(self.customer_name) > 120:
                raise ValueError("customer_name must be 1..120 characters")
            if not self.event_name or len(self.event_name) > 120:
                raise ValueError("event_name must be 1..120 characters")
            if self.seats < 1 or self.seats > 10:
                raise ValueError("seats must be between 1 and 10")

        def model_dump(self) -> dict[str, object]:
            return {
                "customer_name": self.customer_name,
                "event_name": self.event_name,
                "seats": self.seats,
            }

    @dataclass
    class Booking:
        booking_id: int
        customer_name: str
        event_name: str
        seats: int
