# AI 協作提示詞庫
# Effective Prompts for Task Management System Development

**用途**: 精選的、經過實戰驗證的 AI 提示詞，用於各開發階段
**目標**: 提升 AI 協作效率，避免模糊或無效的提問
**原則**: 明確需求、提供上下文、指定輸出格式

---

## 提示詞設計原則

### 好提示詞的特徵

```
✅ 【好提示詞】
明確的目標 + 技術約束 + 預期產出 + 格式要求

範例:
"為用戶註冊 API 編寫 pytest 測試。
技術棧: FastAPI + SQLAlchemy + PostgreSQL
測試案例:
1. 成功註冊 (201)
2. Email 格式錯誤 (422)
3. 密碼太短 (422)
4. 重複 Email (409)
使用 TestClient，生成到 tests/test_auth.py"

---

❌ 【差提示詞】
模糊、缺乏上下文、沒有明確產出

範例:
"幫我寫個註冊功能"
（太模糊，AI 不知道你要什麼）
```

### 提示詞結構模板

```
【背景】[專案/功能背景]
【目標】[要完成什麼]
【技術約束】[使用的技術/框架/版本]
【具體要求】
1. [要求 1]
2. [要求 2]
3. [...]
【預期產出】[檔案路徑、代碼格式、文檔結構等]
【額外需求】[測試、文檔、錯誤處理等]
```

---

## 階段 0: 準備與規劃

### 0.1 分析 PRD 生成技術方案

```prompt
【背景】
我有一份任務管理系統的 PRD (Product Requirements Document)，需要將其轉化為可執行的技術方案。

【PRD 內容】
[貼上 PRD 完整內容或關鍵部分]

【需要你提供】
1. 技術架構建議
   - 後端框架選擇與理由
   - 前端框架選擇與理由
   - 數據庫選擇與理由
   - 認證方案設計
2. 數據庫 Schema 設計
   - 表結構（欄位、類型、約束）
   - 關聯關係
   - 索引設計
3. API 端點設計
   - 方法、路徑、功能
   - 請求/響應格式
   - 認證要求
4. 前端頁面結構
   - 路由設計
   - 組件層級
   - 狀態管理方案
5. 開發優先級建議
   - 哪些功能先做（MVP 範圍）
   - 哪些功能可延後
6. 潛在技術風險與緩解方案

【輸出格式】
Markdown 文檔，包含清晰的章節標題和代碼示例（如需要）
```

**使用時機**: 專案開始時，拿到 PRD 後的第一步
**預期時間**: 5-10 分鐘（AI 生成 + 你審查）
**後續行動**: 將生成的方案保存為 `docs/architecture.md`

---

### 0.2 生成開發路線圖

```prompt
【背景】
基於我們的技術架構方案，需要生成一份可執行的開發路線圖。

【專案資訊】
- 後端: FastAPI + PostgreSQL + SQLAlchemy
- 前端: React (可選)
- 功能: 用戶認證、任務 CRUD、Dashboard 統計
- 目標時間: 6 小時

【需要你提供】
1. 將開發分解成 20-30 個可執行的小任務
2. 每個任務包含:
   - 任務名稱（清晰明確）
   - 預計時間（15min, 30min, 1h 等）
   - 前置依賴（需要先完成哪些任務）
   - 驗收標準（如何判斷完成）
   - 建議使用的開發方法（TDD, AI 生成等）
3. 標示出 3-5 個關鍵里程碑
4. 建議使用 TDD 的部分（需要高質量保證的）

【輸出格式】
Markdown checklist，使用層級結構:
## 階段 1: XXX (預計 Xh)
- [ ] 任務 1 (30min) - 前置: 無 - TDD ✓
  驗收: [標準]
- [ ] 任務 2 (15min) - 前置: 任務 1
  驗收: [標準]
```

**使用時機**: 技術方案確定後，開始編碼前
**預期時間**: 5 分鐘
**後續行動**: 保存為 `docs/roadmap.md`，開發過程中勾選完成項

---

## 階段 1: 專案初始化

### 1.1 生成專案目錄結構

