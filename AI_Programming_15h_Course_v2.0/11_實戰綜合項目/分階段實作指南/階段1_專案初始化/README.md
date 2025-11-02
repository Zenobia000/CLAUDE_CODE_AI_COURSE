# 階段 1: 專案初始化
# Project Initialization - Setup Your Development Environment

**預計時間**: 30 分鐘
**難度**: ★☆☆☆☆ (基礎)
**前置要求**: 完成 Module 2 (CLI 工具精通)
**核心技能**: 專案架構設計、環境配置、版本控制

---

## 📋 階段目標

完成這個階段後，你將擁有：

✅ **完整的專案結構** - 後端 API 的標準目錄架構
✅ **配置完善的開發環境** - Python 虛擬環境 + 依賴管理
✅ **初始化的 Git repository** - 版本控制就緒
✅ **基礎配置文件** - 環境變數、資料庫連線設定
✅ **可運行的 Hello World API** - 驗證環境正常

**成功標準**:
- 能夠執行 `python -m uvicorn src.main:app --reload` 並看到歡迎頁面
- Git repository 已初始化並有第一個 commit
- 所有依賴套件正確安裝
- 專案結構符合最佳實踐

---

## 🎯 為什麼這個階段很重要？

### 類比：蓋房子的地基

就像 Linux 系統管理員在部署新服務前，會先：
1. 準備好目錄結構 (`/var/log`, `/etc/config`)
2. 設定好權限與環境變數
3. 安裝必要的套件 (dependencies)
4. 測試基礎連線是否正常

**專案初始化就是你的「地基」**。地基不穩，後續開發會遇到各種奇怪問題。

### 本階段的關鍵決策點

你會在這個階段做出以下決策（並學會"為什麼"）：

1. **目錄結構設計** - 為什麼用 `src/` 而不是把所有東西放根目錄？
2. **依賴管理方式** - 為什麼用 `requirements.txt` 而不是直接 `pip install`？
3. **配置文件分離** - 為什麼用 `.env` 檔案而不是硬編碼？
4. **Git 忽略規則** - 為什麼虛擬環境不應該進版本控制？

---

## 🛠️ 前置檢查清單

開始前，確認你的環境符合以下要求：

### 必備工具檢查

```bash
# 1. Python 版本 (需要 3.10+)
python3 --version
# 預期輸出: Python 3.10.x 或更高

# 2. pip 版本
pip3 --version
# 預期輸出: pip 22.x 或更高

# 3. Git 已安裝
git --version
# 預期輸出: git version 2.x

# 4. Claude Code 可用
claude --version
# 或確認你在 Claude Code 環境中
```

### 可選工具（建議安裝）

```bash
# 1. pyenv (Python 版本管理)
pyenv --version

# 2. poetry (進階依賴管理，本專案使用 requirements.txt 為簡化)
poetry --version

# 3. httpie 或 curl (API 測試)
http --version
# 或
curl --version
```

### 目錄準備

```bash
# 建立專案根目錄
mkdir task-management-system
cd task-management-system

# 確認當前目錄
pwd
# 預期: /path/to/task-management-system
```

---

## 📝 完整操作步驟

### Step 1.1: Git Repository 初始化 (3 分鐘)

#### 🎯 目標
建立版本控制，確保每一步變更都可追蹤與回滾。

#### 📌 為什麼先初始化 Git？
- **最佳實踐**: 在寫任何代碼前就啟用版本控制
- **安全網**: 實驗失敗時可以輕鬆回滾
- **習慣養成**: 每完成一個小功能就 commit

#### 🔧 操作指令

```bash
# 初始化 Git repository
git init

# 確認初始化成功
git status
# 預期輸出: On branch main (或 master)
#           No commits yet
```

#### 🤖 AI 協作：生成 .gitignore

**情境**: 你需要一個適合 Python + FastAPI 專案的 .gitignore 文件。

