"""Esquemas Pydantic: validación de entrada y forma de salida de la API."""
from pydantic import BaseModel, Field


class RestaurantBase(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    category: str = Field(min_length=1, max_length=50)
    city: str = Field(min_length=1, max_length=50)
    price: int = Field(ge=1, le=3)
    photoUrl: str | None = None


class RestaurantCreate(RestaurantBase):
    """Payload de POST /api/v1/restaurants."""


class RestaurantUpdate(BaseModel):
    """Payload de PATCH /api/v1/restaurants/{id}: solo campos editables.

    Todos opcionales; se actualiza únicamente lo que el cliente envía
    (el servicio usa model_dump(exclude_unset=True)).
    """

    name: str | None = Field(default=None, min_length=1, max_length=100)
    category: str | None = Field(default=None, min_length=1, max_length=50)
    city: str | None = Field(default=None, min_length=1, max_length=50)
    price: int | None = Field(default=None, ge=1, le=3)
    photoUrl: str | None = None


class RestaurantResponse(RestaurantBase):
    """Documento de restaurante tal como lo devuelve la API."""

    id: str
    avgRating: float = 0
    numRatings: int = 0