```prompt
【目標】
為 FastAPI + React 專案生成完整的目錄結構。

【技術棧】
- 後端: FastAPI, PostgreSQL, SQLAlchemy, Pytest
- 前端: React, Axios, Tailwind CSS
- DevOps: Docker, GitHub Actions

【結構要求】
1. 前後端分離（backend/ 和 frontend/）
2. 後端結構:
   - app/ (應用代碼)
     - models/ (SQLAlchemy models)
     - schemas/ (Pydantic schemas)
     - routers/ (API endpoints)
     - services/ (業務邏輯)
     - utils/ (工具函數)
   - tests/ (測試代碼)
   - alembic/ (數據庫遷移)
3. 前端結構:
   - src/
     - components/ (React 組件，按功能分資料夾)
     - services/ (API 呼叫)
     - contexts/ (React Context)
4. 根目錄:
   - docker-compose.yml
   - .github/workflows/
   - docs/

【輸出格式】
1. 完整的目錄樹結構（tree 格式）
2. 每個關鍵目錄的用途說明
3. 需要創建的空檔案列表（__init__.py, README.md 等）
```

**使用時機**: 專案開始，準備創建目錄前
**預期時間**: 3 分鐘
**後續行動**:
```bash
# 使用 AI 輸出創建目錄
mkdir -p backend/app/{models,schemas,routers,services,utils}
# ... 依據 AI 建議創建所有目錄
```

---

### 1.2 生成 pyproject.toml (Poetry)

```prompt
【目標】
為 FastAPI 後端專案生成 pyproject.toml 配置檔。

【專案資訊】
- 專案名稱: task-management-backend
- Python 版本: ^3.10
- 用途: RESTful API for task management

【依賴需求】
核心依賴:
- fastapi = "^0.104.0"
- uvicorn[standard] = "^0.24.0"
- sqlalchemy = "^2.0.0"
- psycopg2-binary = "^2.9.0"
- alembic = "^1.12.0"
- pyjwt = "^2.8.0"
- passlib[bcrypt] = "^1.7.4"
- python-dotenv = "^1.0.0"
- pydantic = "^2.0.0"
- pydantic-settings = "^2.0.0"

開發依賴:
- pytest = "^7.4.0"
- pytest-asyncio = "^0.21.0"
- pytest-cov = "^4.1.0"
- black = "^23.0.0"
- flake8 = "^6.1.0"
- bandit = "^1.7.5"
- safety = "^2.3.0"

【輸出格式】
完整的 pyproject.toml 檔案內容，包含:
1. [tool.poetry] section (metadata)
2. [tool.poetry.dependencies]
3. [tool.poetry.dev-dependencies]
4. [build-system]
5. [tool.pytest.ini_options] (pytest 配置)
6. [tool.black] (格式化配置)
```

**使用時機**: 後端目錄結構建立後
**預期時間**: 2 分鐘
**後續行動**:
```bash
cd backend
# 將 AI 輸出保存為 pyproject.toml
poetry install
```

---

### 1.3 生成 Docker Compose 配置

```prompt
【目標】
為本地開發環境生成 docker-compose.yml。

【服務需求】
1. PostgreSQL 14
   - 容器名: taskdb
   - 端口: 5432:5432
   - 數據庫: taskdb
   - 用戶: taskuser
   - 密碼: taskpass
   - Volume: postgres_data（持久化）
   - 健康檢查: pg_isready
2. Backend (FastAPI) [可選，初期可手動運行]
   - 容器名: task-backend
   - 端口: 8000:8000
   - 依賴: PostgreSQL
   - 環境變數從 .env 讀取
   - Volume: ./backend:/app (代碼同步)
   - 命令: uvicorn app.main:app --host 0.0.0.0 --reload

【配置要求】
- 使用 version: "3.8"
- 所有服務使用 restart: unless-stopped
- 網路: 自定義 network (tasknet)
- 環境變數支援 .env 檔案

【輸出格式】
完整的 docker-compose.yml 檔案
```

**使用時機**: 專案初始化階段，準備啟動本地數據庫
**預期時間**: 3 分鐘
**後續行動**:
```bash
# 將 AI 輸出保存為 docker-compose.yml
docker-compose up -d postgres
docker-compose ps  # 確認運行
```

