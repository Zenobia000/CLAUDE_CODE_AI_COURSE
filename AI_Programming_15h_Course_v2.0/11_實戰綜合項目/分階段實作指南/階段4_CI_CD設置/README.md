# 階段 4: CI/CD 設置 (自動化流程)
# CI/CD Setup with GitHub Actions

**預計時間**: 30 分鐘
**難度**: ★★☆☆☆ (中等偏易)
**前置要求**: 完成階段 1-3 (專案初始化、後端、前端)
**核心技能**: GitHub Actions、Docker、自動化測試、安全掃描

---

## 📋 階段目標

完成這個階段後,你將擁有:

✅ **GitHub Actions workflow** - 每次 push/PR 自動執行
✅ **自動化測試** - 後端測試自動運行,覆蓋率報告
✅ **安全掃描** - Bandit (代碼安全) + Safety (依賴漏洞)
✅ **Docker 容器化** - 後端打包成 Docker image
✅ **持續部署** - (可選) 自動部署到雲平台

**成功標準**:
- GitHub Actions 所有 jobs 通過 (綠色 ✓)
- 測試覆蓋率 ≥ 80%
- 無 critical/high 等級安全漏洞
- Docker image 成功建置

---

## 🎯 為什麼需要 CI/CD？

### 類比：餐廳的品質控制

**沒有 CI/CD (手動檢查)**:
```
開發者提交代碼
    ↓
? 忘記跑測試
    ↓
? 沒發現 bug
    ↓
部署到生產環境
    ↓
💥 用戶發現 bug
```

**有 CI/CD (自動檢查)**:
```
開發者提交代碼 (git push)
    ↓
自動執行測試
    ↓
自動安全掃描
    ↓
✅ 所有檢查通過 → 可以部署
❌ 有問題 → 立即通知,阻止部署
```

### CI/CD 的核心價值

1. **早期發現問題** - bug 在開發階段就被捕獲,修復成本低
2. **保證質量** - 每次變更都經過相同的檢查流程
3. **節省時間** - 自動化替代手動檢查
4. **可追蹤** - 每次建置都有記錄

---

## 🏗️ CI/CD 架構總覽

```
GitHub Repository
    │
    ├─ 開發者 push 代碼
    │      ↓
    ├─ GitHub Actions 觸發
    │      ↓
    ├─ CI Pipeline
    │   ├─ Job 1: 代碼質量檢查 (Linting)
    │   ├─ Job 2: 單元測試 (Pytest)
    │   ├─ Job 3: 安全掃描 (Bandit + Safety)
    │   └─ Job 4: Docker 建置
    │      ↓
    ├─ 所有 jobs 通過 ✅
    │      ↓
    └─ (可選) CD Pipeline
        ├─ 部署到 Staging 環境
        └─ 部署到 Production 環境
```

---

## ⏱️ 時間分配建議

```
總時間: 30 分鐘

子階段 4.1: GitHub Actions Workflow (15 min)
   ├─ 4.1.1 創建 workflow 檔案 (5 min)
   ├─ 4.1.2 配置測試 job (5 min)
   └─ 4.1.3 配置安全掃描 job (5 min)

子階段 4.2: Docker 容器化 (10 min)
   ├─ 4.2.1 創建 Dockerfile (5 min)
   ├─ 4.2.2 Docker Compose 配置 (3 min)
   └─ 4.2.3 建置與測試 (2 min)

子階段 4.3: 部署準備 (5 min)
   ├─ 4.3.1 環境變數配置 (3 min)
   └─ 4.3.2 健康檢查 endpoint (2 min)
```

---

## 📝 詳細實作步驟

### 子階段 4.1: GitHub Actions Workflow (15 min)

#### 4.1.1 創建 Workflow 檔案 (5 min)

**Step 1: 創建目錄與檔案**

```bash
# 在專案根目錄下
mkdir -p .github/workflows
touch .github/workflows/ci.yml
```

**Step 2: 基礎 Workflow 結構**

**檔案**: `.github/workflows/ci.yml`

**AI 協作提示詞**:
```
創建 GitHub Actions workflow 檔案，路徑 .github/workflows/ci.yml

觸發條件:
1. push 到 main 分支
2. pull request 到 main 分支

包含以下 jobs (先寫基本結構,後續補充細節):
1. test - 執行後端測試
2. security - 安全掃描
3. docker - 建置 Docker image

使用 Python 3.10，Ubuntu latest runner

提供完整 YAML 結構框架。
```

**預期產出**:
```yaml
name: CI Pipeline

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      # 後續補充

  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      # 後續補充

  docker:
    runs-on: ubuntu-latest
    needs: [test, security]  # 只有測試和安全檢查通過才建置
    steps:
      - uses: actions/checkout@v3
      # 後續補充
```

---

