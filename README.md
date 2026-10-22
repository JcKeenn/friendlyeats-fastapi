# 🍽️ FriendlyEats FastAPI — Sprint 1

Versión local funcional de **FriendlyEats**: crear, listar, ver, editar y
eliminar restaurantes en **Firestore** (emulador) desde una app **FastAPI**
con vistas HTML.

> Sprint 1 no incluye autenticación, reseñas, imágenes subidas ni despliegue;
> eso corresponde a sprints posteriores.

## ✅ Definición de terminado (cumplida)

| Criterio | Estado |
|---|---|
| Ejecutar con `uvicorn app.main:app --reload` | ✅ (o `python run.py` / F5 en Visual Studio) |
| Abrir http://localhost:8000 y ver el listado | ✅ |
| Crear restaurante desde formulario HTML | ✅ `/restaurants/new` |
| Ver el detalle de un restaurante | ✅ `/restaurants/{id}` |
| Editar y eliminar restaurante | ✅ `/restaurants/{id}/edit` + botón Eliminar |
| Filtrar por ciudad, categoría o precio | ✅ en la UI y en la API |
| Ver datos persistidos en el emulador de Firestore | ✅ UI del emulador en http://127.0.0.1:4000 |
| Pruebas básicas del CRUD | ✅ 14 pruebas, todas pasan |

## 🧰 Requisitos previos

- **Python 3.11+** (probado en 3.14.6)
- **Node.js 18+ / npm** — para la CLI de Firebase (`npm install -g firebase-tools`)
- **Java 11+** — requerido por el emulador de Firestore (probado con OpenJDK 21)
- Git

## 🚀 Ejecución paso a paso

```bash
# 1) Entorno virtual e instalaciones (una sola vez)
python -m venv .venv
.venv\Scripts\activate            # Windows   (source .venv/bin/activate en Linux/Mac)
pip install -r requirements.txt

# 2) Emulador de Firestore (terminal 1)
firebase emulators:start --only firestore

# 3) Datos semilla (terminal 2, la primera vez) — crea 20 restaurantes
python -m scripts.seed

# 4) Aplicación (terminal 2)
uvicorn app.main:app --reload     # equivalente a: python run.py  (o F5 en Visual Studio)
```

- App: **http://localhost:8000**
- Swagger / API interactiva: **http://localhost:8000/docs**
- UI del emulador de Firestore: **http://127.0.0.1:4000** → colección `restaurants`

> Nota: el emulador guarda los datos **en memoria**; si lo reinicias, vuelve a
> ejecutar `python -m scripts.seed`.

## 🧪 Pruebas

```bash
pytest -v
```

`tests/conftest.py` detecta si el emulador está corriendo; si no, lo arranca
solo y lo detiene al terminar (solo hace falta tener `firebase-tools`
instalado). Resultado actual: **14 passed** — CRUD completo, validaciones,
filtros, búsqueda y render HTML.

## 📁 Estructura del proyecto

```
friendlyeats-fastapi/
├── app/
│   ├── main.py                  # FastAPI: API + vistas HTML
│   ├── core/
│   │   ├── config.py            # Settings (pydantic-settings, .env)
│   │   └── firebase.py          # Cliente Firestore (emulador o real)
│   ├── domain/
│   │   ├── models.py            # Entidad Restaurant (dominio)
│   │   └── schemas.py           # Pydantic: Create/Update/Response
│   ├── repositories/
│   │   └── restaurant_repository.py   # TODO el acceso a Firestore
│   ├── services/
│   │   └── restaurant_service.py      # Lógica de negocio
│   ├── api/
│   │   └── v1/restaurants.py     # Endpoints REST /api/v1/restaurants
│   └── templates/               # Jinja2: base, listado, detalle, formulario
├── static/
│   ├── css/styles.css           # Interfaz responsive (escritorio y móvil)
│   ├── js/app.js                # Envía formularios, muestra errores, elimina
│   └── img/placeholder.svg      # Imagen de respaldo cuando no hay foto
├── scripts/seed.py              # 20 restaurantes de prueba (idempotente)
├── tests/                       # conftest (auto-emulador) + 14 pruebas
├── .env.example                 # Variables de entorno (sin credenciales)
├── .firebaserc                  # Proyecto por defecto: friendlyeats-dev
├── firebase.json                 # Emuladores (8080) + UI (4000)
├── firestore.rules              # Reglas (públicas en Sprint 1)
├── firestore.indexes.json        # Índices compuestos para filtros + orden
├── requirements.txt             # Dependencias congeladas
├── run.py                       # F5 en Visual Studio
└── FriendlyEats.sln             # Solución de Visual Studio 2026
```

## 🏗️ Arquitectura (capas)

```
Vistas HTML (Jinja2)     Endpoints REST (FastAPI)
        └──────────┬─────────┘
            RestaurantService        ← lógica de negocio + HTTP errors
                   │
        RestaurantRepository         ← único lugar que toca Firestore
                   │
            Firestore (emulador)    ← colección "restaurants"
```