---

## 階段 2: 後端開發 (TDD)

### 2.1 數據庫 Models 設計

```prompt
【目標】
為任務管理系統設計 SQLAlchemy models。

【數據模型需求】
1. User 表
   - id: Integer, PK, autoincrement
   - email: String(255), unique, not null
   - password_hash: String(255), not null
   - username: String(100), not null
   - created_at: DateTime, default=now
   - updated_at: DateTime, auto-update

2. Task 表
   - id: Integer, PK, autoincrement
   - title: String(200), not null
   - description: Text, nullable
   - status: Enum('TODO', 'IN_PROGRESS', 'DONE'), default='TODO'
   - priority: Enum('LOW', 'MEDIUM', 'HIGH', 'URGENT'), default='MEDIUM'
   - due_date: Date, nullable
   - created_by: Integer, FK(User.id), not null
   - created_at: DateTime, default=now
   - updated_at: DateTime, auto-update
   - is_deleted: Boolean, default=False

【技術要求】
- 使用 SQLAlchemy 2.0 語法
- 使用 declarative_base
- 定義關聯關係: User.tasks (1-N)
- 為查詢優化添加索引:
  - Task.created_by
  - Task.status
  - Task.priority
- 包含 __repr__ 方法便於除錯

【輸出格式】
兩個檔案的完整代碼:
1. backend/app/models/user.py
2. backend/app/models/task.py

包含必要的 imports 和清晰的註解。
```

**使用時機**: 專案初始化完成，開始後端開發
**預期時間**: 10 分鐘
**後續行動**:
- 保存生成的代碼
- 創建數據庫遷移: `alembic revision --autogenerate -m "initial models"`
- 執行遷移: `alembic upgrade head`

---

### 2.2 TDD: 用戶註冊 API - 測試階段

```prompt
【目標】
為用戶註冊 API 編寫完整的 pytest 測試（TDD 第一步）。

【API 規格】
- 端點: POST /api/auth/register
- 請求體: {"email": str, "password": str, "username": str}
- 成功響應 (201): {"id": int, "email": str, "username": str, "created_at": str}
- 錯誤響應: {"error": {"code": str, "message": str}}

【測試案例】
1. test_register_success
   - 發送有效數據
   - 預期: 201, 返回用戶資訊（不含密碼）
   - 驗證: 數據庫中有新用戶

2. test_register_invalid_email
   - Email 格式錯誤 ("invalid-email")
   - 預期: 422, 錯誤訊息提示格式錯誤

3. test_register_password_too_short
   - 密碼少於 8 字元 ("123")
   - 預期: 422, 錯誤訊息提示密碼太短

4. test_register_duplicate_email
   - 先註冊一個用戶，再用相同 Email 註冊
   - 預期: 409, 錯誤訊息提示 Email 已存在

【技術要求】
- 使用 FastAPI TestClient
- 使用 pytest fixtures (例如 client, test_db)
- 測試數據庫隔離（每個測試獨立）
- 包含清晰的測試文檔字串

【輸出格式】
完整的 backend/tests/test_auth.py 檔案（僅包含註冊測試）
包含:
- 必要的 imports
- pytest fixtures (conftest.py 如需要)
- 4 個測試函數，每個都有文檔字串和 assertions
```

**使用時機**: 準備開發註冊功能時（TDD 第一步：先寫測試）
**預期時間**: 10 分鐘
**後續行動**:
```bash
# 運行測試（預期失敗）
pytest tests/test_auth.py::test_register_success -v
# 看到 ❌ FAILED，確認測試設計正確，然後寫實作
```

---

### 2.3 TDD: 用戶註冊 API - 實作階段

