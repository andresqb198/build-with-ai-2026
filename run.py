#!/usr/bin/env python3
"""
Cross-platform CLI para el Sistema de Respuesta a Incidentes de IA.
Reemplaza el Makefile y los scripts .sh — funciona en Linux, macOS y Windows.

Uso:
    python run.py setup     — Instalar dependencias y crear .env
    python run.py start     — Iniciar Langfuse y validar el entorno
    python run.py stop      — Detener los contenedores de Langfuse
    python run.py reset     — Reiniciar Langfuse (elimina todos los datos)
    python run.py run       — Ejecutar el sistema de respuesta a incidentes
    python run.py validate  — Verificar la configuración del entorno
    python run.py help      — Mostrar esta ayuda
"""

import os
import shutil
import subprocess
import sys
import time
import urllib.request
import urllib.error
from pathlib import Path

ROOT = Path(__file__).resolve().parent
COMPOSE_FILE = ROOT / "observability" / "docker-compose.yml"
ENV_FILE = ROOT / ".env"
ENV_EXAMPLE = ROOT / ".env.example"


# ── Helpers ────────────────────────────────────────────────────────────────────

def run(cmd: list[str], **kwargs) -> subprocess.CompletedProcess:
    """Run a command, streaming output to the terminal."""
    return subprocess.run(cmd, check=True, **kwargs)


def compose(*args: str, **kwargs) -> subprocess.CompletedProcess:
    """Run a docker compose command against the observability stack."""
    return run(["docker", "compose", "-f", str(COMPOSE_FILE), *args], **kwargs)


def ok(msg: str) -> None:
    print(f"  [OK]   {msg}")


def warn(msg: str) -> None:
    print(f"  [WARN] {msg}")


def error(msg: str) -> None:
    print(f"  [ERROR] {msg}")


def header(msg: str) -> None:
    width = 48
    print("=" * width)
    print(f"  {msg}")
    print("=" * width)


# ── Commands ───────────────────────────────────────────────────────────────────

def cmd_validate() -> bool:
    """Verify that all required tools and env vars are present."""
    print("Validando el entorno...\n")
    errors = 0

    # Python
    v = sys.version.split()[0]
    if sys.version_info >= (3, 10):
        ok(f"Python {v}")
    else:
        error(f"Python {v} — se requiere 3.10+")
        errors += 1

    # Docker
    if shutil.which("docker"):
        result = subprocess.run(["docker", "--version"], capture_output=True, text=True)
        ok(result.stdout.strip())
    else:
        error("Docker no está instalado — https://docs.docker.com/get-docker/")
        errors += 1

    # Docker Compose
    result = subprocess.run(
        ["docker", "compose", "version"], capture_output=True, text=True
    )
    if result.returncode == 0:
        ok(result.stdout.strip())
    else:
        error("Docker Compose no está disponible")
        errors += 1

    # .env file
    if ENV_FILE.exists():
        ok(".env encontrado")
    else:
        warn(".env no encontrado — copia .env.example y completa tus claves")

    # Load env vars
    env_vars: dict[str, str] = {}
    if ENV_FILE.exists():
        for line in ENV_FILE.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, _, v = line.partition("=")
                env_vars[k.strip()] = v.strip().strip('"').strip("'")

    # Required vars
    for var in ["GOOGLE_API_KEY"]:
        val = env_vars.get(var) or os.getenv(var, "")
        if val:
            ok(f"{var} configurada")
        else:
            error(f"{var} no está configurada")
            errors += 1

    # Optional but expected after first Langfuse setup
    for var in ["LANGFUSE_PUBLIC_KEY", "LANGFUSE_SECRET_KEY"]:
        val = env_vars.get(var) or os.getenv(var, "")
        if val:
            ok(f"{var} configurada")
        else:
            warn(f"{var} no configurada (configúrala después del primer inicio de Langfuse)")

    print()
    if errors:
        print(f"Validación fallida con {errors} error(es).")
        return False
    print("Validación del entorno exitosa.")
    return True


def cmd_setup() -> None:
    """Install Python dependencies and create .env if missing."""
    header("Sistema de Respuesta a Incidentes de IA")
    print()

    if not ENV_FILE.exists():
        if ENV_EXAMPLE.exists():
            shutil.copy(ENV_EXAMPLE, ENV_FILE)
            print("Archivo .env creado desde .env.example")
            print("→ Edita .env y agrega tu GOOGLE_API_KEY antes de continuar.\n")
        else:
            warn(".env.example no encontrado — crea .env manualmente.")

    print("Instalando dependencias de Python...")
    run([sys.executable, "-m", "pip", "install", "-r", str(ROOT / "requirements.txt")])
    print("\n¡Dependencias instaladas!")


def cmd_start() -> None:
    """Start Langfuse and validate the environment."""
    header("Sistema de Respuesta a Incidentes de IA")
    print()

    if not cmd_validate():
        sys.exit(1)

    # Install deps if langchain is missing
    try:
        import langchain  # noqa: F401
    except ImportError:
        print("\nInstalando dependencias de Python...")
        run([sys.executable, "-m", "pip", "install", "-r", str(ROOT / "requirements.txt")])

    print("\nIniciando Langfuse...")
    compose("up", "-d")

    print("Esperando que Langfuse esté listo", end="", flush=True)
    for _ in range(30):
        try:
            urllib.request.urlopen("http://localhost:3000", timeout=2)
            print(" ¡listo!")
            break
        except (urllib.error.URLError, OSError):
            print(".", end="", flush=True)
            time.sleep(2)
    else:
        print()
        warn("Langfuse puede no estar listo aún. Verifica http://localhost:3000")

    print()
    print("=" * 48)
    print("  ¡Configuración completa!")
    print()
    print("  Langfuse UI: http://localhost:3000")
    print("  (Crea una cuenta en la primera visita)")
    print()
    print("  Para ejecutar el taller:")
    print("    python run.py run")
    print("=" * 48)


def cmd_stop() -> None:
    """Stop Langfuse containers."""
    print("Deteniendo Langfuse...")
    compose("down")
    print("Contenedores detenidos.")


def cmd_reset() -> None:
    """Stop Langfuse and wipe all data volumes."""
    print("Reiniciando el entorno del taller...")
    print()
    compose("down", "-v")
    print("Datos de Langfuse eliminados.")
    print()
    print("Para reiniciar, ejecuta: python run.py start")


def cmd_run() -> None:
    """Run the incident response system."""
    run([sys.executable, "-m", "app.main"])


def cmd_help() -> None:
    print(__doc__)


# ── Entry point ────────────────────────────────────────────────────────────────

COMMANDS = {
    "setup": cmd_setup,
    "start": cmd_start,
    "stop": cmd_stop,
    "reset": cmd_reset,
    "run": cmd_run,
    "validate": cmd_validate,
    "help": cmd_help,
}

if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "help"
    fn = COMMANDS.get(cmd)
    if fn is None:
        print(f"Comando desconocido: '{cmd}'")
        print(f"Comandos disponibles: {', '.join(COMMANDS)}")
        sys.exit(1)
    fn()