**提示詞**:
```
請為我生成一個 .gitignore 文件，用於 Python FastAPI 專案。

需要忽略:
1. Python 虛擬環境 (venv/, .venv/, env/)
2. Python 編譯檔 (__pycache__/, *.pyc)
3. IDE 設定檔 (.vscode/, .idea/)
4. 環境變數檔 (.env)
5. 資料庫檔案 (*.db, *.sqlite)
6. 測試覆蓋率報告 (.coverage, htmlcov/)
7. macOS/Windows 系統檔 (.DS_Store, Thumbs.db)

請直接給我完整的 .gitignore 內容，我會複製到專案中。
```

**執行步驟**:
1. 將 AI 生成的內容複製
2. 創建文件:
   ```bash
   # 使用你喜歡的編輯器
   nano .gitignore
   # 或 Claude Code 的 Write 工具
   ```
3. 驗證:
   ```bash
   cat .gitignore | head -10
   ```

#### ✅ 檢查點
- [ ] `.git/` 目錄已創建
- [ ] `.gitignore` 文件已創建且包含常見忽略規則
- [ ] `git status` 顯示 `.gitignore` 為未追蹤文件

---

### Step 1.2: 建立專案目錄結構 (5 分鐘)

#### 🎯 目標
建立符合 FastAPI 最佳實踐的目錄架構。

#### 📌 為什麼要有標準結構？
- **可維護性**: 團隊成員能快速找到對應的代碼
- **可擴展性**: 未來新增功能時有明確的放置位置
- **工具兼容**: 測試、打包工具能正確識別專案結構

#### 🏗️ 標準目錄結構

```
task-management-system/
├── .git/                      # Git 版本控制 (已在 Step 1.1 創建)
├── .gitignore                 # Git 忽略規則 (已在 Step 1.1 創建)
├── src/                       # 【核心】原始碼目錄
│   ├── __init__.py           # Python 套件標識
│   ├── main.py               # FastAPI 應用入口
│   ├── config.py             # 設定管理 (DB URL, JWT secret, etc.)
│   ├── database.py           # 資料庫連線設定
│   ├── models/               # 資料庫模型 (SQLAlchemy ORM)
│   │   └── __init__.py
│   ├── schemas/              # Pydantic schemas (API 請求/響應)
│   │   └── __init__.py
│   ├── routers/              # API 路由 (endpoints)
│   │   └── __init__.py
│   ├── services/             # 業務邏輯層
│   │   └── __init__.py
│   └── utils/                # 工具函數 (auth, helpers)
│       └── __init__.py
├── tests/                     # 測試目錄
│   ├── __init__.py
│   └── conftest.py           # Pytest 配置與 fixtures
├── .env.example              # 環境變數範本
├── .env                      # 實際環境變數 (不進版本控制)
├── requirements.txt          # Python 依賴列表
├── README.md                 # 專案說明文檔
└── docker-compose.yml        # Docker 配置 (可選，後續階段)
```

#### 🔧 快速建立指令

**方法 1: 手動建立 (學習推薦)**
```bash
# 建立主要目錄
mkdir -p src/{models,schemas,routers,services,utils}
mkdir -p tests

# 建立 __init__.py 檔案 (Python 套件標識)
touch src/__init__.py
touch src/models/__init__.py
touch src/schemas/__init__.py
touch src/routers/__init__.py
touch src/services/__init__.py
touch src/utils/__init__.py
touch tests/__init__.py

# 建立核心檔案
touch src/main.py
touch src/config.py
touch src/database.py
touch tests/conftest.py
touch README.md
touch requirements.txt
touch .env.example

# 驗證結構
tree -L 2
# 或
ls -R
```

**方法 2: AI 協作建立 (效率推薦)**

**提示詞**:
```
我需要為 FastAPI 專案建立標準目錄結構。

請生成一個 bash 腳本，創建以下結構:
- src/ 目錄包含: models, schemas, routers, services, utils 子目錄
- tests/ 目錄
- 所有 Python 目錄都要有 __init__.py
- 創建以下檔案: main.py, config.py, database.py, conftest.py, README.md, requirements.txt, .env.example

腳本應該:
1. 使用 mkdir -p 確保目錄不重複創建
2. 使用 touch 創建空白檔案
3. 最後用 tree 或 ls -R 顯示結構驗證

請直接給我可執行的 bash 腳本。
```

將腳本保存為 `setup_structure.sh`，然後執行:
```bash
bash setup_structure.sh
```

