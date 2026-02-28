import unittest
from importlib.util import find_spec

HAS_PYDANTIC = find_spec("pydantic") is not None
HAS_FASTAPI = find_spec("fastapi") is not None and find_spec("httpx") is not None

if HAS_PYDANTIC:
    from pydantic import ValidationError

    from app.models.booking import BookingCreate
    from app.repositories.booking_repository import InMemoryBookingRepository
    from app.services.booking_service import BookingService

if HAS_FASTAPI and HAS_PYDANTIC:
    from fastapi.testclient import TestClient

    from app.main import app


@unittest.skipUnless(HAS_PYDANTIC, "pydantic is not installed in this environment")
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

    def test_get_unknown_booking_returns_none(self) -> None:
        self.assertIsNone(self.service.get_booking(999))

    def test_booking_create_validation(self) -> None:
        with self.assertRaises(ValidationError):
            BookingCreate(customer_name="", event_name="Concert", seats=2)

        with self.assertRaises(ValidationError):
            BookingCreate(customer_name="Alex", event_name="Concert", seats=0)


@unittest.skipUnless(
    HAS_FASTAPI and HAS_PYDANTIC,
    "fastapi/pydantic dependencies are not installed in this environment",
)
class FastAPIEndpointTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.client = TestClient(app)

    def test_health_endpoint(self) -> None:
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "ok")

    def test_create_list_and_get_booking(self) -> None:
        create_response = self.client.post(
            "/bookings",
            json={"customer_name": "Alex", "event_name": "Concert", "seats": 2},
        )
        self.assertEqual(create_response.status_code, 201)
        created = create_response.json()

        list_response = self.client.get("/bookings")
        self.assertEqual(list_response.status_code, 200)
        self.assertGreaterEqual(len(list_response.json()), 1)

        get_response = self.client.get(f"/bookings/{created['booking_id']}")
        self.assertEqual(get_response.status_code, 200)
        self.assertEqual(get_response.json()["customer_name"], "Alex")

    def test_get_unknown_booking_returns_404(self) -> None:
        response = self.client.get("/bookings/9999")
        self.assertEqual(response.status_code, 404)


if __name__ == "__main__":
    unittest.main()
