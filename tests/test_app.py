import unittest
from importlib.util import find_spec

from app.models.booking import BookingCreate
from app.repositories.booking_repository import InMemoryBookingRepository
from app.services.booking_service import BookingService

HAS_FASTAPI = find_spec("fastapi") is not None

if HAS_FASTAPI:
    from fastapi.testclient import TestClient

    from app.main import app


class BookingServiceTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.repository = InMemoryBookingRepository()
        self.service = BookingService(self.repository)

    def test_create_and_get_booking(self) -> None:
        created = self.service.create_booking(
            BookingCreate(customer_name="Alex", event_name="Concert", seats=2)
        )
        fetched = self.service.get_booking(created.booking_id)

        self.assertIsNotNone(fetched)
        self.assertEqual(fetched.customer_name, "Alex")
        self.assertEqual(fetched.event_name, "Concert")
        self.assertEqual(fetched.seats, 2)

    def test_list_bookings(self) -> None:
        self.service.create_booking(
            BookingCreate(customer_name="Alex", event_name="Concert", seats=2)
        )
        self.service.create_booking(
            BookingCreate(customer_name="Sam", event_name="Play", seats=1)
        )

        bookings = self.service.list_bookings()
        self.assertEqual(len(bookings), 2)


@unittest.skipUnless(HAS_FASTAPI, "fastapi is not installed in this environment")
class FastAPIEndpointTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.client = TestClient(app)

    def test_health_endpoint(self) -> None:
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "ok")

    def test_get_unknown_booking_returns_404(self) -> None:
        response = self.client.get("/bookings/9999")
        self.assertEqual(response.status_code, 404)


if __name__ == "__main__":
    unittest.main()
