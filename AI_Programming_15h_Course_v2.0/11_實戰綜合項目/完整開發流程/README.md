# 完整開發流程指南
# Task Management System - Development Workflow

**預計完成時間**: 4-6 小時（實際操作）
**適用對象**: 完成 Modules 0-10 的學員
**核心方法**: AI-Powered Development with EPCV Workflow

---

## 流程總覽

```
階段 0: 準備與規劃 (15min)
   ↓
階段 1: 專案初始化 (30min)
   ↓
階段 2: 後端開發 (1.5h)
   ├─ 2.1 數據庫設計 (20min)
   ├─ 2.2 API 開發 TDD (1h)
   └─ 2.3 驗證與除錯 (10min)
   ↓
階段 3: 前端開發 (1h)
   ├─ 3.1 基礎架構 (15min)
   ├─ 3.2 組件開發 (35min)
   └─ 3.3 API 整合 (10min)
   ↓
階段 4: CI/CD 設置 (30min)
   ├─ 4.1 GitHub Actions (15min)
   ├─ 4.2 Docker 配置 (10min)
   └─ 4.3 部署設置 (5min)
   ↓
階段 5: 文檔與交付 (20min)
   ├─ 5.1 API 文檔 (10min)
   └─ 5.2 部署文檔 (10min)
   ↓
✅ MVP 完成！
```

---

## 階段 0: 準備與規劃 (15 分鐘)

### 目標
- 將 PRD 轉化為技術實作方案
- 生成專案架構文檔
- 建立開發路線圖

### 工具
- Claude Code (分析與規劃模式)

### 操作步驟

#### Step 0.1: 分析 PRD (5 min)

**提示詞**:
```
我有一份產品需求文檔 (PRD)，需要你幫我分析並生成技術實作方案。

[貼上 PRD 內容]

請提供:
1. 技術架構建議（技術棧選擇理由）
2. 數據庫 Schema 設計
3. API 端點設計
4. 前端頁面結構
5. 開發優先級建議（哪些功能先做）
6. 潛在技術風險與解決方案
```

**預期產出**:
- 技術架構文檔
- 數據模型設計
- API 設計概覽

#### Step 0.2: 生成專案路線圖 (5 min)

**提示詞**:
```
基於上述技術方案，請幫我生成一份開發路線圖：

要求:
1. 將開發分解成可執行的小任務
2. 每個任務包含: 名稱、預計時間、前置依賴、驗收標準
3. 標示出關鍵里程碑
4. 建議使用 TDD 的部分

格式: Markdown checklist
```

**預期產出**:
- 詳細的任務分解
- 可追蹤的開發清單

#### Step 0.3: 準備開發環境檢查 (5 min)

**檢查清單**:
```bash
# Python 版本
python3 --version  # 需要 3.10+

# Node.js 版本（如果做前端）
node --version     # 需要 18+

# Docker
docker --version

# Git
git --version

# 虛擬環境工具
poetry --version   # 或 pip

# Claude Code
claude --version
```

### 產出物
- [ ] 技術架構文檔 (`docs/architecture.md`)
- [ ] 開發路線圖 (`docs/roadmap.md`)
- [ ] 環境檢查完成

### 關鍵決策點

**決策 1: 技術棧確認**
- 後端: FastAPI vs Flask vs Django?
  - **建議**: FastAPI（效能好、內建 API 文檔、易測試）
- 前端: React vs Vue.js?
  - **建議**: 看你熟悉哪個，或用 Claude Code 生成最簡單的版本

**決策 2: 開發順序**
- 先後端還是先前端？
  - **建議**: 先後端（TDD 方式），前端直接對接 API

**決策 3: 部署策略**
- 本地開發 → Docker → Cloud
  - **建議**: 先確保本地能跑，再考慮部署

### 階段驗收
- ✅ 理解了 PRD 的所有需求
- ✅ 有清晰的技術方案
- ✅ 知道接下來要做什麼
- ✅ 環境準備就緒

---

## 階段 1: 專案初始化 (30 分鐘)

### 目標
- 建立專案目錄結構
- 初始化 Git repository
- 配置開發環境
- 安裝依賴套件

### 工具
- Claude Code (EPCV workflow)
- Git
- Poetry / npm

### 操作步驟

#### Step 1.1: 生成專案骨架 (10 min)

