#!/usr/bin/env bash

set -euo pipefail

source "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/lib.sh"

compose -f "$(compose_file_for_mode prod)" up --build -d

echo "✅ Servicios en modo producción levantados"
echo "   Frontend: http://localhost"
echo "   Backend:  http://127.0.0.1:8000/api/"
