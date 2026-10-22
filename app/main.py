"""FriendlyEats FastAPI — Sprint 1.

API REST en /api/v1/* + vistas HTML renderizadas con Jinja2.
"""
from pathlib import Path
from urllib.parse import urlencode

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.api.v1.restaurants import router as restaurants_router
from app.services.restaurant_service import RestaurantService

BASE_DIR = Path(__file__).resolve().parent.parent

app = FastAPI(title="FriendlyEats FastAPI")

app.include_router(restaurants_router, prefix="/api/v1")
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")

templates = Jinja2Templates(directory=BASE_DIR / "app" / "templates")
service = RestaurantService()


@app.get("/health")
async def health():
    """S1-04: endpoint de salud."""
    return {"status": "ok"}


@app.get("/algoritmos")
async def algoritmos(request: Request):
    """Investigación de algoritmos de búsqueda: definición, elementos,
    ejemplo, clasificación e infografía."""
    return templates.TemplateResponse(request, "algoritmos.html", {})


def _filters_from_request(request: Request) -> dict:
    """Lee los filtros de la query string y normaliza tipos."""
    price_raw = request.query_params.get("price")
    return {
        "search": (request.query_params.get("search") or "").strip() or None,
        "category": request.query_params.get("category") or None,
        "city": request.query_params.get("city") or None,
        "price": int(price_raw) if price_raw in ("1", "2", "3") else None,
        "order_by": request.query_params.get("order_by") or "name",
        "start_after": request.query_params.get("start_after") or None,
    }


@app.get("/")
async def home(request: Request):
    """Vista de listado con filtros y paginación."""
    filters = _filters_from_request(request)
    restaurants = service.list(**filters)

    next_url = None
    if len(restaurants) == 20:  # probablemente hay más documentos
        query = {k: v for k, v in filters.items() if v}
        query["start_after"] = restaurants[-1]["id"]
        next_url = "/?" + urlencode(query)

    return templates.TemplateResponse(
        request,
        "restaurants.html",
        {
            "restaurants": restaurants,
            "filters": filters,
            "categories": service.distinct_categories(),
            "next_url": next_url,
            "msg": request.query_params.get("msg"),
        },
    )


@app.get("/restaurants/new")
async def new_restaurant_form(request: Request):
    """Formulario HTML para crear un restaurante."""
    return templates.TemplateResponse(
        request, "restaurant_form.html", {"restaurant": None}
    )


@app.get("/restaurants/{restaurant_id}")
async def restaurant_detail(request: Request, restaurant_id: str):
    """Vista de detalle de un restaurante."""
    try:
        restaurant = service.get(restaurant_id)
    except HTTPException:
        return RedirectResponse(
            "/?" + urlencode({"msg": "Restaurante no encontrado"}), status_code=303
        )
    return templates.TemplateResponse(
        request, "restaurant_detail.html", {"restaurant": restaurant}
    )


@app.get("/restaurants/{restaurant_id}/edit")
async def edit_restaurant_form(request: Request, restaurant_id: str):
    """Formulario HTML para editar un restaurante existente."""
    try:
        restaurant = service.get(restaurant_id)
    except HTTPException:
        return RedirectResponse(
            "/?" + urlencode({"msg": "Restaurante no encontrado"}), status_code=303
        )
    return templates.TemplateResponse(
        request, "restaurant_form.html", {"restaurant": restaurant}
    )
