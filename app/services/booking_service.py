from app.models.booking import Booking, BookingCreate
from app.repositories.booking_repository import InMemoryBookingRepository


class BookingService:
    def __init__(self, repository: InMemoryBookingRepository) -> None:
        self.repository = repository

    def create_booking(self, payload: BookingCreate) -> Booking:
        # TODO(auth): Validate caller identity and permissions before booking creation.
        return self.repository.create(payload)

    def get_booking(self, booking_id: int) -> Booking | None:
        # TODO(cache): Use Azure Cache for Redis for frequent booking lookups.
        return self.repository.get(booking_id)

    def list_bookings(self) -> list[Booking]:
        return list(self.repository.list())
