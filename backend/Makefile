.PHONY: install lint typecheck test check migrate run-api run-worker

install:
	python3.12 -m pip install -e '.[dev]'

lint:
	ruff check app tests migrations

typecheck:
	mypy app

test:
	pytest -q

check: lint typecheck test

migrate:
	alembic upgrade head

run-api:
	uvicorn app.main:app --host 0.0.0.0 --port 8000

run-worker:
	python -m app.worker
