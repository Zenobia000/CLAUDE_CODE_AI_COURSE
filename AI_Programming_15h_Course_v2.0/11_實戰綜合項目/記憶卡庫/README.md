# 工作流程決策記憶卡
# Workflow Decision Flashcards

**卡片數量**: 20 張
**卡片類型**: 情境決策型（非定義型）
**使用方法**: Anki / Quizlet / 紙本複習

---

## 記憶卡設計理念

這不是「定義型」記憶卡（如「什麼是 TDD？」），而是**決策型**記憶卡：

```
❌ 錯誤範例：
Q: 什麼是 TDD？
A: Test-Driven Development，先寫測試再寫實作

✅ 正確範例：
Q: 【情境】你要開發用戶註冊 API，應該先做什麼？
A: 【決策】先寫測試（TDD）
   1. 先寫 test_register_success 等測試案例
   2. 運行測試 → 失敗（紅）
   3. 寫最少代碼讓測試通過（綠）
   4. 重構（重構）

   【原因】註冊是關鍵功能，需要高質量保證
   【模組】Module 4 (TDD/BDD)
```

---

## 記憶卡分類

### 🎯 階段 0: 準備與規劃 (3 張)
### 🏗️ 階段 1: 專案初始化 (2 張)
### 💻 階段 2: 後端開發 (7 張)
### 🎨 階段 3: 前端開發 (3 張)
### 🚀 階段 4: CI/CD (2 張)
### 📚 階段 5: 文檔交付 (2 張)
### 🐛 除錯與優化 (1 張)

---

## 🎯 階段 0: 準備與規劃

### 卡片 001: 拿到 PRD 後的第一步

```markdown
Q: 【情境】產品經理給了你一份 10 頁的 PRD，你打開 Claude Code，
   第一句話應該問什麼？

A: 【正確做法】
   "請分析這份 PRD，提供技術實作方案，包含：
   1. 技術棧建議與理由
   2. 數據庫 Schema 設計
   3. API 端點設計
   4. 開發優先級（MVP 範圍）
   5. 潛在技術風險"

   然後貼上完整 PRD。

   【錯誤做法】
   ❌ "幫我寫代碼"（太模糊）
   ❌ 直接開始寫代碼（沒規劃）

   【記憶點】需求分析 → 技術方案 → 再開始編碼
   【關聯模組】Module 0 (情境驅動), Module 2 (EPCV workflow)
```

---

### 卡片 002: 選擇開發順序

```markdown
Q: 【情境】你的專案需要前端、後端、測試、部署。
   應該按什麼順序開發？

A: 【推薦順序】
   1. 後端 API（TDD 方法）
   2. 測試（與後端同步）
   3. 前端（對接 API）
   4. CI/CD（自動化）
   5. 文檔（最後整理）

   【理由】
   - 後端是基礎，API 穩定後前端才好開發
   - TDD 保證後端質量
   - 前端可以快速用 AI 生成
   - CI/CD 在有測試後才有意義

   【替代策略】
   如果你前端更熟練，可以先做簡單 UI mock，
   但最終還是要後端 API 先穩定。

   【記憶點】API 先行，測試同步，前端後置
   【關聯模組】Module 4 (TDD)
```

---

### 卡片 003: 何時需要生成路線圖

```markdown
Q: 【情境】你開始開發前，要不要花時間生成詳細的開發路線圖？

A: 【決策】
   ✅ **需要**，如果：
   - 專案預計 > 4 小時
   - 功能模組 > 3 個
   - 多人協作
   - 你是第一次做類似專案

   ❌ **不需要**，如果：
   - 簡單功能（< 2 小時）
   - 你非常熟悉流程

   【生成方法】
   讓 AI 生成 Markdown checklist，包含：
   - 任務名稱
   - 預計時間
   - 前置依賴
   - 驗收標準

   【時間投資】
   花 10 分鐘生成路線圖 → 節省 1 小時迷茫時間

   【記憶點】複雜專案 → 先規劃路線圖
   【關聯模組】Module 1 (AI 編程思維)
```

---

## 🏗️ 階段 1: 專案初始化

### 卡片 004: 目錄結構生成

