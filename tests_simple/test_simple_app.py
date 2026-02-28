import unittest
from importlib.util import find_spec

HAS_FASTAPI = find_spec("fastapi") is not None and find_spec("httpx") is not None

if HAS_FASTAPI:
    from fastapi.testclient import TestClient

    from simple_app.main import app


@unittest.skipUnless(HAS_FASTAPI, "fastapi/httpx is not installed")
class SimpleAppTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.client = TestClient(app)

    def test_health(self) -> None:
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)

    def test_create_and_read(self) -> None:
        create_response = self.client.post(
            "/bookings",
            json={"customer_name": "Dev", "event_name": "Meetup", "seats": 1},
        )
        self.assertEqual(create_response.status_code, 201)
        booking_id = create_response.json()["booking_id"]

        get_response = self.client.get(f"/bookings/{booking_id}")
        self.assertEqual(get_response.status_code, 200)


if __name__ == "__main__":
    unittest.main()
