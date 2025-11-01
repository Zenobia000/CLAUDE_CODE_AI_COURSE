"""
單元測試 - API 端點測試
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_read_root():
    """測試根路由"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert data["version"] == "1.0.0"


def test_health_check():
    """測試健康檢查端點"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "version" in data
    assert "checks" in data


def test_list_items():
    """測試列出所有項目"""
    response = client.get("/api/items")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0


def test_get_item():
    """測試獲取單個項目"""
    response = client.get("/api/items/1")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert "name" in data
    assert "price" in data


def test_get_item_not_found():
    """測試獲取不存在的項目"""
    response = client.get("/api/items/999")
    assert response.status_code == 404


def test_create_item():
    """測試創建項目"""
    new_item = {
        "name": "Test Item",
        "description": "Test Description",
        "price": 99.99
    }
    response = client.post("/api/items", json=new_item)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == new_item["name"]
    assert data["price"] == new_item["price"]


def test_create_item_invalid():
    """測試創建無效項目"""
    invalid_item = {
        "name": "",  # 無效：名稱不能為空
        "price": -10  # 無效：價格必須為正數
    }
    response = client.post("/api/items", json=invalid_item)
    assert response.status_code == 422  # Validation error


def test_update_item():
    """測試更新項目"""
    update_data = {
        "name": "Updated Item",
        "price": 50.00
    }
    response = client.put("/api/items/1", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == update_data["name"]


def test_delete_item():
    """測試刪除項目"""
    response = client.delete("/api/items/1")
    assert response.status_code == 204
