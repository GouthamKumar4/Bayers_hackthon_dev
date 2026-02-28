from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_endpoint() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_create_and_get_booking() -> None:
    create_response = client.post(
        "/bookings",
        json={"customer_name": "Alex", "event_name": "Concert", "seats": 2},
    )
    assert create_response.status_code == 201
    created_booking = create_response.json()

    get_response = client.get(f"/bookings/{created_booking['booking_id']}")
    assert get_response.status_code == 200
    assert get_response.json()["customer_name"] == "Alex"


def test_get_unknown_booking_returns_404() -> None:
    response = client.get("/bookings/9999")
    assert response.status_code == 404