#### ✅ 檢查點
- [ ] `src/` 目錄已創建且包含 5 個子目錄
- [ ] 所有子目錄都有 `__init__.py`
- [ ] `tests/` 目錄已創建
- [ ] `tree` 或 `ls -R` 輸出與上述結構一致

---

### Step 1.3: 建立 Python 虛擬環境 (3 分鐘)

#### 🎯 目標
隔離專案依賴，避免污染系統 Python 環境。

#### 📌 為什麼需要虛擬環境？
- **依賴隔離**: 不同專案可以使用不同版本的套件
- **乾淨環境**: 不會污染系統 Python
- **可重現性**: 其他人可以用相同環境重現你的專案

#### 🔧 操作指令

```bash
# 創建虛擬環境 (使用 Python 3.10+)
python3 -m venv venv

# 啟動虛擬環境
# macOS/Linux:
source venv/bin/activate

# Windows (Git Bash):
source venv/Scripts/activate

# Windows (CMD):
venv\Scripts\activate.bat

# Windows (PowerShell):
venv\Scripts\Activate.ps1

# 驗證虛擬環境已啟動
which python
# 預期: /path/to/task-management-system/venv/bin/python

# 升級 pip 到最新版本
pip install --upgrade pip
```

#### ⚠️ 常見問題

**Q1: 執行 `python3 -m venv venv` 報錯 "No module named venv"**
- 解決: 安裝 `python3-venv` 套件
  ```bash
  # Ubuntu/Debian
  sudo apt install python3-venv

  # macOS (使用 Homebrew 安裝的 Python 通常已包含)
  brew reinstall python@3.10
  ```

**Q2: 虛擬環境啟動後，`which python` 仍指向系統 Python**
- 檢查: `echo $VIRTUAL_ENV` 是否有輸出
- 解決: 重新啟動終端機並再次執行 `source venv/bin/activate`

#### ✅ 檢查點
- [ ] `venv/` 目錄已創建
- [ ] 終端提示符前出現 `(venv)` 標記
- [ ] `which python` 指向虛擬環境中的 Python
- [ ] `pip --version` 顯示為最新版本

---

### Step 1.4: 安裝核心依賴 (5 分鐘)

#### 🎯 目標
安裝 FastAPI 開發所需的核心套件。

#### 📌 依賴套件說明

| 套件 | 用途 | 為什麼需要 |
|-----|------|-----------|
| `fastapi` | Web 框架 | 建立 RESTful API |
| `uvicorn[standard]` | ASGI 伺服器 | 運行 FastAPI 應用 |
| `sqlalchemy` | ORM | 資料庫操作 |
| `psycopg2-binary` | PostgreSQL 驅動 | 連接 PostgreSQL (或用 `databases[postgresql]`) |
| `python-jose[cryptography]` | JWT | 實作身份驗證 token |
| `passlib[bcrypt]` | 密碼雜湊 | 安全儲存密碼 |
| `python-multipart` | 表單解析 | 處理表單數據 |
| `pydantic[email]` | 數據驗證 | Email 格式驗證 |
| `pytest` | 測試框架 | 單元測試與整合測試 |
| `pytest-cov` | 覆蓋率報告 | 測試覆蓋率分析 |
| `httpx` | HTTP 客戶端 | 測試 API endpoints |

#### 🔧 操作步驟

**Step 4.1: 創建 requirements.txt**

**方法 1: AI 協作生成 (推薦)**

**提示詞**:
```
為 FastAPI 任務管理系統創建 requirements.txt 文件。

專案技術棧:
- FastAPI (Web 框架)
- SQLAlchemy (ORM)
- PostgreSQL (資料庫)
- JWT (身份驗證)
- Pytest (測試)

請包含:
1. 核心依賴 (fastapi, uvicorn, sqlalchemy)
2. 資料庫驅動 (psycopg2-binary)
3. 身份驗證 (python-jose, passlib)
4. 數據驗證 (pydantic with email)
5. 測試工具 (pytest, pytest-cov, httpx)

格式要求:
- 固定版本號 (使用 == 而非 >=)
- 按類別分組並加註解
- 使用當前穩定版本 (2024年10月)

請直接給我完整的 requirements.txt 內容。
```

