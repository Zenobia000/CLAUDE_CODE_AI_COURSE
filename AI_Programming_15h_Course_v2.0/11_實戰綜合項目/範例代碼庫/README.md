# 範例代碼庫與架構參考
# Code Reference & Architecture Guide

**重要說明**:
- 本文檔**不提供完整代碼**（學員應使用 AI 工具生成）
- 提供**架構設計參考**和**關鍵代碼片段**
- 標註「AI 幫助最大的地方」

---

## 📁 專案結構總覽

```
task-management-system/
├── backend/                        # 後端 (FastAPI)
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                 # ⭐ 應用入口
│   │   ├── config.py               # ⭐ 配置管理
│   │   ├── database.py             # ⭐ 數據庫連接
│   │   │
│   │   ├── models/                 # SQLAlchemy Models
│   │   │   ├── __init__.py
│   │   │   ├── user.py             # 用戶模型
│   │   │   └── task.py             # 任務模型
│   │   │
│   │   ├── schemas/                # Pydantic Schemas
│   │   │   ├── __init__.py
│   │   │   ├── user.py             # 用戶 DTO
│   │   │   ├── task.py             # 任務 DTO
│   │   │   └── dashboard.py        # Dashboard DTO
│   │   │
│   │   ├── routers/                # API Endpoints
│   │   │   ├── __init__.py
│   │   │   ├── auth.py             # 認證相關 API
│   │   │   ├── tasks.py            # 任務 CRUD API
│   │   │   └── dashboard.py        # 統計 API
│   │   │
│   │   ├── services/               # 業務邏輯層
│   │   │   ├── __init__.py
│   │   │   ├── auth_service.py     # 認證邏輯
│   │   │   └── task_service.py     # 任務邏輯
│   │   │
│   │   └── utils/                  # 工具函數
│   │       ├── __init__.py
│   │       ├── security.py         # JWT, 密碼加密
│   │       └── dependencies.py     # FastAPI 依賴
│   │
│   ├── tests/                      # 測試代碼
│   │   ├── __init__.py
│   │   ├── conftest.py             # Pytest 配置
│   │   ├── test_auth.py
│   │   ├── test_tasks.py
│   │   └── test_dashboard.py
│   │
│   ├── alembic/                    # 數據庫遷移
│   │   ├── versions/
│   │   └── env.py
│   │
│   ├── .env                        # 環境變數（不提交）
│   ├── .env.example                # 環境變數範例
│   ├── pyproject.toml              # Poetry 配置
│   ├── pytest.ini                  # Pytest 配置
│   ├── Dockerfile                  # 生產環境鏡像
│   └── README.md
│
├── frontend/                       # 前端 (React) [可選]
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Auth/
│   │   │   ├── Dashboard/
│   │   │   └── Tasks/
│   │   ├── services/
│   │   │   ├── api.js
│   │   │   ├── authService.js
│   │   │   └── taskService.js
│   │   ├── contexts/
│   │   │   └── AuthContext.jsx
│   │   ├── App.jsx
│   │   └── index.jsx
│   ├── package.json
│   └── README.md
│
├── .github/
│   └── workflows/
│       └── ci.yml                  # GitHub Actions CI/CD
│
├── docker-compose.yml              # 本地開發環境
├── docker-compose.prod.yml         # 生產環境
├── .gitignore
└── README.md

總計:
- 後端: ~25 個文件
- 前端: ~15 個文件
- 測試: ~10 個文件
- 配置: ~8 個文件
```

---

## 🎯 關鍵文件架構設計

### 1. app/main.py - 應用入口

**職責**: 創建 FastAPI 應用、註冊路由、配置中間件

**架構設計**:
```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth, tasks, dashboard
from app.config import settings

# 創建應用
app = FastAPI(
    title="Task Management API",
    description="RESTful API for task management",
    version="1.0.0"
)

# CORS 配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS.split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 註冊路由
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(tasks.router, prefix="/api/tasks", tags=["Tasks"])
app.include_router(dashboard.router, prefix="/api/dashboard", tags=["Dashboard"])

# 健康檢查
@app.get("/health")
async def health_check():
    return {"status": "healthy"}
```

**AI 幫助**: 可以讓 AI 一次生成整個框架

---

### 2. app/config.py - 配置管理

**職責**: 統一管理環境變數

**架構設計**:
```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # 數據庫
    DATABASE_URL: str

    # JWT
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRATION_DAYS: int = 7

    # CORS
    CORS_ORIGINS: str = "http://localhost:3000"

    class Config:
        env_file = ".env"

settings = Settings()
```

