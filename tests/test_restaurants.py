"""Pruebas básicas del CRUD de restaurantes (S1-24).

Requieren el emulador de Firestore (tests/conftest.py lo arranca solo
si no está corriendo).
"""
import uuid

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def _payload(**overrides) -> dict:
    """Payload válido y único para no colisionar entre corridas."""
    suffix = uuid.uuid4().hex[:8]
    data = {
        "name": f"Restaurante Test {suffix}",
        "category": "Mexicana",
        "city": f"TestCity {suffix}",
        "price": 2,
    }
    data.update(overrides)
    return data


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_create_restaurant():
    payload = _payload()
    response = client.post("/api/v1/restaurants", json=payload)
    assert response.status_code == 201
    body = response.json()
    assert body["name"] == payload["name"]
    assert body["avgRating"] == 0
    assert body["numRatings"] == 0
    assert body["id"]
    client.delete(f"/api/v1/restaurants/{body['id']}")  # limpieza


def test_invalid_price():
    response = client.post("/api/v1/restaurants", json=_payload(price=10))
    assert response.status_code == 422


def test_get_restaurant():
    created = client.post("/api/v1/restaurants", json=_payload()).json()
    response = client.get(f"/api/v1/restaurants/{created['id']}")
    assert response.status_code == 200
    assert response.json()["id"] == created["id"]
    client.delete(f"/api/v1/restaurants/{created['id']}")


def test_get_restaurant_not_found():
    response = client.get("/api/v1/restaurants/no-existe-123")
    assert response.status_code == 404


def test_update_restaurant():
    created = client.post("/api/v1/restaurants", json=_payload()).json()
    response = client.patch(
        f"/api/v1/restaurants/{created['id']}",
        json={"city": "Nueva Ciudad", "price": 3},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["city"] == "Nueva Ciudad"
    assert body["price"] == 3
    assert body["name"] == created["name"]  # no enviado => sin cambios
    client.delete(f"/api/v1/restaurants/{created['id']}")


def test_update_not_found():
    response = client.patch(
        "/api/v1/restaurants/no-existe-123", json={"city": "X"}
    )
    assert response.status_code == 404


def test_delete_restaurant():
    created = client.post("/api/v1/restaurants", json=_payload()).json()
    response = client.delete(f"/api/v1/restaurants/{created['id']}")
    assert response.status_code == 204
    assert client.get(f"/api/v1/restaurants/{created['id']}").status_code == 404


def test_delete_not_found():
    response = client.delete("/api/v1/restaurants/no-existe-123")
    assert response.status_code == 404


def test_list_restaurants():
    first = client.post("/api/v1/restaurants", json=_payload()).json()
    second = client.post("/api/v1/restaurants", json=_payload()).json()
    response = client.get(
        "/api/v1/restaurants", params={"limit": 100, "order_by": "name"}
    )
    assert response.status_code == 200
    names = [r["name"] for r in response.json()]
    assert first["name"] in names and second["name"] in names
    client.delete(f"/api/v1/restaurants/{first['id']}")
    client.delete(f"/api/v1/restaurants/{second['id']}")


def test_filters():
    suffix = uuid.uuid4().hex[:8]
    created = client.post(
        "/api/v1/restaurants",
        json=_payload(city=f"FilterCity {suffix}", category="SushiTest", price=1),
    ).json()
    response = client.get(
        "/api/v1/restaurants",
        params={"city": f"FilterCity {suffix}", "category": "SushiTest", "price": 1},
    )
    assert response.status_code == 200
    results = response.json()
    assert len(results) == 1
    assert results[0]["id"] == created["id"]
    client.delete(f"/api/v1/restaurants/{created['id']}")


def test_invalid_order_by():
    response = client.get("/api/v1/restaurants", params={"order_by": "password"})
    assert response.status_code == 400


def test_home_renders_html():
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert "FriendlyEats" in response.text
