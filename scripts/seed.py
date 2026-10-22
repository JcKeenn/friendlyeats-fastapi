"""Datos semilla: 20 restaurantes de prueba en la colección `restaurants`.

Ejecutar con el emulador de Firestore activo:

    python -m scripts.seed

No duplica: si un restaurante con el mismo nombre ya existe, se omite.
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
    {
        "name": "Asador La Brasa",
        "category": "Parrilla",
        "city": "CDMX",
        "price": 3,
        "photoUrl": "https://images.unsplash.com/photo-1544025162-d76694265947",
        "avgRating": 4.5,
        "numRatings": 33,
    },
    {
        "name": "Ramen Ichiban",
        "category": "Asiática",
        "city": "CDMX",
        "price": 2,
        "photoUrl": "https://images.unsplash.com/photo-1569718212165-3a8278d5f624",
        "avgRating": 4.4,
        "numRatings": 29,
    },
    {
        "name": "Salmón & Co",
        "category": "Mediterránea",
        "city": "Monterrey",
        "price": 3,
        "photoUrl": "https://images.unsplash.com/photo-1467003909585-2f8a72700288",
        "avgRating": 4.6,
        "numRatings": 24,
    },
    {
        "name": "Green Bowl",
        "category": "Vegana",
        "city": "Guadalajara",
        "price": 2,
        "photoUrl": "https://images.unsplash.com/photo-1540189549336-e6e99c3679fe",
        "avgRating": 4.2,
        "numRatings": 17,
    },
    {
        "name": "Desayunos La Parroquia",
        "category": "Desayunos",
        "city": "CDMX",
        "price": 1,
        "photoUrl": "https://images.unsplash.com/photo-1484723091739-30a097e8f929",
        "avgRating": 4.1,
        "numRatings": 26,
    },
    {
        "name": "Fuego y Vino",
        "category": "Española",
        "city": "Querétaro",
        "price": 3,
        "photoUrl": "https://images.unsplash.com/photo-1414235077428-338989a2e8c0",
        "avgRating": 4.7,
        "numRatings": 38,
    },
    {
        "name": "Napoletana 60",
        "category": "Pizza",
        "city": "Guadalajara",
        "price": 2,
        "photoUrl": "https://images.unsplash.com/photo-1565299624946-b28f40a0ae38",
        "avgRating": 4.3,
        "numRatings": 21,
    },
    {
        "name": "Wok Chan",
        "category": "Asiática",
        "city": "Puebla",
        "price": 1,
        "photoUrl": "https://images.unsplash.com/photo-1585032226651-759b368d7246",
        "avgRating": 3.8,
        "numRatings": 13,
    },
    {
        "name": "Maison Bleu",
        "category": "Francesa",
        "city": "CDMX",
        "price": 3,
        "photoUrl": "https://images.unsplash.com/photo-1551218808-94e220e084d2",
        "avgRating": 4.8,
        "numRatings": 52,
    },
    {
        "name": "Dulce Final",
        "category": "Postres",
        "city": "Morelia",
        "price": 1,
        "photoUrl": "https://images.unsplash.com/photo-1565958011703-44f9829ba187",
        "avgRating": 4.0,
        "numRatings": 19,
    },
]


def seed() -> int:
    """Inserta los restaurantes con ID automático (add), sin duplicar por nombre."""
    existing = {
        (doc.to_dict() or {}).get("name")
        for doc in db.collection("restaurants").stream()
    }
    added = 0
    for restaurant in restaurants:
        if restaurant["name"] in existing:
            continue
        db.collection("restaurants").add(restaurant)
        added += 1
    if added:
        print(f"✅ {added} restaurantes de prueba creados en Firestore.")
    else:
        print("ℹ️  Nada nuevo: los restaurantes semilla ya existen.")
    return added


if __name__ == "__main__":
    seed()