```prompt
【目標】
實作用戶註冊 API，讓上述測試通過（TDD 第二步）。

【測試狀態】
測試已寫好在 tests/test_auth.py，目前全部 FAILED。

【實作需求】
1. Pydantic Schemas (backend/app/schemas/user.py)
   - UserCreate (請求): email, password, username
     - email 驗證: EmailStr
     - password 驗證: min_length=8, 需包含字母和數字
     - username: min_length=2, max_length=100
   - UserResponse (響應): id, email, username, created_at
     - 不包含 password_hash

2. 密碼加密工具 (backend/app/utils/security.py)
   - get_password_hash(password: str) -> str
   - verify_password(plain: str, hashed: str) -> bool
   - 使用 passlib 的 bcrypt

3. 業務邏輯 (backend/app/services/auth_service.py)
   - async def register_user(db: Session, user_data: UserCreate) -> User
   - 檢查 Email 是否存在
   - 加密密碼
   - 創建用戶
   - 返回用戶物件

4. API Endpoint (backend/app/routers/auth.py)
   - @router.post("/register", response_model=UserResponse, status_code=201)
   - 呼叫 auth_service.register_user
   - 錯誤處理:
     - 422: 驗證失敗 (Pydantic 自動處理)
     - 409: Email 已存在 (手動拋出 HTTPException)

【技術約束】
- 使用 FastAPI 的依賴注入 (Depends)
- 異步函數 (async def)
- 正確的錯誤碼和訊息

【輸出格式】
4 個完整的檔案代碼:
1. schemas/user.py
2. utils/security.py
3. services/auth_service.py
4. routers/auth.py

每個檔案包含必要的 imports 和註解。
```

**使用時機**: 測試寫完並確認失敗後（TDD 第二步：寫實作）
**預期時間**: 15 分鐘
**後續行動**:
```bash
# 保存所有生成的代碼
# 運行測試（預期通過）
pytest tests/test_auth.py -v
# 看到 ✅ PASSED，繼續下一個功能
```

---

### 2.4 TDD: 用戶登入 API（完整循環）

```prompt
【目標】
使用 TDD 方法實作用戶登入 API（先測試，後實作）。

【API 規格】
- 端點: POST /api/auth/login
- 請求體: {"email": str, "password": str}
- 成功響應 (200): {"access_token": str, "token_type": "bearer", "expires_in": int}
- 錯誤響應 (401): {"error": {"code": "INVALID_CREDENTIALS", "message": "..."}}

【第一步: 寫測試】
測試案例:
1. test_login_success
   - 先註冊用戶，再用正確憑證登入
   - 預期: 200, 返回 JWT token
2. test_login_wrong_password
   - 錯誤密碼
   - 預期: 401
3. test_login_nonexistent_email
   - 不存在的 Email
   - 預期: 401
4. test_token_validation
   - 用返回的 token 呼叫需認證的 API (GET /api/auth/me)
   - 預期: 200, 返回用戶資訊

生成: tests/test_auth.py (新增登入測試)

【第二步: 寫實作】
實作檔案:
1. schemas/user.py (新增)
   - UserLogin: email, password
   - Token: access_token, token_type, expires_in

2. utils/security.py (新增)
   - create_access_token(user_id: int) -> str
   - decode_access_token(token: str) -> int (返回 user_id)
   - 使用 PyJWT
   - Token 有效期: 從環境變數讀取 JWT_EXPIRATION_DAYS

3. services/auth_service.py (新增)
   - async def login_user(db, email, password) -> str
   - 驗證憑證
   - 生成 token

4. routers/auth.py (新增)
   - @router.post("/login")
   - 登入 endpoint

5. utils/dependencies.py (新增)
   - async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User
   - 用於需要認證的 endpoints

6. routers/auth.py (新增)
   - @router.get("/me")
   - 使用 Depends(get_current_user)

【輸出順序】
1. 先輸出測試代碼
2. 說明「運行測試應該失敗」
3. 再輸出實作代碼
4. 說明「運行測試應該通過」

【技術要求】
- JWT 配置從環境變數讀取
- Token 格式: Bearer <token>
- 密碼驗證使用 bcrypt
```

**使用時機**: 註冊功能完成並測試通過後
**預期時間**: 20 分鐘
**後續行動**:
```bash
# 1. 保存測試代碼
# 2. 運行測試 → ❌ FAILED
pytest tests/test_auth.py -k login -v
# 3. 保存實作代碼
# 4. 運行測試 → ✅ PASSED
pytest tests/test_auth.py -k login -v
```

---

### 2.5 批量生成任務 CRUD APIs

