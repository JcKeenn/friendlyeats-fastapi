"""Cliente de Firestore: emulador local (Sprint 1) o proyecto real de Firebase."""
import os

from google.auth import credentials as google_auth_credentials
from google.cloud import firestore

from app.core.config import settings

# Con el emulador activo no se necesitan credenciales reales de Firebase.
if settings.FIRESTORE_EMULATOR_HOST:
    os.environ["FIRESTORE_EMULATOR_HOST"] = settings.FIRESTORE_EMULATOR_HOST


def get_firestore_client() -> firestore.Client:
    """Devuelve un cliente de Firestore según el entorno configurado.

    - Emulador (FIRESTORE_EMULATOR_HOST en .env): credenciales anónimas,
      no requiere cuenta de servicio. Ideal para desarrollo y pruebas.
    - Proyecto real: usa la cuenta de servicio de FIREBASE_CREDENTIALS_PATH.
    """
    project = settings.FIREBASE_PROJECT_ID

    if settings.FIRESTORE_EMULATOR_HOST:
        return firestore.Client(
            project=project,
            credentials=google_auth_credentials.AnonymousCredentials(),
        )

    if settings.FIREBASE_CREDENTIALS_PATH:
        import firebase_admin
        from firebase_admin import credentials as firebase_credentials

        if not firebase_admin._apps:
            credential = firebase_credentials.Certificate(
                settings.FIREBASE_CREDENTIALS_PATH
            )
            firebase_admin.initialize_app(credential, {"projectId": project})
        import firebase_admin as _admin

        return _admin.firestore.client()

    # Sin emulador ni ruta de credenciales: Application Default Credentials.
    return firestore.Client(project=project)


db = get_firestore_client()