#### 4.1.2 配置測試 Job (5 min)

**AI 協作提示詞**:
```
完善 GitHub Actions workflow 中的 test job

要求:
1. 設置 Python 3.10 環境
2. 安裝 Poetry
3. 安裝依賴 (poetry install)
4. 設置測試數據庫 (PostgreSQL service container)
5. 執行測試 (pytest --cov --cov-report=xml)
6. 上傳覆蓋率報告到 Codecov (可選)
7. 測試覆蓋率要求: 80%

環境變數:
- DATABASE_URL=postgresql://testuser:testpass@localhost:5432/testdb
- JWT_SECRET_KEY=test-secret-key

提供完整 test job 的 YAML 配置。
```

**預期產出**:
```yaml
test:
  runs-on: ubuntu-latest

  services:
    postgres:
      image: postgres:14
      env:
        POSTGRES_USER: testuser
        POSTGRES_PASSWORD: testpass
        POSTGRES_DB: testdb
      options: >-
        --health-cmd pg_isready
        --health-interval 10s
        --health-timeout 5s
        --health-retries 5
      ports:
        - 5432:5432

  steps:
    - name: Checkout code
      uses: actions/checkout@v3

    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.10'

    - name: Install Poetry
      run: |
        curl -sSL https://install.python-poetry.org | python3 -
        echo "$HOME/.local/bin" >> $GITHUB_PATH

    - name: Install dependencies
      working-directory: ./backend
      run: |
        poetry install --no-interaction

    - name: Run tests
      working-directory: ./backend
      env:
        DATABASE_URL: postgresql://testuser:testpass@localhost:5432/testdb
        JWT_SECRET_KEY: test-secret-key-for-ci
      run: |
        poetry run pytest --cov=app --cov-report=xml --cov-report=term

    - name: Check coverage
      working-directory: ./backend
      run: |
        poetry run coverage report --fail-under=80

    - name: Upload coverage to Codecov (optional)
      uses: codecov/codecov-action@v3
      with:
        files: ./backend/coverage.xml
        flags: backend
```

**驗證方法**:
```bash
# 本地測試 (模擬 CI 環境)
cd backend
poetry run pytest --cov=app --cov-report=term
poetry run coverage report --fail-under=80
```

---

#### 4.1.3 配置安全掃描 Job (5 min)

**AI 協作提示詞**:
```
完善 GitHub Actions workflow 中的 security job

使用工具:
1. Bandit - Python 代碼安全掃描
2. Safety - 依賴漏洞掃描

要求:
1. 安裝 Poetry 和依賴
2. 執行 Bandit 掃描 (bandit -r app/ -f json -o bandit-report.json)
3. 執行 Safety 掃描 (safety check --json)
4. 如果發現 high/critical 漏洞,job 失敗

提供完整 security job 的 YAML 配置。
```

**預期產出**:
```yaml
security:
  runs-on: ubuntu-latest

  steps:
    - name: Checkout code
      uses: actions/checkout@v3

    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.10'

    - name: Install Poetry
      run: |
        curl -sSL https://install.python-poetry.org | python3 -
        echo "$HOME/.local/bin" >> $GITHUB_PATH

    - name: Install dependencies
      working-directory: ./backend
      run: |
        poetry install --no-interaction
        poetry add --group dev bandit safety

    - name: Run Bandit security scan
      working-directory: ./backend
      run: |
        poetry run bandit -r app/ -f json -o bandit-report.json || true
        poetry run bandit -r app/ -ll  # 只顯示 medium/high

    - name: Run Safety dependency check
      working-directory: ./backend
      run: |
        poetry run safety check --json || true
        poetry run safety check  # 顯示詳細報告

    - name: Upload security reports
      uses: actions/upload-artifact@v3
      if: always()
      with:
        name: security-reports
        path: |
          backend/bandit-report.json
```

**本地測試**:
```bash
cd backend
poetry add --group dev bandit safety
poetry run bandit -r app/ -ll
poetry run safety check
```

---

### 子階段 4.2: Docker 容器化 (10 min)

#### 4.2.1 創建 Dockerfile (5 min)

**檔案**: `backend/Dockerfile`

**AI 協作提示詞**:
```
創建後端 Dockerfile，路徑 backend/Dockerfile

要求:
1. 基於 python:3.10-slim
2. 安裝 Poetry
3. 複製依賴檔案 (pyproject.toml, poetry.lock)
4. 安裝依賴 (poetry install --no-dev --no-interaction)
5. 複製應用代碼
6. 暴露 8000 端口
7. 啟動命令: uvicorn app.main:app --host 0.0.0.0 --port 8000

優化:
- 使用多階段建置 (減少 image 大小)
- 不包含開發依賴
- 設置非 root 用戶運行

提供完整 Dockerfile。
```