將生成的內容保存到 `requirements.txt`。

**方法 2: 手動創建範例**

```txt
# Web Framework
fastapi==0.104.1
uvicorn[standard]==0.24.0

# Database
sqlalchemy==2.0.23
psycopg2-binary==2.9.9
# Alternative: databases[postgresql]==0.8.0

# Authentication & Security
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-multipart==0.0.6

# Data Validation
pydantic[email]==2.5.0

# Development & Testing
pytest==7.4.3
pytest-cov==4.1.0
httpx==0.25.1

# Environment Variables
python-dotenv==1.0.0
```

**Step 4.2: 安裝依賴**

```bash
# 確保虛擬環境已啟動 (看到 (venv) 提示符)
pip install -r requirements.txt

# 驗證安裝
pip list | grep fastapi
pip list | grep uvicorn
pip list | grep sqlalchemy
```

**Step 4.3: 驗證安裝成功**

```bash
# 測試 FastAPI 是否可導入
python -c "import fastapi; print(f'FastAPI version: {fastapi.__version__}')"

# 測試 uvicorn 是否可運行
uvicorn --version
```

#### ⚠️ 常見問題

**Q1: `psycopg2-binary` 安裝失敗 (Windows)**
- 原因: 缺少 C 編譯器
- 解決: 改用 `psycopg2-binary` (已編譯版本) 或使用 `databases[postgresql]`

**Q2: 安裝速度很慢**
- 解決: 使用國內鏡像源
  ```bash
  pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
  ```

#### ✅ 檢查點
- [ ] `requirements.txt` 已創建且包含所有必要套件
- [ ] 所有套件安裝成功 (無錯誤訊息)
- [ ] `pip list` 顯示所有依賴套件
- [ ] FastAPI 和 uvicorn 可正常導入

---

### Step 1.5: 創建 Hello World API (8 分鐘)

#### 🎯 目標
創建最簡單的 FastAPI 應用，驗證環境配置正確。

#### 📌 為什麼從 Hello World 開始？
- **驗證環境**: 確認所有依賴都正確安裝
- **理解基礎**: 了解 FastAPI 的基本結構
- **快速反饋**: 立即看到成果，建立信心

#### 🔧 操作步驟

**Step 5.1: 編寫 src/main.py**

**提示詞 (AI 協作)**:
```
為 FastAPI 專案創建一個簡單的 main.py 入口文件。

需求:
1. 創建 FastAPI 應用實例
2. 設定應用標題、描述、版本 (Task Management System v1.0)
3. 創建一個 root endpoint (GET /) 返回歡迎訊息
4. 創建一個 health check endpoint (GET /health) 返回系統狀態

格式要求:
- 使用 FastAPI 最佳實踐
- 包含適當的註解
- 使用 async def (異步函數)

請直接給我完整的 src/main.py 代碼。
```

**參考實作**:

```python
# src/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# 創建 FastAPI 應用實例
app = FastAPI(
    title="Task Management System",
    description="A simple task management API built with FastAPI",
    version="1.0.0",
    docs_url="/docs",  # Swagger UI
    redoc_url="/redoc"  # ReDoc
)

# CORS 中間件配置 (允許前端連接)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生產環境應設定具體域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Root endpoint - 歡迎訊息
@app.get("/")
async def root():
    """
    Root endpoint - 返回歡迎訊息
    """
    return {
        "message": "Welcome to Task Management System API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }

# Health check endpoint - 系統狀態檢查
@app.get("/health")
async def health_check():
    """
    Health check endpoint - 用於監控系統是否正常運行
    """
    return {
        "status": "healthy",
        "service": "task-management-api"
    }

# Startup event - 應用啟動時執行
@app.on_event("startup")
async def startup_event():
    print("🚀 Task Management System API is starting...")

# Shutdown event - 應用關閉時執行
@app.on_event("shutdown")
async def shutdown_event():
    print("🛑 Task Management System API is shutting down...")
```

**Step 5.2: 運行應用**