```markdown
Q: 【情境】你要建立一個 FastAPI + React 專案，
   應該自己手動創建目錄，還是讓 AI 生成？

A: 【正確做法】讓 AI 生成

   【Prompt】
   "為 FastAPI + React 專案生成完整目錄結構，
   要求前後端分離，包含 models, schemas, routers, services, tests"

   【執行】
   ```bash
   # 複製 AI 輸出的目錄結構
   mkdir -p backend/app/{models,schemas,routers,services,utils}
   mkdir -p backend/tests
   # ... 等等
   ```

   【優點】
   - 符合最佳實踐
   - 不會遺漏關鍵目錄
   - 節省 10-15 分鐘

   【注意】
   生成後要理解每個目錄的用途，不要盲目複製

   【記憶點】專案結構 → 讓 AI 生成，人來理解
   【關聯模組】Module 2 (Claude Code)
```

---

### 卡片 005: 依賴管理選擇

```markdown
Q: 【情境】Python 專案依賴管理，應該用 pip, pipenv, 還是 Poetry？

A: 【推薦】Poetry

   【理由】
   1. 依賴解析更可靠（鎖定版本）
   2. 虛擬環境自動管理
   3. pyproject.toml 統一配置
   4. 發布到 PyPI 更方便

   【使用】
   ```bash
   poetry init
   poetry add fastapi sqlalchemy
   poetry add --dev pytest black
   poetry install
   poetry shell  # 進入虛擬環境
   ```

   【替代】
   如果團隊已經用 pip + requirements.txt，
   保持一致性更重要。

   【記憶點】新專案 → Poetry，已有專案 → 保持一致
   【關聯模組】實戰經驗
```

---

## 💻 階段 2: 後端開發

### 卡片 006: TDD 紅綠重構循環

```markdown
Q: 【情境】你要開發註冊 API，寫了測試後，測試失敗了。
   接下來應該做什麼？

A: 【正確流程】
   1. ✅ 確認測試失敗是預期的（因為還沒實作）
   2. ✅ 寫**最少**代碼讓測試通過
   3. ✅ 運行測試 → 通過（綠燈）
   4. ✅ 重構代碼（如需要）
   5. ✅ 再次運行測試 → 仍通過

   【錯誤做法】
   ❌ 測試失敗就慌了，開始亂改
   ❌ 測試通過後就不管了，不重構
   ❌ 一次寫太多代碼，不知道哪裡出錯

   【核心原則】
   紅（❌ 測試失敗）→ 綠（✅ 測試通過）→ 重構（♻️ 優化代碼）

   每次循環只做一件事，保持小步前進。

   【記憶點】TDD = 紅綠重構循環，小步快跑
   【關聯模組】Module 4 (TDD/BDD)
```

---

### 卡片 007: 權限檢查的位置

```markdown
Q: 【情境】用戶要更新任務，需要檢查「是否是任務創建者」。
   這個權限檢查應該寫在哪裡？

A: 【正確位置】Service Layer (services/task_service.py)

   ```python
   async def update_task(db, task_id, task_data, user_id):
       # 1. 查詢任務
       task = await get_task_by_id(db, task_id)
       if not task:
           raise HTTPException(404, "Task not found")

       # 2. 權限檢查 ✅ 在這裡
       if task.created_by != user_id:
           raise HTTPException(403, "Permission denied")

       # 3. 更新任務
       # ...
   ```

   【錯誤位置】
   ❌ Router (routers/tasks.py) - 太薄，應該只負責 HTTP
   ❌ Model (models/task.py) - 不應該包含業務邏輯

   【原則】
   Router（薄層）→ Service（厚層，業務邏輯）→ Model（數據層）

   【記憶點】權限檢查 → Service Layer
   【關聯模組】Module 7 (DDD), 軟體工程原則
```

---

### 卡片 008: 密碼加密的時機

```markdown
Q: 【情境】用戶註冊時，密碼應該在哪個階段加密？

A: 【正確時機】在 Service Layer，保存到數據庫之前

   ```python
   # services/auth_service.py
   async def register_user(db, user_data: UserCreate):
       # 1. 檢查 Email 是否存在
       existing = await get_user_by_email(db, user_data.email)
       if existing:
           raise HTTPException(409, "Email already exists")

       # 2. 加密密碼 ✅ 在這裡
       hashed_password = get_password_hash(user_data.password)

       # 3. 創建用戶
       user = User(
           email=user_data.email,
           password_hash=hashed_password,  # 存儲加密後的
           username=user_data.username
       )
       db.add(user)
       await db.commit()
       return user
   ```

   【絕對不可以】
   ❌ 在 Router 加密（邏輯不該在這）
   ❌ 在 Model 加密（會導致密碼驗證時無法比對）
   ❌ 存儲明文密碼（安全災難）

   【加密工具】
   使用 passlib 的 bcrypt，cost factor ≥ 12

   【記憶點】密碼加密 → Service Layer，保存前加密
   【關聯模組】Module 10 (安全性)
```

---

### 卡片 009: 何時使用軟刪除 vs 硬刪除

```markdown
Q: 【情境】用戶要刪除任務，應該直接從數據庫刪除（硬刪除），
   還是標記為已刪除（軟刪除）？

A: 【決策】

   ✅ **軟刪除**（推薦），如果：
   - 需要保留數據以供審計
   - 可能需要恢復
   - 數據有關聯關係（避免外鍵問題）
   - MVP 階段（方便除錯）

   ```python
   # 軟刪除
   task.is_deleted = True
   await db.commit()

   # 查詢時過濾
   tasks = await db.query(Task).filter(Task.is_deleted == False).all()
   ```

   ❌ **硬刪除**，如果：
   - 數據包含敏感資訊（如 GDPR 要求）
   - 存儲空間有限
   - 明確不需要恢復

   ```python
   # 硬刪除
   await db.delete(task)
   await db.commit()
   ```

   【MVP 建議】
   先用軟刪除，後期可以加「永久刪除」功能。

   【記憶點】MVP → 軟刪除（is_deleted flag）
   【關聯模組】數據庫設計最佳實踐
```

---

### 卡片 010: 測試數據庫隔離

```markdown
Q: 【情境】你在寫測試，發現前一個測試創建的數據影響了下一個測試。
   怎麼解決？

A: 【解決方法】使用 pytest fixtures 實現測試隔離

   ```python
   # conftest.py
   @pytest.fixture
   async def test_db():
       # 每個測試前: 創建新數據庫連接
       engine = create_async_engine("sqlite+aiosqlite:///:memory:")
       async with engine.begin() as conn:
           await conn.run_sync(Base.metadata.create_all)

       async_session = sessionmaker(engine, class_=AsyncSession)
       async with async_session() as session:
           yield session

       # 每個測試後: 清理數據庫
       async with engine.begin() as conn:
           await conn.run_sync(Base.metadata.drop_all)

   # 測試中使用
   async def test_register_success(test_db):
       # test_db 是乾淨的，沒有其他測試的數據
       user = await register_user(test_db, user_data)
       assert user.email == "test@example.com"
   ```

   【關鍵】
   - 每個測試獨立的數據庫
   - 使用 in-memory SQLite（快速）
   - 測試結束自動清理

   【記憶點】測試隔離 → pytest fixtures + in-memory DB
   【關聯模組】Module 4 (TDD)
```

---

### 卡片 011: 分頁查詢的實作

```markdown
Q: 【情境】GET /api/tasks 需要支援分頁（page, limit）。
   SQL 查詢應該怎麼寫？

A: 【正確實作】

   ```python
   async def get_tasks(db, user_id, page=1, limit=20):
       # 計算 offset
       offset = (page - 1) * limit

       # 查詢總數（用於計算總頁數）
       total = await db.query(Task).filter(
           Task.created_by == user_id,
           Task.is_deleted == False
       ).count()

       # 分頁查詢
       tasks = await db.query(Task).filter(
           Task.created_by == user_id,
           Task.is_deleted == False
       ).offset(offset).limit(limit).all()

       # 計算總頁數
       total_pages = (total + limit - 1) // limit

       return {
           "tasks": tasks,
           "total": total,
           "page": page,
           "limit": limit,
           "total_pages": total_pages
       }
   ```

   【公式】
   - offset = (page - 1) × limit
   - total_pages = ⌈total / limit⌉

   【記憶點】分頁 = offset + limit，記得返回總數
   【關聯模組】SQL 基礎
```

