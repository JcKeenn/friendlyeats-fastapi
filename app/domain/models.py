"""Modelo de dominio del restaurante."""
from dataclasses import dataclass

PRICE_LABELS = {1: "$", 2: "$$", 3: "$$$"}


@dataclass
class Restaurant:
    """Entidad central de FriendlyEats (Sprint 1).

    El precio es un entero 1-3 ($, $$, $$$). `avgRating` y `numRatings`
    nacen en 0 al crear un restaurante; las reseñas (Sprint 2) los actualizan.
    """

    id: str
    name: str
    category: str
    city: str
    price: int
    photoUrl: str | None = None
    avgRating: float = 0.0
    numRatings: int = 0
