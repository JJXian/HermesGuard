from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.testclient import TestClient
from hermesguard_server.app import create_app
from hermesguard_server.config import Settings


def build_test_app() -> FastAPI:
    settings = Settings(environment="test")
    app = create_app(settings)

    @asynccontextmanager
    async def empty_lifespan(_: FastAPI) -> AsyncIterator[None]:
        yield

    app.router.lifespan_context = empty_lifespan
    return app


def test_live_health_check() -> None:
    app = build_test_app()

    with TestClient(app) as client:
        response = client.get("/health/live")

    assert response.status_code == 200
    assert response.json() == {"status": "ok", "service": "hermesguard-server"}


def test_ready_when_dependencies_are_available() -> None:
    app = build_test_app()

    async def available(_: FastAPI) -> dict[str, str]:
        return {"mysql": "up", "redis": "up"}

    app.state.readiness_probe = available
    with TestClient(app) as client:
        response = client.get("/health/ready")

    assert response.status_code == 200
    assert response.json() == {
        "status": "ready",
        "dependencies": {"mysql": "up", "redis": "up"},
    }


def test_ready_when_a_dependency_is_unavailable() -> None:
    app = build_test_app()

    async def unavailable(_: FastAPI) -> dict[str, str]:
        return {"mysql": "up", "redis": "down"}

    app.state.readiness_probe = unavailable
    with TestClient(app) as client:
        response = client.get("/health/ready")

    assert response.status_code == 503
    assert response.json()["status"] == "not_ready"