**提示詞** (Claude Code):
```
為一個 FastAPI + React 的任務管理系統創建完整的專案目錄結構。

要求:
1. 前後端分離 (backend/ 和 frontend/)
2. 後端使用 FastAPI, PostgreSQL, SQLAlchemy, Pytest
3. 前端使用 React, Axios, Tailwind CSS
4. 包含 Docker 配置
5. 包含完整的配置文件 (.gitignore, .env.example, README.md)
6. 包含測試目錄結構

請生成完整的目錄結構和必要的空檔案。
```

**預期目錄結構**:
```
task-management-system/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                 # FastAPI app
│   │   ├── config.py               # Configuration
│   │   ├── database.py             # Database connection
│   │   ├── models/                 # SQLAlchemy models
│   │   │   ├── __init__.py
│   │   │   ├── user.py
│   │   │   └── task.py
│   │   ├── schemas/                # Pydantic schemas
│   │   │   ├── __init__.py
│   │   │   ├── user.py
│   │   │   └── task.py
│   │   ├── routers/                # API endpoints
│   │   │   ├── __init__.py
│   │   │   ├── auth.py
│   │   │   ├── tasks.py
│   │   │   └── dashboard.py
│   │   ├── services/               # Business logic
│   │   │   ├── __init__.py
│   │   │   ├── auth_service.py
│   │   │   └── task_service.py
│   │   └── utils/                  # Utilities
│   │       ├── __init__.py
│   │       ├── security.py         # Password hashing, JWT
│   │       └── dependencies.py     # FastAPI dependencies
│   ├── tests/
│   │   ├── __init__.py
│   │   ├── conftest.py             # Pytest fixtures
│   │   ├── test_auth.py
│   │   ├── test_tasks.py
│   │   └── test_dashboard.py
│   ├── alembic/                    # Database migrations
│   │   └── versions/
│   ├── .env.example
│   ├── pyproject.toml              # Poetry config
│   ├── pytest.ini
│   └── README.md
├── frontend/
│   ├── public/
│   │   └── index.html
│   ├── src/
│   │   ├── components/             # React components
│   │   │   ├── Auth/
│   │   │   │   ├── Login.jsx
│   │   │   │   └── Register.jsx
│   │   │   ├── Dashboard/
│   │   │   │   └── Dashboard.jsx
│   │   │   ├── Tasks/
│   │   │   │   ├── TaskList.jsx
│   │   │   │   ├── TaskItem.jsx
│   │   │   │   ├── TaskForm.jsx
│   │   │   │   └── TaskDetail.jsx
│   │   │   └── Common/
│   │   │       ├── Navbar.jsx
│   │   │       ├── Loading.jsx
│   │   │       └── ErrorMessage.jsx
│   │   ├── services/               # API calls
│   │   │   ├── api.js              # Axios instance
│   │   │   ├── authService.js
│   │   │   └── taskService.js
│   │   ├── contexts/               # React Context
│   │   │   └── AuthContext.jsx
│   │   ├── App.jsx
│   │   ├── index.jsx
│   │   └── index.css
│   ├── package.json
│   ├── tailwind.config.js
│   └── README.md
├── docker-compose.yml              # Local development
├── .github/
│   └── workflows/
│       └── ci.yml                  # GitHub Actions
├── docs/
│   ├── architecture.md
│   └── api-design.md
├── .gitignore
└── README.md
```

**執行**:
```bash
# 使用 Claude Code 生成目錄結構
claude /execute "創建上述專案結構的所有目錄和空檔案"

# 確認結構
tree -L 3 task-management-system/
```

#### Step 1.2: 初始化 Git Repository (5 min)

```bash
cd task-management-system

# 初始化 Git
git init

# 創建 .gitignore
cat > .gitignore << 'EOF'
# Python
__pycache__/
*.py[cod]
*$py.class
.venv/
venv/
.env

# Node.js
node_modules/
.npm
.eslintcache

# IDE
.vscode/
.idea/
*.swp
*.swo

# Database
*.db
*.sqlite3

# Docker
.dockerignore

# OS
.DS_Store
Thumbs.db
EOF

# 首次 commit
git add .
git commit -m "feat(project): initial project structure

- Backend: FastAPI + PostgreSQL + SQLAlchemy
- Frontend: React + Tailwind CSS
- Docker Compose for local development
- GitHub Actions CI/CD setup

🤖 Generated with Claude Code
Co-Authored-By: Claude <noreply@anthropic.com>"
```

#### Step 1.3: 後端依賴安裝 (10 min)