---

### 卡片 012: API 錯誤碼選擇

```markdown
Q: 【情境】以下場景應該返回哪個 HTTP 狀態碼？
   1. 用戶嘗試更新他人的任務
   2. 任務 ID 不存在
   3. 請求缺少必填欄位
   4. 用戶嘗試用已存在的 Email 註冊

A: 【正確答案】
   1. **403 Forbidden** - 用戶嘗試更新他人的任務
      （有權限認證，但無操作權限）

   2. **404 Not Found** - 任務 ID 不存在
      （資源不存在）

   3. **422 Unprocessable Entity** - 請求缺少必填欄位
      （請求格式正確，但內容無法處理）

   4. **409 Conflict** - Email 已存在
      （資源衝突）

   【常見錯誤】
   ❌ 全部用 400 Bad Request（太籠統）
   ❌ 用 401 處理權限問題（401 是「未認證」，不是「無權限」）

   【記憶口訣】
   - 400: 請求錯誤（籠統）
   - 401: 未認證（沒登入）
   - 403: 無權限（登入了但不能操作）
   - 404: 不存在
   - 409: 衝突（資源重複）
   - 422: 無法處理（格式對但內容錯）

   【記憶點】權限 → 403, 不存在 → 404, 衝突 → 409
   【關聯模組】HTTP 協議基礎
```

---

## 🎨 階段 3: 前端開發

### 卡片 013: 前端 API 錯誤處理

```markdown
Q: 【情境】前端呼叫 API 時，後端返回 401 Unauthorized。
   前端應該如何處理？

A: 【正確做法】Axios Response Interceptor

   ```javascript
   // src/services/api.js
   api.interceptors.response.use(
     response => response,
     error => {
       if (error.response) {
         switch (error.response.status) {
           case 401:
             // Token 過期或無效
             localStorage.removeItem('token');
             window.location.href = '/login';
             break;
           case 403:
             alert('你沒有權限執行此操作');
             break;
           case 404:
             alert('資源不存在');
             break;
           default:
             alert('發生錯誤: ' + error.response.data.error.message);
         }
       }
       return Promise.reject(error);
     }
   );
   ```

   【優點】
   - 集中處理，不用每個 API 呼叫都寫
   - 401 自動跳轉登入頁
   - 用戶體驗友善

   【記憶點】API 錯誤 → Axios interceptor 集中處理
   【關聯模組】前端架構最佳實踐
```

---

### 卡片 014: Token 存儲位置

```markdown
Q: 【情境】前端拿到 JWT token 後，應該存在哪裡？
   1. localStorage
   2. sessionStorage
   3. Cookie
   4. 內存（變數）

A: 【選擇】取決於需求

   **1. localStorage** ✅ 推薦（MVP）
   - 優點: 持久化，關閉瀏覽器仍有效
   - 缺點: XSS 攻擊風險
   - 適用: 一般 Web 應用

   **2. sessionStorage**
   - 優點: 關閉 tab 就清除
   - 缺點: 用戶體驗差（每次都要重新登入）
   - 適用: 高安全需求場景

   **3. HttpOnly Cookie** ✅ 最安全（生產環境）
   - 優點: 防 XSS，自動發送
   - 缺點: 需要後端配合，CSRF 風險（需 CSRF token）
   - 適用: 生產環境

   **4. 內存**
   - 優點: 最安全（無法被腳本讀取）
   - 缺點: 刷新頁面就丟失
   - 適用: 單頁應用（配合 refresh token）

   【MVP 建議】
   localStorage（簡單，夠用）

   【生產環境】
   HttpOnly Cookie + CSRF token

   【記憶點】MVP → localStorage, 生產 → HttpOnly Cookie
   【關聯模組】Module 10 (安全性)
```

---

### 卡片 015: 前端狀態管理選擇

```markdown
Q: 【情境】React 專案需要管理用戶登入狀態和任務列表。
   應該用 Redux, Context API, 還是 Zustand？

A: 【決策】

   **Context API** ✅ 推薦（MVP）
   - 優點: React 內建，無需額外依賴，學習成本低
   - 缺點: 效能優化需要手動處理
   - 適用: 中小型專案，狀態不複雜

   ```javascript
   // AuthContext.jsx
   const AuthContext = createContext();
   export const useAuth = () => useContext(AuthContext);

   export const AuthProvider = ({ children }) => {
     const [user, setUser] = useState(null);
     const login = async (email, password) => { /* ... */ };
     const logout = () => { /* ... */ };

     return (
       <AuthContext.Provider value={{ user, login, logout }}>
         {children}
       </AuthContext.Provider>
     );
   };
   ```

   **Redux**
   - 適用: 大型專案，多團隊協作，需要時間旅行除錯
   - 缺點: 學習成本高，樣板代碼多

   **Zustand**
   - 適用: 想要比 Redux 簡單，比 Context 效能好
   - 優點: 語法簡潔，效能好

   【MVP 建議】
   Context API（已經夠用）

   【記憶點】MVP → Context API，複雜專案 → Redux/Zustand
   【關聯模組】React 狀態管理最佳實踐
```

---

## 🚀 階段 4: CI/CD

### 卡片 016: CI Pipeline 失敗處理

```markdown
Q: 【情境】你 push 代碼到 GitHub，CI pipeline 失敗了。
   應該怎麼處理？

A: 【處理流程】

   1. **查看失敗的 Job**
      - 進入 GitHub Actions 頁面
      - 找到紅色 ❌ 的 job

   2. **查看錯誤日誌**
      - 展開失敗的 step
      - 找到錯誤訊息（通常在最後幾行）

   3. **本地複現**
      ```bash
      # 如果是測試失敗
      pytest -v

      # 如果是 linting 失敗
      flake8 app/

      # 如果是安全掃描失敗
      bandit -r app/ -ll
      ```

   4. **修復問題**
      - 修復代碼
      - 本地驗證通過

   5. **重新提交**
      ```bash
      git add .
      git commit -m "fix: resolve CI pipeline failure"
      git push
      ```

   【常見失敗原因】
   - 測試失敗（代碼有 bug）
   - Linting 失敗（格式問題）
   - 安全掃描失敗（有漏洞）
   - 依賴安裝失敗（版本衝突）

   【記憶點】CI 失敗 → 看日誌 → 本地複現 → 修復 → 重新提交
   【關聯模組】Module 5 (CI/CD)
```

---

### 卡片 017: Docker vs 本地環境

```markdown
Q: 【情境】開發時應該用 Docker，還是直接在本地環境運行？

A: 【推薦】Docker（尤其是數據庫）

   **Docker 運行數據庫** ✅
   ```bash
   docker-compose up -d postgres
   ```
   - 優點:
     - 環境一致（避免「在我機器上能跑」問題）
     - 易清理（docker-compose down -v）
     - 不污染本地系統

   **本地運行應用** ✅
   ```bash
   poetry shell
   uvicorn app.main:app --reload
   ```
   - 優點:
     - 熱重載快
     - 易除錯
     - IDE 支援好

   **全部 Docker** ⚠️
   ```bash
   docker-compose up
   ```
   - 優點: 完全一致的環境
   - 缺點: 熱重載慢，除錯不方便
   - 適用: 部署測試

   【MVP 建議】
   Docker 跑數據庫，本地跑應用

   【記憶點】開發 → Docker DB + 本地 app, 部署 → 全 Docker
   【關聯模組】Module 8 (Docker)
```

---

## 📚 階段 5: 文檔交付

### 卡片 018: API 文檔的最低標準

```markdown
Q: 【情境】你的 FastAPI 自動生成了 Swagger 文檔，
   還需要額外寫文檔嗎？

A: 【決策】需要增強，但不用從頭寫

   **最低標準**:
   1. ✅ 每個 endpoint 有 summary（一句話功能描述）
   2. ✅ 每個 endpoint 有 description（詳細說明）
   3. ✅ 請求參數有說明
   4. ✅ 響應有 example
   5. ✅ 錯誤碼有說明

   **實作方法**:
   ```python
   @router.post(
       "/register",
       summary="用戶註冊",  # ✅ 添加
       description="創建新用戶帳號，Email 必須唯一",  # ✅ 添加
       responses={  # ✅ 添加
           201: {"description": "註冊成功"},
           409: {"description": "Email 已存在"}
       }
   )
   async def register(user_data: UserCreate):
       # ...
   ```

   **驗證**:
   訪問 http://localhost:8000/docs
   - 看起來專業嗎？
   - 新來的開發者能看懂嗎？

   【記憶點】Swagger 自動生成 + 手動增強關鍵資訊
   【關聯模組】技術寫作最佳實踐
```