- **API** (`app/api/v1`): valida y responde JSON. Montada en `/api/v1`.
- **Service** (`app/services`): reglas de negocio (404/400, orden permitido).
- **Repository** (`app/repositories`): aísla Firestore; se puede cambiar de
  base de datos sin tocar el resto.
- **Domain** (`app/domain`): esquemas Pydantic (validación) y entidad.
- **Core** (`app/core`): configuración por entorno y cliente de Firestore.

## 🔌 API REST

| Método | Ruta | Descripción |
|---|---|---|
| GET | `/health` | `{"status": "ok"}` |
| GET | `/api/v1/restaurants` | Lista (búsqueda `search` — prefijo de nombre o ciudad; filtros `category`, `city`, `price`; `order_by=name\|avgRating`; `limit`; `start_after`) |
| POST | `/api/v1/restaurants` | Crea (201) — `avgRating=0`, `numRatings=0` automáticos |
| GET | `/api/v1/restaurants/{id}` | Detalle (404 si no existe) |
| PATCH | `/api/v1/restaurants/{id}` | Actualiza solo los campos enviados |
| DELETE | `/api/v1/restaurants/{id}` | Elimina (204 / 404) |

### Vistas HTML

| Ruta | Vista |
|---|---|
| `/` | Listado con tarjetas, panel de búsqueda, filtros y paginación |
| `/restaurants/new` | Formulario crear |
| `/restaurants/{id}` | Detalle con acciones Editar/Eliminar |
| `/restaurants/{id}/edit` | Formulario editar (mismo template) |

## 📝 Decisiones técnicas

1. **Credenciales anónimas con el emulador** (`app/core/firebase.py`): con
   `FIRESTORE_EMULATOR_HOST` activo no se necesita cuenta de servicio —
   cero credenciales en el repo. Para un proyecto real se usa
   `FIREBASE_CREDENTIALS_PATH` con `firebase-admin`.
2. **`.gitignore` no usa `*.json` global**: el PDF lo sugiere, pero eso
   excluiría `firebase.json` y `firestore.indexes.json` (necesarios). En su
   lugar se ignoran `secrets/`, `.env` y los JSON de cuentas de servicio
   (`*-firebase-adminsdk-*.json`) — el criterio de aceptación se cumple.
3. **Índices compuestos** (`firestore.indexes.json`): Firestore exige índices
   para `where(...) + order_by(...)` en un proyecto real; se declaran todas
   las combinaciones de filtros × orden (name ASC / avgRating DESC).
4. **`order_by=avgRating` ordena descendente** (mejor calificados primero);
   `name` es ascendente.
5. **Paginación por cursor** (`start_after`): se devuelve el link
   "Siguiente página" solo cuando la página viene llena (20 docs).
6. **Pruebas auto-suficientes**: `tests/conftest.py` arranca el emulador si
   no está corriendo, así `pytest -v` funciona solo.
7. **`run.py` + `FriendlyEats.sln`**: para desarrollar y depurar con F5 en
   Visual Studio 2026 (Python workload instalada).
8. **Búsqueda "Buscar" con OR de Firestore**: `search` busca por prefijo de
   nombre (`name >= q` y `name <= q + \uf8ff`) **o** ciudad exacta con
   `OrFilter`; con búsqueda activa se ordena por `name` para usar índices
   simples. El dropdown de Categoría se llena con las categorías reales de la
   colección (`distinct_categories`). El panel (Buscar/Categoría/Precio +
   Limpiar) aplica los filtros al cambiar de opción o al pulsar Enter.

## 📦 Entregables del Sprint 1 y cómo verificarlos

| Entregable | Cómo demostrarlo |
|---|---|
| App FastAPI ejecutándose localmente | `uvicorn app.main:app --reload` → http://localhost:8000 |
| Firestore conectado al emulador | `firebase emulators:start --only firestore`; la app lista/crea documentos |
| CRUD completo de restaurantes | Crear en `/restaurants/new`, ver detalle, editar y eliminar desde la UI (o probar en http://localhost:8000/docs) |
| Vistas HTML para listar, crear, ver, editar y eliminar | Navegar `/`, `/restaurants/new`, `/restaurants/{id}`, `/restaurants/{id}/edit` |
| Filtros básicos por ciudad, categoría y precio | Panel de búsqueda de la portada (Buscar por nombre o ciudad + Categoría + Precio + Limpiar) o `GET /api/v1/restaurants?search=Puebla&price=2` |
| Datos semilla cargados | `python -m scripts.seed` → aparecen 20 restaurantes |
| Pruebas básicas del CRUD | `pytest -v` → 14 passed |
| README con instrucciones | Este archivo |

Los documentos persistidos se ven en la **UI del emulador**:
http://127.0.0.1:4000 → Firestore → Data → colección `restaurants`.

## 🔜 Sprint 2 (siguiente)

Firebase Authentication, control de propietario con `ownerId`, Security
Rules por propietario y reseñas con transacciones (recalcular `avgRating`
y `numRatings`).
