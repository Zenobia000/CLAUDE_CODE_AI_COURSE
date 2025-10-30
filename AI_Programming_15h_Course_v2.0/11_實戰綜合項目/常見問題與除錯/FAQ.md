# 常見問題與除錯指南
# Frequently Asked Questions & Troubleshooting

**問題數量**: 20+ 個常見問題
**覆蓋範圍**: 專案初始化到部署的各個階段
**使用方法**: 遇到問題時，先來這裡查找解決方案

---

## 問題分類

### 🏗️ 專案初始化問題 (6 個)
### 💻 後端開發問題 (8 個)
### 🎨 前端開發問題 (4 個)
### 🚀 CI/CD 與部署問題 (4 個)

---

## 🏗️ 專案初始化問題

### Q1: Poetry install 很慢或失敗

**症狀**:
```bash
poetry install
# 卡住很久或報錯 "Solving dependencies..."
```

**原因**:
- 網路問題（國外源下載慢）
- 依賴版本衝突
- 快取損壞

**解決方案**:

**方案 1: 使用國內鏡像**
```bash
# 設置 PyPI 鏡像
poetry config repositories.pypi https://pypi.tuna.tsinghua.edu.cn/simple

# 或使用阿里雲鏡像
poetry config repositories.pypi https://mirrors.aliyun.com/pypi/simple/
```

**方案 2: 清除快取**
```bash
poetry cache clear pypi --all
poetry install
```

**方案 3: 增加 timeout**
```bash
poetry config installer.max-workers 10
poetry install --no-cache
```

**方案 4: 降級 Poetry 版本（如果是 Poetry 本身的 bug）**
```bash
pip install --upgrade poetry==1.6.1
```

---

### Q2: Docker Compose 啟動失敗 (端口被佔用)

**症狀**:
```bash
docker-compose up -d postgres
# ERROR: for postgres  Cannot start service postgres:
# Bind for 0.0.0.0:5432 failed: port is already allocated
```

**原因**:
本地已經運行了 PostgreSQL 或其他服務佔用 5432 端口

**解決方案**:

**方案 1: 停止本地 PostgreSQL**
```bash
# macOS
brew services stop postgresql

# Ubuntu
sudo systemctl stop postgresql

# Windows (以管理員運行)
net stop postgresql-x64-14
```

**方案 2: 修改 Docker Compose 端口**
```yaml
# docker-compose.yml
services:
  postgres:
    ports:
      - "5433:5432"  # 改用 5433
```

然後修改 `.env`:
```env
DATABASE_URL=postgresql://taskuser:taskpass@localhost:5433/taskdb
```

**方案 3: 查看並殺死佔用端口的進程**
```bash
# macOS/Linux
lsof -i :5432
kill -9 <PID>

# Windows
netstat -ano | findstr :5432
taskkill /PID <PID> /F
```

---

### Q3: 數據庫連接失敗

**症狀**:
```bash
uvicorn app.main:app --reload
# sqlalchemy.exc.OperationalError: (psycopg2.OperationalError)
# could not connect to server: Connection refused
```

**原因**:
- PostgreSQL 容器未啟動
- DATABASE_URL 配置錯誤
- 數據庫未創建

**解決方案**:

**Step 1: 檢查容器狀態**
```bash
docker-compose ps
# 確認 postgres 顯示 "Up"
```

**Step 2: 檢查 DATABASE_URL**
```bash
cat backend/.env
# 確認格式: postgresql://user:pass@host:port/dbname
```

**Step 3: 測試連接**
```bash
# 進入容器
docker exec -it taskdb psql -U taskuser -d taskdb

# 如果能進入，說明數據庫正常
# 輸入 \q 退出
```

**Step 4: 重建數據庫**
```bash
docker-compose down -v  # -v 刪除 volumes
docker-compose up -d postgres
```

---

### Q4: Alembic 遷移失敗

**症狀**:
```bash
alembic upgrade head
# FAILED: Can't locate revision identified by 'xxxxx'
```

**原因**:
- 遷移歷史混亂
- 數據庫與遷移腳本不同步

**解決方案**:

**方案 1: 重置遷移（開發階段可用）**
```bash
# 1. 刪除遷移文件（保留 versions/ 目錄）
rm -rf alembic/versions/*.py

# 2. 刪除數據庫
docker-compose down -v
docker-compose up -d postgres

# 3. 重新生成遷移
alembic revision --autogenerate -m "initial migration"
alembic upgrade head
```

