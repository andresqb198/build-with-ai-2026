#!/usr/bin/env bash
set -euo pipefail

errors=0

echo "Validating environment..."
echo ""

# Check Python
if command -v python3 &>/dev/null; then
    py_version=$(python3 --version 2>&1)
    echo "[OK] Python: $py_version"
else
    echo "[ERROR] Python 3 is not installed"
    errors=$((errors + 1))
fi

# Check Docker
if command -v docker &>/dev/null; then
    echo "[OK] Docker: $(docker --version 2>&1 | head -1)"
else
    echo "[ERROR] Docker is not installed"
    errors=$((errors + 1))
fi

# Check Docker Compose
if docker compose version &>/dev/null 2>&1; then
    echo "[OK] Docker Compose: $(docker compose version 2>&1 | head -1)"
else
    echo "[ERROR] Docker Compose is not available"
    errors=$((errors + 1))
fi

# Check .env file
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

if [ -f "$PROJECT_DIR/.env" ]; then
    echo "[OK] .env file found"
else
    echo "[WARN] .env file not found — copy .env.example to .env and fill in your keys"
fi

# Check required env vars (load .env if present)
if [ -f "$PROJECT_DIR/.env" ]; then
    set -a
    source "$PROJECT_DIR/.env"
    set +a
fi

for var in GOOGLE_API_KEY; do
    if [ -n "${!var:-}" ]; then
        echo "[OK] $var is set"
    else
        echo "[ERROR] $var is not set"
        errors=$((errors + 1))
    fi
done

for var in LANGFUSE_PUBLIC_KEY LANGFUSE_SECRET_KEY; do
    if [ -n "${!var:-}" ]; then
        echo "[OK] $var is set"
    else
        echo "[WARN] $var is not set (configure after Langfuse first launch)"
    fi
done

echo ""
if [ "$errors" -gt 0 ]; then
    echo "Validation failed with $errors error(s)."
    exit 1
else
    echo "Environment validation passed."
fi