**提示詞** (Claude Code):
```
為後端專案生成 pyproject.toml (Poetry) 配置文件。

依賴需求:
- FastAPI
- Uvicorn (ASGI server)
- SQLAlchemy (ORM)
- Psycopg2-binary (PostgreSQL driver)
- Alembic (Database migrations)
- PyJWT (JWT authentication)
- Passlib[bcrypt] (Password hashing)
- Python-dotenv (Environment variables)
- Pydantic (Data validation)

開發依賴:
- Pytest
- Pytest-asyncio
- Pytest-cov (Coverage)
- Black (Code formatter)
- Flake8 (Linter)
- Bandit (Security linter)
```

**執行**:
```bash
cd backend

# 使用 Claude Code 生成 pyproject.toml
claude /execute "生成上述 pyproject.toml"

# 安裝依賴
poetry install

# 啟動虛擬環境
poetry shell

# 驗證安裝
python -c "import fastapi; print(fastapi.__version__)"
```

#### Step 1.4: 前端依賴安裝 (5 min)

```bash
cd frontend

# 創建 React app (或使用 Claude Code 生成 package.json)
npx create-react-app . --template cra-template

# 安裝額外依賴
npm install axios react-router-dom

# 安裝 Tailwind CSS
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p

# 驗證
npm start  # 確認能啟動
```

#### Step 1.5: Docker Compose 配置 (5 min)

**提示詞** (Claude Code):
```
生成 docker-compose.yml 用於本地開發環境。

需要的服務:
1. PostgreSQL 14 (端口 5432)
   - 數據庫名: taskdb
   - 用戶: taskuser
   - 密碼: taskpass
   - Volume 持久化
2. Backend (FastAPI, 端口 8000)
   - 依賴 PostgreSQL
   - 自動重載
3. Frontend (React dev server, 端口 3000)
   - 依賴 Backend

包含健康檢查和重啟策略。
```

**執行**:
```bash
# 使用 Claude Code 生成 docker-compose.yml
claude /execute "生成上述 docker-compose.yml"

# 測試啟動
docker-compose up -d postgres

# 確認數據庫運行
docker-compose ps
```

### 產出物
- [ ] 完整的專案目錄結構
- [ ] Git repository 初始化
- [ ] 後端依賴安裝完成
- [ ] 前端依賴安裝完成（可選）
- [ ] Docker Compose 配置完成

### 關鍵決策點

**決策 1: 使用 Poetry 還是 pip？**
- **建議**: Poetry（依賴管理更清晰，虛擬環境自動管理）

**決策 2: 前端要不要一起做？**
- **建議**: MVP 階段可以先專注後端，用 FastAPI 自帶的 Swagger UI 測試
- 前端可以最後快速用 Claude Code/Cursor 生成

**決策 3: 本地數據庫還是 Docker？**
- **建議**: Docker（環境一致性好，易清理）

### 常見問題

**Q1: Poetry install 很慢怎麼辦？**
```bash
# 使用國內鏡像
poetry config repositories.pypi https://pypi.tuna.tsinghua.edu.cn/simple
```

**Q2: Docker Compose 啟動失敗？**
```bash
# 檢查端口佔用
lsof -i :5432
lsof -i :8000

# 查看日誌
docker-compose logs postgres
```

**Q3: 前端 npm install 失敗？**
```bash
# 清除緩存
npm cache clean --force
rm -rf node_modules package-lock.json
npm install
```

### 階段驗收
- ✅ 專案結構符合標準
- ✅ Git history 有首次 commit
- ✅ 可以進入後端虛擬環境
- ✅ Docker Compose 可以啟動數據庫
- ✅ 知道每個目錄的用途

---

## 階段 2: 後端開發 (1.5 小時)

### 目標
- 使用 TDD 方法開發 RESTful API
- 完成數據庫模型與遷移
- 實作身份驗證與授權
- 達到 80% 測試覆蓋率

### 工具
- Claude Code (TDD workflow)
- Pytest
- FastAPI

### 總體策略

**TDD 紅綠重構循環**:
```
1. ❌ 寫測試 → 測試失敗（紅）
2. ✅ 寫實作 → 測試通過（綠）
3. ♻️  重構代碼 → 測試仍通過
```

### 子階段 2.1: 數據庫設計 (20 分鐘)

#### Step 2.1.1: 設計 SQLAlchemy Models (10 min)

**提示詞** (Claude Code):
```
基於 PRD 的數據模型，生成 SQLAlchemy models。

要求:
1. User model (用戶表)
   - id, email (unique), password_hash, username, created_at, updated_at
2. Task model (任務表)
   - id, title, description, status (enum), priority (enum),
     due_date, created_by (FK), created_at, updated_at, is_deleted
3. 使用 SQLAlchemy 2.0 語法
4. 包含關聯關係 (User 1-N Task)
5. 包含索引優化

生成到 backend/app/models/
```

