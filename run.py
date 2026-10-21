"""Arranque de desarrollo para FriendlyEats.

Equivale a `uvicorn app.main:app --reload`:
    python run.py
o simplemente F5 dentro de Visual Studio 2026.

Requisito: el emulador de Firestore debe estar corriendo
    firebase emulators:start --only firestore
"""
import uvicorn

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
