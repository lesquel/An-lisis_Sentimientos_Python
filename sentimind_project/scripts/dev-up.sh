#!/usr/bin/env bash

set -euo pipefail

source "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/lib.sh"

compose -f "$(compose_file_for_mode dev)" up --build -d

echo "✅ Servicios en desarrollo levantados"
echo "   Frontend: http://localhost:5173"
echo "   Backend:  http://127.0.0.1:8000/api/"