**預期產出**:
- `models/user.py`
- `models/task.py`

#### Step 2.1.2: 設置數據庫連接 (5 min)

**提示詞** (Claude Code):
```
生成 database.py 用於設置數據庫連接。

要求:
1. 使用 SQLAlchemy async engine
2. 從環境變數讀取 DATABASE_URL
3. 包含 sessionmaker 和 get_db dependency
4. 包含創建表的函數
```

**預期產出**:
- `app/database.py`

#### Step 2.1.3: 配置環境變數 (5 min)

```bash
# 創建 .env
cat > backend/.env << 'EOF'
DATABASE_URL=postgresql://taskuser:taskpass@localhost:5432/taskdb
JWT_SECRET_KEY=your-super-secret-key-change-in-production
JWT_ALGORITHM=HS256
JWT_EXPIRATION_DAYS=7
CORS_ORIGINS=http://localhost:3000
EOF

# 創建 .env.example (不含敏感信息)
cp backend/.env backend/.env.example
```

**提示詞** (Claude Code):
```
生成 config.py 用於管理配置。

要求:
1. 使用 Pydantic BaseSettings
2. 從 .env 讀取環境變數
3. 包含驗證與默認值
```

### 子階段 2.2: API 開發 (TDD) (1 小時)

#### TDD Workflow 說明

每個 API endpoint 遵循以下流程：

```
1. 寫測試 (test_*.py)
   ↓
2. 運行測試 (pytest) → ❌ 失敗
   ↓
3. 寫最少代碼讓測試通過
   ↓
4. 運行測試 (pytest) → ✅ 通過
   ↓
5. 重構代碼（如需要）
   ↓
6. 運行測試 (pytest) → ✅ 仍通過
```

#### Step 2.2.1: 用戶註冊 API (TDD) (15 min)

**Phase 1: 寫測試**

**提示詞** (Claude Code):
```
為用戶註冊 API 寫測試。

需要測試的案例:
1. 成功註冊 (201)
2. Email 格式錯誤 (422)
3. 密碼太短 (422)
4. 重複 Email (409)

使用 FastAPI TestClient 和 pytest。
生成到 tests/test_auth.py
```

**執行測試**:
```bash
cd backend
pytest tests/test_auth.py::test_register_success -v

# 預期結果: ❌ FAILED (因為還沒實作)
```

**Phase 2: 寫實作**

**提示詞** (Claude Code):
```
實作用戶註冊 API。

要求:
1. POST /api/auth/register
2. 使用 Pydantic schema 驗證輸入
3. 使用 bcrypt 加密密碼
4. 防止重複 Email
5. 返回創建的用戶資訊（不含密碼）

生成:
- schemas/user.py (UserCreate, UserResponse)
- services/auth_service.py (register_user 函數)
- routers/auth.py (註冊 endpoint)
- utils/security.py (密碼加密函數)
```

**執行測試**:
```bash
pytest tests/test_auth.py::test_register_success -v

# 預期結果: ✅ PASSED
```

**Phase 3: 運行所有註冊測試**:
```bash
pytest tests/test_auth.py -k register -v

# 確保所有 4 個測試都通過
```

#### Step 2.2.2: 用戶登入 API (TDD) (10 min)

**重複 TDD 流程**:

1. **寫測試** (Claude Code):
```
為登入 API 寫測試。

測試案例:
1. 成功登入 (200, 返回 JWT token)
2. 錯誤密碼 (401)
3. 不存在的 Email (401)
4. Token 驗證成功
```

2. **寫實作** (Claude Code):
```
實作登入 API。

要求:
1. POST /api/auth/login
2. 驗證密碼（使用 bcrypt）
3. 生成 JWT token
4. Token 包含 user_id 和過期時間

更新:
- schemas/user.py (UserLogin, Token)
- services/auth_service.py (login_user)
- routers/auth.py (登入 endpoint)
- utils/security.py (JWT 生成/驗證)
```

3. **運行測試**:
```bash
pytest tests/test_auth.py -k login -v
```

#### Step 2.2.3: 獲取當前用戶 API (TDD) (5 min)

**快速實作**:

**提示詞** (Claude Code):
```
實作「獲取當前用戶」API (TDD)。

1. 先寫測試:
   - 成功獲取 (200)
   - 無效 token (401)
   - 過期 token (401)

2. 實作:
   - GET /api/auth/me
   - 依賴 JWT token 驗證
   - 返回當前用戶資訊

3. 創建 FastAPI dependency: get_current_user
```

