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

## Control multiplataforma (Windows y Linux)

También puedes usar un controlador único en Python para ejecutar todo junto o por servicio.

### Linux / macOS

```bash
python3 scripts/ctl.py setup

# Docker (todo junto o independiente)
python3 scripts/ctl.py up --runtime docker --mode dev --target all
python3 scripts/ctl.py up --runtime docker --mode dev --target backend
python3 scripts/ctl.py up --runtime docker --mode dev --target frontend
python3 scripts/ctl.py down --runtime docker --mode dev --target all

# Local (todo junto o independiente)
python3 scripts/ctl.py up --runtime local --target all
python3 scripts/ctl.py up --runtime local --target backend
python3 scripts/ctl.py up --runtime local --target frontend

# Base de datos
python3 scripts/ctl.py db --runtime docker --action migrate
python3 scripts/ctl.py db --runtime local --action migrate
```

### Windows (PowerShell / CMD)

```powershell
py scripts/ctl.py setup

# Docker
py scripts/ctl.py up --runtime docker --mode dev --target all
py scripts/ctl.py up --runtime docker --mode dev --target backend
py scripts/ctl.py up --runtime docker --mode dev --target frontend
py scripts/ctl.py down --runtime docker --mode dev --target all

# Local
py scripts/ctl.py up --runtime local --target all
py scripts/ctl.py up --runtime local --target backend
py scripts/ctl.py up --runtime local --target frontend

# Base de datos
py scripts/ctl.py db --runtime docker --action migrate
py scripts/ctl.py db --runtime local --action migrate
```

## Estructura

```text
./
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
