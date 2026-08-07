from collections.abc import AsyncIterator

import pytest_asyncio
from httpx import ASGITransport, AsyncClient

from app.core.config import Settings
from app.db.session import Database
from app.main import create_app
from app.services.dispatcher import FakeAnalysisDispatcher


@pytest_asyncio.fixture
async def database() -> AsyncIterator[Database]:
    database = Database("sqlite+aiosqlite:///:memory:")
    await database.create_schema_for_tests()
    yield database
    await database.dispose()


@pytest_asyncio.fixture
async def client(database: Database) -> AsyncIterator[AsyncClient]:
    settings = Settings(
        database_url="sqlite+aiosqlite:///:memory:",
        environment="test",
        dispatch_mode="fake",
    )
    dispatcher = FakeAnalysisDispatcher(database)
    app = create_app(settings=settings, database=database, dispatcher=dispatcher)
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        yield client
    await dispatcher.close()