```prompt
【目標】
一次性生成任務管理的 5 個 CRUD API（使用 TDD 方法）。

【APIs 列表】
1. POST /api/tasks - 創建任務
2. GET /api/tasks - 查詢任務列表（支援過濾、排序、分頁）
3. GET /api/tasks/{id} - 查詢單一任務
4. PUT /api/tasks/{id} - 更新任務
5. DELETE /api/tasks/{id} - 刪除任務（軟刪除）

【權限規則】
- 所有 API 需要認證（使用 get_current_user）
- 用戶只能操作自己創建的任務
- 查詢列表默認只返回當前用戶的任務

【第一步: 生成完整測試】
為每個 API 生成測試案例，測試覆蓋:
- 成功案例
- 驗證失敗（缺少欄位、無效值）
- 權限失敗（操作他人任務）
- 404 (資源不存在)

生成: tests/test_tasks.py (完整的 20+ 測試案例)

【第二步: 生成實作代碼】
1. schemas/task.py
   - TaskCreate: title, description, priority, due_date
   - TaskUpdate: title?, description?, status?, priority?, due_date?
   - TaskResponse: 完整任務資訊
   - TaskListResponse: 任務列表 + 分頁資訊

2. services/task_service.py
   - create_task(db, task_data, user_id)
   - get_tasks(db, user_id, status?, priority?, sort_by?, page?, limit?)
   - get_task_by_id(db, task_id, user_id) - 檢查權限
   - update_task(db, task_id, task_data, user_id) - 檢查權限
   - delete_task(db, task_id, user_id) - 檢查權限，軟刪除

3. routers/tasks.py
   - 5 個 endpoints
   - 使用 Depends(get_current_user) 獲取當前用戶
   - 權限檢查
   - 錯誤處理 (404, 403)

【查詢 API 特殊要求】
GET /api/tasks 支援 query parameters:
- status: Enum (TODO, IN_PROGRESS, DONE)
- priority: Enum (LOW, MEDIUM, HIGH, URGENT)
- sort_by: Enum (created_at, updated_at, due_date, priority)
- order: Enum (asc, desc), default=desc
- page: int, default=1
- limit: int, default=20

【輸出格式】
1. 先輸出完整測試代碼 (tests/test_tasks.py)
2. 再輸出實作代碼（schemas, services, routers）
3. 附上運行指令

【預期結果】
- 20+ 個測試案例
- 5 個 API endpoints
- 完整的權限控制
- 支援分頁與過濾
```

**使用時機**: 用戶認證完成後，開始核心功能開發
**預期時間**: 30-40 分鐘
**後續行動**:
```bash
# 分批運行測試，逐個修復
pytest tests/test_tasks.py::test_create_task -v
pytest tests/test_tasks.py::test_list_tasks -v
# ... 依次驗證
```

---

## 階段 3: 前端開發（可選）

### 3.1 生成 API 服務層

```prompt
【目標】
為 React 前端創建 API 服務層。

【技術棧】
- Axios
- TypeScript (或 JavaScript)
- Token 存儲: localStorage

【需要生成】
1. src/services/api.js
   - 創建 Axios instance
   - baseURL: 從環境變數讀取 (REACT_APP_API_BASE_URL)
   - Request interceptor: 自動添加 JWT token (從 localStorage)
   - Response interceptor:
     - 401 錯誤: 自動清除 token，跳轉到登入頁
     - 其他錯誤: 統一格式化錯誤訊息

2. src/services/authService.js
   - register(email, password, username) -> Promise
   - login(email, password) -> Promise
   - logout() - 清除 token
   - getCurrentUser() -> Promise
   - getToken() / setToken() / removeToken()

3. src/services/taskService.js
   - createTask(taskData) -> Promise
   - getTasks(filters) -> Promise
   - getTaskById(id) -> Promise
   - updateTask(id, taskData) -> Promise
   - deleteTask(id) -> Promise

【錯誤處理】
- 所有函數捕獲錯誤並返回統一格式:
  { error: { code, message } }

【輸出格式】
3 個完整的 JavaScript 檔案
```

