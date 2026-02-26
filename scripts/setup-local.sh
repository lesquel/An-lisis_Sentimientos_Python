#!/usr/bin/env bash

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

if command -v uv >/dev/null 2>&1; then
  echo "📦 Instalando dependencias backend con uv..."
  (cd "$ROOT_DIR/backend" && uv sync)
else
  echo "⚠️ uv no está instalado, se omite instalación de backend local."
fi

if command -v bun >/dev/null 2>&1; then
  echo "📦 Instalando dependencias frontend con bun..."
  (cd "$ROOT_DIR/frontend" && bun install)
elif command -v npm >/dev/null 2>&1; then
  echo "📦 Instalando dependencias frontend con npm..."
  (cd "$ROOT_DIR/frontend" && npm install)
else
  echo "⚠️ No se encontró bun ni npm; no se pudieron instalar dependencias de frontend."
fi

echo "✅ Setup local completado"
