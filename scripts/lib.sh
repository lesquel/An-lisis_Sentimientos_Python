#!/usr/bin/env bash

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

compose() {
  if command -v docker >/dev/null 2>&1 && docker compose version >/dev/null 2>&1; then
    docker compose "$@"
  elif command -v docker-compose >/dev/null 2>&1; then
    docker-compose "$@"
  else
    echo "Error: no se encontró Docker Compose (docker compose o docker-compose)." >&2
    exit 1
  fi
}

compose_file_for_mode() {
  local mode="${1:-dev}"
  case "$mode" in
    dev)
      echo "$ROOT_DIR/docker-compose.dev.yml"
      ;;
    prod)
      echo "$ROOT_DIR/docker-compose.yml"
      ;;
    *)
      echo "Error: modo inválido '$mode'. Usa: dev | prod" >&2
      exit 1
      ;;
  esac
}
