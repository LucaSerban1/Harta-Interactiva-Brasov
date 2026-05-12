from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_get_locations_returns_list():
    response = client.get("/locations/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_locations_not_empty():
    response = client.get("/locations/")
    data = response.json()
    assert len(data) > 0

def test_get_location_by_id():
    response = client.get("/locations/1")
    assert response.status_code == 200
    data = response.json()
    assert "name" in data
    assert "lat" in data
    assert "lng" in data
    assert "category" in data

def test_get_location_not_found():
    response = client.get("/locations/99999")
    assert response.status_code == 404

def test_search_by_keyword():
    response = client.get("/locations/?q=cafe")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_filter_by_category():
    response = client.get("/locations/?category=cafe")
    assert response.status_code == 200
    data = response.json()
    for loc in data:
        assert loc["category"] == "cafe"