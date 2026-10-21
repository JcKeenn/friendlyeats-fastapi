"""Configuración central: valores leídos de variables de entorno (.env)."""
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Ajustes de la aplicación (ver .env.example)."""

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )

    APP_NAME: str = "FriendlyEats FastAPI"
    ENVIRONMENT: str = "local"
    FIREBASE_PROJECT_ID: str = "friendlyeats-dev"
    FIREBASE_CREDENTIALS_PATH: str | None = None
    FIRESTORE_EMULATOR_HOST: str | None = None


settings = Settings()
