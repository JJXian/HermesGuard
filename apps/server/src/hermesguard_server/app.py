"""FastAPI 应用工厂。"""

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from redis.asyncio import Redis

from hermesguard_server.config import Settings, get_settings
from hermesguard_server.database import (
    create_engine,
    create_session_factory,
)
from hermesguard_server.health import probe_dependencies
from hermesguard_server.health import router as health_router


def create_app(settings: Settings | None = None) -> FastAPI:
    """创建并配置 HermesGuard API 应用。"""
    app_settings = settings or get_settings()

    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncIterator[None]:
        app.state.db_engine = create_engine(app_settings)
        app.state.db_session_factory = create_session_factory(
            app.state.db_engine,
        )
        app.state.redis = Redis.from_url(app_settings.redis_url, decode_responses=True)
        try:
            yield
        finally:
            await app.state.redis.aclose()
            await app.state.db_engine.dispose()

    app = FastAPI(
        title=app_settings.app_name,
        version="0.1.0",
        lifespan=lifespan,
    )
    app.state.settings = app_settings
    app.state.readiness_probe = probe_dependencies
    app.add_middleware(
        CORSMiddleware,
        allow_origins=app_settings.cors_origin_list,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(health_router)
    return app