**方案 2: 手動同步（生產環境）**
```bash
# 查看當前版本
alembic current

# 查看所有版本
alembic history

# 回退到特定版本
alembic downgrade <revision>

# 再升級
alembic upgrade head
```

---

### Q5: Git 提交時報錯 (pre-commit hooks)

**症狀**:
```bash
git commit -m "..."
# pre-commit hook failed: black reformatted files
```

**原因**:
代碼格式不符合 Black 標準

**解決方案**:

**方案 1: 自動格式化後重新提交**
```bash
# Black 會自動格式化文件
black app/ tests/

# 重新 add 格式化後的文件
git add app/ tests/

# 再次提交
git commit -m "..."
```

**方案 2: 跳過 pre-commit hooks（不推薦）**
```bash
git commit -m "..." --no-verify
```

**方案 3: 設置 IDE 自動格式化**
- VSCode: 安裝 Black extension，設置 "Format On Save"
- PyCharm: Settings → Tools → Black → 勾選 "On save"

---

### Q6: Python 版本不符合要求

**症狀**:
```bash
poetry install
# The current project's Python requirement (>=3.10) is not compatible
# with your Python version (3.9.x)
```

**原因**:
系統 Python 版本太舊

**解決方案**:

**方案 1: 使用 pyenv 安裝正確版本**
```bash
# 安裝 pyenv (如果沒有)
curl https://pyenv.run | bash

# 安裝 Python 3.10
pyenv install 3.10.12

# 設置本地版本
cd task-management-system/backend
pyenv local 3.10.12

# 驗證
python --version  # 應該顯示 3.10.12

# 重新安裝依賴
poetry env use python3.10
poetry install
```

**方案 2: 修改 pyproject.toml (不推薦)**
```toml
[tool.poetry.dependencies]
python = "^3.9"  # 降低要求
```

---

## 💻 後端開發問題

### Q7: FastAPI 啟動失敗 (ImportError)

**症狀**:
```bash
uvicorn app.main:app --reload
# ImportError: cannot import name 'xxx' from 'app.models'
```

**原因**:
- 循環導入
- 模組路徑錯誤
- 缺少 `__init__.py`

**解決方案**:

**Step 1: 檢查 `__init__.py`**
```bash
# 確認每個目錄都有 __init__.py
ls app/models/__init__.py
ls app/schemas/__init__.py
# ... 等等
```

**Step 2: 檢查導入順序**
```python
# ❌ 錯誤: 循環導入
# models/user.py
from app.models.task import Task  # Task 又導入 User

# ✅ 正確: 使用字串引用
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

class User(Base):
    tasks = relationship("Task", back_populates="creator")  # 字串引用
```

**Step 3: 使用絕對導入**
```python
# ❌ 相對導入
from .models import User

# ✅ 絕對導入
from app.models.user import User
```

---

### Q8: 測試失敗: Database session 問題

**症狀**:
```bash
pytest tests/test_auth.py
# sqlalchemy.exc.InvalidRequestError: Object '<User>' is already attached to session
```

**原因**:
測試間數據庫 session 未正確隔離

**解決方案**:

**正確的 pytest fixture**:
```python
# conftest.py
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base

@pytest.fixture(scope="function")
def test_db():
    """每個測試函數獨立的數據庫 session"""
    # 使用 in-memory SQLite
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)

    SessionLocal = sessionmaker(bind=engine)
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(engine)

# 測試中使用
def test_register(test_db):
    user = User(email="test@example.com")
    test_db.add(user)
    test_db.commit()
    test_db.refresh(user)  # ✅ 確保 user 是 detached 的
    assert user.id is not None
```

---

### Q9: JWT Token 驗證失敗

**症狀**:
```bash
curl -H "Authorization: Bearer <token>" http://localhost:8000/api/auth/me
# 401 Unauthorized: "Could not validate credentials"
```

**原因**:
- Token 過期
- JWT_SECRET_KEY 不一致
- Token 格式錯誤

**解決方案**:

**Step 1: 檢查 Token 是否過期**
```python
# 使用 jwt.io 解碼 token
import jwt
token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
decoded = jwt.decode(token, options={"verify_signature": False})
print(decoded)  # 查看 'exp' (expiration time)
```

**Step 2: 檢查 SECRET_KEY**
```bash
# 確認 .env 中的 SECRET_KEY 一致
cat backend/.env | grep JWT_SECRET_KEY
```

