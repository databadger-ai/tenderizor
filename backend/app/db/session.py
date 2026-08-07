from collections.abc import AsyncIterator

from sqlalchemy import text
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.pool import StaticPool

from app.db.base import Base


class Database:
    def __init__(self, url: str) -> None:
        engine_kwargs: dict[str, object] = {"pool_pre_ping": True}
        if url == "sqlite+aiosqlite:///:memory:":
            engine_kwargs.update(
                {"poolclass": StaticPool, "connect_args": {"check_same_thread": False}}
            )
        self.engine: AsyncEngine = create_async_engine(url, **engine_kwargs)
        self.session_factory = async_sessionmaker(self.engine, expire_on_commit=False)

    async def session(self) -> AsyncIterator[AsyncSession]:
        async with self.session_factory() as session:
            yield session

    async def check(self) -> None:
        async with self.engine.connect() as connection:
            await connection.execute(text("SELECT 1"))

    async def create_schema_for_tests(self) -> None:
        async with self.engine.begin() as connection:
            await connection.run_sync(Base.metadata.create_all)

    async def dispose(self) -> None:
        await self.engine.dispose()