#### Step 2.2.4: 任務 CRUD APIs (TDD) (25 min)

**提示詞** (Claude Code - 一次性生成全部)**:
```
使用 TDD 方法實作任務管理的 5 個 API endpoints。

順序:
1. POST /api/tasks (創建任務)
   測試: 成功創建, 缺少必填欄位, 無效優先級

2. GET /api/tasks (查詢任務列表)
   測試: 成功查詢, 按狀態過濾, 按優先級過濾, 分頁

3. GET /api/tasks/{id} (查詢單一任務)
   測試: 成功查詢, 任務不存在, 無權限查看他人任務

4. PUT /api/tasks/{id} (更新任務)
   測試: 成功更新, 無權限更新他人任務, 任務不存在

5. DELETE /api/tasks/{id} (刪除任務)
   測試: 成功刪除, 無權限刪除他人任務, 任務不存在

每個 endpoint:
- 先寫所有測試 (tests/test_tasks.py)
- 再寫實作 (routers/tasks.py, services/task_service.py)
- 驗證測試通過

權限規則: 用戶只能操作自己創建的任務
```

**執行策略**:
```bash
# 一次完成一個 endpoint 的 TDD 循環
pytest tests/test_tasks.py::test_create_task -v
# ... 實作 ...
pytest tests/test_tasks.py::test_create_task -v  # 通過

# 然後下一個
pytest tests/test_tasks.py::test_list_tasks -v
# ... 繼續 ...
```

#### Step 2.2.5: Dashboard API (TDD) (5 min)

**提示詞** (Claude Code):
```
實作 Dashboard 統計 API (TDD)。

1. 測試:
   - 成功獲取統計數據
   - 數據正確性驗證

2. 實作:
   - GET /api/dashboard/stats
   - 返回: 總任務數, 各狀態數量, 各優先級數量, 即將到期, 已逾期

生成:
- schemas/dashboard.py
- routers/dashboard.py
- tests/test_dashboard.py
```

### 子階段 2.3: 驗證與除錯 (10 分鐘)

#### Step 2.3.1: 運行完整測試套件 (5 min)

```bash
cd backend

# 運行所有測試
pytest -v

# 檢查測試覆蓋率
pytest --cov=app --cov-report=html

# 查看覆蓋率報告
open htmlcov/index.html
```

**目標**: 覆蓋率 ≥ 80%

#### Step 2.3.2: 代碼品質檢查 (3 min)

```bash
# Linting
flake8 app/ --max-line-length=100

# 格式化
black app/ tests/

# 安全掃描
bandit -r app/ -ll
```

#### Step 2.3.3: 啟動 API 並手動測試 (2 min)

```bash
# 啟動服務
uvicorn app.main:app --reload

# 訪問自動生成的 API 文檔
open http://localhost:8000/docs

# 測試註冊/登入流程
```

### 產出物
- [ ] 完整的數據庫模型
- [ ] 9 個 API endpoints (全部有測試)
- [ ] JWT 認證系統
- [ ] 測試覆蓋率 ≥ 80%
- [ ] 通過 Linting 和安全掃描
- [ ] Swagger 文檔可訪問

### 關鍵決策點

**決策 1: 使用 Sync 還是 Async？**
- **建議**: Async (FastAPI 原生支持，效能更好)
- 但如果不熟悉，Sync 也可以

**決策 2: 測試數據庫用什麼？**
- **建議**: SQLite in-memory (快速，隔離性好)
- 或者 Docker 跑一個測試用 PostgreSQL

**決策 3: 軟刪除還是硬刪除？**
- **建議**: 軟刪除 (is_deleted flag)，可恢復數據

### 常見問題

**Q1: TDD 寫測試很慢怎麼辦？**
- 讓 Claude Code 一次生成所有測試案例
- 你負責審查測試是否覆蓋所有情境

**Q2: 測試一直失敗？**
```bash
# 逐步除錯
pytest tests/test_auth.py::test_register_success -v -s

# 使用 pdb 除錯
pytest --pdb
```

**Q3: JWT token 驗證失敗？**
- 檢查 SECRET_KEY 是否一致
- 檢查 token 是否正確傳遞（Header: Authorization: Bearer <token>）

### AI 協作技巧

**高效 Prompt 範例**:
```
【明確的需求】實作用戶註冊 API
【技術約束】使用 FastAPI, SQLAlchemy, bcrypt
【測試要求】包含 4 個測試案例（成功、格式錯誤、密碼太短、重複 Email）
【代碼風格】遵循 PEP 8, 使用 type hints
【預期產出】完整的文件路徑和代碼

請按照 TDD 順序：先生成測試，再生成實作。
```

