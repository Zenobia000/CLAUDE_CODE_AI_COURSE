"""
資料庫連線管理

簡化版本：使用 SQLite
生產環境應該使用 PostgreSQL
"""
from typing import Generator


class SessionLocal:
    """資料庫 Session（簡化版本）"""
    def __init__(self):
        self.db = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass


def get_db() -> Generator:
    """
    獲取資料庫 Session

    使用方式：
    db = Depends(get_db)
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        pass  # 實際應該關閉連線
