from collections.abc import AsyncIterator
from typing import Annotated, cast

from fastapi import Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.dispatcher import AnalysisDispatcher


async def get_session(request: Request) -> AsyncIterator[AsyncSession]:
    async with request.app.state.database.session_factory() as session:
        yield session


def get_dispatcher(request: Request) -> AnalysisDispatcher:
    return cast(AnalysisDispatcher, request.app.state.dispatcher)


SessionDependency = Annotated[AsyncSession, Depends(get_session)]
DispatcherDependency = Annotated[AnalysisDispatcher, Depends(get_dispatcher)]
