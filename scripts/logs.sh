#!/usr/bin/env bash

set -euo pipefail

source "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/lib.sh"

MODE="${1:-dev}"
SERVICE="${2:-}"

if [[ -n "$SERVICE" ]]; then
  compose -f "$(compose_file_for_mode "$MODE")" logs -f --tail=200 "$SERVICE"
else
  compose -f "$(compose_file_for_mode "$MODE")" logs -f --tail=200
fi
