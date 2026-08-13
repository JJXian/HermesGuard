.PHONY: setup check test lint typecheck web-build api worker beat web infra-up infra-down up down

setup:
	uv sync --all-packages
	npm --prefix apps/web install

test:
	.venv/bin/pytest -q

lint:
	.venv/bin/ruff check .
	npm --prefix apps/web run lint

typecheck:
	.venv/bin/mypy
	npm --prefix apps/web run typecheck

web-build:
	npm --prefix apps/web run build

check: test lint typecheck web-build

api:
	uv run --package hermesguard-server uvicorn hermesguard_server.main:app --port 8001 --reload

worker:
	uv run --package hermesguard-server celery -A hermesguard_server.celery_app:celery_app worker --loglevel=INFO

beat:
	uv run --package hermesguard-server celery -A hermesguard_server.celery_app:celery_app beat --loglevel=INFO

web:
	npm --prefix apps/web run dev

infra-up:
	docker compose -f deploy/docker-compose.yml up -d mysql redis

infra-down:
	docker compose -f deploy/docker-compose.yml down

up:
	docker compose -f deploy/docker-compose.yml up -d --build

down:
	docker compose -f deploy/docker-compose.yml down
