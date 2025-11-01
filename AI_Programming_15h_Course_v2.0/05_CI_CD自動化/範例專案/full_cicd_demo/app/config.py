"""
應用配置管理

使用 pydantic-settings 管理多環境配置
"""
from pydantic_settings import BaseSettings
from functools import lru_cache
from typing import Optional


class Settings(BaseSettings):
    """應用配置"""

    # 環境設定
    environment: str = "development"
    debug: bool = False

    # 應用設定
    app_name: str = "Full CI/CD Demo"
    app_version: str = "1.0.0"
    api_prefix: str = "/api"

    # 資料庫設定
    database_url: str = "sqlite:///./app.db"

    # 安全設定
    secret_key: str = "your-secret-key-change-in-production"
    allowed_hosts: list[str] = ["*"]

    # Redis 設定（可選）
    redis_url: Optional[str] = None

    # 功能開關
    enable_swagger: bool = True
    enable_cors: bool = True

    # 日誌設定
    log_level: str = "INFO"

    class Config:
        env_file = ".env"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    """獲取配置（單例模式）"""
    return Settings()
