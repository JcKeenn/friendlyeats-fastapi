"""Endpoints REST de restaurantes (JSON) — Sprint 1."""
from fastapi import APIRouter, Query

from app.domain.schemas import RestaurantCreate, RestaurantResponse, RestaurantUpdate
from app.services.restaurant_service import RestaurantService

router = APIRouter(prefix="/restaurants", tags=["Restaurants"])
service = RestaurantService()


@router.get("", response_model=list[RestaurantResponse])
async def list_restaurants(
    category: str | None = None,
    city: str | None = None,
    price: int | None = Query(default=None, ge=1, le=3),
    order_by: str = "name",
    limit: int = Query(default=20, ge=1, le=100),
    start_after: str | None = None,
):
    """Lista de restaurantes con filtros, orden y paginación por cursor."""
    return service.list(
        category=category,
        city=city,
        price=price,
        order_by=order_by,
        limit=limit,
        start_after=start_after,
    )


@router.get("/{restaurant_id}", response_model=RestaurantResponse)
async def get_restaurant(restaurant_id: str):
    """Detalle de un restaurante; 404 si no existe."""
    return service.get(restaurant_id)


@router.post("", status_code=201, response_model=RestaurantResponse)
async def create_restaurant(payload: RestaurantCreate):
    """Crea un restaurante: guarda el documento y devuelve su ID."""
    return service.create(payload)


@router.patch("/{restaurant_id}", response_model=RestaurantResponse)
async def update_restaurant(restaurant_id: str, payload: RestaurantUpdate):
    """Actualiza solo los campos permitidos enviados."""
    return service.update(restaurant_id, payload)


@router.delete("/{restaurant_id}", status_code=204)
async def delete_restaurant(restaurant_id: str):
    """Elimina un restaurante; 204 si OK, 404 si no existe."""
    service.delete(restaurant_id)
