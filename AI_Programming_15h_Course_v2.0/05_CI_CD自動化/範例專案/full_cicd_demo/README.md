# Full CI/CD Demo - 完整 CI/CD 示範專案

[![CI Pipeline](https://github.com/your-username/full-cicd-demo/actions/workflows/ci.yml/badge.svg)](https://github.com/your-username/full-cicd-demo/actions/workflows/ci.yml)
[![CD Pipeline](https://github.com/your-username/full-cicd-demo/actions/workflows/cd.yml/badge.svg)](https://github.com/your-username/full-cicd-demo/actions/workflows/cd.yml)

這是一個完整的 CI/CD 示範專案，展示如何使用 GitHub Actions 建立端到端的持續整合與持續部署管線。

## 📋 專案特色

- ✅ **FastAPI 應用**：現代化的 Python Web 框架
- ✅ **完整測試**：單元測試 + 整合測試
- ✅ **程式碼品質**：Black、Flake8、isort 檢查
- ✅ **安全掃描**：多層次安全掃描（CodeQL、Snyk、Trivy）
- ✅ **Docker 容器化**：多階段構建優化
- ✅ **多環境部署**：開發、測試、生產三環境
- ✅ **健康檢查**：自動化部署驗證
- ✅ **完整文檔**：詳細的設定和使用說明

---

## 🚀 快速開始

### 前置需求

- Python 3.11+
- Docker & Docker Compose
- Git

### 本地開發

```bash
# 1. 克隆專案
git clone https://github.com/your-username/full-cicd-demo.git
cd full-cicd-demo

# 2. 創建虛擬環境
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. 安裝依賴
pip install -r requirements.txt

# 4. 運行應用
uvicorn app.main:app --reload

# 5. 訪問 API 文檔
# 瀏覽器訪問：http://localhost:8000/docs
```

### 使用 Docker

```bash
# 使用 docker-compose 啟動
docker-compose up -d

# 查看日誌
docker-compose logs -f

# 停止服務
docker-compose down
```

---

## 🧪 執行測試

```bash
# 執行所有測試
pytest

# 執行測試並生成覆蓋率報告
pytest --cov=app --cov-report=html

# 檢查代碼品質
black --check app tests
flake8 app tests
isort --check app tests
```

---

## 📁 專案結構

```
full_cicd_demo/
├── app/                      # 應用程式代碼
│   ├── main.py              # FastAPI 主應用
│   ├── config.py            # 配置管理
│   ├── models.py            # Pydantic 模型
│   └── database.py          # 資料庫連線
│
├── tests/                    # 測試代碼
│   ├── unit/                # 單元測試
│   └── integration/         # 整合測試
│
├── .github/workflows/        # GitHub Actions workflows
│   ├── ci.yml               # 持續整合
│   └── cd.yml               # 持續部署
│
├── deployment/              # 部署配置
│   ├── dev/                 # 開發環境
│   ├── staging/             # 測試環境
│   └── production/          # 生產環境
│
├── scripts/                 # 部署腳本
│   ├── health-check.sh      # 健康檢查
│   └── smoke-test.sh        # 煙霧測試
│
├── Dockerfile               # Docker 映像配置
├── docker-compose.yml       # Docker Compose 配置
├── requirements.txt         # Python 依賴
└── README.md               # 本文件
```

---

## 🔄 CI/CD 管線

### CI Pipeline（持續整合）

觸發條件：Push 到 main/develop 分支，或 Pull Request

```
┌─────────────────────────────────────┐
│  Stage 1: 程式碼品質（並行）          │
├─────────────────────────────────────┤
│  • Lint (black, flake8, isort)     │
│  • Test (pytest)                    │
│  • Security Scan (safety, bandit)  │
└─────────────────────────────────────┘
             ↓
┌─────────────────────────────────────┐
│  Stage 2: Docker 構建               │
├─────────────────────────────────────┤
│  • Build Docker image               │
│  • Push to GHCR                     │
│  • Container scan (Trivy)           │
└─────────────────────────────────────┘
```

### CD Pipeline（持續部署）

觸發條件：CI Pipeline 成功完成

```
main 分支：
  ├─> 部署到 Staging（自動）
  └─> 部署到 Production（需審批）

develop 分支：
  └─> 部署到 Development（自動）
```

---

## 🌍 環境配置

### 開發環境（Development）

- **URL**: https://dev.example.com
- **部署**: 自動部署（develop 分支）
- **配置**: `deployment/dev/.env`

### 測試環境（Staging）

- **URL**: https://staging.example.com
- **部署**: 自動部署（main 分支）
- **配置**: `deployment/staging/.env`

### 生產環境（Production）

- **URL**: https://app.example.com
- **部署**: 需要審批後部署（main 分支）
- **配置**: `deployment/production/.env`

---

## 🔒 安全性

### 多層次安全掃描

1. **靜態代碼分析**（CodeQL）
   - SQL 注入檢測
   - XSS 漏洞檢測
   - 安全最佳實踐檢查

2. **依賴漏洞掃描**（Safety/Snyk）
   - 檢查已知 CVE
   - 自動建議升級版本

3. **容器掃描**（Trivy）
   - 掃描 Docker 映像
   - 檢測基礎映像漏洞

### Secrets 管理

所有敏感資訊使用 GitHub Secrets 管理：

- `DATABASE_URL`: 資料庫連線字串
- `SECRET_KEY`: 應用密鑰
- `SSH_PRIVATE_KEY`: 部署用 SSH 密鑰

---

## 📊 API 文檔

### 主要端點

| 端點 | 方法 | 說明 |
|------|------|------|
| `/` | GET | 根路由 |
| `/health` | GET | 健康檢查 |
| `/api/items` | GET | 列出所有項目 |
| `/api/items/{id}` | GET | 獲取單個項目 |
| `/api/items` | POST | 創建新項目 |
| `/api/items/{id}` | PUT | 更新項目 |
| `/api/items/{id}` | DELETE | 刪除項目 |

### 互動式文檔

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

---

## 🛠️ 部署指南

### 首次部署設置

1. **Fork 此專案**

2. **設定 GitHub Secrets**

   前往 `Settings > Secrets and variables > Actions`：

   ```
   - DEV_HOST: 開發環境主機
   - DEV_USER: SSH 用戶名
   - STAGING_HOST: 測試環境主機
   - STAGING_USER: SSH 用戶名
   - PROD_HOST: 生產環境主機
   - PROD_USER: SSH 用戶名
   - SSH_PRIVATE_KEY: SSH 私鑰
   ```

3. **配置環境保護規則**

   前往 `Settings > Environments > production`：

   - 勾選「Required reviewers」
   - 添加審批者

4. **推送代碼**

   ```bash
   git push origin main
   ```

### 部署到不同環境

```bash
# 部署到開發環境
git push origin develop

# 部署到測試/生產環境
git push origin main
# 然後在 GitHub Actions 中審批生產部署
```

---

## 🧰 常用命令

```bash
# 本地開發
uvicorn app.main:app --reload

# 運行測試
pytest -v

# 代碼格式化
black app tests
isort app tests

# 安全掃描
safety check
bandit -r app

# Docker 操作
docker build -t full-cicd-demo .
docker run -p 8000:8000 full-cicd-demo

# 健康檢查
./scripts/health-check.sh http://localhost:8000

# 煙霧測試
./scripts/smoke-test.sh http://localhost:8000
```

---

## 📚 學習資源

- [FastAPI 官方文檔](https://fastapi.tiangolo.com/)
- [GitHub Actions 文檔](https://docs.github.com/en/actions)
- [Docker 最佳實踐](https://docs.docker.com/develop/dev-best-practices/)
- [12-Factor App](https://12factor.net/)

---

## 🤝 貢獻指南

1. Fork 專案
2. 創建功能分支 (`git checkout -b feature/amazing-feature`)
3. 提交變更 (`git commit -m 'Add amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 開啟 Pull Request

---

## 📄 授權

MIT License

---

## 👥 作者

**AI Programming Course**

- 課程網站：https://example.com
- GitHub：[@your-org](https://github.com/your-org)

---

## 🙏 致謝

感謝所有為這個專案做出貢獻的開發者！

---

**Happy Coding!** 🚀
