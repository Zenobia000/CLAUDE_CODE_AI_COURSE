"""
FastAPI 示範應用 - Full CI/CD Demo

這是一個完整的示範專案，展示如何建立端到端的 CI/CD 管線。
"""
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import List, Optional
import logging

from .config import get_settings, Settings
from .models import Item, ItemCreate, ItemUpdate, HealthCheck
from .database import get_db, SessionLocal

# 設定日誌
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# 創建 FastAPI 應用
app = FastAPI(
    title="Full CI/CD Demo API",
    description="完整的 CI/CD 示範專案",
    version="1.0.0"
)

# CORS 設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生產環境應該限制來源
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """根路由 - 歡迎訊息"""
    settings = get_settings()
    return {
        "message": "Welcome to Full CI/CD Demo API",
        "version": "1.0.0",
        "environment": settings.environment,
        "docs": "/docs"
    }


@app.get("/health", response_model=HealthCheck)
async def health_check():
    """
    健康檢查端點

    檢查項目：
    - 應用程式狀態
    - 資料庫連線（如果已配置）
    - 環境配置
    """
    settings = get_settings()

    checks = {
        "application": "ok",
        "database": "ok",  # 簡化版本，實際應該測試連線
        "environment": settings.environment
    }

    is_healthy = all(v == "ok" for k, v in checks.items() if k != "environment")

    if not is_healthy:
        raise HTTPException(status_code=503, detail={
            "status": "unhealthy",
            "checks": checks
        })

    return {
        "status": "healthy",
        "version": "1.0.0",
        "environment": settings.environment,
        "checks": checks
    }


# Items CRUD API
@app.get("/api/items", response_model=List[Item])
async def list_items(
    skip: int = 0,
    limit: int = 100,
    db: SessionLocal = Depends(get_db)
):
    """列出所有項目"""
    # 簡化版本：使用記憶體存儲
    # 實際專案應該從資料庫讀取
    items = [
        Item(id=1, name="Item 1", description="First item", price=10.50),
        Item(id=2, name="Item 2", description="Second item", price=20.00),
        Item(id=3, name="Item 3", description="Third item", price=15.75),
    ]
    return items[skip : skip + limit]


@app.get("/api/items/{item_id}", response_model=Item)
async def get_item(item_id: int):
    """獲取單個項目"""
    # 簡化版本
    if item_id < 1 or item_id > 3:
        raise HTTPException(status_code=404, detail="Item not found")

    return Item(
        id=item_id,
        name=f"Item {item_id}",
        description=f"Description for item {item_id}",
        price=10.0 * item_id
    )


@app.post("/api/items", response_model=Item, status_code=201)
async def create_item(item: ItemCreate):
    """創建新項目"""
    logger.info(f"Creating new item: {item.name}")

    # 簡化版本：返回創建的項目
    return Item(
        id=999,  # 實際應該由資料庫生成
        name=item.name,
        description=item.description,
        price=item.price
    )


@app.put("/api/items/{item_id}", response_model=Item)
async def update_item(item_id: int, item: ItemUpdate):
    """更新項目"""
    logger.info(f"Updating item {item_id}")

    if item_id < 1 or item_id > 3:
        raise HTTPException(status_code=404, detail="Item not found")

    return Item(
        id=item_id,
        name=item.name or f"Item {item_id}",
        description=item.description or f"Description for item {item_id}",
        price=item.price or 10.0
    )


@app.delete("/api/items/{item_id}", status_code=204)
async def delete_item(item_id: int):
    """刪除項目"""
    logger.info(f"Deleting item {item_id}")

    if item_id < 1 or item_id > 3:
        raise HTTPException(status_code=404, detail="Item not found")

    return None


# 錯誤處理
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """全域錯誤處理"""
    logger.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