### 階段驗收
- ✅ 所有測試通過 (`pytest -v`)
- ✅ 測試覆蓋率 ≥ 80%
- ✅ Swagger UI 可以手動測試所有 API
- ✅ 無安全漏洞（Bandit 掃描通過）
- ✅ 代碼格式化（Black）
- ✅ 可以完成完整的用戶註冊→登入→創建任務→查詢任務流程

---

## 階段 3: 前端開發 (1 小時) [可選]

### 目標
- 快速搭建簡單但完整的 Web UI
- 連接後端 API
- 實作基本的用戶體驗

### 工具
- Cursor (快速 UI 開發)
- React + Tailwind CSS

### 策略
**不追求完美，追求可用**：
- 使用 Cursor 快速生成組件
- 使用 Tailwind CSS 快速樣式
- 專注功能實現，不糾結 UI 細節

### 子階段 3.1: 基礎架構 (15 分鐘)

#### Step 3.1.1: 配置 Axios 與 Auth Context (5 min)

**提示詞** (Cursor):
```
創建 API 服務層和認證 Context。

1. src/services/api.js
   - Axios instance
   - Base URL: http://localhost:8000
   - Request interceptor (自動添加 JWT token)
   - Response interceptor (處理 401 錯誤)

2. src/contexts/AuthContext.jsx
   - 提供 login, register, logout 方法
   - 存儲 token 到 localStorage
   - 提供 currentUser 狀態
```

#### Step 3.1.2: 路由設置 (5 min)

**提示詞** (Cursor):
```
使用 React Router 設置路由。

路由結構:
- / → Login/Register
- /dashboard → Dashboard (需登入)
- /tasks → Task List (需登入)
- /tasks/:id → Task Detail (需登入)

包含 PrivateRoute 組件（檢查登入狀態）
```

#### Step 3.1.3: 通用組件 (5 min)

**提示詞** (Cursor):
```
創建通用 UI 組件：

1. Navbar.jsx
   - Logo, 用戶名, 登出按鈕
   - Tailwind 樣式

2. Loading.jsx
   - 簡單的 spinner

3. ErrorMessage.jsx
   - 顯示錯誤訊息的組件
```

### 子階段 3.2: 頁面組件開發 (35 分鐘)

#### Step 3.2.1: 登入/註冊頁面 (10 min)

**提示詞** (Cursor):
```
創建登入和註冊頁面。

要求:
1. 使用 Tailwind CSS
2. 表單驗證（前端驗證）
3. 錯誤提示
4. 登入成功後跳轉到 /dashboard

組件:
- src/components/Auth/Login.jsx
- src/components/Auth/Register.jsx
```

#### Step 3.2.2: Dashboard 頁面 (10 min)

**提示詞** (Cursor):
```
創建 Dashboard 頁面。

功能:
1. 調用 GET /api/dashboard/stats
2. 顯示 4 個統計卡片:
   - 總任務數
   - 待辦任務
   - 進行中任務
   - 已完成任務
3. 使用 Recharts 或簡單的 CSS 顯示優先級分佈
4. 「創建任務」按鈕

使用 Tailwind CSS 美化。
```

#### Step 3.2.3: 任務列表頁面 (10 min)

**提示詞** (Cursor):
```
創建任務列表頁面。

功能:
1. 調用 GET /api/tasks
2. 顯示任務列表（卡片式）
3. 過濾器（狀態、優先級）
4. 排序選擇器
5. 每個任務卡片:
   - 標題, 優先級標籤, 狀態標籤, 截止日期
   - 編輯按鈕, 刪除按鈕
6. 分頁控制

組件:
- src/components/Tasks/TaskList.jsx
- src/components/Tasks/TaskItem.jsx
```

#### Step 3.2.4: 任務表單（創建/編輯） (5 min)

**提示詞** (Cursor):
```
創建任務表單組件。

功能:
1. 可用於創建和編輯
2. 欄位: 標題, 描述, 優先級, 截止日期, 狀態（編輯時）
3. 表單驗證
4. 提交到 POST /api/tasks 或 PUT /api/tasks/{id}

使用 Modal 或獨立頁面。
```

### 子階段 3.3: API 整合測試 (10 分鐘)

#### Step 3.3.1: 測試完整流程 (10 min)

```bash
# 同時啟動後端和前端
# Terminal 1
cd backend
uvicorn app.main:app --reload

# Terminal 2
cd frontend
npm start
```

