SHELL := /bin/bash

.PHONY: help dev prod down down-v logs status restart test lint setup health

help:
	@echo "Comandos disponibles:"
	@echo "  make dev      - Levanta backend + frontend en modo desarrollo"
	@echo "  make prod     - Levanta backend + frontend en modo producción"
	@echo "  make down     - Detiene contenedores del modo desarrollo"
	@echo "  make down-v   - Detiene y elimina volúmenes del modo desarrollo"
	@echo "  make logs     - Muestra logs del modo desarrollo"
	@echo "  make status   - Muestra estado de contenedores del modo desarrollo"
	@echo "  make restart  - Reinicia entorno de desarrollo"
	@echo "  make test     - Ejecuta tests backend"
	@echo "  make lint     - Ejecuta lint de frontend"
	@echo "  make setup    - Instala dependencias locales (sin Docker)"
	@echo "  make health   - Verifica health endpoints"

dev:
	@./scripts/dev-up.sh

prod:
	@./scripts/prod-up.sh

down:
	@./scripts/down.sh dev

down-v:
	@./scripts/down.sh dev --volumes

logs:
	@./scripts/logs.sh dev

status:
	@./scripts/status.sh dev

restart: down dev

test:
	@./scripts/test.sh

lint:
	@./scripts/lint.sh

setup:
	@./scripts/setup-local.sh

health:
	@./scripts/health.sh