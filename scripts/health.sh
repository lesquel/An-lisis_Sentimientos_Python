#!/usr/bin/env bash

set -euo pipefail

BACKEND_URL="${BACKEND_URL:-http://127.0.0.1:8000/api/}"
FRONTEND_DEV_URL="${FRONTEND_DEV_URL:-http://localhost:5173}"

check_url() {
  local name="$1"
  local url="$2"
  if curl -fsS "$url" >/dev/null; then
    echo "✅ $name OK -> $url"
  else
    echo "❌ $name FAIL -> $url"
    return 1
  fi
}

check_url "Backend API" "$BACKEND_URL"
check_url "Frontend (dev)" "$FRONTEND_DEV_URL"
