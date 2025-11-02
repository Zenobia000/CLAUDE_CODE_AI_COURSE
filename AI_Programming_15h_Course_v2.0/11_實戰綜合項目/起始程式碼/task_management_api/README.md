# Task Management System API

> 基於 FastAPI 的任務管理系統後端 API - AI 編程速成課程實戰專案

---

## 🚀 快速開始

### 前置要求

- Python 3.10+
- Poetry (依賴管理)
- Docker & Docker Compose (數據庫)

### 安裝步驟

```bash
# 1. 安裝依賴
poetry install

# 2. 創建環境變數檔案
cp .env.example .env
# 編輯 .env，修改必要的配置

# 3. 啟動數據庫
docker-compose up -d

# 4. 運行數據庫遷移（階段 2 會創建）
# poetry run alembic upgrade head

# 5. 啟動開發服務器
poetry run uvicorn app.main:app --reload
```

訪問:
- API: http://localhost:8000
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

---

## 📁 專案結構

```
task_management_api/
├── src/
│   ├── models/          # SQLAlchemy 數據庫模型
│   ├── routers/         # FastAPI 路由 (API endpoints)
│   └── services/        # 業務邏輯層
├── tests/               # 測試代碼
├── alembic/            # 數據庫遷移 (待創建)
├── .env                 # 環境變數 (從 .env.example 複製)
├── pyproject.toml       # 依賴配置
└── docker-compose.yml   # Docker 配置
```

---

## 🛠️ 開發指令

```bash
# 啟動開發服務器（自動重載）
poetry run uvicorn app.main:app --reload

# 運行測試
poetry run pytest

# 測試覆蓋率
poetry run pytest --cov=app --cov-report=html

# 代碼格式化
poetry run black .

# 代碼檢查
poetry run ruff check .

# 數據庫遷移
poetry run alembic revision --autogenerate -m "description"
poetry run alembic upgrade head
```

---

## 📝 開發流程

**這是起始程式碼，你需要按照實作指南完成開發：**

1. **階段 1**: 專案初始化 ✅ (部分完成 - 環境已設置)
2. **階段 2**: 後端開發 → **從這裡開始**
   - 使用 TDD 方法開發 API
   - 參考：`分階段實作指南/階段2_後端開發/README.md`
3. **階段 3**: 前端開發
4. **階段 4**: CI/CD 設置
5. **階段 5**: 文檔交付

---

## 🔑 環境變數說明

關鍵環境變數（`.env` 檔案）：

| 變數 | 說明 | 範例 |
|-----|------|------|
| `DATABASE_URL` | PostgreSQL 連接字串 | `postgresql://user:pass@localhost:5432/dbname` |
| `JWT_SECRET_KEY` | JWT 加密密鑰 | 隨機生成的長字串 |
| `JWT_EXPIRATION_DAYS` | Token 有效期 | `7` |
| `CORS_ORIGINS` | 允許的前端來源 | `http://localhost:3000` |

**⚠️ 重要**: 生產環境請務必修改 `JWT_SECRET_KEY`！

---

## 🧪 測試

```bash
# 運行所有測試
poetry run pytest

# 運行特定測試
poetry run pytest tests/test_auth.py

# 查看測試覆蓋率
poetry run pytest --cov=app --cov-report=term-missing

# 生成 HTML 覆蓋率報告
poetry run pytest --cov=app --cov-report=html
open htmlcov/index.html
```

**目標**: 測試覆蓋率 ≥ 80%

---

## 🐳 Docker 使用

```bash
# 啟動數據庫
docker-compose up -d

# 查看狀態
docker-compose ps

# 查看日誌
docker-compose logs -f postgres

# 停止服務
docker-compose down

# 清除數據（重置數據庫）
docker-compose down -v
```

---

## 📚 學習資源

本專案是 **AI 編程速成課程** 的實戰專案，建議配合以下資源學習：

- **專案需求/PRD.md** - 完整需求文檔
- **分階段實作指南/** - 逐步開發指引
- **AI協作提示詞庫/** - 有效的 AI 提示詞
- **範例代碼庫/** - 架構參考
- **評估標準/** - 自我檢查清單

---

## 🤝 貢獻指南

如果這是團隊協作專案：

1. Fork 本專案
2. 創建 feature 分支 (`git checkout -b feature/amazing-feature`)
3. 提交變更 (`git commit -m 'feat: add amazing feature'`)
4. Push 到分支 (`git push origin feature/amazing-feature`)
5. 開啟 Pull Request

---

## 📄 授權

本專案採用 MIT License 授權 - 詳見 [LICENSE](LICENSE) 文件

---

**開始你的開發之旅吧！記住：這只是起點，真正的學習在於實作過程。** 🚀