```bash
# 確保在專案根目錄
pwd
# 預期: /path/to/task-management-system

# 啟動開發伺服器 (帶自動重載)
python -m uvicorn src.main:app --reload --host 0.0.0.0 --port 8000

# 預期輸出:
# INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
# INFO:     Started reloader process [xxxxx] using WatchFiles
# INFO:     Started server process [xxxxx]
# INFO:     Waiting for application startup.
# 🚀 Task Management System API is starting...
# INFO:     Application startup complete.
```

**Step 5.3: 測試 API**

**方法 1: 瀏覽器測試**
1. 打開瀏覽器訪問 `http://localhost:8000`
2. 應該看到 JSON 響應:
   ```json
   {
     "message": "Welcome to Task Management System API",
     "version": "1.0.0",
     "docs": "/docs",
     "health": "/health"
   }
   ```

**方法 2: curl 測試**
```bash
# 測試 root endpoint
curl http://localhost:8000/

# 測試 health check
curl http://localhost:8000/health

# 測試 API 文檔
curl http://localhost:8000/docs
# 或直接瀏覽器訪問查看 Swagger UI
```

**方法 3: httpie 測試 (如果已安裝)**
```bash
http GET http://localhost:8000/
http GET http://localhost:8000/health
```

**Step 5.4: 探索自動生成的 API 文檔**

1. 訪問 `http://localhost:8000/docs` (Swagger UI)
2. 你會看到:
   - 所有 API endpoints 列表
   - 每個 endpoint 的詳細說明
   - 可互動的測試界面

3. 訪問 `http://localhost:8000/redoc` (ReDoc)
   - 更美觀的文檔展示

#### ✅ 檢查點
- [ ] `src/main.py` 已創建
- [ ] `uvicorn` 成功啟動且無錯誤
- [ ] 訪問 `http://localhost:8000` 返回正確 JSON
- [ ] `/health` endpoint 正常運作
- [ ] `/docs` 顯示 Swagger UI 界面

---

### Step 1.6: 環境變數配置 (4 分鐘)

#### 🎯 目標
設定環境變數管理敏感資訊 (資料庫 URL、JWT secret 等)。

#### 📌 為什麼需要環境變數？
- **安全性**: 敏感資訊不進版本控制
- **靈活性**: 不同環境 (開發/測試/生產) 使用不同配置
- **最佳實踐**: 符合 12-Factor App 原則

#### 🔧 操作步驟

**Step 6.1: 創建 .env.example (範本)**

```bash
# .env.example - 環境變數範本 (會進版本控制)
# 複製此文件為 .env 並填入實際值

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/task_management

# JWT Authentication
SECRET_KEY=your-secret-key-change-this-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=10080

# Application
APP_ENV=development
DEBUG=True

# CORS
CORS_ORIGINS=http://localhost:3000,http://localhost:5173
```

**Step 6.2: 創建實際的 .env 文件**

```bash
# 複製範本
cp .env.example .env

# 編輯 .env 填入實際值
nano .env
```

**Step 6.3: 創建 src/config.py (配置管理)**

**提示詞 (AI 協作)**:
```
創建 src/config.py 用於管理環境變數。

需求:
1. 使用 pydantic BaseSettings 管理配置
2. 從 .env 文件讀取環境變數
3. 提供以下配置:
   - DATABASE_URL (資料庫連線)
   - SECRET_KEY (JWT 密鑰)
   - ALGORITHM (JWT 算法, 預設 HS256)
   - ACCESS_TOKEN_EXPIRE_MINUTES (Token 有效期, 預設 7 天)
   - APP_ENV (環境: development/production)
   - DEBUG (是否開啟 debug 模式)

4. 使用 Singleton 模式 (全域只有一個 settings 實例)

請給我完整的 src/config.py 代碼。
```

**參考實作**:

```python
# src/config.py
from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    """
    應用配置管理 - 從環境變數讀取
    """
    # Database
    DATABASE_URL: str = "sqlite:///./test.db"  # 預設使用 SQLite (開發用)

    # JWT Authentication
    SECRET_KEY: str = "your-secret-key-here-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 10080  # 7 days

    # Application
    APP_ENV: str = "development"
    DEBUG: bool = True

    # CORS
    CORS_ORIGINS: str = "http://localhost:3000,http://localhost:5173"

    class Config:
        env_file = ".env"
        case_sensitive = False

# 創建全域 settings 實例 (Singleton)
settings = Settings()
```

