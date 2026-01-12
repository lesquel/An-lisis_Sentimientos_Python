#!/bin/bash
set -e

echo "🚀 Starting SentiMind Backend..."

# Ejecutar migraciones
echo "📦 Running database migrations..."
python manage.py migrate --noinput

# Colectar archivos estáticos
echo "📁 Collecting static files..."
python manage.py collectstatic --noinput

# Iniciar gunicorn
echo "🌐 Starting Gunicorn on port ${PORT:-8000}..."
exec gunicorn sentimind.wsgi:application \
    --bind 0.0.0.0:${PORT:-8000} \
    --workers 2 \
    --threads 2 \
    --timeout 120 \
    --access-logfile - \
    --error-logfile -
