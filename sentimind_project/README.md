# Sentimind Network

Plataforma web para análisis de sentimientos y emociones en texto usando Django REST + React + modelo NLP (Zero-Shot, XLM-RoBERTa).

## Estado del proyecto

- API backend en Django REST Framework con JWT.
- Frontend React + Vite para publicación y visualización de posts.
- Flujo Docker para desarrollo y producción.
- Taxonomía de 25 emociones con clasificación multi-etiqueta.

## Demo local rápida

### Opción recomendada (Docker)

```bash
make dev
```

Servicios:
- Frontend: http://localhost:5173
- Backend API: http://127.0.0.1:8000/api/
- Admin Django: http://127.0.0.1:8000/admin/

### Detener servicios

```bash
make down
```

## Scripts y tareas

El proyecto incluye comandos estándar para operación diaria:

```bash
make help
make dev        # levantar entorno de desarrollo
make prod       # levantar entorno producción
make logs       # logs en tiempo real
make status     # estado de contenedores
make test       # tests backend
make lint       # lint frontend
make health     # verificación de endpoints
```

En VS Code también están disponibles en `Run Task...` con prefijo **Sentimind:**.

## Estructura

```text
sentimind_project/
├── backend/                # Django + DRF + motor NLP
├── frontend/               # React + Vite
├── scripts/                # scripts operativos del proyecto
├── .vscode/tasks.json      # tareas ejecutables desde VS Code
├── docker-compose.yml      # stack producción
├── docker-compose.dev.yml  # stack desarrollo
└── DOCUMENTACION.md        # documentación académica/técnica
```

## Documentación

- Resumen rápido: `RESUMEN_DOCUMENTACION.md`
- Documentación principal: `DOCUMENTACION.md`
- Versión extendida: `DOCUMENTACION_COMPLETA.md`
- Backend: `backend/README.md`
- Frontend: `frontend/README.md`

## Contribuir

Las contribuciones son bienvenidas. Revisa:

- `CONTRIBUTING.md`
- `CODE_OF_CONDUCT.md`
- `SECURITY.md`

## Licencia

Este proyecto está bajo la licencia MIT. Ver `LICENSE`.