**手動測試清單**:
- [ ] 註冊新用戶
- [ ] 登入
- [ ] 查看 Dashboard
- [ ] 創建任務
- [ ] 查看任務列表
- [ ] 編輯任務
- [ ] 刪除任務
- [ ] 登出

### 產出物
- [ ] 5 個頁面組件
- [ ] API 服務層
- [ ] 認證系統
- [ ] 響應式 UI（基本）

### 關鍵決策點

**決策 1: 用 Cursor 還是手寫？**
- **建議**: Cursor 生成初版，手動調整細節

**決策 2: UI 框架選擇**
- **建議**: Tailwind CSS（快速，無需額外學習組件庫）

**決策 3: 狀態管理**
- **建議**: Context API 足夠（避免 Redux 複雜性）

### 階段驗收
- ✅ 可以完成完整的用戶流程
- ✅ UI 基本可用（不要求美觀）
- ✅ API 呼叫正常
- ✅ 錯誤處理正確

---

## 階段 4: CI/CD 設置 (30 分鐘)

### 目標
- 建立自動化測試流程
- 設置安全掃描
- 配置 Docker 部署
- 實現持續集成

### 工具
- GitHub Actions
- Docker
- Bandit, Safety

### 子階段 4.1: GitHub Actions Workflow (15 分鐘)

#### Step 4.1.1: 創建 CI Workflow (15 min)

**提示詞** (Claude Code):
```
創建 GitHub Actions workflow 用於 CI。

要求:
1. Trigger: push 到 main, pull_request
2. Jobs:
   a) Backend Testing
      - Setup Python 3.10
      - Install dependencies (poetry)
      - Run pytest
      - Upload coverage report
   b) Backend Security Scan
      - Run bandit (security linter)
      - Run safety (dependency vulnerability check)
   c) Frontend Build (可選)
      - Setup Node.js 18
      - npm install
      - npm run build
3. 只有所有 jobs 通過才算成功

生成到 .github/workflows/ci.yml
```

**測試 Workflow**:
```bash
# Push 到 GitHub
git add .
git commit -m "ci: add GitHub Actions workflow"
git push origin main

# 查看 GitHub Actions 頁面
```

### 子階段 4.2: Docker 配置 (10 分鐘)

#### Step 4.2.1: 後端 Dockerfile (5 min)

**提示詞** (Claude Code):
```
為後端創建生產環境 Dockerfile。

要求:
1. Base image: python:3.10-slim
2. 使用 Poetry 安裝依賴
3. 多階段構建（減小鏡像大小）
4. 非 root 用戶運行
5. Health check

生成到 backend/Dockerfile
```

#### Step 4.2.2: 生產 Docker Compose (5 min)

**提示詞** (Claude Code):
```
創建生產環境 docker-compose.yml。

服務:
1. postgres (持久化 volume)
2. backend (構建自 Dockerfile)
3. nginx (反向代理，可選)

包含:
- 重啟策略
- 健康檢查
- 日誌配置
- 環境變數從 .env 讀取

生成到 docker-compose.prod.yml
```

**測試**:
```bash
# 本地測試生產配置
docker-compose -f docker-compose.prod.yml build
docker-compose -f docker-compose.prod.yml up -d
```

### 子階段 4.3: 部署設置 (5 分鐘) [可選]

#### Step 4.3.1: 部署到 Railway/Render (5 min)

**Railway 部署**:
```bash
# 安裝 Railway CLI
npm install -g @railway/cli

# 登入
railway login

# 初始化
railway init

# 部署
railway up
```

**或使用 Claude Code 生成部署文檔**:
```
創建部署指南。

內容:
1. 環境變數設置
2. 數據庫遷移步驟
3. 部署命令
4. 健康檢查驗證
5. 常見部署問題排查

生成到 docs/deployment.md
```

### 產出物
- [ ] GitHub Actions workflow
- [ ] 生產 Dockerfile
- [ ] Docker Compose 生產配置
- [ ] 部署文檔

### 階段驗收
- ✅ GitHub Actions 所有 checks 通過
- ✅ Docker image 可以構建
- ✅ 本地 Docker 環境運行正常
- ✅ 有清晰的部署文檔

---

## 階段 5: 文檔與交付 (20 分鐘)

### 目標
- 生成完整的 API 文檔
- 撰寫部署與維護文檔
- 整理專案 README

### 子階段 5.1: API 文檔 (10 分鐘)

#### Step 5.1.1: 增強 Swagger/OpenAPI 文檔 (10 min)

