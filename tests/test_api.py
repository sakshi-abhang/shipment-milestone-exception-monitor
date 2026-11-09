from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)
def test_health_check():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "healthy"
    }
    
def test_get_all_shipments():
    response = client.get("/shipments")

    assert response.status_code == 200
    assert isinstance(response.json(), list)
    
def test_shipment_not_found():
    response = client.get(
        "/shipments/SHP-DOES-NOT-EXIST"
    )

    assert response.status_code == 404

    assert response.json() == {
        "detail": "Shipment not found"
    }
    
def test_get_existing_shipment():
    shipment_data = {
        "shipment_id": "SHP-TEST-001",
        "container_number": "TEST1234567",
        "booking_number": "BOOK-TEST-001",
        "origin": "Mumbai",
        "destination": "Rotterdam",
        "planned_departure": "2026-11-10T08:00:00",
        "planned_arrival": "2026-11-30T10:00:00",
        "predicted_arrival": "2026-11-30T10:00:00",
        "status": "BOOKED"
    }

    create_response = client.post(
        "/shipments",
        json=shipment_data
    )

    assert create_response.status_code == 201

    response = client.get(
        "/shipments/SHP-TEST-001"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["shipment_id"] == "SHP-TEST-001"
    assert data["origin"] == "Mumbai"
    assert data["destination"] == "Rotterdam"
    assert data["status"] == "BOOKED"