**最佳實踐**:
- 所有配置從環境變數讀取
- 提供合理的默認值
- 使用 Pydantic 驗證

**AI 幫助**: 給 AI 一份環境變數列表，它會生成完整的 Settings 類

---

### 3. app/database.py - 數據庫連接

**職責**: 設置 SQLAlchemy engine 和 session

**架構設計**:
```python
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from app.config import settings

# 創建 engine
engine = create_engine(settings.DATABASE_URL, echo=False)

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()

# Dependency for FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

**重要**: 使用依賴注入模式，便於測試

---

### 4. models/ - 數據模型層

**職責**: 定義數據庫表結構

**設計原則**:
- 每個模型一個文件
- 只包含數據結構，不包含業務邏輯
- 使用索引優化查詢

**user.py 範例結構**:
```python
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    username = Column(String(100), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 關聯關係
    tasks = relationship("Task", back_populates="creator")

    def __repr__(self):
        return f"<User(id={self.id}, email='{self.email}')>"
```

**task.py 關鍵設計**:
- 使用 Enum 類型定義狀態和優先級
- 軟刪除標記 (is_deleted)
- 索引: created_by, status, priority, due_date

**AI 幫助**: 給 AI PRD 中的數據模型需求，它會生成完整的 SQLAlchemy models

---

### 5. schemas/ - 數據傳輸對象 (DTO)

**職責**: 定義 API 請求和響應的數據格式

**設計原則**:
- 輸入驗證（UserCreate, TaskCreate）
- 輸出過濾（UserResponse 不包含密碼）
- 複用基礎 Schema

**user.py 範例結構**:
```python
from pydantic import BaseModel, EmailStr, validator
from datetime import datetime

class UserBase(BaseModel):
    email: EmailStr
    username: str

class UserCreate(UserBase):
    password: str

    @validator('password')
    def password_strength(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters')
        return v

class UserResponse(UserBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True  # 允許從 ORM 模型創建
```

**AI 幫助**: 讓 AI 生成 Schema 時，明確指定「輸入 Schema」和「輸出 Schema」的區別

---

### 6. routers/ - API 端點層

**職責**: 處理 HTTP 請求、調用 Service 層、返回響應

**設計原則**:
- 薄層：只負責 HTTP 相關邏輯
- 業務邏輯在 Service 層
- 使用依賴注入

**auth.py 範例結構**:
```python
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.user import UserCreate, UserResponse, Token
from app.services import auth_service

router = APIRouter()

@router.post("/register", response_model=UserResponse, status_code=201)
async def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """
    用戶註冊

    - **email**: 必須是有效的 email 格式
    - **password**: 至少 8 字元
    - **username**: 顯示名稱
    """
    try:
        user = await auth_service.register_user(db, user_data)
        return user
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e))
```

**tasks.py 關鍵設計**:
- 所有 endpoints 需要認證（Depends(get_current_user)）
- 權限檢查在 Service 層
- 使用 Query Parameters 過濾和分頁

**AI 幫助**: 一次生成所有 CRUD endpoints，包含完整的文檔字串

---

### 7. services/ - 業務邏輯層

**職責**: 核心業務邏輯、數據庫操作、權限檢查

**設計原則**:
- 厚層：所有業務邏輯在這裡
- 可測試：不依賴 HTTP 框架
- 事務管理

**auth_service.py 關鍵函數**:
```python
from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate
from app.utils.security import get_password_hash

async def register_user(db: Session, user_data: UserCreate) -> User:
    # 1. 檢查 Email 是否存在
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise ValueError("Email already exists")

    # 2. 加密密碼
    hashed_password = get_password_hash(user_data.password)

    # 3. 創建用戶
    user = User(
        email=user_data.email,
        password_hash=hashed_password,
        username=user_data.username
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user
```

**task_service.py 關鍵設計**:
- 權限檢查函數: `check_task_permission(task, user_id, action)`
- 分頁查詢: `get_tasks(db, user_id, filters, page, limit)`
- 軟刪除: `delete_task(db, task_id, user_id)` 設置 is_deleted=True

**AI 幫助**: Service 層最適合讓 AI 生成，因為邏輯清晰、模式化

---

### 8. utils/ - 工具函數

**職責**: 通用工具、安全相關、依賴注入

**security.py 關鍵函數**:
```python
from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta
from app.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(user_id: int) -> str:
    expire = datetime.utcnow() + timedelta(days=settings.JWT_EXPIRATION_DAYS)
    to_encode = {"sub": str(user_id), "exp": expire}
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    return encoded_jwt

def decode_access_token(token: str) -> int:
    payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
    user_id = int(payload.get("sub"))
    return user_id
```

**dependencies.py 關鍵函數**:
```python
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.database import get_db
from app.utils.security import decode_access_token
from app.models.user import User

security = HTTPBearer()

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    token = credentials.credentials
    try:
        user_id = decode_access_token(token)
    except:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    return user
```

**AI 幫助**: 安全相關代碼最適合讓 AI 生成，因為有標準模式

---

### 9. tests/ - 測試層

**職責**: 單元測試、整合測試

**conftest.py 關鍵配置**:
```python
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from app.main import app
from app.database import Base, get_db

# 測試數據庫 (in-memory SQLite)
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def test_db():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def client(test_db):
    def override_get_db():
        try:
            yield test_db
        finally:
            test_db.close()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
```

**test_auth.py 測試結構**:
```python
def test_register_success(client):
    response = client.post("/api/auth/register", json={
        "email": "test@example.com",
        "password": "SecurePass123",
        "username": "Test User"
    })
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "test@example.com"
    assert "password" not in data  # 確保不返回密碼

def test_register_duplicate_email(client):
    # 先註冊一次
    client.post("/api/auth/register", json={...})

    # 再次註冊相同 Email
    response = client.post("/api/auth/register", json={...})
    assert response.status_code == 409
```

**AI 幫助**: 給 AI 完整的 API spec，它會生成所有測試案例

---

## 🏗️ 架構設計模式總結

### 分層架構

```
HTTP Request
     ↓
[Router Layer]        # 薄層：HTTP 處理
     ↓
[Service Layer]       # 厚層：業務邏輯
     ↓
[Model Layer]         # 數據層：ORM
     ↓
Database
```

### 依賴流向

```
main.py
  ↓
routers/  ← schemas/
  ↓
services/ ← models/ ← database.py
  ↓
utils/
```

### 關鍵設計決策

| 問題 | 決策 | 理由 |
|-----|------|------|
| 業務邏輯放哪？ | Service Layer | 可測試、可複用 |
| 權限檢查放哪？ | Service Layer | 集中管理、避免遺漏 |
| 密碼何時加密？ | Service Layer | 保存前加密 |
| 刪除用硬刪還是軟刪？ | 軟刪除 (is_deleted) | 可恢復、審計 |
| 測試數據庫用什麼？ | SQLite in-memory | 快速、隔離 |
| API 錯誤碼如何選？ | RESTful 標準 | 語義明確 |

---

## 🤖 AI 協作最佳實踐

### 讓 AI 一次性生成的部分

1. **Models**: 給 AI 數據模型需求，生成完整的 SQLAlchemy models
2. **Schemas**: 給 AI API 規格，生成完整的 Pydantic schemas
3. **Security Utils**: 標準模式，AI 生成最快
4. **測試框架**: conftest.py 和基礎測試案例

### 需要人工審查的部分

1. **Service Layer**: 業務邏輯需要仔細驗證
2. **權限檢查**: 安全關鍵，不能有漏洞
3. **錯誤處理**: 確保錯誤訊息不洩漏敏感資訊

### 逐步迭代的部分

1. **API Endpoints**: 先生成一個，測試通過後再生成下一個
2. **測試案例**: 先生成成功案例，再補充失敗案例

---

## 📝 代碼質量檢查清單

### 提交代碼前檢查

- [ ] 所有測試通過 (`pytest -v`)
- [ ] 覆蓋率 ≥ 80% (`pytest --cov=app`)
- [ ] Linting 通過 (`flake8 app/`)
- [ ] 格式化 (`black app/ tests/`)
- [ ] 安全掃描通過 (`bandit -r app/`)
- [ ] API 文檔完整 (訪問 `/docs`)
- [ ] 環境變數示例正確 (`.env.example`)

---

## 🎓 學習資源

### 官方文檔
- **FastAPI**: https://fastapi.tiangolo.com/
- **SQLAlchemy**: https://docs.sqlalchemy.org/
- **Pydantic**: https://docs.pydantic.dev/
- **Pytest**: https://docs.pytest.org/

### 推薦閱讀
- Clean Architecture (Robert C. Martin)
- Domain-Driven Design (Eric Evans)
- RESTful API 設計最佳實踐

---

**記住**:

完整的代碼應該由**你和 AI 一起生成**，而不是直接複製範例。

這個文檔的目的是：
1. 提供架構設計參考
2. 標註關鍵設計決策
3. 指出 AI 幫助最大的地方

**真正的學習發生在「你向 AI 提問 → AI 生成代碼 → 你理解並驗證」的過程中**。

開始你的編碼之旅吧！ 🚀
