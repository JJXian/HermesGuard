"""SQLAlchemy 异步数据库基础设施。"""

from collections.abc import AsyncIterator

from fastapi import Request
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from hermesguard_server.config import Settings


def create_engine(settings: Settings) -> AsyncEngine:
    """根据应用配置创建异步数据库连接池。"""
    return create_async_engine(
        settings.database_url,
        pool_pre_ping=True,
    )


def create_session_factory(
    engine: AsyncEngine,
) -> async_sessionmaker[AsyncSession]:
    """创建绑定到指定 Engine 的异步 Session 工厂。"""
    return async_sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False,
        autoflush=False,
    )


async def get_db_session(request: Request) -> AsyncIterator[AsyncSession]:
    """为一次 HTTP 请求提供独立的数据库 Session。"""
    session_factory: async_sessionmaker[AsyncSession]
    session_factory = request.app.state.db_session_factory

    async with session_factory() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise