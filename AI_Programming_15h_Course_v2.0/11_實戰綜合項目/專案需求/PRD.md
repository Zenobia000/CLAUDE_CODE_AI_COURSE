# Product Requirements Document (PRD)
# Task Management System - MVP Version

**文檔版本**: v1.0
**建立日期**: 2025-10-30
**產品經理**: [Your Name]
**開發時間**: 2 週（MVP）
**目標發布日期**: Week 2

---

## 1. 專案背景與目標

### 1.1 業務背景

**現狀問題**:
- 公司目前使用 Excel 管理團隊任務，效率低下
- 多人編輯時容易產生衝突
- 無法即時查看任務狀態
- 缺乏權限管理，任何人都能修改所有任務
- 無法追蹤任務歷史記錄

**業務需求**:
- 需要一個輕量級的任務管理工具
- 支援多用戶同時使用
- 清晰的任務狀態管理
- 基本的數據統計與視覺化
- 能夠快速部署與維護

**目標用戶**:
- 內部團隊成員（10-50 人）
- 技術水平：基本電腦操作能力
- 使用場景：日常任務追蹤與協作

### 1.2 產品目標

**主要目標**:
1. 替代現有的 Excel 任務管理流程
2. 提升團隊任務管理效率 30%
3. 減少任務遺漏與重複工作

**次要目標**:
1. 為未來功能擴展打下基礎
2. 建立可複用的技術架構
3. 培養團隊使用線上工具的習慣

### 1.3 成功指標 (KPIs)

| 指標 | 目標值 | 衡量方式 |
|-----|-------|---------|
| 用戶註冊率 | 80% 團隊成員 | 註冊數 / 總人數 |
| 日活用戶 | 60% | DAU / 註冊用戶 |
| 任務創建數 | > 50 tasks/week | 系統統計 |
| 用戶滿意度 | ≥ 4.0/5.0 | 問卷調查 |
| 系統可用性 | 99% | 監控系統 |

---

## 2. 功能需求

### 2.1 用戶管理

#### 2.1.1 用戶註冊
**功能描述**: 新用戶能夠註冊帳號

**詳細需求**:
- 必填欄位:
  - Email (唯一，作為登入帳號)
  - 密碼 (最短 8 字元，需包含字母與數字)
  - 用戶名稱 (顯示名稱)
- 驗證規則:
  - Email 格式驗證
  - 密碼強度檢查
  - 防止重複註冊
- 安全要求:
  - 密碼加密存儲 (bcrypt)
  - 不回傳明文密碼

**API Endpoint**:
```http
POST /api/auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "SecurePass123",
  "username": "John Doe"
}

Response 201:
{
  "id": 1,
  "email": "user@example.com",
  "username": "John Doe",
  "created_at": "2025-10-30T10:00:00Z"
}
```

#### 2.1.2 用戶登入
**功能描述**: 已註冊用戶能夠登入系統

**詳細需求**:
- 登入方式: Email + Password
- 返回 JWT token（有效期 7 天）
- 登入失敗提示（不透露具體原因，防止暴力破解）

**API Endpoint**:
```http
POST /api/auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "SecurePass123"
}

Response 200:
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 604800
}
```

#### 2.1.3 獲取當前用戶資訊
**功能描述**: 已登入用戶能查看自己的資料

**API Endpoint**:
```http
GET /api/auth/me
Authorization: Bearer <token>

Response 200:
{
  "id": 1,
  "email": "user@example.com",
  "username": "John Doe",
  "created_at": "2025-10-30T10:00:00Z"
}
```

---

### 2.2 任務管理 (核心功能)

#### 2.2.1 創建任務
**功能描述**: 用戶能夠創建新任務

**詳細需求**:
- 必填欄位:
  - 標題 (1-200 字元)
  - 描述 (可選，最多 2000 字元)
  - 優先級 (LOW / MEDIUM / HIGH / URGENT)
  - 截止日期 (可選)
- 自動欄位:
  - 創建者 (當前登入用戶)
  - 創建時間
  - 初始狀態 (TODO)

**API Endpoint**:
```http
POST /api/tasks
Authorization: Bearer <token>
Content-Type: application/json

{
  "title": "實作用戶認證功能",
  "description": "使用 JWT 實作登入/註冊功能",
  "priority": "HIGH",
  "due_date": "2025-11-05"
}

Response 201:
{
  "id": 1,
  "title": "實作用戶認證功能",
  "description": "使用 JWT 實作登入/註冊功能",
  "status": "TODO",
  "priority": "HIGH",
  "due_date": "2025-11-05",
  "created_by": 1,
  "created_at": "2025-10-30T10:00:00Z",
  "updated_at": "2025-10-30T10:00:00Z"
}
```

#### 2.2.2 查看任務列表
**功能描述**: 用戶能夠查看所有任務（分頁、過濾、排序）

**詳細需求**:
- 默認顯示: 當前用戶創建的任務
- 支援過濾:
  - 按狀態過濾 (TODO / IN_PROGRESS / DONE)
  - 按優先級過濾
  - 按創建者過濾
- 支援排序:
  - 按創建時間排序 (默認)
  - 按更新時間排序
  - 按優先級排序
  - 按截止日期排序
- 分頁: 每頁 20 筆

**API Endpoint**:
```http
GET /api/tasks?status=TODO&priority=HIGH&sort_by=due_date&page=1&limit=20
Authorization: Bearer <token>

Response 200:
{
  "tasks": [
    {
      "id": 1,
      "title": "實作用戶認證功能",
      "status": "TODO",
      "priority": "HIGH",
      "due_date": "2025-11-05",
      "created_by": 1,
      "created_at": "2025-10-30T10:00:00Z"
    }
  ],
  "total": 1,
  "page": 1,
  "limit": 20,
  "total_pages": 1
}
```

#### 2.2.3 查看單一任務詳情
**功能描述**: 用戶能夠查看任務的完整資訊

**API Endpoint**:
```http
GET /api/tasks/{task_id}
Authorization: Bearer <token>

Response 200:
{
  "id": 1,
  "title": "實作用戶認證功能",
  "description": "使用 JWT 實作登入/註冊功能",
  "status": "TODO",
  "priority": "HIGH",
  "due_date": "2025-11-05",
  "created_by": 1,
  "created_at": "2025-10-30T10:00:00Z",
  "updated_at": "2025-10-30T10:00:00Z"
}
```

#### 2.2.4 更新任務
**功能描述**: 用戶能夠更新任務資訊

**權限規則**:
- 只有任務創建者能更新
- 所有欄位都可更新（除了 id, created_by, created_at）

**API Endpoint**:
```http
PUT /api/tasks/{task_id}
Authorization: Bearer <token>
Content-Type: application/json

{
  "title": "實作用戶認證功能（已完成）",
  "status": "DONE",
  "priority": "MEDIUM"
}

Response 200:
{
  "id": 1,
  "title": "實作用戶認證功能（已完成）",
  "description": "使用 JWT 實作登入/註冊功能",
  "status": "DONE",
  "priority": "MEDIUM",
  "due_date": "2025-11-05",
  "created_by": 1,
  "created_at": "2025-10-30T10:00:00Z",
  "updated_at": "2025-10-30T12:30:00Z"
}
```

#### 2.2.5 刪除任務
**功能描述**: 用戶能夠刪除任務

**權限規則**:
- 只有任務創建者能刪除
- 軟刪除（保留數據，標記為已刪除）

**API Endpoint**:
```http
DELETE /api/tasks/{task_id}
Authorization: Bearer <token>

Response 204: No Content
```

---

### 2.3 任務狀態管理

#### 2.3.1 狀態定義
- **TODO** (待辦): 新創建的任務，尚未開始
- **IN_PROGRESS** (進行中): 正在處理的任務
- **DONE** (完成): 已完成的任務

#### 2.3.2 狀態流轉規則
```
TODO ──────────→ IN_PROGRESS ──────────→ DONE
  ↑                   ↓                    ↓
  └───────────────────┴────────────────────┘
  (可以隨時改回任何狀態)
```

**業務規則**:
- 所有狀態之間可以自由切換（MVP 階段簡化處理）
- 未來可擴展為嚴格的狀態機

---

### 2.4 優先級管理

#### 2.4.1 優先級定義
| 優先級 | 英文代碼 | 顏色標示 | 說明 |
|-------|---------|---------|-----|
| 緊急 | URGENT | 紅色 | 需立即處理 |
| 高 | HIGH | 橙色 | 重要且緊急 |
| 中 | MEDIUM | 黃色 | 正常優先級 |
| 低 | LOW | 綠色 | 可延後處理 |

#### 2.4.2 優先級業務規則
- 默認優先級: MEDIUM
- 可在任何時候修改優先級
- 優先級影響任務列表的默認排序

---

### 2.5 Dashboard (統計面板)

#### 2.5.1 統計數據
**功能描述**: 顯示任務的統計資訊

**統計項目**:
1. 總任務數
2. 各狀態任務數
   - 待辦 (TODO)
   - 進行中 (IN_PROGRESS)
   - 已完成 (DONE)
3. 各優先級任務數
4. 即將到期的任務 (7 天內)
5. 已逾期的任務

**API Endpoint**:
```http
GET /api/dashboard/stats
Authorization: Bearer <token>

Response 200:
{
  "total_tasks": 25,
  "status_distribution": {
    "TODO": 10,
    "IN_PROGRESS": 8,
    "DONE": 7
  },
  "priority_distribution": {
    "URGENT": 2,
    "HIGH": 5,
    "MEDIUM": 12,
    "LOW": 6
  },
  "upcoming_due": 3,
  "overdue": 1
}
```

#### 2.5.2 視覺化圖表
**展示方式**:
- 狀態分佈: 圓餅圖
- 優先級分佈: 長條圖
- 趨勢分析: 折線圖（可選，MVP 可不做）

---

## 3. 非功能需求

### 3.1 效能要求

| 指標 | 要求 | 衡量方式 |
|-----|-----|---------|
| API 回應時間 | < 200ms (P95) | 性能測試 |
| 並發用戶數 | 支援 50 人同時使用 | 負載測試 |
| 資料庫查詢 | < 100ms | 日誌監控 |
| 前端首次加載 | < 3s | Lighthouse |

### 3.2 安全性要求

#### 3.2.1 認證與授權
- [x] 使用 JWT token 進行身份驗證
- [x] Token 有效期: 7 天
- [x] 密碼使用 bcrypt 加密 (cost factor: 12)
- [x] 防止暴力破解 (rate limiting)

#### 3.2.2 數據安全
- [x] 所有 API 使用 HTTPS
- [x] 輸入驗證 (防止 SQL injection, XSS)
- [x] CORS 配置正確
- [x] 敏感資訊不記錄在日誌中

#### 3.2.3 權限控制
- [x] 用戶只能操作自己的任務
- [x] API endpoint 都需要認證（除了註冊/登入）

### 3.3 可用性要求

| 指標 | 要求 |
|-----|-----|
| 系統可用性 | 99% (允許每月 7.2 小時停機) |
| 錯誤率 | < 1% |
| 恢復時間 | < 1 小時 |

### 3.4 可維護性要求

- [x] 代碼測試覆蓋率 ≥ 80%
- [x] 代碼遵循 PEP 8 (Python) 或 ESLint (JavaScript)
- [x] 完整的 API 文檔 (OpenAPI/Swagger)
- [x] 清晰的代碼註釋
- [x] 版本控制 (Git)
- [x] CI/CD 自動化部署

### 3.5 擴展性要求

- [x] 數據庫支援水平擴展 (PostgreSQL)
- [x] API 設計遵循 RESTful 原則
- [x] 前後端分離架構
- [x] 容器化部署 (Docker)

---

## 4. 技術約束

### 4.1 技術棧要求

**後端**:
- 語言: Python 3.10+
- 框架: FastAPI
- 數據庫: PostgreSQL 14+
- ORM: SQLAlchemy
- 認證: JWT (PyJWT)
- 測試: Pytest

**前端** (可選 Vue.js):
- 框架: React 18+ 或 Vue 3+
- 狀態管理: Context API / Pinia
- HTTP 客戶端: Axios
- UI 框架: Tailwind CSS

**DevOps**:
- 版本控制: Git + GitHub
- CI/CD: GitHub Actions
- 容器化: Docker + Docker Compose
- 雲平台: (可選) Railway / Render / Vercel

### 4.2 環境要求

| 環境 | 用途 | 配置 |
|-----|-----|-----|
| Development | 本地開發 | Docker Compose |
| Testing | 自動化測試 | GitHub Actions |
| Production | 生產環境 | Cloud Platform |

### 4.3 相容性要求

**瀏覽器支援**:
- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

**設備支援**:
- 桌面優先 (Desktop-first)
- 響應式設計 (支援平板與手機瀏覽)

---

## 5. 數據模型

### 5.1 User (用戶表)

| 欄位 | 類型 | 約束 | 說明 |
|-----|-----|-----|-----|
| id | Integer | PK, Auto-increment | 用戶 ID |
| email | String(255) | Unique, Not Null | 登入帳號 |
| password_hash | String(255) | Not Null | 加密後的密碼 |
| username | String(100) | Not Null | 顯示名稱 |
| created_at | DateTime | Not Null, Default Now | 創建時間 |
| updated_at | DateTime | Not Null, Auto-update | 更新時間 |

### 5.2 Task (任務表)

| 欄位 | 類型 | 約束 | 說明 |
|-----|-----|-----|-----|
| id | Integer | PK, Auto-increment | 任務 ID |
| title | String(200) | Not Null | 任務標題 |
| description | Text | Nullable | 任務描述 |
| status | Enum | Not Null, Default 'TODO' | TODO/IN_PROGRESS/DONE |
| priority | Enum | Not Null, Default 'MEDIUM' | LOW/MEDIUM/HIGH/URGENT |
| due_date | Date | Nullable | 截止日期 |
| created_by | Integer | FK(User.id), Not Null | 創建者 ID |
| created_at | DateTime | Not Null, Default Now | 創建時間 |
| updated_at | DateTime | Not Null, Auto-update | 更新時間 |
| is_deleted | Boolean | Default False | 軟刪除標記 |

### 5.3 關聯關係

```
User (1) ──< (N) Task
  │               │
  └─── created_by ┘
```

---

## 6. API 設計總覽

### 6.1 API 端點清單

| 方法 | 端點 | 功能 | 認證 |
|-----|-----|-----|-----|
| POST | /api/auth/register | 用戶註冊 | 否 |
| POST | /api/auth/login | 用戶登入 | 否 |
| GET | /api/auth/me | 獲取當前用戶 | 是 |
| POST | /api/tasks | 創建任務 | 是 |
| GET | /api/tasks | 查看任務列表 | 是 |
| GET | /api/tasks/{id} | 查看任務詳情 | 是 |
| PUT | /api/tasks/{id} | 更新任務 | 是 |
| DELETE | /api/tasks/{id} | 刪除任務 | 是 |
| GET | /api/dashboard/stats | 獲取統計數據 | 是 |

**總計**: 9 個 API endpoints

### 6.2 錯誤碼設計

| HTTP Status | 錯誤碼 | 說明 |
|------------|-------|-----|
| 400 | INVALID_INPUT | 輸入驗證失敗 |
| 401 | UNAUTHORIZED | 未認證或 token 失效 |
| 403 | FORBIDDEN | 無權限操作 |
| 404 | NOT_FOUND | 資源不存在 |
| 409 | CONFLICT | 資源衝突 (如重複註冊) |
| 422 | UNPROCESSABLE_ENTITY | 無法處理的實體 |
| 500 | INTERNAL_ERROR | 伺服器錯誤 |

**錯誤回應格式**:
```json
{
  "error": {
    "code": "INVALID_INPUT",
    "message": "Email format is invalid",
    "details": {
      "field": "email",
      "value": "invalid-email"
    }
  }
}
```

---

## 7. 用戶介面設計

### 7.1 頁面結構

```
App
├── Login/Register Page         # 登入/註冊頁
├── Dashboard                   # 主面板（包含統計）
└── Task Management
    ├── Task List               # 任務列表頁
    ├── Task Detail             # 任務詳情頁
    └── Create/Edit Task Form   # 創建/編輯任務表單
```

### 7.2 頁面描述

#### 7.2.1 登入/註冊頁
**組件**:
- Logo
- 登入表單 (Email, Password, Login Button)
- 註冊表單 (Email, Password, Username, Register Button)
- 切換登入/註冊的 Tab

#### 7.2.2 Dashboard
**組件**:
- 頂部導航欄 (Logo, 用戶名, 登出按鈕)
- 統計卡片 (4 個卡片):
  - 總任務數
  - 待辦任務數
  - 進行中任務數
  - 已完成任務數
- 優先級分佈圖 (長條圖)
- 快速操作按鈕 (創建任務)

#### 7.2.3 任務列表頁
**組件**:
- 頂部操作欄:
  - 篩選器 (狀態、優先級)
  - 排序選擇器
  - 搜尋框
  - 創建任務按鈕
- 任務卡片列表:
  - 標題
  - 優先級標籤
  - 狀態標籤
  - 截止日期
  - 操作按鈕 (編輯、刪除)
- 分頁控制

#### 7.2.4 任務詳情頁
**組件**:
- 麵包屑導航
- 任務完整資訊:
  - 標題
  - 描述 (Markdown 渲染)
  - 狀態、優先級、截止日期
  - 創建者、創建時間、更新時間
- 操作按鈕 (編輯、刪除、返回)

#### 7.2.5 創建/編輯任務表單
**組件**:
- 標題輸入框
- 描述編輯器 (支援 Markdown)
- 優先級選擇器 (下拉選單)
- 截止日期選擇器 (日期選擇器)
- 狀態選擇器 (編輯時可見)
- 提交按鈕、取消按鈕

### 7.3 UI/UX 要求

- **響應式設計**: 支援桌面、平板、手機
- **加載狀態**: 所有 API 呼叫顯示 loading indicator
- **錯誤提示**: 友善的錯誤訊息
- **成功反饋**: 操作成功後顯示 toast 通知
- **鍵盤快捷鍵**: Ctrl+N (創建任務), ESC (關閉彈窗)

---

## 8. 部署要求

### 8.1 部署架構

```
User Browser
     ↓
   (HTTPS)
     ↓
Frontend (Vercel/Netlify)
     ↓
   (API Calls)
     ↓
Backend (Railway/Render)
     ↓
   (SQL)
     ↓
PostgreSQL Database
```

### 8.2 環境變數

**後端**:
```env
DATABASE_URL=postgresql://user:pass@host:5432/dbname
JWT_SECRET_KEY=<random-secret-key>
JWT_ALGORITHM=HS256
JWT_EXPIRATION_DAYS=7
CORS_ORIGINS=https://yourdomain.com
```

**前端**:
```env
REACT_APP_API_BASE_URL=https://api.yourdomain.com
```

### 8.3 部署清單

- [ ] 後端部署到雲平台
- [ ] 前端部署到 CDN
- [ ] 數據庫遷移執行
- [ ] 環境變數配置
- [ ] HTTPS 憑證配置
- [ ] CI/CD pipeline 運行成功
- [ ] 健康檢查 endpoint 正常
- [ ] 監控與日誌配置

---

## 9. 測試要求

### 9.1 測試範圍

| 測試類型 | 覆蓋率要求 | 工具 |
|---------|----------|-----|
| 單元測試 | ≥ 80% | Pytest |
| 整合測試 | ≥ 60% | Pytest + TestClient |
| E2E 測試 | 關鍵流程 | (可選) Playwright |
| 安全測試 | 100% | Bandit, Safety |

### 9.2 關鍵測試案例

**用戶認證**:
- [x] 成功註冊
- [x] 重複 email 註冊失敗
- [x] 密碼驗證失敗
- [x] 成功登入
- [x] 錯誤密碼登入失敗
- [x] Token 驗證

**任務管理**:
- [x] 創建任務
- [x] 必填欄位驗證
- [x] 查詢自己的任務
- [x] 無法查詢他人的任務
- [x] 更新任務
- [x] 無法更新他人的任務
- [x] 刪除任務
- [x] 無法刪除他人的任務

**邊界測試**:
- [x] 標題長度限制
- [x] 描述長度限制
- [x] 無效的狀態值
- [x] 無效的優先級值
- [x] 無效的日期格式

---

## 10. 驗收標準

### 10.1 功能驗收

- [ ] 所有 API endpoints 正常運作
- [ ] 前端所有頁面正常顯示
- [ ] 用戶能完成完整的任務管理流程
- [ ] Dashboard 統計數據正確
- [ ] 權限控制正確（用戶只能操作自己的任務）

### 10.2 質量驗收

- [ ] 測試覆蓋率 ≥ 80%
- [ ] 所有測試通過
- [ ] 無 critical/high 等級的安全漏洞
- [ ] 代碼遵循 Linting 規則
- [ ] API 文檔完整

### 10.3 效能驗收

- [ ] API 回應時間 < 200ms (P95)
- [ ] 前端首次加載 < 3s
- [ ] 支援 50 人同時使用

### 10.4 文檔驗收

- [ ] API 文檔完整 (Swagger/OpenAPI)
- [ ] README 包含安裝與運行指南
- [ ] 部署文檔完整
- [ ] 架構圖清晰

---

## 11. 未來擴展方向（超出 MVP 範圍）

### 11.1 短期擴展 (v1.1)
- 任務分配給其他用戶
- 任務評論功能
- 任務附件上傳
- Email 通知

### 11.2 中期擴展 (v1.2)
- 任務標籤 (Tags)
- 任務看板視圖 (Kanban)
- 團隊協作
- 即時通知 (WebSocket)

### 11.3 長期擴展 (v2.0)
- 專案管理 (Project)
- 時間追蹤
- 甘特圖
- 報表與分析
- 第三方整合 (Slack, Jira)

---

## 12. 風險與假設

### 12.1 技術風險

| 風險 | 影響 | 緩解措施 |
|-----|-----|---------|
| 數據庫效能瓶頸 | 中 | 添加索引、查詢優化 |
| 並發處理錯誤 | 高 | 事務控制、樂觀鎖 |
| 安全漏洞 | 高 | 安全審查、定期更新 |

### 12.2 業務假設

- 用戶規模不會超過 100 人（6 個月內）
- 任務數據量不會超過 10,000 筆（6 個月內）
- 用戶有基本的電腦操作能力
- 用戶接受 Web 應用形式（不需要桌面/行動應用）

---

## 13. 專案時間表

| 階段 | 時間 | 交付物 |
|-----|-----|--------|
| 需求確認 | Day 1 | 本 PRD |
| 技術設計 | Day 1-2 | 技術架構文檔 |
| 後端開發 | Day 2-5 | API 完成 + 測試 |
| 前端開發 | Day 5-8 | UI 完成 + 整合 |
| 測試與修復 | Day 9-10 | 所有測試通過 |
| 部署與上線 | Day 11-12 | 生產環境運行 |
| 文檔整理 | Day 13-14 | 完整文檔 |

**總時間**: 14 天（2 週）

---

## 14. 附錄

### 14.1 參考資料
- FastAPI 官方文檔: https://fastapi.tiangolo.com/
- PostgreSQL 文檔: https://www.postgresql.org/docs/
- JWT 介紹: https://jwt.io/

### 14.2 聯絡人
- 產品經理: [Name] - [Email]
- 技術負責人: [Name] - [Email]
- UI/UX 設計師: [Name] - [Email]

### 14.3 變更記錄

| 版本 | 日期 | 變更內容 | 負責人 |
|-----|-----|---------|-------|
| v1.0 | 2025-10-30 | 初始版本 | [Your Name] |

---

**PRD 狀態**: ✅ 已確認
**開發狀態**: 🚀 準備開始

**下一步**: 閱讀 `完整開發流程/README.md` 開始開發！