**Step 6.4: 驗證配置**

```bash
# 測試配置是否正確載入
python -c "from src.config import settings; print(f'DB URL: {settings.DATABASE_URL}'); print(f'Secret Key: {settings.SECRET_KEY[:10]}...')"

# 預期輸出:
# DB URL: postgresql://user:password@localhost:5432/task_management
# Secret Key: your-secre...
```

#### ✅ 檢查點
- [ ] `.env.example` 已創建 (會進版本控制)
- [ ] `.env` 已創建 (不進版本控制，在 .gitignore 中)
- [ ] `src/config.py` 已創建
- [ ] 配置可正確載入且無錯誤

---

### Step 1.7: 第一次 Git Commit (3 分鐘)

#### 🎯 目標
將專案初始化的所有變更提交到版本控制。

#### 📌 提交什麼？不提交什麼？

**應該提交的**:
- ✅ 所有原始碼 (src/)
- ✅ 測試目錄結構 (tests/)
- ✅ 配置範本 (.env.example)
- ✅ 依賴列表 (requirements.txt)
- ✅ Git 忽略規則 (.gitignore)
- ✅ 文檔 (README.md)

**不應該提交的**:
- ❌ 虛擬環境 (venv/)
- ❌ 編譯檔 (__pycache__/)
- ❌ 實際環境變數 (.env)
- ❌ IDE 設定 (.vscode/, .idea/)

#### 🔧 操作步驟

```bash
# 檢查待提交的文件
git status

# 預期看到:
# Untracked files:
#   .env.example
#   .gitignore
#   README.md
#   requirements.txt
#   src/
#   tests/

# 將所有文件加入暫存區
git add .

# 再次檢查 (確保 .env 和 venv/ 沒有被加入)
git status

# 預期看到:
# Changes to be committed:
#   new file:   .env.example
#   new file:   .gitignore
#   ...
# (不應該看到 .env 或 venv/)

# 提交變更
git commit -m "feat(project): initialize project structure

- Setup FastAPI application with basic endpoints
- Configure environment variables management
- Add core dependencies (FastAPI, SQLAlchemy, JWT)
- Create standard project directory structure
- Add .gitignore for Python projects

Project is ready for development.
"

# 檢查提交歷史
git log --oneline
```

#### ✅ 檢查點
- [ ] `git status` 顯示 "nothing to commit, working tree clean"
- [ ] `git log` 顯示至少一個 commit
- [ ] `.env` 和 `venv/` 未被提交
- [ ] 所有原始碼和配置範本已提交

---

## 🎉 階段完成檢查

恭喜！如果你完成了所有步驟，現在你應該擁有：

### 功能驗證

執行以下指令確認一切正常：

```bash
# 1. 虛擬環境已啟動
echo $VIRTUAL_ENV
# 預期: 非空輸出 (虛擬環境路徑)

# 2. 依賴已安裝
pip list | grep -E "fastapi|uvicorn|sqlalchemy"
# 預期: 看到這三個套件

# 3. API 可運行
python -m uvicorn src.main:app --reload &
sleep 3
curl http://localhost:8000/health
# 預期: {"status":"healthy","service":"task-management-api"}
pkill -f uvicorn

# 4. Git repository 正常
git log --oneline
# 預期: 至少一個 commit

# 5. 配置可載入
python -c "from src.config import settings; print('Config OK')"
# 預期: Config OK
```

### 檢查清單

- [ ] **專案結構完整** - 所有目錄和文件都已創建
- [ ] **虛擬環境正常** - 依賴隔離，不污染系統
- [ ] **依賴全部安裝** - 無安裝錯誤
- [ ] **Hello World API 可運行** - 訪問 /health 成功
- [ ] **環境變數配置正確** - settings 可正常載入
- [ ] **Git 版本控制就緒** - 已有初始 commit
- [ ] **.gitignore 正確設定** - .env 和 venv/ 被忽略

### 自我評估