**Step 3: 檢查 Token 格式**
```bash
# Header 必須是 "Bearer <token>" 格式
# ❌ 錯誤
Authorization: <token>

# ✅ 正確
Authorization: Bearer <token>
```

**Step 4: 測試 Token 生成與驗證**
```python
# 測試腳本
from app.utils.security import create_access_token, decode_access_token

token = create_access_token(user_id=1)
print(f"Generated token: {token}")

user_id = decode_access_token(token)
print(f"Decoded user_id: {user_id}")
```

---

### Q10: CORS 錯誤 (前後端連接時)

**症狀**:
```
Access to fetch at 'http://localhost:8000/api/tasks' from origin
'http://localhost:3000' has been blocked by CORS policy
```

**原因**:
後端未配置 CORS

**解決方案**:

```python
# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# ✅ 添加 CORS 中間件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # 前端地址
    allow_credentials=True,
    allow_methods=["*"],  # 允許所有 HTTP 方法
    allow_headers=["*"],  # 允許所有 Headers
)
```

**生產環境配置**:
```python
import os

allowed_origins = os.getenv("CORS_ORIGINS", "").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,  # 從環境變數讀取
    # ...
)
```

`.env`:
```env
CORS_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
```

---

### Q11: Pydantic 驗證失敗但不知道原因

**症狀**:
```bash
422 Unprocessable Entity
{
  "detail": [
    {
      "loc": ["body", "email"],
      "msg": "value is not a valid email address",
      "type": "value_error.email"
    }
  ]
}
```

**原因**:
Pydantic 驗證規則未通過

**解決方案**:

**Step 1: 查看詳細錯誤**
- `loc`: 錯誤位置 (`["body", "email"]` 表示請求 body 中的 email 欄位)
- `msg`: 錯誤訊息
- `type`: 錯誤類型

**Step 2: 檢查 Schema 定義**
```python
# schemas/user.py
from pydantic import BaseModel, EmailStr, validator

class UserCreate(BaseModel):
    email: EmailStr  # ✅ 自動驗證 email 格式
    password: str
    username: str

    @validator('password')
    def password_strength(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters')
        if not any(char.isdigit() for char in v):
            raise ValueError('Password must contain at least one digit')
        return v
```

**Step 3: 測試 Schema**
```python
# 單獨測試 Schema
from app.schemas.user import UserCreate

# ❌ 這會失敗
data = {"email": "invalid-email", "password": "123", "username": "Test"}
try:
    user = UserCreate(**data)
except Exception as e:
    print(e)  # 查看具體錯誤
```

---

### Q12: SQLAlchemy 查詢結果為空

**症狀**:
```python
tasks = db.query(Task).filter(Task.status == "TODO").all()
print(tasks)  # []
# 明明數據庫裡有數據，但查不到
```

**原因**:
- 過濾條件錯誤
- 忘記 commit
- 查詢了錯誤的表

**解決方案**:

**Step 1: 檢查數據是否真的在數據庫**
```bash
docker exec -it taskdb psql -U taskuser -d taskdb

taskdb=# SELECT * FROM tasks;
# 查看是否有數據
```

**Step 2: 打印 SQL 語句**
```python
from sqlalchemy import create_engine

engine = create_engine(DATABASE_URL, echo=True)  # echo=True 打印 SQL
# 運行查詢，查看生成的 SQL
```

**Step 3: 檢查過濾條件**
```python
# ❌ 錯誤: 字串比較
Task.status == "TODO"  # 如果 status 是 Enum，這樣不對

# ✅ 正確: 使用 Enum
from app.models.task import TaskStatus
Task.status == TaskStatus.TODO
```

**Step 4: 確認 commit**
```python
# 寫入操作後必須 commit
task = Task(title="Test")
db.add(task)
db.commit()  # ✅ 不要忘記
db.refresh(task)  # 刷新獲取 ID
```

---

### Q13: 測試覆蓋率不達標

**症狀**:
```bash
pytest --cov=app
# Coverage: 65%
# 需要達到 80%
```

**原因**:
缺少測試案例，尤其是錯誤處理和邊界條件

**解決方案**:

**Step 1: 查看未覆蓋的代碼**
```bash
pytest --cov=app --cov-report=html
open htmlcov/index.html
# 紅色部分是未覆蓋的代碼
```

**Step 2: 補充測試案例**