**使用時機**: 前端開發開始時，先建立 API 層
**預期時間**: 10 分鐘
**後續行動**: 測試 API 呼叫是否正常

---

### 3.2 快速生成 React 登入頁面

```prompt
【目標】
用 Cursor 或 Claude Code 快速生成登入/註冊頁面。

【設計要求】
- 使用 Tailwind CSS
- 包含登入和註冊兩個 Tab
- 響應式設計
- 表單驗證（前端驗證）
- Loading 狀態
- 錯誤提示

【功能需求】
1. 登入表單
   - Email input (type=email)
   - Password input (type=password)
   - 登入按鈕
   - 切換到註冊的連結

2. 註冊表單
   - Email input
   - Username input
   - Password input
   - 確認密碼 input
   - 註冊按鈕
   - 切換到登入的連結

3. 邏輯
   - 表單提交呼叫 authService
   - 成功: 保存 token，跳轉到 /dashboard
   - 失敗: 顯示錯誤訊息

【組件結構】
src/components/Auth/
  - AuthPage.jsx (父組件，包含 Tab 切換)
  - LoginForm.jsx
  - RegisterForm.jsx

【輸出格式】
3 個完整的 React 組件，包含 Tailwind classes
```

**使用時機**: API 服務層完成後，開始 UI 開發
**預期時間**: 15 分鐘（Cursor 生成 + 調整）
**後續行動**: 測試登入/註冊流程

---

## 階段 4: CI/CD 設置

### 4.1 生成 GitHub Actions Workflow

```prompt
【目標】
創建 GitHub Actions workflow 用於持續集成。

【Workflow 需求】
觸發條件:
- push 到 main 分支
- pull_request 到 main 分支

Jobs:
1. backend-test (運行後端測試)
   - 使用 Python 3.10
   - 安裝 Poetry
   - 安裝依賴
   - 運行 pytest (包含覆蓋率)
   - 上傳覆蓋率報告到 Codecov (可選)

2. backend-security (安全掃描)
   - 運行 bandit (安全 linter)
   - 運行 safety check (依賴漏洞檢查)
   - 失敗則阻止合併

3. backend-lint (代碼品質)
   - 運行 flake8
   - 運行 black --check

4. frontend-build (可選，如有前端)
   - 使用 Node.js 18
   - npm install
   - npm run build
   - 確認構建成功

【技術要求】
- 使用 GitHub Actions 官方 actions (setup-python, setup-node)
- 使用 cache 加速依賴安裝
- 所有 jobs 並行運行
- 提供清晰的 job 名稱和步驟名稱

【輸出格式】
完整的 .github/workflows/ci.yml 檔案
```

**使用時機**: 後端開發完成，準備部署前
**預期時間**: 10 分鐘
**後續行動**:
```bash
git add .github/workflows/ci.yml
git commit -m "ci: add GitHub Actions workflow"
git push origin main
# 查看 GitHub Actions 頁面確認運行
```

---

### 4.2 生成生產環境 Dockerfile

```prompt
【目標】
為後端創建生產環境 Dockerfile。

【要求】
1. 多階段構建
   - Stage 1: builder (安裝依賴)
   - Stage 2: runtime (複製依賴，運行應用)

2. 優化鏡像大小
   - 使用 python:3.10-slim 作為 base
   - 只複製必要檔案
   - 清理緩存

3. 安全性
   - 使用非 root 用戶運行
   - 最小權限

4. 健康檢查
   - 檢查 /health endpoint

5. 環境變數
   - DATABASE_URL
   - JWT_SECRET_KEY
   - 其他配置從環境變數讀取

【技術細節】
- 使用 Poetry 安裝依賴
- 暴露端口 8000
- CMD: uvicorn app.main:app --host 0.0.0.0 --port 8000

【輸出格式】
完整的 backend/Dockerfile，包含註解說明每個步驟
```

**使用時機**: 準備部署時
**預期時間**: 5 分鐘
**後續行動**:
```bash
cd backend
docker build -t task-backend:latest .
docker run -p 8000:8000 --env-file .env task-backend:latest
```

---

## 階段 5: 文檔生成

### 5.1 增強 API 文檔

