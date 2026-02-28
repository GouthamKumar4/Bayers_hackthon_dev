from collections.abc import Iterable

from app.models.booking import Booking, BookingCreate


class InMemoryBookingRepository:
    """Simple in-memory repository for ticket bookings."""

    def __init__(self) -> None:
        self._bookings: dict[int, Booking] = {}
        self._next_id = 1

    def create(self, request: BookingCreate) -> Booking:
        booking = Booking(booking_id=self._next_id, **request.model_dump())
        self._bookings[self._next_id] = booking
        self._next_id += 1
        return booking

    def get(self, booking_id: int) -> Booking | None:
        return self._bookings.get(booking_id)

    def list(self) -> Iterable[Booking]:
        return self._bookings.values()

    # TODO(database): Replace this in-memory store with Azure Database for PostgreSQL
    # or Azure SQL and proper migration tooling.