**提示詞** (Claude Code):
```
為所有 API endpoints 添加詳細的文檔字串。

要求:
1. 每個 endpoint 包含:
   - 功能描述
   - 請求參數說明
   - 響應示例
   - 錯誤碼說明
2. 使用 FastAPI 的 description, response_description
3. 為 Pydantic schemas 添加 example

更新所有 routers/*.py 文件。
```

**驗證**:
```bash
uvicorn app.main:app --reload
open http://localhost:8000/docs
# 確認文檔完整且清晰
```

### 子階段 5.2: 專案文檔 (10 分鐘)

#### Step 5.2.1: 撰寫 README.md (5 min)

**提示詞** (Claude Code):
```
生成專案主 README.md。

包含:
1. 專案簡介
2. 功能列表
3. 技術棧
4. 快速開始
   - 環境要求
   - 安裝步驟
   - 運行步驟
5. API 文檔連結
6. 測試
7. 部署
8. 授權

風格: 專業、清晰、包含程式碼示例
```

#### Step 5.2.2: 開發者文檔 (5 min)

**提示詞** (Claude Code):
```
生成 docs/development.md 開發者指南。

包含:
1. 專案結構說明
2. 開發工作流程
3. 如何添加新 API endpoint
4. 測試編寫指南
5. 代碼風格規範
6. 常見問題

生成到 docs/development.md
```

### 產出物
- [ ] 完整的 Swagger API 文檔
- [ ] 專案 README.md
- [ ] 開發者文檔
- [ ] 部署文檔

### 階段驗收
- ✅ README 清晰，新人能按照步驟運行專案
- ✅ API 文檔完整，可直接用於前端對接
- ✅ 開發者文檔詳細，團隊成員能快速上手

---

## 🎉 專案完成檢查清單

### 功能完整性
- [ ] 9 個 API endpoints 全部實作
- [ ] 用戶註冊/登入流程正常
- [ ] 任務 CRUD 操作正常
- [ ] Dashboard 統計正確
- [ ] 權限控制正確（用戶只能操作自己的任務）

### 代碼質量
- [ ] 測試覆蓋率 ≥ 80%
- [ ] 所有測試通過
- [ ] 通過 Linting (flake8)
- [ ] 代碼格式化 (black)
- [ ] 無安全漏洞 (bandit, safety)

### 部署就緒
- [ ] Docker Compose 可以一鍵啟動
- [ ] GitHub Actions CI 通過
- [ ] 環境變數正確配置
- [ ] 數據庫遷移腳本完整

### 文檔完整
- [ ] README.md 清晰
- [ ] API 文檔完整 (Swagger)
- [ ] 部署文檔詳細
- [ ] 開發者指南完整

### 最終驗證
```bash
# 1. 運行所有測試
pytest -v --cov=app

# 2. 安全掃描
bandit -r app/ -ll
safety check

# 3. 啟動完整系統
docker-compose up -d

# 4. 手動測試關鍵流程
# 5. 檢查 GitHub Actions 狀態
```

---

## 時間回顧與反思

完成專案後，花 10 分鐘反思：

### 反思問題
1. **哪個階段最花時間？為什麼？**
2. **AI 在哪個地方幫助最大？**
3. **遇到最大的困難是什麼？如何解決的？**
4. **如果重來一次，會調整哪個流程？**
5. **學到最重要的三件事是什麼？**

### 記錄學習筆記
```markdown
## 專案完成筆記

**實際完成時間**: X 小時

### 時間分配
- 階段 0: X min
- 階段 1: X min
- 階段 2: X min
- 階段 3: X min
- 階段 4: X min
- 階段 5: X min

### 最有效的 AI Prompts
1. [記錄你最常用的 prompt]
2. [...]

### 遇到的問題與解決方法
1. 問題: [描述]
   解決: [描述]
2. [...]

### 下次可以改進的地方
1. [...]
2. [...]
```

---

## 下一步行動

完成 MVP 後，你可以：

### 短期（1 週內）
- [ ] 部署到雲端平台
- [ ] 添加監控與日誌
- [ ] 挑戰「進階擴展」功能

### 中期（1 個月內）
- [ ] 用相同流程開發另一個專案
- [ ] 寫技術文章分享經驗
- [ ] 建立個人專案模板

### 長期（3 個月內）
- [ ] 參與開源專案貢獻
- [ ] 在工作中應用 AI 協作技能
- [ ] 教別人你的工作流程

---

**恭喜你完成了完整的開發流程！**

你現在擁有：
✅ 一個完整的企業級專案
✅ 可複製的開發工作流程
✅ AI 協作的實戰經驗
✅ 全棧開發的系統化理解

**這就是情境驅動學習的力量！** 🚀
