"""API 进程入口。"""

import uvicorn

from hermesguard_server.app import create_app
from hermesguard_server.config import get_settings

app = create_app()


def run() -> None:
    """使用 Uvicorn 启动 API。"""
    settings = get_settings()
    uvicorn.run(
        "hermesguard_server.main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=settings.environment == "development",
    )
