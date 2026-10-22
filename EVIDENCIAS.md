# Evidencias del Sprint 1 — FriendlyEats

Cada entregable del Sprint 1 con su evidencia incluida en este paquete y cómo
verificarlo en vivo. Las capturas están en `docs/evidencias/`.

## Mapa entregable → evidencia

| # | Entregable | Evidencia incluida | Verificación en vivo |
|---|---|---|---|
| 1 | Repositorio Git (S1-01) | Historial en `.git` (`git log --oneline`) + `.gitignore` + `README.md` | `git log --oneline` |
| 2 | Entorno Python reproducible (S1-02) | `requirements.txt` (59 paquetes congelados) | `pip install -r requirements.txt` |
| 3 | Estructura por capas (S1-03) | Carpetas `app/api`, `app/services`, `app/repositories`, `app/domain`, `app/core` | explorar el repo |
| 4 | `GET /health` (S1-04) | `docs/evidencias/pytest-output.txt` (test_health) | `curl http://localhost:8000/health` → `{"status":"ok"}` |
| 5 | `.env.example` sin credenciales (S1-05) | `.env.example` (solo nombres de variables) | revisar archivo |
| 6 | Emulador Firestore (S1-06/S1-07) | `firebase.json` (firestore 8080 + UI 4000) | `firebase emulators:start --only firestore` |
| 7 | FastAPI conectado a Firestore (S1-08) | `docs/evidencias/crud-output.txt` | la app lista/crea/borra documentos |
| 8 | Esquemas Pydantic (S1-09) | `app/domain/schemas.py` | POST con `price=10` → 422 |
| 9 | CRUD completo (S1-10..S1-15) | `docs/evidencias/crud-output.txt` (201→200→200→204→404) | `python -m scripts.demo_crud` |
| 10 | Filtros (S1-16) | `docs/evidencias/05-filtros.png` + salida del filtro en `crud-output.txt` | `/?city=Puebla` en la UI |
| 11 | Vistas HTML (S1-17..S1-20) | `01-listado.png`, `02-detalle.png`, `03-formulario-nuevo.png`, `04-formulario-editar.png` | http://localhost:8000 |
| 12 | CSS responsive (S1-21) | `static/css/styles.css` + media query móvil | abrir en móvil / DevTools |
| 13 | JS del formulario (S1-22) | `static/js/app.js` (crea/edita/elimina + errores) | crear/editar/eliminar desde la UI |
| 14 | Datos semilla (S1-23) | `docs/evidencias/seed-output.txt` (10 restaurantes) + `06-emulador-firestore.png` | `python -m scripts.seed` |
| 15 | Pruebas del CRUD (S1-24) | `docs/evidencias/pytest-output.txt` → **15 passed** | `pytest -v` |
| 16 | README (S1-25) | `README.md` (comandos, arquitectura, decisiones) | — |
| 17 | Persistencia en el emulador | `06-emulador-firestore.png` (colección `restaurants` con documentos) + `firestore-rest-documentos.txt` | http://127.0.0.1:4000/firestore/default/data/restaurants |

## Repositorio (S1-01)

- **Tipo:** Git en la raíz del proyecto (`friendlyeats-fastapi/.git`), creado con
  `git init` y **publicado en GitHub**:
  **https://github.com/JcKeenn/friendlyeats-fastapi** (privado, cuenta JcKeenn).
- **Rama:** `main` · remote `origin` configurado · historial completo en el push.
- **Autor:** Daix \<daix@users.noreply.github.com\> · octubre de 2026.
- Verificación: `git remote -v`, `git log origin/main --oneline`.
- Ninguna credencial queda en Git: `.gitignore` excluye `.env`, `secrets/` y los
  JSON de cuentas de servicio.

## Cómo regenerar las evidencias

```bash
firebase emulators:start --only firestore   # terminal 1
uvicorn app.main:app --reload              # terminal 2

python -m scripts.seed                 # datos semilla (10 restaurantes)
python -m scripts.demo_crud            # demostración del CRUD por HTTP
pytest -v                              # 15 pruebas
```

## Capturas incluidas (`docs/evidencias/`)

| Archivo | Contenido |
|---|---|
| `01-listado.png` | Listado con tarjetas de los 10 restaurantes semilla |
| `02-detalle.png` | Vista de detalle con botones Editar/Eliminar |
| `03-formulario-nuevo.png` | Formulario de creación |
| `04-formulario-editar.png` | Formulario de edición (mismo template, precargado) |
| `05-filtros.png` | Filtro aplicado: `city=Puebla`, `price=2`, orden por calificación |
| `06-emulador-firestore.png` | UI del Emulator Suite: colección `restaurants` con sus documentos |
| `crud-output.txt` | Salida real del CRUD por HTTP (201/200/204/404/422) |
| `pytest-output.txt` | Salida real de `pytest -v` (15 passed) |
| `seed-output.txt` | Salida real de la carga de datos semilla |
| `firestore-rest-documentos.json` | Documentos crudos servidos por el emulador (prueba REST de persistencia) |

> Fecha de generación: 21 de octubre de 2026. Todas las salidas fueron
> producidas ejecutando el proyecto incluido en este paquete.
> Re-verificado el 22 de octubre de 2026: `pytest -v` → **15 passed**
> (emulador auto-arrancado por `tests/conftest.py`).
