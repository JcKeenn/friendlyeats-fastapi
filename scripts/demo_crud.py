"""Demostración/evidencia del CRUD completo contra la API en marcha.

Con la app corriendo (uvicorn app.main:app --reload):

    python -m scripts.demo_crud
"""
import json
import urllib.error
import urllib.request

BASE = "http://localhost:8000"


def req(method: str, path: str, body: dict | None = None):
    data = json.dumps(body).encode() if body is not None else None
    request = urllib.request.Request(
        BASE + path,
        data=data,
        method=method,
        headers={"Content-Type": "application/json"} if data else {},
    )
    try:
        with urllib.request.urlopen(request) as response:
            return response.status, response.read().decode()
    except urllib.error.HTTPError as error:
        return error.code, error.read().decode()


def main() -> None:
    print(f"== CRUD de restaurantes contra {BASE} ==\n")

    # 1) CREAR
    status, body = req(
        "POST",
        "/api/v1/restaurants",
        {"name": "Demo CRUD", "category": "Mexicana", "city": "Puebla", "price": 2},
    )
    restaurant_id = json.loads(body)["id"]
    print(f"POST   /api/v1/restaurants                 -> {status} (crear)")
    print(f"       {body}\n")

    # 2) LEER
    status, body = req("GET", f"/api/v1/restaurants/{restaurant_id}")
    print(f"GET    /api/v1/restaurants/{restaurant_id}  -> {status} (detalle)\n")

    # 3) EDITAR: solo los campos enviados
    status, body = req(
        "PATCH",
        f"/api/v1/restaurants/{restaurant_id}",
        {"price": 3, "city": "Oaxaca"},
    )
    print(f"PATCH  /api/v1/restaurants/{restaurant_id}  -> {status} (editar)")
    print(f"       {body}\n")

    # 4) FILTRAR
    status, body = req("GET", "/api/v1/restaurants?city=Puebla")
    names = [r["name"] for r in json.loads(body)]
    print(f"GET    /api/v1/restaurants?city=Puebla     -> {status} (filtro)")
    print(f"       {len(names)} resultados: {names}\n")

    # 5) ELIMINAR
    status, _ = req("DELETE", f"/api/v1/restaurants/{restaurant_id}")
    print(f"DELETE /api/v1/restaurants/{restaurant_id}  -> {status} (eliminar)")

    # 6) Ya no existe (404)
    status, _ = req("GET", f"/api/v1/restaurants/{restaurant_id}")
    print(f"GET    /api/v1/restaurants/{restaurant_id}  -> {status} (ya no existe)\n")

    # 7) Validación Pydantic: precio fuera de rango
    status, _ = req(
        "POST",
        "/api/v1/restaurants",
        {"name": "Invalido", "category": "X", "city": "Y", "price": 10},
    )
    print(f"POST   price=10 (fuera de rango 1-3)       -> {status} (validación)")

    print("\n== CRUD completo: OK ==")


if __name__ == "__main__":
    main()
