"""应用配置。"""

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """从环境变量加载 HermesGuard 服务配置。"""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="HERMESGUARD_",
        extra="ignore",
    )

    app_name: str = "HermesGuard API"
    environment: str = "development"
    api_host: str = "0.0.0.0"
    api_port: int = 8001
    cors_origins: str = "http://localhost:5173,http://localhost:8080"

    mysql_host: str = "127.0.0.1"
    mysql_port: int = 3307
    mysql_database: str = "hermesguard"
    mysql_user: str = "hermesguard"
    mysql_password: str = "hermesguard"

    redis_host: str = "127.0.0.1"
    redis_port: int = 6380
    redis_database: int = 0

    @property
    def database_url(self) -> str:
        """生成 SQLAlchemy 异步数据库连接地址。"""
        return (
            f"mysql+aiomysql://{self.mysql_user}:{self.mysql_password}"
            f"@{self.mysql_host}:{self.mysql_port}/{self.mysql_database}?charset=utf8mb4"
        )

    @property
    def redis_url(self) -> str:
        """生成 Redis 连接地址。"""
        return f"redis://{self.redis_host}:{self.redis_port}/{self.redis_database}"

    @property
    def cors_origin_list(self) -> list[str]:
        """将逗号分隔的跨域来源转换成列表。"""
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]


@lru_cache
def get_settings() -> Settings:
    """返回进程内复用的配置实例。"""
    return Settings()
