#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

echo "============================================"
echo "  AI Incident Response System — Setup"
echo "============================================"
echo ""

# Validate environment
bash "$SCRIPT_DIR/validate_env.sh"

# Install dependencies if needed
if ! python3 -c "import langchain" 2>/dev/null; then
    echo ""
    echo "Installing Python dependencies..."
    pip install -r "$PROJECT_DIR/requirements.txt"
fi

# Start Langfuse
echo ""
echo "Starting Langfuse..."
docker compose -f "$PROJECT_DIR/langfuse/docker-compose.yml" up -d

echo "Waiting for Langfuse to be ready..."
for i in $(seq 1 30); do
    if curl -s http://localhost:3000 >/dev/null 2>&1; then
        echo "Langfuse is ready!"
        break
    fi
    if [ "$i" -eq 30 ]; then
        echo "WARNING: Langfuse may not be ready yet. Check http://localhost:3000"
    fi
    sleep 2
done

echo ""
echo "============================================"
echo "  Setup complete!"
echo ""
echo "  Langfuse UI: http://localhost:3000"
echo "  (Create an account on first visit)"
echo ""
echo "  To run the workshop:"
echo "    python -m app.main"
echo "============================================"
