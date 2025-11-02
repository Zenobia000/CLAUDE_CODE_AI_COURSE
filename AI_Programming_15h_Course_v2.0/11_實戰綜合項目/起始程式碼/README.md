# 起始程式碼 (Starter Code)
# Quick Start Template for Task Management System

**用途**: 提供基礎專案骨架，讓學員能快速開始開發，而無需從零配置環境。

---

## 📋 這個目錄包含什麼？

本目錄提供 **最小化的專案模板**，包括：

✅ **基礎目錄結構** - 符合最佳實踐的資料夾組織
✅ **配置文件模板** - pyproject.toml, .gitignore, .env.example
✅ **Docker 配置** - docker-compose.yml 快速啟動數據庫
✅ **空白模組檔案** - 帶有基本 import 和結構註釋

❌ **不包含**：
- 業務邏輯實作（需要你自己寫）
- API endpoints 實作
- 測試代碼（需使用 TDD 方法自己寫）

---

## 🚀 快速開始

### 方式 1: 使用起始程式碼（推薦給初學者）

```bash
# 1. 複製起始程式碼到你的工作目錄
cp -r 起始程式碼/task_management_api ~/my-task-project
cd ~/my-task-project

# 2. 創建虛擬環境
poetry install

# 3. 啟動數據庫
docker-compose up -d

# 4. 開始開發！
# 跟隨「分階段實作指南/階段1_專案初始化」繼續
```

---

### 方式 2: 從零開始（推薦給有經驗者）

如果你想完全從零搭建，可以不使用起始程式碼：

```bash
# 完全按照「分階段實作指南/階段1」的步驟
mkdir task-management-system
cd task-management-system
poetry init
# ... 後續步驟
```

---

## 📁 起始程式碼結構

```
task_management_api/
├── .github/
│   └── workflows/
│       └── .gitkeep           # CI/CD workflow 放這裡
│
├── src/                       # 源代碼目錄
│   ├── models/                # SQLAlchemy 模型
│   │   └── .gitkeep
│   ├── routers/               # FastAPI 路由
│   │   └── .gitkeep
│   └── services/              # 業務邏輯層
│       └── .gitkeep
│
├── tests/                     # 測試代碼
│   └── .gitkeep
│
├── .env.example               # 環境變數範例
├── .gitignore                 # Git 忽略文件
├── docker-compose.yml         # Docker 配置
├── pyproject.toml             # Poetry 依賴管理
└── README.md                  # 專案說明
```

---

## 🛠️ 已提供的配置文件

### 1. `pyproject.toml`

基礎的 Python 專案配置，包含：
- 專案元數據
- 核心依賴（FastAPI, SQLAlchemy, PostgreSQL driver）
- 開發依賴（pytest, black, ruff）

你可能需要添加：
- JWT 相關依賴（PyJWT, passlib）
- 其他你選擇的庫

---

### 2. `.env.example`

環境變數範例：

```env
# Database
DATABASE_URL=postgresql://taskuser:taskpass@localhost:5432/taskdb

# JWT
JWT_SECRET_KEY=your-secret-key-here
JWT_ALGORITHM=HS256
JWT_EXPIRATION_DAYS=7

# Environment
ENVIRONMENT=development
```

**重要**: 複製為 `.env` 並修改敏感資訊！

---

### 3. `docker-compose.yml`

快速啟動 PostgreSQL 數據庫：

```yaml
version: '3.8'
services:
  postgres:
    image: postgres:14-alpine
    environment:
      POSTGRES_USER: taskuser
      POSTGRES_PASSWORD: taskpass
      POSTGRES_DB: taskdb
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
volumes:
  postgres_data:
```

---

### 4. `.gitignore`

已配置忽略：
- Python 虛擬環境 (`.venv`, `__pycache__`)
- 環境變數檔案 (`.env`)
- IDE 配置 (`.vscode`, `.idea`)
- 數據庫文件

---

## 📝 下一步該做什麼？

使用起始程式碼後，跟隨實作指南：

1. **階段 1: 專案初始化** ✅ (部分完成)
   - 環境已設置
   - 需要配置數據庫連接

