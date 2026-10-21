// FriendlyEats Sprint 1 — formularios (crear/editar) y borrado en el frontend.

function formatError(error) {
  if (!error) return "";
  if (Array.isArray(error.detail)) {
    const first = error.detail[0] || {};
    const field = (first.loc || []).slice(1).join(".");
    return `${field ? field + ": " : ""}${first.msg || "dato inválido"}`;
  }
  return typeof error.detail === "string" ? error.detail : "Error al guardar";
}

const form = document.getElementById("restaurant-form");

if (form) {
  form.addEventListener("submit", async (event) => {
    event.preventDefault();
    const restaurantId = form.dataset.restaurantId;
    const data = Object.fromEntries(new FormData(form));
    data.price = Number(data.price);
    if (!data.photoUrl) delete data.photoUrl; // opcional: no enviar vacío

    const url = restaurantId
      ? `/api/v1/restaurants/${restaurantId}`
      : "/api/v1/restaurants";
    const method = restaurantId ? "PATCH" : "POST";

    const response = await fetch(url, {
      method,
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
    });

    const message = document.getElementById("message");
    if (response.ok) {
      const msg = restaurantId
        ? "Restaurante actualizado correctamente"
        : "Restaurante creado correctamente";
      window.location.href = "/?msg=" + encodeURIComponent(msg);
    } else {
      const error = await response.json().catch(() => null);
      message.textContent = formatError(error) || "Error al guardar";
    }
  });
}

document.querySelectorAll('[data-action="delete"]').forEach((button) => {
  button.addEventListener("click", async () => {
    if (!confirm("¿Eliminar este restaurante? Esta acción no se puede deshacer.")) {
      return;
    }
    const response = await fetch(
      `/api/v1/restaurants/${button.dataset.id}`,
      { method: "DELETE" }
    );
    if (response.ok) {
      window.location.href = "/?msg=" + encodeURIComponent("Restaurante eliminado");
    } else {
      alert("No se pudo eliminar el restaurante");
    }
  });
});