---

### 卡片 019: README 必備內容

```markdown
Q: 【情境】你要寫專案 README，至少需要包含哪些內容？

A: 【必備內容】（按順序）

   1. **專案標題與簡介** (1-2 句話)
      "Task Management System - 輕量級任務管理工具"

   2. **功能列表** (3-5 個核心功能)
      - 用戶註冊/登入
      - 任務 CRUD
      - Dashboard 統計

   3. **技術棧**
      - 後端: FastAPI, PostgreSQL
      - 前端: React

   4. **快速開始** ⭐ 最重要
      ```bash
      # 環境要求
      Python 3.10+, Docker

      # 安裝
      poetry install

      # 運行
      docker-compose up -d postgres
      uvicorn app.main:app --reload

      # 訪問
      http://localhost:8000/docs
      ```

   5. **測試**
      ```bash
      pytest -v
      ```

   6. **API 文檔連結**
      Swagger UI: http://localhost:8000/docs

   7. **授權** (MIT, Apache 等)

   【驗證標準】
   ✅ 新人能按照步驟成功運行專案嗎？

   【記憶點】README = 專案的「使用說明書」
   【關聯模組】開源專案最佳實踐
```

---

## 🐛 除錯與優化

### 卡片 020: 遇到問題時的思考流程

```markdown
Q: 【情境】你遇到一個 bug，但不知道問題在哪。
   應該按什麼順序排查？

A: 【系統化除錯流程】

   1. **複現問題**
      - 能穩定複現嗎？
      - 複現步驟是什麼？

   2. **查看錯誤訊息**
      - 完整的錯誤訊息是什麼？
      - 堆疊追蹤指向哪裡？

   3. **縮小範圍**
      - 是前端問題還是後端問題？
      - 是數據庫問題還是邏輯問題？
      - 用 `print()` 或 `console.log()` 追蹤

   4. **檢查輸入輸出**
      - 輸入的數據格式正確嗎？
      - 輸出的數據符合預期嗎？

   5. **查看日誌**
      - 後端日誌有錯誤嗎？
      - 數據庫查詢成功了嗎？

   6. **簡化問題**
      - 能寫一個最小複現案例嗎？
      - 去掉無關代碼後問題還在嗎？

   7. **尋求幫助**（如果卡住超過 30 分鐘）
      - Google 錯誤訊息
      - 問 AI: "這個錯誤是什麼原因？如何解決？"
      - 在 Stack Overflow 搜尋

   【AI 協作】
   給 AI 提供:
   - 完整錯誤訊息
   - 相關代碼
   - 你已經嘗試的方法

   【記憶點】除錯 = 複現 → 縮小範圍 → 檢查輸入輸出 → 查日誌 → 問 AI
   【關聯模組】Module 6 (除錯技巧)
```

---

## 使用建議

### Anki 導入格式

```
# 卡片正面
【情境】你拿到 PRD 後，第一步應該做什麼？

# 卡片背面
【正確做法】
讓 AI 分析 PRD，生成技術方案
包含: 技術棧、Schema、API 設計、優先級、風險

【錯誤做法】
❌ 直接開始寫代碼

【記憶點】需求分析 → 技術方案 → 編碼

【關聯模組】Module 0, Module 2
```

### 複習策略

**第一次複習**: 專案完成後立即
**第二次複習**: 1 天後
**第三次複習**: 1 週後
**第四次複習**: 1 個月後

### 自我測試

看到「情境」後，先不看答案，自己思考：
1. 我會怎麼做？
2. 為什麼這樣做？
3. 還有其他選擇嗎？

然後對照「正確做法」，看看差距在哪。

---

**記住**: 這些卡片不是「背答案」，而是**訓練決策思維**。

真實專案中不會有標準答案，但有「更好的選擇」和「常見的坑」。
這些卡片幫你建立「專案直覺」，知道什麼時候該做什麼。🎯
