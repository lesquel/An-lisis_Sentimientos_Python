#!/usr/bin/env bash

set -euo pipefail

source "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/lib.sh"

MODE="${1:-dev}"
EXTRA_ARGS=()

if [[ "${2:-}" == "--volumes" ]]; then
  EXTRA_ARGS+=(--volumes --remove-orphans)
fi

compose -f "$(compose_file_for_mode "$MODE")" down "${EXTRA_ARGS[@]}"

echo "🛑 Servicios detenidos (${MODE})"