回答以下問題檢驗你的理解：

1. **為什麼要使用虛擬環境？**
   <details>
   <summary>點擊查看答案</summary>

   - 隔離專案依賴，不污染系統 Python
   - 不同專案可使用不同版本套件
   - 便於重現開發環境
   </details>

2. **為什麼 .env 不應該進版本控制？**
   <details>
   <summary>點擊查看答案</summary>

   - 包含敏感資訊 (密碼、API keys)
   - 不同環境需要不同配置
   - 安全最佳實踐
   </details>

3. **src/ 目錄中為什麼需要 `__init__.py`？**
   <details>
   <summary>點擊查看答案</summary>

   - 標識該目錄為 Python 套件
   - 允許從該目錄導入模組
   - Python 導入機制的要求
   </details>

---

## 🚨 常見問題與除錯

### 問題 1: uvicorn 啟動報錯 "ModuleNotFoundError: No module named 'src'"

**原因**: Python 找不到 `src` 模組

**解決方案**:
```bash
# 確保在專案根目錄執行
pwd

# 方案 1: 使用模組執行方式 (推薦)
python -m uvicorn src.main:app --reload

# 方案 2: 將當前目錄加入 PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
uvicorn src.main:app --reload
```

---

### 問題 2: API 可以訪問但自動重載不工作

**原因**: uvicorn 的 `--reload` 監聽失效

**解決方案**:
```bash
# 檢查是否使用了 --reload 參數
ps aux | grep uvicorn

# 重新啟動並確保使用 --reload
pkill -f uvicorn
python -m uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

---

### 問題 3: git add . 後發現 venv/ 被加入

**原因**: .gitignore 未正確設定或未生效

**解決方案**:
```bash
# 1. 確認 .gitignore 包含 venv/
cat .gitignore | grep venv

# 2. 如果已經被追蹤，需要移除
git rm -r --cached venv/
git commit -m "chore: remove venv from git tracking"

# 3. 確認 .gitignore 生效
git status
# 不應該再看到 venv/
```

---

### 問題 4: pydantic_settings 導入錯誤

**原因**: pydantic v2 需要單獨安裝 pydantic-settings

**解決方案**:
```bash
# 安裝 pydantic-settings
pip install pydantic-settings==2.1.0

# 更新 requirements.txt
echo "pydantic-settings==2.1.0" >> requirements.txt

# 或使用舊版 pydantic v1
pip install "pydantic==1.10.13"
```

---

## 📚 延伸學習資源

### 官方文檔
- [FastAPI 官方教程](https://fastapi.tiangolo.com/tutorial/)
- [Pydantic Settings](https://docs.pydantic.dev/latest/concepts/pydantic_settings/)
- [Uvicorn 文檔](https://www.uvicorn.org/)

### 相關課程模組
- **Module 2**: Claude Code CLI 工具精通
- **Module 5**: CI/CD 與部署自動化
- **Module 10**: 安全性最佳實踐

### 最佳實踐文章
- [12-Factor App](https://12factor.net/) - 環境變數管理原則
- [Python Project Structure](https://docs.python-guide.org/writing/structure/) - 專案結構最佳實踐

---

## 🎯 下一階段預告

完成專案初始化後，接下來進入**階段 2: 後端開發**。

你將學習:
- 📊 **資料庫設計** - 使用 SQLAlchemy 建立 User 和 Task 模型
- 🧪 **TDD 開發** - 測試驅動開發 8 個 API endpoints
- 🔐 **身份驗證** - 實作 JWT token 機制
- ✅ **輸入驗證** - 使用 Pydantic schemas

**準備工作**:
1. 確保本階段所有檢查點都已通過
2. API 能正常運行且自動重載工作
3. 理解了為什麼需要這些配置

**前往**: `分階段實作指南/階段2_後端開發/README.md`

---

## 📝 學習筆記區

**建議記錄**:
1. 你遇到的問題和解決方法
2. 最有效的 AI 提示詞
3. 你認為需要改進的地方
4. 對下一階段的疑問

```
我的筆記:
-
-
-
```

---

**階段 1 完成！準備好進入實際開發了嗎？ 🚀**