**確保覆蓋**:
1. 成功案例 (Happy Path)
2. 失敗案例 (錯誤處理)
3. 邊界條件 (Edge Cases)
4. 權限檢查

**範例**:
```python
# 如果 update_task 覆蓋率低，補充這些測試:

def test_update_task_success(test_db, auth_token):
    # 成功案例
    pass

def test_update_task_not_found(test_db, auth_token):
    # 404 案例
    pass

def test_update_task_permission_denied(test_db, auth_token):
    # 403 案例
    pass

def test_update_task_invalid_status(test_db, auth_token):
    # 422 案例
    pass
```

**Step 3: 排除不需要測試的代碼**
```toml
# pyproject.toml
[tool.pytest.ini_options]
addopts = "--cov=app --cov-report=term --cov-report=html"

[tool.coverage.run]
omit = [
    "*/tests/*",
    "*/migrations/*",
    "*/__init__.py",
]
```

---

### Q14: Async/Await 使用錯誤

**症狀**:
```python
RuntimeError: asyncio.run() cannot be called from a running event loop
```

**原因**:
在已有的事件循環中又調用了 `asyncio.run()`

**解決方案**:

**正確的 Async 使用**:
```python
# ✅ 在路由中使用 async
@router.get("/tasks")
async def get_tasks(db: Session = Depends(get_db)):
    tasks = await task_service.get_tasks(db)  # await async 函數
    return tasks

# ✅ Service 層
async def get_tasks(db: Session):
    result = await db.execute(select(Task))
    tasks = result.scalars().all()
    return tasks
```

**常見錯誤**:
```python
# ❌ 混用 sync 和 async
@router.get("/tasks")
def get_tasks(db: Session = Depends(get_db)):  # 應該是 async def
    tasks = await task_service.get_tasks(db)  # 錯誤: 在 sync 函數中 await
```

---

## 🎨 前端開發問題

### Q15: Axios 請求失敗 (Network Error)

**症狀**:
```javascript
Error: Network Error
    at createError (createError.js:16)
```

**原因**:
- 後端未啟動
- CORS 未配置
- API 地址錯誤

**解決方案**:

**Step 1: 確認後端運行**
```bash
# 訪問後端健康檢查
curl http://localhost:8000/docs
# 應該看到 Swagger UI
```

**Step 2: 檢查 API 地址**
```javascript
// src/services/api.js
const api = axios.create({
  baseURL: process.env.REACT_APP_API_BASE_URL || 'http://localhost:8000',
});

// .env
REACT_APP_API_BASE_URL=http://localhost:8000
```

**Step 3: 檢查 CORS（見 Q10）**

**Step 4: 使用瀏覽器 DevTools 查看**
- 打開 Chrome DevTools → Network tab
- 查看請求是否發送
- 查看響應狀態碼和錯誤訊息

---

### Q16: React 組件不更新

**症狀**:
```javascript
const [tasks, setTasks] = useState([]);

// 調用 API 後
const newTasks = await taskService.getTasks();
setTasks(newTasks);
// UI 沒有更新
```

**原因**:
- State 未正確更新
- 依賴數組錯誤
- 對象引用未改變

**解決方案**:

**方案 1: 確保返回新數組/對象**
```javascript
// ❌ 錯誤: 直接修改 state
tasks.push(newTask);
setTasks(tasks);  # React 認為引用沒變，不會重新渲染

// ✅ 正確: 返回新數組
setTasks([...tasks, newTask]);

// 或
setTasks(prevTasks => [...prevTasks, newTask]);
```

**方案 2: 檢查 useEffect 依賴**
```javascript
useEffect(() => {
  fetchTasks();
}, []);  // ✅ 空數組: 只在 mount 時執行

useEffect(() => {
  fetchTasks();
}, [filters]);  // ✅ 依賴 filters: filters 改變時執行
```

**方案 3: 使用 React DevTools 除錯**
- 安裝 React Developer Tools
- 查看 Component State
- 確認 state 確實改變了

---

### Q17: Token 在刷新頁面後丟失

**症狀**:
刷新頁面後，用戶需要重新登入

**原因**:
Token 只存在內存（state），未持久化

**解決方案**:

**方案 1: 使用 localStorage**
```javascript
// src/services/authService.js
export const setToken = (token) => {
  localStorage.setItem('token', token);
};

export const getToken = () => {
  return localStorage.getItem('token');
};

export const removeToken = () => {
  localStorage.removeItem('token');
};

// Login 後
const response = await api.post('/api/auth/login', { email, password });
setToken(response.data.access_token);
```

