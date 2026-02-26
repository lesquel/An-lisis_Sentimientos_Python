# Backend - Sentimind

Backend REST API construido con Django y Django REST Framework.

## Stack

- Python 3.13+
- Django + DRF
- JWT con `djangorestframework-simplejwt`
- Motor de clasificación en `core/application/ai_service.py`

## Ejecutar local (sin Docker)

```bash
uv sync
uv run python manage.py migrate
uv run python manage.py runserver
```

## Ejecutar tests

```bash
uv run python manage.py test
```

## Evaluación del modelo

```bash
uv run python evaluate_model.py
```

## Variables de entorno

Basarse en:

- `.env.example`

Variables típicas:

- `DEBUG`
- `SECRET_KEY`
- `ALLOWED_HOSTS`

## API principal

- Auth: `/api/auth/*`
- Posts: `/api/posts/`

