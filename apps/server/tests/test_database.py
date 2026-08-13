from contextlib import asynccontextmanager
from types import SimpleNamespace
from typing import Any
from unittest.mock import AsyncMock, MagicMock

import pytest
from fastapi.testclient import TestClient
from hermesguard_server.app import create_app
from hermesguard_server.config import Settings
from hermesguard_server.database import (
    create_engine,
    create_session_factory,
    get_db_session,
)
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
)


@pytest.mark.asyncio
async def test_create_session_factory() -> None:
    settings = Settings(environment="test")
    engine = create_engine(settings)

    try:
        session_factory = create_session_factory(engine)

        assert session_factory.kw["bind"] is engine
        assert session_factory.class_ is AsyncSession
        assert session_factory.kw["expire_on_commit"] is False
        assert session_factory.kw["autoflush"] is False
    finally:
        await engine.dispose()


@pytest.mark.asyncio
async def test_get_db_session_yields_async_session() -> None:
    engine = create_engine(Settings(environment="test"))
    session_factory = create_session_factory(engine)

    request = SimpleNamespace(
        app=SimpleNamespace(
            state=SimpleNamespace(
                db_session_factory=session_factory,
            )
        )
    )

    dependency = get_db_session(request)  # type: ignore[arg-type]

    try:
        session = await anext(dependency)
        assert isinstance(session, AsyncSession)
    finally:
        await dependency.aclose()
        await engine.dispose()



@pytest.mark.asyncio
async def test_get_db_session_rolls_back_on_error() -> None:
    session = MagicMock()
    session.rollback = AsyncMock()

    @asynccontextmanager
    async def session_context() -> Any:
        yield session

    session_factory = MagicMock(return_value=session_context())
    request = SimpleNamespace(
        app=SimpleNamespace(
            state=SimpleNamespace(
                db_session_factory=session_factory,
            )
        )
    )

    dependency = get_db_session(request)  # type: ignore[arg-type]

    yielded_session = await anext(dependency)
    assert yielded_session is session

    with pytest.raises(RuntimeError, match="模拟业务异常"):
        await dependency.athrow(RuntimeError("模拟业务异常"))

    session.rollback.assert_awaited_once()


def test_app_lifespan_initializes_database_resources() -> None:
    app = create_app(Settings(environment="test"))

    with TestClient(app):
        assert isinstance(app.state.db_engine, AsyncEngine)
        assert isinstance(
            app.state.db_session_factory,
            async_sessionmaker,
        )