# syntax=docker/dockerfile:1

# ============================================
# Frontend Dockerfile con Bun
# ============================================

FROM oven/bun:1 AS builder

WORKDIR /app

# Copiar archivos de dependencias
COPY package.json bun.lock* ./

# Instalar dependencias
RUN bun install --frozen-lockfile

# Copiar código fuente
COPY . .

# Build de producción
RUN bun run build

# ============================================
# Imagen de producción con Nginx
# ============================================
FROM nginx:alpine AS runtime

# Copiar configuración personalizada de nginx
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Copiar archivos estáticos del build
COPY --from=builder /app/dist /usr/share/nginx/html

# Exponer puerto
EXPOSE 80

# Healthcheck
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD wget --no-verbose --tries=1 --spider http://localhost/ || exit 1

CMD ["nginx", "-g", "daemon off;"]
