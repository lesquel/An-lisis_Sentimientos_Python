# syntax=docker/dockerfile:1

# ============================================
# Backend Dockerfile con UV
# ============================================

FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim AS builder

WORKDIR /app

# Habilitar bytecode compilation para mejor rendimiento
ENV UV_COMPILE_BYTECODE=1
# Copiar desde la cache en lugar de link (para Docker)
ENV UV_LINK_MODE=copy

# Instalar dependencias primero (mejor caching)
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    uv sync --frozen --no-install-project --no-dev

# Copiar el proyecto
COPY . .

# Sincronizar el proyecto
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev

# ============================================
# Imagen final de producción
# ============================================
FROM python:3.13-slim-bookworm AS runtime

WORKDIR /app

# Crear usuario no-root para seguridad
RUN groupadd --gid 1000 appgroup && \
    useradd --uid 1000 --gid appgroup --shell /bin/bash --create-home appuser

# Copiar el entorno virtual desde el builder
COPY --from=builder --chown=appuser:appgroup /app /app

# Configurar el PATH para usar el entorno virtual
ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Variables de Django
ENV DJANGO_SETTINGS_MODULE=sentimind.settings

# Exponer puerto
EXPOSE 8000

# Cambiar a usuario no-root
USER appuser

# Comando para ejecutar la aplicación
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
