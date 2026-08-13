"""服务存活与依赖就绪检查。"""

from typing import Any

from fastapi import APIRouter, Request, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from redis.asyncio import Redis
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncEngine

router = APIRouter(prefix="/health", tags=["健康检查"])


class LiveResponse(BaseModel):
    """存活检查响应。"""

    status: str
    service: str


async def probe_dependencies(app: Any) -> dict[str, str]:
    """探测 MySQL 和 Redis 是否可以响应最小查询。"""
    dependencies: dict[str, str] = {}
    engine: AsyncEngine = app.state.db_engine
    redis: Redis = app.state.redis

    try:
        async with engine.connect() as connection:
            await connection.execute(text("SELECT 1"))
        dependencies["mysql"] = "up"
    except Exception:  # noqa: BLE001 - 健康检查必须收敛所有驱动层异常
        dependencies["mysql"] = "down"

    try:
        await redis.ping()
        dependencies["redis"] = "up"
    except Exception:  # noqa: BLE001 - 健康检查必须收敛所有驱动层异常
        dependencies["redis"] = "down"

    return dependencies


@router.get("/live", response_model=LiveResponse)
async def live() -> LiveResponse:
    """确认 API 进程可以响应请求。"""
    return LiveResponse(status="ok", service="hermesguard-server")


@router.get("/ready")
async def ready(request: Request) -> JSONResponse:
    """确认 API 依赖的 MySQL 与 Redis 均已就绪。"""
    dependencies = await request.app.state.readiness_probe(request.app)
    is_ready = all(value == "up" for value in dependencies.values())
    return JSONResponse(
        status_code=status.HTTP_200_OK if is_ready else status.HTTP_503_SERVICE_UNAVAILABLE,
        content={"status": "ready" if is_ready else "not_ready", "dependencies": dependencies},
    )
