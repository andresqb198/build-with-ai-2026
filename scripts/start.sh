#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

echo "============================================"
echo "  Sistema de Respuesta a Incidentes de IA"
echo "============================================"
echo ""

# Validar entorno
bash "$SCRIPT_DIR/validate_env.sh"

# Instalar dependencias si es necesario
if ! python3 -c "import langchain" 2>/dev/null; then
    echo ""
    echo "Instalando dependencias de Python..."
    pip install -r "$PROJECT_DIR/requirements.txt"
fi

# Iniciar Langfuse
echo ""
echo "Iniciando Langfuse..."
docker compose -f "$PROJECT_DIR/observability/docker-compose.yml" up -d

echo "Esperando que Langfuse esté listo..."
for i in $(seq 1 30); do
    if curl -s http://localhost:3000 >/dev/null 2>&1; then
        echo "¡Langfuse está listo!"
        break
    fi
    if [ "$i" -eq 30 ]; then
        echo "ADVERTENCIA: Langfuse puede no estar listo aún. Verifica http://localhost:3000"
    fi
    sleep 2
done

echo ""
echo "============================================"
echo "  ¡Configuración completa!"
echo ""
echo "  Langfuse UI: http://localhost:3000"
echo "  (Crea una cuenta en la primera visita)"
echo ""
echo "  Para ejecutar el taller:"
echo "    python -m app.main"
echo "============================================"
