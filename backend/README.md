# CanadaBuys Tender Backend

Phase-0 FastAPI vertical slice for pasted tender evidence, durable analysis, deterministic
eligibility gating, human corrections, and immutable audit events.

## Commands

```bash
python3.12 -m venv .venv
.venv/bin/pip install -e '.[dev]'
.venv/bin/alembic upgrade head
.venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000
.venv/bin/python -m app.worker
```

The API and worker are separate processes. Production uses PostgreSQL and Temporal. Tests use
SQLite and a deterministic analyzer/dispatcher; they never call a model provider. Configuration
is read from process environment variables prefixed with `TENDER_`; no env file is loaded by the
application. Conventional deployment names such as `DATABASE_URL`, `TEMPORAL_ADDRESS`,
`OPENAI_MODEL`, and `OPENAI_REASONING_EFFORT` are also accepted through explicit aliases.

Important variables are `TENDER_DATABASE_URL`, `TENDER_TEMPORAL_ADDRESS`,
`TENDER_TEMPORAL_NAMESPACE`, and `TENDER_TEMPORAL_TASK_QUEUE`. The OpenAI SDK reads its own
credential from the process environment at worker runtime; never put credentials in prompts,
workflow payload metadata, source control, or logs.

Container commands:

```bash
docker run IMAGE uvicorn app.main:app --host 0.0.0.0 --port 8000
docker run IMAGE python -m app.worker
docker run IMAGE alembic upgrade head
```
