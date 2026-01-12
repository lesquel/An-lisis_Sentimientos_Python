# syntax=docker/dockerfile:1

# ============================================
# Backend Dockerfile con UV - OPTIMIZADO
# ============================================

FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim AS builder

WORKDIR /app

# Habilitar bytecode compilation para mejor rendimiento
ENV UV_COMPILE_BYTECODE=1
# Copiar desde la cache en lugar de link (para Docker)
ENV UV_LINK_MODE=copy
# Forzar PyTorch CPU-only (reduce de 2GB a 200MB)
ENV UV_EXTRA_INDEX_URL=https://download.pytorch.org/whl/cpu

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

# Instalar bash para el entrypoint
RUN apt-get update && apt-get install -y --no-install-recommends bash \
    && rm -rf /var/lib/apt/lists/*

# Crear usuario no-root para seguridad
RUN groupadd --gid 1000 appgroup && \
    useradd --uid 1000 --gid appgroup --shell /bin/bash --create-home appuser

# Copiar el entorno virtual desde el builder
COPY --from=builder --chown=appuser:appgroup /app /app

# Crear directorios con permisos de escritura
# Incluye .cache para modelos de HuggingFace
RUN mkdir -p /app/data /app/staticfiles /app/.cache && \
    chown -R appuser:appgroup /app/data /app/staticfiles /app/.cache

# Configurar HuggingFace para usar el directorio de cache correcto
ENV HF_HOME=/app/.cache
ENV HUGGINGFACE_HUB_CACHE=/app/.cache

# Hacer el entrypoint ejecutable
RUN chmod +x /app/entrypoint.sh

# Configurar el PATH para usar el entorno virtual
ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Variables de Django
ENV DJANGO_SETTINGS_MODULE=sentimind.settings

# Puerto para Render y otros servicios
ENV PORT=8000
EXPOSE 8000

# Cambiar a usuario no-root
USER appuser

# Usar entrypoint script
CMD ["/app/entrypoint.sh"]
