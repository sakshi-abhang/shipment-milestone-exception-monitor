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
    response = client.get(
        "/shipments/SHP-001"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["shipment_id"] == "SHP-001"
    assert "origin" in data
    assert "destination" in data
    assert "status" in data