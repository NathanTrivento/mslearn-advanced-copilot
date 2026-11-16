from main import app
from fastapi.testclient import TestClient

client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200


def test_countries():
    response = client.get("/countries")
    assert response.status_code == 200
    assert sorted(response.json()) == ["England", "France", "Germany", "Italy", "Peru", "Portugal", "Spain"]


def test_monthly_average():
    response = client.get("/countries/Spain/Seville/January")
    assert response.status_code == 200
    assert response.json() == {"high": 61, "low": 41}


def test_regions_returns_city_names():
    response = client.get("/regions/Portugal")
    assert response.status_code == 200
    assert response.json() == ["Lisbon", "Porto"]


def test_unknown_region_returns_not_found():
    response = client.get("/regions/spain")
    assert response.status_code == 404
    assert response.json() == {"detail": "Region not found"}


def test_spain_region_returns_city_names():
    """Return exactly the city names configured for Spain."""
    response = client.get("/regions/Spain")
    assert response.status_code == 200
    assert response.json() == ["Seville"]


def test_post_to_region_city_list_returns_method_not_allowed():
    """Reject POST requests to the region city-list route."""
    response = client.post("/regions/Spain")
    assert response.status_code == 405


def test_openapi_includes_region_city_list_path():
    """Expose the region city-list route in the OpenAPI paths."""
    response = client.get("/openapi.json")
    assert response.status_code == 200
    assert "/regions/{region}" in response.json()["paths"]
