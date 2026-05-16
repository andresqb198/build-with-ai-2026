#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

echo "Reiniciando el entorno del taller..."
echo ""

# Detener y eliminar contenedores + volúmenes de Langfuse
docker compose -f "$PROJECT_DIR/langfuse/docker-compose.yml" down -v 2>/dev/null || true

echo "Datos de Langfuse eliminados."
echo ""
echo "Para reiniciar, ejecuta: ./scripts/start.sh"
