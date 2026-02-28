from functools import lru_cache

from app.repositories.booking_repository import InMemoryBookingRepository
from app.services.booking_service import BookingService


@lru_cache
def get_booking_service() -> BookingService:
    repository = InMemoryBookingRepository()
    return BookingService(repository)