**預期產出**:
```dockerfile
# backend/Dockerfile

# Stage 1: Builder
FROM python:3.10-slim as builder

WORKDIR /app

# Install Poetry
RUN pip install --no-cache-dir poetry==1.6.1

# Copy dependency files
COPY pyproject.toml poetry.lock ./

# Install dependencies (no dev dependencies)
RUN poetry config virtualenvs.create false \
    && poetry install --no-dev --no-interaction --no-ansi

# Stage 2: Runtime
FROM python:3.10-slim

WORKDIR /app

# Create non-root user
RUN useradd -m -u 1000 appuser

# Copy installed packages from builder
COPY --from=builder /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy application code
COPY --chown=appuser:appuser ./app ./app

# Switch to non-root user
USER appuser

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD python -c "import requests; requests.get('http://localhost:8000/health')"

# Run application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**測試建置**:
```bash
cd backend
docker build -t task-management-backend:latest .
```

---

#### 4.2.2 Docker Compose 配置 (3 min)

**檔案**: `docker-compose.yml` (根目錄)

**AI 協作提示詞**:
```
創建 Docker Compose 檔案，路徑 docker-compose.yml

服務:
1. postgres - PostgreSQL 14
   - 環境變數從 .env 讀取
   - 數據持久化 (volume)
   - 健康檢查

2. backend - 後端服務
   - build from ./backend
   - depends_on postgres (等待數據庫健康)
   - 環境變數從 .env 讀取
   - 端口映射 8000:8000

3. frontend (可選) - 前端服務
   - nginx 提供靜態檔案
   - 端口映射 3000:80

網路: 所有服務在同一個 network

提供完整 docker-compose.yml。
```

**預期產出**:
```yaml
version: '3.8'

services:
  postgres:
    image: postgres:14-alpine
    container_name: taskdb
    environment:
      POSTGRES_USER: ${DB_USER:-taskuser}
      POSTGRES_PASSWORD: ${DB_PASSWORD:-taskpass}
      POSTGRES_DB: ${DB_NAME:-taskdb}
    ports:
      - "${DB_PORT:-5432}:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${DB_USER:-taskuser}"]
      interval: 10s
      timeout: 5s
      retries: 5
    networks:
      - app-network

  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    container_name: task-backend
    depends_on:
      postgres:
        condition: service_healthy
    environment:
      DATABASE_URL: postgresql://${DB_USER:-taskuser}:${DB_PASSWORD:-taskpass}@postgres:5432/${DB_NAME:-taskdb}
      JWT_SECRET_KEY: ${JWT_SECRET_KEY}
      JWT_ALGORITHM: HS256
      JWT_EXPIRATION_DAYS: 7
    ports:
      - "8000:8000"
    networks:
      - app-network
    restart: unless-stopped

volumes:
  postgres_data:

networks:
  app-network:
    driver: bridge
```

**測試運行**:
```bash
# 創建 .env 檔案
cat > .env << EOF
DB_USER=taskuser
DB_PASSWORD=taskpass
DB_NAME=taskdb
JWT_SECRET_KEY=your-super-secret-key-change-in-production
EOF

# 啟動服務
docker-compose up -d

# 檢查狀態
docker-compose ps

# 查看日誌
docker-compose logs -f backend

# 測試 API
curl http://localhost:8000/health
```

---

#### 4.2.3 GitHub Actions Docker Job (2 min)

**AI 協作提示詞**:
```
完善 GitHub Actions workflow 中的 docker job

要求:
1. 只有在 test 和 security jobs 通過後才執行
2. 建置 Docker image
3. (可選) 推送到 Docker Hub 或 GitHub Container Registry
4. 標記 image 為 latest 和 commit SHA

提供完整 docker job 的 YAML 配置。
```

**預期產出**:
```yaml
docker:
  runs-on: ubuntu-latest
  needs: [test, security]
  if: github.event_name == 'push' && github.ref == 'refs/heads/main'

  steps:
    - name: Checkout code
      uses: actions/checkout@v3

    - name: Set up Docker Buildx
      uses: docker/setup-buildx-action@v2

    - name: Log in to Docker Hub (optional)
      uses: docker/login-action@v2
      with:
        username: ${{ secrets.DOCKER_USERNAME }}
        password: ${{ secrets.DOCKER_PASSWORD }}

    - name: Extract metadata
      id: meta
      uses: docker/metadata-action@v4
      with:
        images: your-dockerhub-username/task-management-backend
        tags: |
          type=ref,event=branch
          type=sha,prefix={{branch}}-
          type=raw,value=latest,enable={{is_default_branch}}

    - name: Build and push Docker image
      uses: docker/build-push-action@v4
      with:
        context: ./backend
        file: ./backend/Dockerfile
        push: true
        tags: ${{ steps.meta.outputs.tags }}
        labels: ${{ steps.meta.outputs.labels }}
        cache-from: type=gha
        cache-to: type=gha,mode=max
