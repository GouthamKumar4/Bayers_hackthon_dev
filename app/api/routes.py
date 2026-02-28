from fastapi import APIRouter, Depends, HTTPException, status

from app.core.dependencies import get_booking_service
from app.models.booking import Booking, BookingCreate
from app.services.booking_service import BookingService

router = APIRouter()


@router.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "booking-ticket-service"}


@router.post("/bookings", response_model=Booking, status_code=status.HTTP_201_CREATED)
def create_booking(
    payload: BookingCreate,
    service: BookingService = Depends(get_booking_service),
) -> Booking:
    return service.create_booking(payload)


@router.get("/bookings", response_model=list[Booking])
def list_bookings(service: BookingService = Depends(get_booking_service)) -> list[Booking]:
    return service.list_bookings()


@router.get("/bookings/{booking_id}", response_model=Booking)
def get_booking(
    booking_id: int,
    service: BookingService = Depends(get_booking_service),
) -> Booking:
    booking = service.get_booking(booking_id)
    if not booking:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Booking {booking_id} not found",
        )
    return booking
