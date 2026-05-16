#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

echo "Resetting workshop environment..."
echo ""

# Stop and remove Langfuse containers + volumes
docker compose -f "$PROJECT_DIR/langfuse/docker-compose.yml" down -v 2>/dev/null || true

echo "Langfuse data cleared."
echo ""
echo "To restart, run: ./scripts/start.sh"
