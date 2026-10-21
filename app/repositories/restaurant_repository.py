"""Capa de datos: TODO el acceso a Firestore queda aislado aquí."""
from google.cloud.firestore import Client, Query
from google.cloud.firestore_v1.base_query import FieldFilter

from app.core.firebase import db

ORDER_FIELDS = {"name", "avgRating"}
PAGE_SIZE = 20


class RestaurantRepository:
    """Repositorio de la colección `restaurants` en Firestore."""

    def __init__(self, client: Client | None = None):
        self.collection = (client or db).collection("restaurants")

    def create(self, data: dict) -> dict:
        """Crea un documento con ID automático y rating inicial en cero."""
        payload = {**data, "avgRating": 0, "numRatings": 0}
        ref = self.collection.document()
        ref.set(payload)
        return {**payload, "id": ref.id}

    def get(self, restaurant_id: str) -> dict | None:
        doc = self.collection.document(restaurant_id).get()
        if not doc.exists:
            return None
        return {**doc.to_dict(), "id": doc.id}

    def list(
        self,
        category: str | None = None,
        city: str | None = None,
        price: int | None = None,
        order_by: str = "name",
        limit: int = PAGE_SIZE,
        start_after: str | None = None,
    ) -> list[dict]:
        """Lista filtrada, ordenada y paginada por cursor (start_after)."""
        query: Query = self.collection

        if category:
            query = query.where(filter=FieldFilter("category", "==", category))
        if city:
            query = query.where(filter=FieldFilter("city", "==", city))
        if price is not None:
            query = query.where(filter=FieldFilter("price", "==", price))

        field = "name" if order_by == "name" else "avgRating"
        direction = Query.ASCENDING if field == "name" else Query.DESCENDING
        query = query.order_by(field, direction=direction).limit(limit)

        if start_after:
            cursor_doc = self.collection.document(start_after).get()
            if cursor_doc.exists:
                query = query.start_after(cursor_doc)

        return [{**doc.to_dict(), "id": doc.id} for doc in query.stream()]

    def update(self, restaurant_id: str, data: dict) -> dict | None:
        ref = self.collection.document(restaurant_id)
        if not ref.get().exists:
            return None
        ref.update(data)
        return self.get(restaurant_id)

    def delete(self, restaurant_id: str) -> bool:
        ref = self.collection.document(restaurant_id)
        if not ref.get().exists:
            return False
        ref.delete()
        return True
