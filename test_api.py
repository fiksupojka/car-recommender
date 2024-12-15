from fastapi.testclient import TestClient

from main import app
import pytest

@pytest.fixture(scope="module")
def client(): #db_session):
    yield TestClient(app)

def test_read_cars(client):
    response = client.get("/cars/")
    assert response.status_code == 200
    assert len(response.json()) == 4340

def test_search_cars(client):
    response = client.post("/cars/search/", json={"fuel": ["Petrol"]})
    assert response.status_code == 200
    results = response.json()
    assert len(results) == 2123
    assert all(car['fuel'] == 'Petrol' for car in results)

    response = client.post("/cars/search/", json={"fuel": ["Diesel"]})
    assert response.status_code == 200
    results = response.json()
    assert len(results) == 2153
    assert all(car['fuel'] == 'Diesel' for car in results)

    response = client.post("/cars/search/", json={"name": ["Maruti"]})
    assert response.status_code == 200
    results = response.json()
    assert len(results) == 1280

    response = client.post("/cars/search/", json={"name": ["Skoda"]})
    assert response.status_code == 200
    results = response.json()
    assert len(results) == 68

    response = client.post("/cars/search/", json={"name": ["Maruti", 'Skoda']})
    assert response.status_code == 200
    results = response.json()
    assert len(results) == 1280 + 68