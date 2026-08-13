"""Celery Worker 与 Beat 进程入口。"""

from celery import Celery

from hermesguard_server.config import get_settings

settings = get_settings()

celery_app = Celery(
    "hermesguard",
    broker=settings.redis_url,
    backend=settings.redis_url,
)
celery_app.conf.update(
    broker_connection_retry_on_startup=True,
    enable_utc=True,
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="Asia/Shanghai",
)
