#!/usr/bin/env bash
set -euo pipefail

errors=0

echo "Validando el entorno..."
echo ""

# Verificar Python
if command -v python3 &>/dev/null; then
    py_version=$(python3 --version 2>&1)
    echo "[OK] Python: $py_version"
else
    echo "[ERROR] Python 3 no está instalado"
    errors=$((errors + 1))
fi

# Verificar Docker
if command -v docker &>/dev/null; then
    echo "[OK] Docker: $(docker --version 2>&1 | head -1)"
else
    echo "[ERROR] Docker no está instalado"
    errors=$((errors + 1))
fi

# Verificar Docker Compose
if docker compose version &>/dev/null 2>&1; then
    echo "[OK] Docker Compose: $(docker compose version 2>&1 | head -1)"
else
    echo "[ERROR] Docker Compose no está disponible"
    errors=$((errors + 1))
fi

# Verificar archivo .env
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

if [ -f "$PROJECT_DIR/.env" ]; then
    echo "[OK] Archivo .env encontrado"
else
    echo "[WARN] Archivo .env no encontrado — copia .env.example a .env y completa tus claves"
fi

# Verificar variables de entorno requeridas (cargar .env si existe)
if [ -f "$PROJECT_DIR/.env" ]; then
    set -a
    source "$PROJECT_DIR/.env"
    set +a
fi

for var in GOOGLE_API_KEY; do
    if [ -n "${!var:-}" ]; then
        echo "[OK] $var está configurada"
    else
        echo "[ERROR] $var no está configurada"
        errors=$((errors + 1))
    fi
done

for var in LANGFUSE_PUBLIC_KEY LANGFUSE_SECRET_KEY; do
    if [ -n "${!var:-}" ]; then
        echo "[OK] $var está configurada"
    else
        echo "[WARN] $var no está configurada (configurar después del primer inicio de Langfuse)"
    fi
done

echo ""
if [ "$errors" -gt 0 ]; then
    echo "Validación fallida con $errors error(es)."
    exit 1
else
    echo "Validación del entorno exitosa."
fi
