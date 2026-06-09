from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_get_reviews_for_location():
    response = client.get("/reviews/1")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_create_review_valid(auth_headers):
    response = client.post("/reviews/", json={
        "location_id": 1,
        "rating": 5,
        "text": "Locatie foarte frumoasa si linistita!"
    }, headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["rating"] == 5
    assert "text" in data

def test_create_review_invalid_rating_too_high(auth_headers):
    response = client.post("/reviews/", json={
        "location_id": 1,
        "rating": 6,
        "text": "Text valid pentru recenzie"
    }, headers=auth_headers)
    assert response.status_code == 422

def test_create_review_invalid_rating_too_low(auth_headers):
    response = client.post("/reviews/", json={
        "location_id": 1,
        "rating": 0,
        "text": "Text valid pentru recenzie"
    }, headers=auth_headers)
    assert response.status_code == 422

def test_create_review_text_too_short(auth_headers):
    response = client.post("/reviews/", json={
        "location_id": 1,
        "rating": 4,
        "text": "Scurt"
    }, headers=auth_headers)
    assert response.status_code == 422

def test_create_review_xss_sanitization(auth_headers):
    response = client.post("/reviews/", json={
        "location_id": 1,
        "rating": 3,
        "text": "<script>alert('xss')</script> Recenzie normala cu text suficient"
    }, headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert "<script>" not in data["text"]
    assert "alert" in data["text"]
