"""
Pydantic 資料模型
"""
from pydantic import BaseModel, Field
from typing import Optional


class ItemBase(BaseModel):
    """Item 基礎模型"""
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    price: float = Field(..., gt=0)


class ItemCreate(ItemBase):
    """創建 Item 的請求模型"""
    pass


class ItemUpdate(BaseModel):
    """更新 Item 的請求模型"""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    price: Optional[float] = Field(None, gt=0)


class Item(ItemBase):
    """Item 完整模型（包含 ID）"""
    id: int

    class Config:
        from_attributes = True


class HealthCheck(BaseModel):
    """健康檢查回應模型"""
    status: str
    version: str
    environment: str
    checks: dict
