# 階段 2: 後端開發 (TDD 方法)
# Backend Development with Test-Driven Development

**預計時間**: 1.5 小時
**難度**: ★★★☆☆ (中等)
**前置要求**: 完成階段 1 (專案初始化)
**核心技能**: TDD 開發、API 設計、資料庫建模、JWT 身份驗證

---

## 📋 階段目標

完成這個階段後，你將擁有：

✅ **完整的資料庫模型** - User 和 Task 兩個 SQLAlchemy 模型
✅ **8 個 RESTful API endpoints** - 全部通過測試
✅ **JWT 身份驗證系統** - 註冊、登入、token 驗證
✅ **80%+ 測試覆蓋率** - 使用 pytest 編寫的完整測試
✅ **輸入驗證與錯誤處理** - Pydantic schemas 自動驗證
✅ **API 自動文檔** - Swagger UI 可互動測試

**成功標準**:
- 所有測試通過 (`pytest` 全部綠燈)
- 測試覆蓋率 ≥ 80% (`pytest --cov`)
- 可透過 Swagger UI 測試所有 endpoints
- 無安全漏洞 (密碼已加密、SQL 注入防護)

---

## 🎯 為什麼使用 TDD？

### 類比：建築師的藍圖

傳統開發像是「邊蓋房子邊畫藍圖」：
- ❌ 蓋完才發現尺寸不對
- ❌ 需要大量返工
- ❌ 品質難以保證

TDD 像是「先畫藍圖再蓋房子」：
- ✅ 先定義「房子應該長什麼樣」(測試)
- ✅ 再實作「如何蓋出這樣的房子」(代碼)
- ✅ 自動檢查「是否符合藍圖」(測試執行)

### TDD 的三個步驟 (Red-Green-Refactor)

```
1. 🔴 Red   - 寫一個失敗的測試 (定義需求)
2. 🟢 Green - 寫最簡單的代碼讓測試通過 (實作功能)
3. 🔵 Refactor - 重構代碼提升質量 (優化)
```

**本階段會嚴格遵守這個流程**，你會親身體驗 TDD 的威力。

---

## 📐 API 設計概覽

我們將開發以下 8 個 API endpoints：

### 身份驗證相關 (3 個)
```http
POST   /api/auth/register      # 用戶註冊
POST   /api/auth/login         # 用戶登入
GET    /api/auth/me            # 獲取當前用戶資訊
```

### 任務管理相關 (5 個)
```http
POST   /api/tasks              # 創建任務
GET    /api/tasks              # 獲取任務列表 (支援過濾)
GET    /api/tasks/{task_id}    # 獲取單個任務
PUT    /api/tasks/{task_id}    # 更新任務
DELETE /api/tasks/{task_id}    # 刪除任務
```

---

## 🗄️ 資料庫設計

### Schema 設計

我們將創建兩個資料表：