2. **階段 2: 後端開發** → 開始這裡
   - 使用 TDD 方法開發 API
   - 參考「分階段實作指南/階段2_後端開發」

3. **階段 3-5**: 前端、CI/CD、文檔

---

## 💡 使用建議

### 對於初學者

✅ **建議使用起始程式碼**

優點：
- 省去環境配置時間（15-20 分鐘）
- 避免常見的配置錯誤
- 專注在學習業務邏輯開發

使用方法：
- 複製整個 `task_management_api/` 到你的工作目錄
- 按照 README 指示安裝依賴
- 直接開始階段 2 的開發

---

### 對於有經驗者

⭐ **建議從零開始**

優點：
- 理解每個配置的作用
- 培養專案初始化能力
- 可自由選擇技術方案

使用方法：
- 參考起始程式碼的結構
- 按照「分階段實作指南/階段1」完整走一遍
- 起始程式碼僅作為參考

---

## 🤔 常見問題

### Q1: 起始程式碼包含完整功能嗎？

**A**: **不包含！** 這只是空殼骨架。

包含：
- ✅ 目錄結構
- ✅ 配置文件
- ✅ 空白的模組文件（帶註釋）

不包含：
- ❌ API endpoints 實作
- ❌ 數據庫模型定義
- ❌ 業務邏輯代碼
- ❌ 測試代碼

**你需要自己（在 AI 輔助下）完成所有業務邏輯！**

---

### Q2: 為什麼不提供完整的起始代碼？

**A**: 課程設計理念：

1. **情境驅動學習** - 從問題出發，不是從代碼出發
2. **AI 協作能力培養** - 學會如何讓 AI 幫你生成代碼
3. **真實工作場景** - 實際工作中沒有「完美模板」

提供完整代碼會：
- ❌ 讓學員養成「複製貼上」習慣
- ❌ 失去與 AI 協作的練習機會
- ❌ 無法培養「從零到一」的能力

---

### Q3: 可以不用起始程式碼嗎？

**A**: **當然可以！**

起始程式碼是**可選的輔助工具**，不是必須。

你可以：
- 完全按照「階段1_專案初始化」從零開始
- 使用自己習慣的專案結構
- 選擇不同的技術方案（如 Django 而非 FastAPI）

**只要最後符合 PRD 需求即可！**

---

### Q4: 起始程式碼的版本是最新的嗎？

**A**: 起始程式碼使用的依賴版本：

- Python: 3.10+
- FastAPI: 0.104+
- SQLAlchemy: 2.0+
- PostgreSQL: 14+

如果你想使用更新版本，可以自行修改 `pyproject.toml`。

---

## 🔧 自定義起始程式碼

你可以根據需求修改：

### 更換數據庫

```yaml
# docker-compose.yml
services:
  mysql:  # 改用 MySQL
    image: mysql:8.0
    environment:
      MYSQL_ROOT_PASSWORD: rootpass
      MYSQL_DATABASE: taskdb
```

### 添加其他服務

```yaml
services:
  postgres:
    # ... 已有配置

  redis:  # 添加 Redis
    image: redis:7-alpine
    ports:
      - "6379:6379"
```

### 修改依賴

```bash
# 添加新依賴
poetry add email-validator

# 移除不需要的依賴
poetry remove some-package
```

---

## 📚 相關資源

- **分階段實作指南/** - 詳細開發步驟
- **AI協作提示詞庫/** - 如何讓 AI 幫你生成代碼
- **範例代碼庫/** - 架構參考與關鍵片段
- **專案需求/PRD.md** - 完整需求文檔

---

## ⚡ 快速指令參考

```bash
# 安裝依賴
poetry install

# 啟動數據庫
docker-compose up -d

# 查看數據庫狀態
docker-compose ps

# 停止數據庫
docker-compose down

# 清除數據（重置數據庫）
docker-compose down -v

# 運行開發服務器
poetry run uvicorn app.main:app --reload

# 運行測試
poetry run pytest

# 代碼格式化
poetry run black .
poetry run ruff check .
```

---

**開始你的實戰專案之旅吧！記住：起始程式碼只是幫你省時間，真正的學習在於你自己動手實作。** 🚀