```prompt
【目標】
為所有 API endpoints 添加詳細的文檔字串，增強 Swagger UI。

【需要更新的檔案】
- routers/auth.py
- routers/tasks.py
- routers/dashboard.py

【文檔要求】
每個 endpoint 包含:
1. 功能描述（summary）
2. 詳細說明（description）
3. 請求參數說明
4. 響應示例（成功和錯誤）
5. 錯誤碼列表

【範例格式】
```python
@router.post(
    "/register",
    response_model=UserResponse,
    status_code=201,
    summary="用戶註冊",
    description="創建新用戶帳號。Email 必須唯一，密碼需至少 8 字元。",
    responses={
        201: {
            "description": "註冊成功",
            "content": {
                "application/json": {
                    "example": {
                        "id": 1,
                        "email": "user@example.com",
                        "username": "John Doe"
                    }
                }
            }
        },
        409: {"description": "Email 已存在"}
    }
)
```

【輸出格式】
更新後的完整 router 檔案（3 個）
```

**使用時機**: 功能開發完成，準備交付前
**預期時間**: 15 分鐘
**後續行動**: 訪問 `http://localhost:8000/docs` 確認文檔完整

---

### 5.2 生成專案 README

```prompt
【目標】
為專案生成專業的 README.md。

【內容結構】
1. 專案標題與簡介
   - Logo (可選)
   - 一句話描述專案
   - 主要功能列表

2. 功能特性
   - 用戶認證（JWT）
   - 任務 CRUD
   - Dashboard 統計
   - RESTful API
   - 完整測試（80% 覆蓋率）
   - CI/CD

3. 技術棧
   - 後端、前端、數據庫、DevOps

4. 快速開始
   - 環境要求
   - 安裝步驟（逐步命令）
   - 運行步驟
   - 訪問地址

5. API 文檔
   - Swagger UI 連結
   - 主要 endpoints 列表

6. 測試
   - 運行測試命令
   - 查看覆蓋率命令

7. 部署
   - Docker 部署步驟
   - 環境變數說明

8. 專案結構
   - 目錄樹

9. 授權
   - MIT License

【風格】
- 專業、清晰
- 包含代碼示例
- 使用 badge (可選): ![Tests](url) ![Coverage](url)

【輸出格式】
完整的 README.md 檔案（Markdown 格式）
```

**使用時機**: 專案完成，準備交付或開源時
**預期時間**: 10 分鐘
**後續行動**: 將 README.md 放在專案根目錄

---

## 提示詞使用技巧總結

### 1. 提供足夠的上下文
```
❌ "幫我寫個 API"
✅ "為任務管理系統寫用戶註冊 API，使用 FastAPI + SQLAlchemy，
   需要包含 Email 驗證、密碼加密、重複檢查"
```

### 2. 明確技術約束
```
❌ "用 Python 寫"
✅ "使用 Python 3.10, FastAPI 0.104, SQLAlchemy 2.0, 異步語法"
```

### 3. 指定輸出格式
```
❌ "給我代碼"
✅ "生成完整的 Python 檔案，包含:
   - 必要的 imports
   - Type hints
   - Docstrings
   - 錯誤處理
   保存到 backend/app/services/auth_service.py"
```

### 4. 分步驟提問
```
不要: "一次生成整個專案"
改成:
1. 先生成數據模型
2. 再生成測試
3. 然後生成實作
4. 最後生成文檔
```

### 5. 驗證 AI 輸出
```
收到 AI 代碼後:
1. 先理解邏輯（不要盲目複製）
2. 檢查錯誤處理
3. 確認符合專案規範
4. 測試是否運行
5. 如有問題，追問 AI
```

---

## 模組關聯

本提示詞庫整合了：
- **Module 2 (CLI 工具)**: EPCV workflow 提示方法
- **Module 4 (TDD)**: 測試先行的提示策略
- **Module 9 (多工具協作)**: 不同階段選擇合適工具的提示
- **Module 10 (安全性)**: 安全檢查的提示詞

---

**記住**: 好的提示詞 = 明確需求 + 技術細節 + 預期產出

把這個提示詞庫當作「翻譯手冊」——你知道要什麼，AI 幫你生成代碼。
