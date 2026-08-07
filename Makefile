.PHONY: install format lint typecheck test build up down logs migrate smoke qa

install:
	uv sync --project backend --all-extras
	npm --prefix frontend install

format:
	uv run --project backend ruff format backend

lint:
	uv run --project backend ruff check backend
	npm --prefix frontend run lint

typecheck:
	uv run --project backend mypy backend
	npm --prefix frontend run typecheck

test:
	uv run --project backend pytest backend/tests
	npm --prefix frontend run test

build:
	npm --prefix frontend run build
	docker compose build

up:
	docker compose up -d --build

down:
	docker compose down

logs:
	docker compose logs --tail=200 api worker web

migrate:
	cd backend && uv run alembic upgrade head

smoke:
	curl --fail --silent http://localhost:8000/health/live
	curl --fail --silent http://localhost:8000/health/ready
	curl --fail --silent http://localhost:3100/health

qa: lint typecheck test build