**方案 2: AuthContext 初始化時讀取 token**
```javascript
export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const token = getToken();
    if (token) {
      // 驗證 token 並獲取用戶資訊
      authService.getCurrentUser()
        .then(setUser)
        .catch(() => removeToken())
        .finally(() => setLoading(false));
    } else {
      setLoading(false);
    }
  }, []);

  if (loading) return <div>Loading...</div>;

  return (
    <AuthContext.Provider value={{ user, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};
```

---

### Q18: ESLint 或編譯錯誤

**症狀**:
```bash
npm start
# Compiled with warnings.
# 'useState' is not defined  no-undef
```

**原因**:
缺少必要的 import

**解決方案**:

**自動修復**:
```bash
npm run lint -- --fix
```

**常見問題**:
```javascript
// ❌ 缺少 import
const [state, setState] = useState(0);

// ✅ 添加 import
import { useState } from 'react';
const [state, setState] = useState(0);
```

**禁用特定規則（不推薦）**:
```javascript
// eslint-disable-next-line no-console
console.log('Debug info');
```

---

## 🚀 CI/CD 與部署問題

### Q19: GitHub Actions 失敗

**症狀**:
CI pipeline 顯示紅色 ❌

**解決方案**:

見「記憶卡 016」的詳細流程

**快速檢查清單**:
- [ ] 本地測試通過嗎？(`pytest -v`)
- [ ] 本地 Linting 通過嗎？(`flake8 app/`)
- [ ] 依賴文件正確嗎？(`pyproject.toml`)
- [ ] GitHub Actions 的 Python 版本正確嗎？

---

### Q20: Docker 構建失敗

**症狀**:
```bash
docker build -t task-backend .
# ERROR: failed to solve: failed to compute cache key
```

**原因**:
- Dockerfile 語法錯誤
- 文件路徑錯誤
- 基礎鏡像拉取失敗

**解決方案**:

**Step 1: 檢查 Dockerfile 語法**
```dockerfile
# ✅ 正確
FROM python:3.10-slim
WORKDIR /app
COPY pyproject.toml poetry.lock ./
RUN pip install poetry && poetry install --no-dev
COPY . .
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0"]
```

**Step 2: 使用 .dockerignore**
```
# .dockerignore
__pycache__
*.pyc
.env
.venv
.git
tests/
htmlcov/
```

**Step 3: 逐層構建除錯**
```bash
# 只構建到某一層
docker build --target builder -t task-backend:test .
```

---

## 🆘 終極除錯流程

### 當你完全卡住時（超過 1 小時）

**Step 1: 深呼吸，冷靜 3 分鐘** ☕

**Step 2: 系統化檢查**
1. [ ] 能複現問題嗎？
2. [ ] 錯誤訊息完整複製了嗎？
3. [ ] Google 過了嗎？
4. [ ] 查過官方文檔了嗎？

**Step 3: 向 AI 求助的正確方式**

```
【提問模板】
我在開發 FastAPI 專案時遇到問題：

【錯誤訊息】
[完整的錯誤訊息，包含堆疊追蹤]

【相關代碼】
[貼上相關代碼片段]

【環境資訊】
- Python 版本: 3.10.12
- FastAPI 版本: 0.104.0
- 作業系統: macOS / Ubuntu / Windows

【已嘗試的方法】
1. [方法 1] - 結果: [失敗/成功]
2. [方法 2] - 結果: [失敗/成功]

【預期行為】
[你期望發生什麼]

【實際行為】
[實際發生了什麼]
```

**Step 4: 建立最小複現案例**

把問題簡化到最小，去掉無關代碼

**Step 5: 休息一下**

有時候離開 10 分鐘，回來就有靈感了

---

## 預防勝於治療

### 開發最佳實踐

1. **頻繁測試**: 每完成一個小功能就測試
2. **小步提交**: 每 15-30 分鐘 commit 一次
3. **讀錯誤訊息**: 不要跳過，仔細讀
4. **使用版本控制**: 隨時可以回滾
5. **記錄學習**: 遇到問題後，記下解決方法

---

**記住**: 每個開發者都會遇到問題，區別在於解決問題的效率。

建立系統化的除錯流程，遇到問題不慌張，按步驟排查，90% 的問題都能解決！🛠️