```

---

### 子階段 4.3: 部署準備 (5 min)

#### 4.3.1 環境變數配置 (3 min)

**GitHub Secrets 設置**:

1. 進入 GitHub repo → Settings → Secrets and variables → Actions
2. 添加以下 secrets:

```
DOCKER_USERNAME=your-dockerhub-username
DOCKER_PASSWORD=your-dockerhub-password
JWT_SECRET_KEY=your-production-secret-key
DATABASE_URL=postgresql://user:pass@host:5432/db (生產環境)
```

**本地 .env 範例**:

**檔案**: `.env.example`

```env
# Database
DB_USER=taskuser
DB_PASSWORD=change-this-password
DB_NAME=taskdb
DB_PORT=5432

# JWT
JWT_SECRET_KEY=change-this-to-random-secret-key
JWT_ALGORITHM=HS256
JWT_EXPIRATION_DAYS=7

# CORS
CORS_ORIGINS=http://localhost:3000,http://localhost:5173

# Environment
ENVIRONMENT=development
```

**重要**: 確保 `.env` 在 `.gitignore` 中！

---

#### 4.3.2 健康檢查 Endpoint (2 min)

**檔案**: `backend/app/main.py`

**AI 協作提示詞**:
```
在 FastAPI 應用中添加健康檢查 endpoint

路徑: GET /health

返回:
{
  "status": "healthy",
  "timestamp": "2025-10-30T12:00:00Z",
  "version": "1.0.0"
}

不需要認證

添加到 app/main.py
```

**預期產出**:
```python
from datetime import datetime

@app.get("/health")
async def health_check():
    """健康檢查 endpoint (用於 Docker healthcheck 和監控)"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "version": "1.0.0"
    }
```

**測試**:
```bash
curl http://localhost:8000/health
```

---

## ✅ 階段完成檢查清單

### CI/CD Pipeline
- [ ] GitHub Actions workflow 創建完成
- [ ] push 代碼後自動觸發 workflow
- [ ] test job 通過 (所有測試通過,覆蓋率 ≥ 80%)
- [ ] security job 通過 (無 critical/high 漏洞)
- [ ] docker job 成功建置 image

### Docker
- [ ] Dockerfile 創建完成
- [ ] 本地能成功建置 Docker image
- [ ] docker-compose up 能正常啟動服務
- [ ] 健康檢查 endpoint 正常

### 安全性
- [ ] 所有敏感資訊使用環境變數
- [ ] .env 檔案在 .gitignore 中
- [ ] GitHub Secrets 配置完成
- [ ] 密碼和 secret keys 已更換 (不使用範例值)

---

## 🐛 常見問題

### Q1: GitHub Actions 中 Poetry 安裝失敗

**症狀**:
```
curl: (7) Failed to connect to install.python-poetry.org
```

**解決方案**:
```yaml
- name: Install Poetry
  run: |
    pip install poetry==1.6.1  # 直接用 pip 安裝
```

---

### Q2: Docker 建置時記憶體不足

**症狀**:
```
Error: failed to solve: executor failed running: out of memory
```

**解決方案**:
```yaml
- name: Build Docker image
  uses: docker/build-push-action@v4
  with:
    context: ./backend
    push: false
    cache-from: type=gha  # 使用 GitHub Actions cache
    cache-to: type=gha,mode=max
```

---

### Q3: 測試在 CI 中失敗但本地通過

**可能原因**:
1. 本地環境變數與 CI 不同
2. 時區差異導致時間相關測試失敗
3. 依賴版本不一致

**解決方案**:
```yaml
- name: Run tests
  env:
    TZ: UTC  # 統一時區
    DATABASE_URL: ${{ secrets.DATABASE_URL }}
  run: |
    poetry run pytest -v  # 顯示詳細輸出
```

---

## 🚀 下一步

恭喜完成 CI/CD 設置！現在每次 push 代碼都會自動測試和檢查質量。

**接下來**:
→ 前往 `階段5_文檔交付/README.md` 生成完整的專案文檔

---

## 📚 延伸學習

### 進階 CI/CD 功能

1. **多環境部署**
   - Staging 環境自動部署 (develop 分支)
   - Production 環境手動審批後部署 (main 分支)

2. **效能測試**
   - 使用 Locust 或 k6 進行負載測試
   - API 回應時間監控

3. **自動化發布**
   - 使用 semantic-release 自動生成版本號
   - 自動生成 CHANGELOG

4. **監控與告警**
   - 整合 Sentry (錯誤追蹤)
   - 整合 Prometheus + Grafana (指標監控)

---

**記住**: CI/CD 是「自動化的安全網」,讓你放心地快速迭代！
