"""Datos semilla: 10 restaurantes de prueba en la colección `restaurants`.

Ejecutar con el emulador de Firestore activo:

    python -m scripts.seed
"""
from app.core.firebase import db

restaurants = [
    {
        "name": "La Abuela",
        "category": "Mexicana",
        "city": "Puebla",
        "price": 2,
        "photoUrl": "https://images.unsplash.com/photo-1552566626-52f8b828add9",
        "avgRating": 4.5,
        "numRatings": 20,
    },
    {
        "name": "Pizza Central",
        "category": "Pizza",
        "city": "Puebla",
        "price": 1,
        "photoUrl": "https://images.unsplash.com/photo-1513104890138-7c749659a591",
        "avgRating": 4.0,
        "numRatings": 12,
    },
    {
        "name": "Tacos El Güero",
        "category": "Tacos",
        "city": "CDMX",
        "price": 1,
        "photoUrl": "https://images.unsplash.com/photo-1565299585323-38d6b0865b47",
        "avgRating": 4.8,
        "numRatings": 35,
    },
    {
        "name": "Mariscos El Muelle",
        "category": "Mariscos",
        "city": "Veracruz",
        "price": 2,
        "photoUrl": "https://images.unsplash.com/photo-1559339352-11d035aa65de",
        "avgRating": 4.3,
        "numRatings": 18,
    },
    {
        "name": "Trattoria Bella",
        "category": "Italiana",
        "city": "CDMX",
        "price": 3,
        "photoUrl": "https://images.unsplash.com/photo-1517248135467-4c7edcad34c4",
        "avgRating": 4.6,
        "numRatings": 41,
    },
    {
        "name": "Verde Vegano",
        "category": "Vegana",
        "city": "Guadalajara",
        "price": 2,
        "photoUrl": "https://images.unsplash.com/photo-1512621776951-a57141f2eefd",
        "avgRating": 4.1,
        "numRatings": 9,
    },
    {
        "name": "Sushi Nara",
        "category": "Asiática",
        "city": "Monterrey",
        "price": 3,
        "photoUrl": "https://images.unsplash.com/photo-1579871494447-9811cf80d66c",
        "avgRating": 4.7,
        "numRatings": 27,
    },
    {
        "name": "Burger Nation",
        "category": "Hamburguesas",
        "city": "Monterrey",
        "price": 1,
        "photoUrl": "https://images.unsplash.com/photo-1568901346375-23c9450c58cd",
        "avgRating": 3.9,
        "numRatings": 15,
    },
    {
        "name": "Carnitas Don Lupito",
        "category": "Mexicana",
        "city": "Morelia",
        "price": 2,
        "photoUrl": "https://images.unsplash.com/photo-1504674900247-0877df9cc836",
        "avgRating": 4.4,
        "numRatings": 22,
    },
    {
        "name": "Café de Olla Bistro",
        "category": "Desayunos",
        "city": "Puebla",
        "price": 2,
        "photoUrl": "https://images.unsplash.com/photo-1521017432531-fbd92d768814",
        "avgRating": 4.2,
        "numRatings": 14,
    },
]


def seed() -> int:
    """Inserta los restaurantes con ID automático (add)."""
    for restaurant in restaurants:
        db.collection("restaurants").add(restaurant)
    print(f"✅ {len(restaurants)} restaurantes de prueba creados en Firestore.")
    return len(restaurants)


if __name__ == "__main__":
    seed()