**users 表** (用戶資訊)
```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    username VARCHAR(100) NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**tasks 表** (任務資訊)
```sql
CREATE TABLE tasks (
    id SERIAL PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    status VARCHAR(20) DEFAULT 'TODO',  -- TODO, IN_PROGRESS, DONE
    priority VARCHAR(20) DEFAULT 'MEDIUM',  -- LOW, MEDIUM, HIGH, URGENT
    due_date TIMESTAMP,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**關聯關係**: 一個用戶 (User) 可以有多個任務 (Task) - **一對多關係**

---

## 🛠️ 完整操作步驟

### Step 2.1: 資料庫連線設定 (10 分鐘)

#### 🎯 目標
設定 SQLAlchemy 與 PostgreSQL 的連線，創建 Database Session 管理。

#### 📌 為什麼先設定資料庫？
- 後續的 models 和 API 都依賴資料庫連線
- 確保環境配置正確（DATABASE_URL）
- 建立資料庫操作的基礎架構

#### 🔧 操作步驟

**Step 2.1.1: 啟動 PostgreSQL (使用 Docker)**

**情境**: 你不想在本機直接安裝 PostgreSQL，使用 Docker 容器更乾淨。

```bash
# 創建 docker-compose.yml
cat > docker-compose.yml <<EOF
version: '3.8'

services:
  postgres:
    image: postgres:15-alpine
    container_name: task_management_db
    environment:
      POSTGRES_USER: taskuser
      POSTGRES_PASSWORD: taskpass
      POSTGRES_DB: task_management
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U taskuser"]
      interval: 10s
      timeout: 5s
      retries: 5

volumes:
  postgres_data:
EOF

# 啟動 PostgreSQL
docker-compose up -d

# 驗證資料庫運行
docker-compose ps
# 預期: task_management_db 狀態為 Up (healthy)

# 測試連線
docker exec -it task_management_db psql -U taskuser -d task_management -c "SELECT version();"
```

**如果不使用 Docker**（直接安裝 PostgreSQL）:
```bash
# Ubuntu/Debian
sudo apt install postgresql postgresql-contrib
sudo systemctl start postgresql

# macOS (Homebrew)
brew install postgresql
brew services start postgresql

# 創建資料庫
createdb task_management
```

**Step 2.1.2: 更新 .env 配置**

```bash
# 編輯 .env 文件
nano .env
```

更新 DATABASE_URL:
```env
# 使用 Docker PostgreSQL
DATABASE_URL=postgresql://taskuser:taskpass@localhost:5432/task_management

# 或使用本地 PostgreSQL (根據你的實際配置)
# DATABASE_URL=postgresql://postgres:postgres@localhost:5432/task_management
```

**Step 2.1.3: 創建 src/database.py**

**🤖 AI 協作提示詞**:
```
為 FastAPI + SQLAlchemy 專案創建資料庫連線配置文件 src/database.py。

需求:
1. 從 src.config 導入 settings 獲取 DATABASE_URL
2. 創建 SQLAlchemy engine (支援連線池)
3. 創建 SessionLocal (資料庫 session 工廠)
4. 創建 Base (declarative_base，用於定義 models)
5. 提供 get_db() 函數作為 FastAPI dependency

技術要求:
- 使用 SQLAlchemy 2.0 語法
- 連線池大小: 5-20
- 自動提交關閉 (autocommit=False)
- 自動刷新關閉 (autoflush=False)
- 使用 async 或 sync (本專案用 sync 簡化)

請給我完整的 src/database.py 代碼。
```

**參考實作**:
```python
# src/database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from src.config import settings

# 創建資料庫引擎
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,  # 連線前檢查可用性
    pool_size=5,  # 連線池大小
    max_overflow=10  # 最大溢出連線數
)

# 創建 Session 工廠
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# 創建 Base class (所有 models 繼承此類)
Base = declarative_base()

# Dependency: 提供資料庫 session
def get_db():
    """
    FastAPI dependency: 提供資料庫 session

    使用方式:
    ```python
    @app.get("/items")
    def read_items(db: Session = Depends(get_db)):
        items = db.query(Item).all()
        return items
    ```
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

**Step 2.1.4: 驗證資料庫連線**

```bash
# 測試連線是否成功
python -c "from src.database import engine; print('Database connected:', engine.url)"

# 預期輸出:
# Database connected: postgresql://taskuser:***@localhost:5432/task_management
```

#### ✅ 檢查點
- [ ] PostgreSQL 資料庫運行中
- [ ] `.env` 的 DATABASE_URL 正確
- [ ] `src/database.py` 已創建
- [ ] 資料庫連線測試成功

---

### Step 2.2: 創建資料庫 Models (15 分鐘)

#### 🎯 目標
使用 SQLAlchemy 定義 User 和 Task 兩個 ORM 模型。

#### 📌 為什麼先寫 Models？
- Models 是資料結構的定義，是整個應用的基礎
- 後續的 API 和測試都依賴這些 models
- 遵循「由內而外」的開發原則（先數據層，再業務層，最後表示層）

#### 🔧 操作步驟

**Step 2.2.1: 創建 User Model**

**🤖 AI 協作提示詞**:
```
創建 SQLAlchemy User 模型 (src/models/user.py)。

需求:
1. 表名: users
2. 欄位:
   - id: 主鍵，自動遞增
   - email: 字串(255)，唯一，不可空
   - username: 字串(100)，不可空
   - hashed_password: 字串(255)，不可空
   - created_at: 時間戳，預設當前時間
3. 關聯:
   - tasks: relationship 到 Task model (一對多)

技術要求:
- 繼承 Base (from src.database import Base)
- 使用 SQLAlchemy 2.0 語法
- email 欄位建立唯一索引
- 提供 __repr__ 方法方便除錯

請給我完整的 src/models/user.py 代碼。
```

**參考實作**:
```python
# src/models/user.py
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from src.database import Base

class User(Base):
    """
    User Model - 用戶資訊表
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    username = Column(String(100), nullable=False)
    hashed_password = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationship: 一個用戶可以有多個任務
    tasks = relationship("Task", back_populates="owner", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<User(id={self.id}, email={self.email})>"
```

**Step 2.2.2: 創建 Task Model**

**🤖 AI 協作提示詞**:
```
創建 SQLAlchemy Task 模型 (src/models/task.py)。

需求:
1. 表名: tasks
2. 欄位:
   - id: 主鍵，自動遞增
   - title: 字串(200)，不可空
   - description: 文本，可空
   - status: 枚舉 (TODO, IN_PROGRESS, DONE)，預設 TODO
   - priority: 枚舉 (LOW, MEDIUM, HIGH, URGENT)，預設 MEDIUM
   - due_date: 日期時間，可空
   - user_id: 外鍵連接 users.id
   - created_at: 時間戳，預設當前時間
   - updated_at: 時間戳，自動更新
3. 關聯:
   - owner: relationship 到 User model (多對一)

技術要求:
- 使用 Python Enum 定義狀態和優先級
- user_id 外鍵設定 ON DELETE CASCADE
- updated_at 自動更新時間戳

請給我完整的 src/models/task.py 代碼。
```

**參考實作**:
```python
# src/models/task.py
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from enum import Enum as PyEnum
from src.database import Base

# 定義枚舉類型
class TaskStatus(str, PyEnum):
    TODO = "TODO"
    IN_PROGRESS = "IN_PROGRESS"
    DONE = "DONE"

class TaskPriority(str, PyEnum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    URGENT = "URGENT"

class Task(Base):
    """
    Task Model - 任務資訊表
    """
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    status = Column(SQLEnum(TaskStatus), default=TaskStatus.TODO, nullable=False)
    priority = Column(SQLEnum(TaskPriority), default=TaskPriority.MEDIUM, nullable=False)
    due_date = Column(DateTime(timezone=True), nullable=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationship: 一個任務屬於一個用戶
    owner = relationship("User", back_populates="tasks")

    def __repr__(self):
        return f"<Task(id={self.id}, title={self.title}, status={self.status})>"
```

**Step 2.2.3: 更新 src/models/__init__.py**

```python
# src/models/__init__.py
from src.models.user import User
from src.models.task import Task, TaskStatus, TaskPriority

__all__ = ["User", "Task", "TaskStatus", "TaskPriority"]
```

**Step 2.2.4: 創建資料表**

```bash
# 創建初始化腳本 create_tables.py
cat > create_tables.py <<'EOF'
from src.database import Base, engine
from src.models import User, Task

# 創建所有資料表
Base.metadata.create_all(bind=engine)
print("✅ Database tables created successfully!")
EOF

# 執行腳本
python create_tables.py

# 驗證資料表是否創建
docker exec -it task_management_db psql -U taskuser -d task_management -c "\dt"

# 預期輸出:
#           List of relations
#  Schema |  Name  | Type  |  Owner
# --------+--------+-------+----------
#  public | tasks  | table | taskuser
#  public | users  | table | taskuser
```

#### ✅ 檢查點
- [ ] `src/models/user.py` 已創建
- [ ] `src/models/task.py` 已創建
- [ ] `src/models/__init__.py` 已更新
- [ ] 資料表成功創建（users 和 tasks）
- [ ] 沒有 SQLAlchemy 錯誤

---

### Step 2.3: 創建 Pydantic Schemas (10 分鐘)

#### 🎯 目標
定義 API 請求/響應的數據結構和驗證規則。

#### 📌 為什麼需要 Schemas？
- **Models vs Schemas**:
  - Models (SQLAlchemy) = 資料庫結構
  - Schemas (Pydantic) = API 接口結構
- **自動驗證**: Pydantic 自動驗證請求數據
- **自動文檔**: FastAPI 根據 schemas 生成 Swagger UI

#### 🔧 操作步驟

**Step 2.3.1: 創建 User Schemas**

```python
# src/schemas/user.py
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional

# 用戶註冊請求
class UserCreate(BaseModel):
    email: EmailStr = Field(..., example="user@example.com")
    username: str = Field(..., min_length=2, max_length=100, example="John Doe")
    password: str = Field(..., min_length=8, example="SecurePass123")

# 用戶登入請求
class UserLogin(BaseModel):
    email: EmailStr
    password: str

# 用戶響應 (不包含密碼)
class UserResponse(BaseModel):
    id: int
    email: str
    username: str
    created_at: datetime

    class Config:
        from_attributes = True  # Pydantic v2 (舊版用 orm_mode = True)

# Token 響應
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
```

**Step 2.3.2: 創建 Task Schemas**

```python
# src/schemas/task.py
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from src.models.task import TaskStatus, TaskPriority

# 任務創建請求
class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200, example="Complete project documentation")
    description: Optional[str] = Field(None, example="Write comprehensive README and API docs")
    status: TaskStatus = TaskStatus.TODO
    priority: TaskPriority = TaskPriority.MEDIUM
    due_date: Optional[datetime] = None

# 任務更新請求 (所有欄位可選)
class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    status: Optional[TaskStatus] = None
    priority: Optional[TaskPriority] = None
    due_date: Optional[datetime] = None

# 任務響應
class TaskResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    status: TaskStatus
    priority: TaskPriority
    due_date: Optional[datetime]
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
```

**Step 2.3.3: 更新 __init__.py**

```python
# src/schemas/__init__.py
from src.schemas.user import UserCreate, UserLogin, UserResponse, Token
from src.schemas.task import TaskCreate, TaskUpdate, TaskResponse

__all__ = [
    "UserCreate",
    "UserLogin",
    "UserResponse",
    "Token",
    "TaskCreate",
    "TaskUpdate",
    "TaskResponse"
]
```

#### ✅ 檢查點
- [ ] `src/schemas/user.py` 已創建
- [ ] `src/schemas/task.py` 已創建
- [ ] 可以成功導入所有 schemas: `python -c "from src.schemas import *"`

---

### Step 2.4: 實作身份驗證工具 (JWT) (15 分鐘)

#### 🎯 目標
實作 JWT token 生成、密碼雜湊、token 驗證等工具函數。

#### 📌 為什麼需要這些工具？
- **安全性**: 密碼不能明文存儲，必須加密
- **無狀態認證**: JWT 允許無狀態的身份驗證
- **統一管理**: 將認證邏輯集中管理，避免重複代碼

#### 🔧 操作步驟

**Step 2.4.1: 創建 src/utils/auth.py**

**🤖 AI 協作提示詞**:
```
創建 FastAPI JWT 身份驗證工具 (src/utils/auth.py)。

需求:
1. 密碼雜湊函數:
   - hash_password(password: str) -> str
   - verify_password(plain_password: str, hashed_password: str) -> bool
   - 使用 passlib + bcrypt

2. JWT token 函數:
   - create_access_token(data: dict) -> str
   - decode_access_token(token: str) -> dict
   - 使用 python-jose
   - 從 settings 讀取 SECRET_KEY 和 ALGORITHM

3. 依賴函數:
   - get_current_user(token: str, db: Session) -> User
   - 作為 FastAPI dependency 使用

技術要求:
- 處理 token 過期異常
- 處理無效 token 異常
- 返回清晰的錯誤訊息

請給我完整的 src/utils/auth.py 代碼。
```

**參考實作**:
```python
# src/utils/auth.py
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from src.config import settings
from src.database import get_db
from src.models.user import User

# 密碼雜湊上下文
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# HTTP Bearer token scheme
security = HTTPBearer()

# ===== 密碼處理函數 =====

def hash_password(password: str) -> str:
    """
    雜湊密碼
    """
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    驗證密碼
    """
    return pwd_context.verify(plain_password, hashed_password)

# ===== JWT Token 函數 =====

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    創建 JWT access token

    Args:
        data: 要編碼的數據 (通常包含 user_id)
        expires_delta: token 有效期 (預設從 settings 讀取)

    Returns:
        JWT token 字符串
    """
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def decode_access_token(token: str) -> dict:
    """
    解碼 JWT token

    Args:
        token: JWT token 字符串

    Returns:
        解碼後的數據

    Raises:
        HTTPException: token 無效或過期
    """
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

# ===== FastAPI 依賴函數 =====

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    """
    獲取當前認證用戶 (FastAPI dependency)

    使用方式:
    ```python
    @app.get("/me")
    def get_me(current_user: User = Depends(get_current_user)):
        return current_user
    ```

    Args:
        credentials: HTTP Bearer token
        db: 資料庫 session

    Returns:
        User 實例

    Raises:
        HTTPException: 認證失敗
    """
    token = credentials.credentials
    payload = decode_access_token(token)

    user_id: int = payload.get("sub")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials"
        )

    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )

    return user
```

**Step 2.4.2: 測試驗證工具**

```bash
# 測試密碼雜湊
python -c "
from src.utils.auth import hash_password, verify_password
hashed = hash_password('test123')
print('Hashed:', hashed)
print('Verify OK:', verify_password('test123', hashed))
print('Verify Fail:', verify_password('wrong', hashed))
"

# 測試 JWT token
python -c "
from src.utils.auth import create_access_token, decode_access_token
token = create_access_token({'sub': 1})
print('Token:', token)
print('Decoded:', decode_access_token(token))
"
```

#### ✅ 檢查點
- [ ] `src/utils/auth.py` 已創建
- [ ] 密碼雜湊測試通過
- [ ] JWT token 生成和解碼測試通過

---

### Step 2.5: 編寫測試用例 - TDD 第一步 (20 分鐘)

#### 🎯 目標
遵循 TDD 原則，**先寫測試**，定義 API 應該如何運作。

#### 📌 TDD 核心理念
```
🔴 Red → 🟢 Green → 🔵 Refactor

1. 先寫失敗的測試 (定義需求)
2. 寫最簡代碼讓測試通過 (實作功能)
3. 重構代碼提升質量 (優化)
```

我們現在在 **🔴 Red 階段** - 寫測試。

#### 🔧 操作步驟

**Step 2.5.1: 創建 Pytest 配置**

```python
# tests/conftest.py
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.main import app
from src.database import Base, get_db

# 使用 SQLite 記憶體資料庫進行測試
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Fixture: 資料庫 session
@pytest.fixture(scope="function")
def db_session():
    """
    為每個測試創建獨立的資料庫 session
    測試結束後清理
    """
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)

# Fixture: FastAPI Test Client
@pytest.fixture(scope="function")
def client(db_session):
    """
    FastAPI 測試客戶端
    """
    def override_get_db():
        try:
            yield db_session
        finally:
            db_session.close()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()
```

**Step 2.5.2: 編寫 Auth API 測試**

```python
# tests/test_auth.py
import pytest
from fastapi.testclient import TestClient

class TestAuth:
    """身份驗證 API 測試"""

    def test_register_success(self, client):
        """測試成功註冊"""
        response = client.post(
            "/api/auth/register",
            json={
                "email": "test@example.com",
                "username": "Test User",
                "password": "SecurePass123"
            }
        )
        assert response.status_code == 201
        data = response.json()
        assert data["email"] == "test@example.com"
        assert data["username"] == "Test User"
        assert "id" in data
        assert "password" not in data  # 不應返回密碼

    def test_register_duplicate_email(self, client):
        """測試重複 email 註冊"""
        # 第一次註冊
        client.post(
            "/api/auth/register",
            json={
                "email": "test@example.com",
                "username": "User 1",
                "password": "Pass123"
            }
        )
        # 第二次用相同 email 註冊
        response = client.post(
            "/api/auth/register",
            json={
                "email": "test@example.com",
                "username": "User 2",
                "password": "Pass456"
            }
        )
        assert response.status_code == 409  # Conflict

    def test_register_invalid_email(self, client):
        """測試無效 email 格式"""
        response = client.post(
            "/api/auth/register",
            json={
                "email": "not-an-email",
                "username": "User",
                "password": "Pass123"
            }
        )
        assert response.status_code == 422  # Validation Error

    def test_login_success(self, client):
        """測試成功登入"""
        # 先註冊
        client.post(
            "/api/auth/register",
            json={
                "email": "test@example.com",
                "username": "Test User",
                "password": "SecurePass123"
            }
        )
        # 登入
        response = client.post(
            "/api/auth/login",
            json={
                "email": "test@example.com",
                "password": "SecurePass123"
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"

    def test_login_wrong_password(self, client):
        """測試錯誤密碼"""
        # 先註冊
        client.post(
            "/api/auth/register",
            json={
                "email": "test@example.com",
                "username": "Test User",
                "password": "CorrectPass"
            }
        )
        # 用錯誤密碼登入
        response = client.post(
            "/api/auth/login",
            json={
                "email": "test@example.com",
                "password": "WrongPass"
            }
        )
        assert response.status_code == 401  # Unauthorized

    def test_get_current_user(self, client):
        """測試獲取當前用戶資訊"""
        # 註冊並登入
        client.post(
            "/api/auth/register",
            json={
                "email": "test@example.com",
                "username": "Test User",
                "password": "Pass123"
            }
        )
        login_response = client.post(
            "/api/auth/login",
            json={"email": "test@example.com", "password": "Pass123"}
        )
        token = login_response.json()["access_token"]

        # 使用 token 獲取用戶資訊
        response = client.get(
            "/api/auth/me",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["email"] == "test@example.com"

    def test_get_current_user_invalid_token(self, client):
        """測試無效 token"""
        response = client.get(
            "/api/auth/me",
            headers={"Authorization": "Bearer invalid-token"}
        )
        assert response.status_code == 401
```

**Step 2.5.3: 編寫 Task API 測試**

```python
# tests/test_tasks.py
import pytest
from datetime import datetime, timedelta

class TestTasks:
    """任務管理 API 測試"""

    @pytest.fixture
    def auth_token(self, client):
        """創建用戶並獲取 token (fixture)"""
        client.post(
            "/api/auth/register",
            json={
                "email": "user@example.com",
                "username": "User",
                "password": "Pass123"
            }
        )
        response = client.post(
            "/api/auth/login",
            json={"email": "user@example.com", "password": "Pass123"}
        )
        return response.json()["access_token"]

    def test_create_task_success(self, client, auth_token):
        """測試成功創建任務"""
        response = client.post(
            "/api/tasks",
            json={
                "title": "Test Task",
                "description": "Task description",
                "priority": "HIGH"
            },
            headers={"Authorization": f"Bearer {auth_token}"}
        )
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "Test Task"
        assert data["status"] == "TODO"
        assert data["priority"] == "HIGH"

    def test_create_task_unauthorized(self, client):
        """測試未認證創建任務"""
        response = client.post(
            "/api/tasks",
            json={"title": "Task"}
        )
        assert response.status_code == 401

    def test_get_tasks_list(self, client, auth_token):
        """測試獲取任務列表"""
        # 創建兩個任務
        for i in range(2):
            client.post(
                "/api/tasks",
                json={"title": f"Task {i}"},
                headers={"Authorization": f"Bearer {auth_token}"}
            )

        # 獲取列表
        response = client.get(
            "/api/tasks",
            headers={"Authorization": f"Bearer {auth_token}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2

    def test_get_single_task(self, client, auth_token):
        """測試獲取單個任務"""
        # 創建任務
        create_response = client.post(
            "/api/tasks",
            json={"title": "Task 1"},
            headers={"Authorization": f"Bearer {auth_token}"}
        )
        task_id = create_response.json()["id"]

        # 獲取任務
        response = client.get(
            f"/api/tasks/{task_id}",
            headers={"Authorization": f"Bearer {auth_token}"}
        )
        assert response.status_code == 200
        assert response.json()["id"] == task_id

    def test_update_task(self, client, auth_token):
        """測試更新任務"""
        # 創建任務
        create_response = client.post(
            "/api/tasks",
            json={"title": "Original"},
            headers={"Authorization": f"Bearer {auth_token}"}
        )
        task_id = create_response.json()["id"]

        # 更新任務
        response = client.put(
            f"/api/tasks/{task_id}",
            json={"title": "Updated", "status": "IN_PROGRESS"},
            headers={"Authorization": f"Bearer {auth_token}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Updated"
        assert data["status"] == "IN_PROGRESS"

    def test_delete_task(self, client, auth_token):
        """測試刪除任務"""
        # 創建任務
        create_response = client.post(
            "/api/tasks",
            json={"title": "To Delete"},
            headers={"Authorization": f"Bearer {auth_token}"}
        )
        task_id = create_response.json()["id"]

        # 刪除任務
        response = client.delete(
            f"/api/tasks/{task_id}",
            headers={"Authorization": f"Bearer {auth_token}"}
        )
        assert response.status_code == 204

        # 驗證已刪除
        get_response = client.get(
            f"/api/tasks/{task_id}",
            headers={"Authorization": f"Bearer {auth_token}"}
        )
        assert get_response.status_code == 404
```

**Step 2.5.4: 運行測試 (應該全部失敗 - 🔴 Red)**

```bash
# 運行測試
pytest tests/ -v

# 預期輸出: 所有測試都 FAILED (因為還沒實作 API)
# 這是正常的！這就是 TDD 的第一步
```

#### ✅ 檢查點
- [ ] `tests/conftest.py` 已創建
- [ ] `tests/test_auth.py` 已創建（6 個測試）
- [ ] `tests/test_tasks.py` 已創建（6 個測試）
- [ ] 運行 `pytest` 顯示所有測試失敗（預期行為）

---

### Step 2.6: 實作 Auth API Endpoints (15 分鐘)

#### 🎯 目標
實作身份驗證相關的 3 個 API endpoints，讓測試通過（🟢 Green）。

#### 🔧 操作步驟

**Step 2.6.1: 創建 Auth Router**

```python
# src/routers/auth.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.database import get_db
from src.models.user import User
from src.schemas.user import UserCreate, UserLogin, UserResponse, Token
from src.utils.auth import hash_password, verify_password, create_access_token, get_current_user

router = APIRouter(prefix="/api/auth", tags=["Authentication"])

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """
    用戶註冊

    - 檢查 email 是否已存在
    - 雜湊密碼
    - 創建用戶
    """
    # 檢查 email 是否已存在
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered"
        )

    # 創建用戶
    hashed_pw = hash_password(user_data.password)
    new_user = User(
        email=user_data.email,
        username=user_data.username,
        hashed_password=hashed_pw
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@router.post("/login", response_model=Token)
def login(credentials: UserLogin, db: Session = Depends(get_db)):
    """
    用戶登入

    - 驗證 email 和密碼
    - 生成 JWT token
    """
    # 查找用戶
    user = db.query(User).filter(User.email == credentials.email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )

    # 驗證密碼
    if not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )

    # 生成 token
    access_token = create_access_token(data={"sub": user.id})

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    """
    獲取當前用戶資訊
    """
    return current_user
```

**Step 2.6.2: 註冊 Auth Router 到 main.py**

```python
# src/main.py (修改)
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.routers import auth  # 新增

app = FastAPI(
    title="Task Management System",
    description="A simple task management API built with FastAPI",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 註冊路由
app.include_router(auth.router)  # 新增

@app.get("/")
async def root():
    return {
        "message": "Welcome to Task Management System API",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.get("/health")
async def health():
    return {"status": "healthy"}
```

**Step 2.6.3: 更新 src/routers/__init__.py**

```python
# src/routers/__init__.py
from src.routers import auth

__all__ = ["auth"]
```

**Step 2.6.4: 運行測試驗證 Auth API**

```bash
# 只運行 auth 測試
pytest tests/test_auth.py -v

# 預期: 所有測試通過 ✅
# PASSED tests/test_auth.py::TestAuth::test_register_success
# PASSED tests/test_auth.py::TestAuth::test_register_duplicate_email
# ... (共 6 個 PASSED)
```

#### ✅ 檢查點
- [ ] `src/routers/auth.py` 已創建
- [ ] Auth router 已註冊到 main.py
- [ ] `pytest tests/test_auth.py` 全部通過

---

### Step 2.7: 實作 Task API Endpoints (20 分鐘)

#### 🎯 目標
實作任務管理相關的 5 個 API endpoints。

#### 🔧 操作步驟

**Step 2.7.1: 創建 Task Router**

```python
# src/routers/tasks.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from src.database import get_db
from src.models.user import User
from src.models.task import Task
from src.schemas.task import TaskCreate, TaskUpdate, TaskResponse
from src.utils.auth import get_current_user

router = APIRouter(prefix="/api/tasks", tags=["Tasks"])

@router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(
    task_data: TaskCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """創建任務"""
    new_task = Task(
        **task_data.dict(),
        user_id=current_user.id
    )
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task

@router.get("/", response_model=List[TaskResponse])
def get_tasks(
    status: str = None,
    priority: str = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    獲取任務列表

    支援過濾:
    - status: TODO, IN_PROGRESS, DONE
    - priority: LOW, MEDIUM, HIGH, URGENT
    """
    query = db.query(Task).filter(Task.user_id == current_user.id)

    if status:
        query = query.filter(Task.status == status)
    if priority:
        query = query.filter(Task.priority == priority)

    tasks = query.all()
    return tasks

@router.get("/{task_id}", response_model=TaskResponse)
def get_task(
    task_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """獲取單個任務"""
    task = db.query(Task).filter(
        Task.id == task_id,
        Task.user_id == current_user.id
    ).first()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    return task

@router.put("/{task_id}", response_model=TaskResponse)
def update_task(
    task_id: int,
    task_update: TaskUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """更新任務"""
    task = db.query(Task).filter(
        Task.id == task_id,
        Task.user_id == current_user.id
    ).first()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    # 更新欄位 (只更新提供的欄位)
    update_data = task_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(task, field, value)

    db.commit()
    db.refresh(task)
    return task

@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    task_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """刪除任務"""
    task = db.query(Task).filter(
        Task.id == task_id,
        Task.user_id == current_user.id
    ).first()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    db.delete(task)
    db.commit()
    return None
```

**Step 2.7.2: 註冊 Task Router**

```python
# src/main.py (修改)
from src.routers import auth, tasks  # 新增 tasks

# 註冊路由
app.include_router(auth.router)
app.include_router(tasks.router)  # 新增
```

```python
# src/routers/__init__.py
from src.routers import auth, tasks

__all__ = ["auth", "tasks"]
```

**Step 2.7.3: 運行所有測試**

```bash
# 運行所有測試
pytest tests/ -v

# 預期: 所有 12 個測試全部通過 ✅
# tests/test_auth.py::TestAuth::test_register_success PASSED
# tests/test_auth.py::TestAuth::test_register_duplicate_email PASSED
# ... (6 個 auth 測試)
# tests/test_tasks.py::TestTasks::test_create_task_success PASSED
# tests/test_tasks.py::TestTasks::test_create_task_unauthorized PASSED
# ... (6 個 task 測試)
```

#### ✅ 檢查點
- [ ] `src/routers/tasks.py` 已創建
- [ ] Task router 已註冊到 main.py
- [ ] `pytest tests/` 全部通過（12/12 tests）

---

### Step 2.8: 測試覆蓋率檢查 (5 分鐘)

#### 🎯 目標
確認測試覆蓋率達到 80% 以上。

#### 🔧 操作步驟

```bash
# 運行測試並生成覆蓋率報告
pytest tests/ --cov=src --cov-report=term-missing --cov-report=html

# 預期輸出範例:
# Name                       Stmts   Miss  Cover   Missing
# --------------------------------------------------------
# src/__init__.py                0      0   100%
# src/config.py                 20      0   100%
# src/database.py               15      0   100%
# src/models/user.py            12      0   100%
# src/models/task.py            15      0   100%
# src/routers/auth.py           45      2    96%   55-56
# src/routers/tasks.py          60      3    95%   88-90
# src/schemas/user.py           18      0   100%
# src/schemas/task.py           20      0   100%
# src/utils/auth.py             40      1    98%   65
# --------------------------------------------------------
# TOTAL                        245     6    98%

# 打開 HTML 報告查看詳細資訊
# htmlcov/index.html
```

**如果覆蓋率低於 80%**:
- 檢查哪些代碼未被測試覆蓋
- 補充測試用例
- 移除無用代碼

#### ✅ 檢查點
- [ ] 測試覆蓋率 ≥ 80%
- [ ] 已生成 HTML 覆蓋率報告

---

## 🎉 階段完成檢查

恭喜！完成後端開發，現在你擁有：

### 功能驗證清單

```bash
# 1. 所有測試通過
pytest tests/ -v
# 預期: 12/12 tests passed

# 2. 測試覆蓋率達標
pytest --cov=src --cov-report=term
# 預期: Coverage ≥ 80%

# 3. API 可正常運行
python -m uvicorn src.main:app --reload &
sleep 3

# 測試註冊
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","username":"Test","password":"Pass12345"}'

# 測試登入
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"Pass12345"}'

# 4. Swagger UI 可用
# 訪問 http://localhost:8000/docs
```

### 成果檢查清單

- [ ] **2 個資料庫模型** - User & Task (SQLAlchemy)
- [ ] **8 個 API endpoints** - 全部實作並測試通過
- [ ] **12 個測試用例** - 100% 通過率
- [ ] **80%+ 測試覆蓋率** - pytest-cov 驗證
- [ ] **JWT 身份驗證** - 註冊、登入、token 驗證
- [ ] **輸入驗證** - Pydantic schemas 自動驗證
- [ ] **錯誤處理** - 適當的 HTTP 狀態碼與錯誤訊息
- [ ] **API 文檔** - Swagger UI 自動生成

### TDD 流程回顧

你剛才完成了完整的 TDD 循環：

1. **🔴 Red** - 先寫測試 (Step 2.5)
2. **🟢 Green** - 實作代碼讓測試通過 (Step 2.6-2.7)
3. **🔵 Refactor** - (可選) 重構代碼提升質量

---

## 🚨 常見問題與除錯

### 問題 1: 測試運行時資料庫錯誤

**錯誤訊息**: `sqlalchemy.exc.OperationalError: no such table: users`

**原因**: 測試資料庫未正確初始化

**解決方案**:
```python
# 檢查 tests/conftest.py 中是否有:
Base.metadata.create_all(bind=engine)

# 確保在 conftest.py 導入了所有 models:
from src.models import User, Task
```

---

### 問題 2: Token 認證失敗

**錯誤訊息**: `401 Unauthorized: Could not validate credentials`

**可能原因**:
1. Token 格式錯誤 (缺少 "Bearer " 前綴)
2. SECRET_KEY 不一致
3. Token 已過期

**除錯步驟**:
```bash
# 1. 檢查 token 格式
# 正確: Authorization: Bearer <token>
# 錯誤: Authorization: <token>

# 2. 驗證 SECRET_KEY
python -c "from src.config import settings; print(settings.SECRET_KEY)"

# 3. 生成新 token 測試
python -c "
from src.utils.auth import create_access_token
token = create_access_token({'sub': 1})
print('Token:', token)
"
```

---

### 問題 3: CORS 錯誤 (前端連接時)

**錯誤訊息**: `Access to XMLHttpRequest blocked by CORS policy`

**解決方案**:
```python
# src/main.py
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # 指定前端域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

### 問題 4: 測試覆蓋率未達標

**當前覆蓋率**: 65% (低於 80%)

**解決步驟**:
```bash
# 1. 查看詳細報告
pytest --cov=src --cov-report=html
# 打開 htmlcov/index.html

# 2. 找出未覆蓋的代碼行

# 3. 補充測試用例
# 例如: 測試邊界情況、錯誤處理分支
```

---

## 📚 延伸學習

### 本階段學到的核心概念

1. **TDD 開發流程** - Red-Green-Refactor
2. **RESTful API 設計** - HTTP 方法與狀態碼
3. **SQLAlchemy ORM** - 資料庫模型與關聯
4. **JWT 身份驗證** - 無狀態認證機制
5. **Pydantic 驗證** - 自動請求驗證
6. **Pytest 測試** - 單元測試與整合測試

### 推薦閱讀

- [FastAPI 官方教程](https://fastapi.tiangolo.com/tutorial/)
- [SQLAlchemy 關聯關係](https://docs.sqlalchemy.org/en/14/orm/relationships.html)
- [JWT 介紹](https://jwt.io/introduction)
- [Pytest 最佳實踐](https://docs.pytest.org/en/latest/goodpractices.html)

---

## 🎯 下一階段預告

完成後端開發後，接下來進入**階段 3: 前端開發**。

你將學習:
- 🎨 **React 快速開發** - 使用 AI 加速 UI 開發
- 🔌 **API 整合** - 前後端連接
- 🎭 **狀態管理** - React Hooks 管理應用狀態
- 🚀 **快速原型** - 使用 Cursor/Copilot 提升效率

**準備工作**:
1. 確保後端 API 全部測試通過
2. 後端服務保持運行 (uvicorn)
3. 理解 RESTful API 的調用方式

**前往**: `分階段實作指南/階段3_前端開發/README.md`

---

**階段 2 完成！你已經具備完整的後端開發能力 🎉**
