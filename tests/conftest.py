"""Fixture compartida: garantiza el emulador de Firestore durante las pruebas.

Si el puerto 8080 ya responde, lo reutiliza (no lo detiene al terminar).
Si no, arranca `firebase emulators:start --only firestore` y lo detiene
al finalizar la sesión de pytest.
"""
import os
import shutil
import socket
import subprocess
import time
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parent.parent
EMULATOR_HOST = "127.0.0.1"
EMULATOR_PORT = 8080
STARTUP_TIMEOUT = 120


def _emulator_is_up() -> bool:
    try:
        with socket.create_connection((EMULATOR_HOST, EMULATOR_PORT), timeout=1):
            return True
    except OSError:
        return False


def _firebase_cli() -> str | None:
    cli = shutil.which("firebase") or shutil.which("firebase.cmd")
    if cli:
        return cli
    # Ruta por defecto de una instalación global con npm en Windows
    fallback = Path(os.environ.get("APPDATA", "")) / "npm" / "firebase.cmd"
    return str(fallback) if fallback.exists() else None


def _stop(process: subprocess.Popen) -> None:
    try:
        if os.name == "nt":
            subprocess.run(
                ["taskkill", "/PID", str(process.pid), "/T", "/F"],
                capture_output=True,
                check=False,
            )
        else:
            process.terminate()
    finally:
        try:
            process.wait(timeout=15)
        except subprocess.TimeoutExpired:
            process.kill()


@pytest.fixture(scope="session", autouse=True)
def firestore_emulator():
    os.environ.setdefault(
        "FIRESTORE_EMULATOR_HOST", f"{EMULATOR_HOST}:{EMULATOR_PORT}"
    )

    process = None
    if not _emulator_is_up():
        cli = _firebase_cli()
        if not cli:
            pytest.fail(
                "El emulador de Firestore no está corriendo y no se encontró la CLI "
                "de Firebase.\nInstálala con:  npm install -g firebase-tools\n"
                "o arranca el emulador manualmente:  firebase emulators:start "
                "--only firestore"
            )
        log = open(
            PROJECT_ROOT / "firestore-emulator-tests.log", "w", encoding="utf-8"
        )
        process = subprocess.Popen(
            [cli, "emulators:start", "--only", "firestore", "--project", "friendlyeats-dev"],
            cwd=PROJECT_ROOT,
            stdout=log,
            stderr=subprocess.STDOUT,
        )
        deadline = time.time() + STARTUP_TIMEOUT
        while time.time() < deadline:
            if _emulator_is_up():
                break
            if process.poll() is not None:
                pytest.fail(
                    "El emulador terminó inesperadamente; revisa "
                    "firestore-emulator-tests.log"
                )
            time.sleep(1)
        else:
            _stop(process)
            pytest.fail(
                f"El emulador no respondió en {STARTUP_TIMEOUT}s; revisa "
                "firestore-emulator-tests.log"
            )

    yield

    if process is not None:
        _stop(process)
