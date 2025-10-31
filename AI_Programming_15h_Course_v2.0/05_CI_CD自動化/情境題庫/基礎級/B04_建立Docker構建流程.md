# B04：建立Docker構建流程

## 📋 情境資訊

**難度等級**：⭐ 基礎級
**預估時間**：35 分鐘
**核心技能**：Docker、GitHub Container Registry、多階段構建
**前置知識**：B03（整合靜態分析）

---

## 🎯 情境背景

你的團隊現在有了完整的測試、品質檢查和安全掃描，但部署時又遇到新問題：

**環境不一致災難**：
```bash
# 開發環境（Mac）
$ python --version
Python 3.11.5

$ pip list | grep fastapi
fastapi==0.104.1

# 生產環境（Ubuntu）
$ python3 --version
Python 3.8.10

$ pip3 list | grep fastapi
fastapi==0.95.2

# 結果：「在我電腦上可以跑」症候群復發！
```

**昨天的部署事故**：
1. 小明在本機開發時用 Python 3.11 的新語法
2. 生產環境是 Python 3.8，不支援該語法
3. 部署失敗，服務中斷 2 小時
4. 緊急回退，加班修復相容性

**DevOps 團隊的要求**：
> 「我們需要容器化！Docker 可以確保開發、測試、生產環境完全一致。」

**團隊決定**：
> 「建立自動化 Docker 構建流程，每次 CI 通過後自動產生 Docker 映像。」

**你的任務**：
在現有的 CI/CD 管線中加入 Docker 構建流程，自動產生最佳化的容器映像。

---

## 📦 專案結構

延續 B03 的專案：

```
my-fastapi-project/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── models.py
│   ├── utils.py
│   └── security.py
│
├── tests/
│   ├── __init__.py
│   ├── test_main.py
│   └── test_security.py
│
├── requirements.txt
├── pyproject.toml
├── .bandit
├── Dockerfile              # 新增：Docker 構建檔案
├── .dockerignore           # 新增：Docker 忽略檔案
├── docker-compose.yml      # 新增：本機開發用
├── .github/
│   └── workflows/
│       └── test.yml        # 現有的完整 CI workflow
│
├── .gitignore
└── README.md
```

**應用程式範例（app/main.py）**：
```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
import uvicorn

app = FastAPI(
    title="My FastAPI App",
    description="A sample FastAPI application with CI/CD",
    version="1.0.0"
)

class HealthResponse(BaseModel):
    status: str
    environment: str
    version: str

@app.get("/")
def read_root():
    return {"message": "Hello World"}

@app.get("/health", response_model=HealthResponse)
def health_check():
    return HealthResponse(
        status="healthy",
        environment=os.getenv("ENVIRONMENT", "development"),
        version="1.0.0"
    )

@app.get("/users/{user_id}")
def get_user(user_id: int):
    if user_id < 1:
        raise HTTPException(status_code=400, detail="Invalid user ID")
    return {"user_id": user_id, "name": f"User {user_id}"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

**依賴檔案（requirements.txt）**：
```
fastapi==0.104.1
uvicorn[standard]==0.24.0
pydantic==2.4.2
python-multipart==0.0.6
```

---

## 🎯 任務目標

### 必達目標
1. ✅ 建立生產級別的 **Dockerfile**（多階段構建）
2. ✅ 建立 **.dockerignore** 最佳化構建效率
3. ✅ 在 GitHub Actions 中整合 **Docker 構建**
4. ✅ 推送映像到 **GitHub Container Registry**
5. ✅ 確保映像安全性（非 root 使用者、健康檢查）

### 加分項目
- 🌟 建立 **docker-compose.yml** 用於本機開發
- 🌟 使用 **BuildKit** 加速構建
- 🌟 實作 **Docker 映像快取** 策略
- 🌟 加入 **映像掃描**（漏洞檢測）

---

## 📚 學習檢查點

完成此情境題時，請確認你能回答：

### Checkpoint 1：Docker 基礎
- [ ] 什麼是容器化？解決了什麼問題？
- [ ] Dockerfile 的基本結構是什麼？
- [ ] 多階段構建的優勢是什麼？
- [ ] .dockerignore 的作用是什麼？

### Checkpoint 2：最佳實踐
- [ ] 為什麼要使用非 root 使用者執行容器？
- [ ] 如何最小化 Docker 映像大小？
- [ ] 什麼是映像層（layer）快取？
- [ ] 健康檢查（health check）的重要性？

### Checkpoint 3：CI/CD 整合
- [ ] 如何在 GitHub Actions 中構建 Docker 映像？
- [ ] GitHub Container Registry 與 Docker Hub 的差異？
- [ ] 如何管理 Docker 映像的標籤（tag）？

---

## 🚀 實作步驟

### 方法 1：用 Claude 生成（推薦）

#### 步驟 1：準備提示詞

```
我需要為 Python FastAPI 應用建立完整的 Docker 化流程。

應用詳情：
- FastAPI 應用
- Python 3.11
- 依賴在 requirements.txt 中
- 應用監聽 port 8000

需求：
1. 生產級別的 Dockerfile（多階段構建）
2. 最小化映像大小
3. 安全性（非 root 使用者）
4. 加入健康檢查
5. GitHub Actions workflow 自動構建並推送到 GHCR
6. 本機開發用的 docker-compose.yml

請提供：
1. 完整的 Dockerfile
2. .dockerignore 檔案
3. docker-compose.yml
4. 修改後的 GitHub Actions workflow
5. 本機測試指令

請加上詳細註解說明每個步驟的原理。
```

#### 步驟 2：建立 Docker 檔案

根據 Claude 的建議，建立所需檔案：

```bash
# 建立 Dockerfile
touch Dockerfile

# 建立 .dockerignore
touch .dockerignore

# 建立 docker-compose.yml
touch docker-compose.yml
```

#### 步驟 3：本機測試

```bash
# 構建映像
docker build -t my-fastapi-app .

# 執行容器
docker run -p 8000:8000 my-fastapi-app

# 測試應用
curl http://localhost:8000/health
```

#### 步驟 4：修改 Workflow

將 Claude 生成的 Docker 構建步驟加入現有 workflow。

### 方法 2：手動編寫（學習用）

#### 步驟 1：建立 Dockerfile

**多階段構建 Dockerfile**：

```dockerfile
# ===== 第一階段：構建階段 =====
FROM python:3.11 AS builder

# 設定工作目錄
WORKDIR /app

# 複製依賴檔案（利用 Docker layer 快取）
COPY requirements.txt .

# 安裝依賴到用戶目錄（不需要 root 權限）
RUN pip install --user --no-cache-dir --upgrade pip && \
    pip install --user --no-cache-dir -r requirements.txt

# ===== 第二階段：執行階段 =====
FROM python:3.11-slim AS runtime

# 建立非 root 使用者
RUN useradd --create-home --shell /bin/bash --uid 1000 appuser

# 設定工作目錄
WORKDIR /app

# 從構建階段複製已安裝的依賴
COPY --from=builder /root/.local /home/appuser/.local

# 複製應用程式代碼
COPY --chown=appuser:appuser app/ ./app/

# 設定環境變數
ENV PATH=/home/appuser/.local/bin:$PATH \
    PYTHONPATH=/app \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# 切換到非 root 使用者
USER appuser

# 暴露端口
EXPOSE 8000

# 健康檢查
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# 啟動應用
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

#### 步驟 2：建立 .dockerignore

```dockerignore
# Git
.git
.gitignore
.gitattributes

# CI/CD
.github

# Python
__pycache__
*.pyc
*.pyo
*.pyd
.Python
env
pip-log.txt
pip-delete-this-directory.txt
.tox
.coverage
.coverage.*
.pytest_cache
nosetests.xml
coverage.xml
*.cover
*.log
.cache
.mypy_cache

# Virtual environments
.venv
venv/
ENV/

# IDEs
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
.DS_Store?
._*
.Spotlight-V100
.Trashes
ehthumbs.db
Thumbs.db

# Documentation
*.md
docs/

# Tests
tests/
test_*.py
*_test.py

# Development files
docker-compose.yml
Dockerfile*
requirements-dev.txt

# Build artifacts
build/
dist/
*.egg-info/
```

#### 步驟 3：建立 docker-compose.yml

```yaml
version: '3.8'

services:
  app:
    build:
      context: .
      dockerfile: Dockerfile
    ports:
      - "8000:8000"
    environment:
      - ENVIRONMENT=development
      - DEBUG=true
    volumes:
      # 開發時即時載入代碼變更
      - ./app:/app/app:ro
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s

  # 可選：加入資料庫服務
  db:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: myapp
      POSTGRES_USER: myuser
      POSTGRES_PASSWORD: mypassword
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    restart: unless-stopped

volumes:
  postgres_data:
```

#### 步驟 4：修改 GitHub Actions Workflow

在現有 workflow 中加入 Docker 構建 job：

```yaml
name: Complete CI/CD Pipeline with Docker

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}

jobs:
  # ... 保留現有的 quality-check, security-scan, test jobs

  # 新增：Docker 構建
  build-and-push:
    name: Build and Push Docker Image
    needs: [quality-check, security-scan, test]
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write

    steps:
    - name: Checkout code
      uses: actions/checkout@v4

    # 設定 Docker Buildx（支援進階功能）
    - name: Set up Docker Buildx
      uses: docker/setup-buildx-action@v3

    # 登入 GitHub Container Registry
    - name: Login to Container Registry
      uses: docker/login-action@v3
      with:
        registry: ${{ env.REGISTRY }}
        username: ${{ github.actor }}
        password: ${{ secrets.GITHUB_TOKEN }}

    # 提取 metadata（標籤、labels）
    - name: Extract metadata
      id: meta
      uses: docker/metadata-action@v5
      with:
        images: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}
        tags: |
          type=ref,event=branch
          type=ref,event=pr
          type=sha,prefix={{branch}}-
          type=raw,value=latest,enable={{is_default_branch}}

    # 構建並推送 Docker 映像
    - name: Build and push Docker image
      uses: docker/build-push-action@v5
      with:
        context: .
        platforms: linux/amd64,linux/arm64  # 多平台支援
        push: true
        tags: ${{ steps.meta.outputs.tags }}
        labels: ${{ steps.meta.outputs.labels }}
        cache-from: type=gha  # GitHub Actions 快取
        cache-to: type=gha,mode=max

    # 輸出映像資訊
    - name: Output image info
      run: |
        echo "## 🐳 Docker Image Built" >> $GITHUB_STEP_SUMMARY
        echo "" >> $GITHUB_STEP_SUMMARY
        echo "**Registry:** ${{ env.REGISTRY }}" >> $GITHUB_STEP_SUMMARY
        echo "**Repository:** ${{ env.IMAGE_NAME }}" >> $GITHUB_STEP_SUMMARY
        echo "**Tags:**" >> $GITHUB_STEP_SUMMARY
        echo '${{ steps.meta.outputs.tags }}' | sed 's/^/- /' >> $GITHUB_STEP_SUMMARY
```

---

## ✅ 參考解答

### 完整 Dockerfile

```dockerfile
# ===== Multi-stage build for optimized production image =====

# Stage 1: Builder
FROM python:3.11 AS builder

# Set build arguments
ARG DEBIAN_FRONTEND=noninteractive

# Install system dependencies needed for building
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy dependency files first (for better layer caching)
COPY requirements.txt .

# Install Python dependencies to user directory
RUN pip install --user --no-cache-dir --upgrade pip && \
    pip install --user --no-cache-dir -r requirements.txt

# Stage 2: Runtime
FROM python:3.11-slim AS runtime

# Install runtime dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Create non-root user for security
RUN useradd --create-home --shell /bin/bash --uid 1000 appuser

# Set working directory
WORKDIR /app

# Copy installed packages from builder stage
COPY --from=builder /root/.local /home/appuser/.local

# Copy application code with proper ownership
COPY --chown=appuser:appuser app/ ./app/

# Set environment variables
ENV PATH=/home/appuser/.local/bin:$PATH \
    PYTHONPATH=/app \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PORT=8000

# Switch to non-root user
USER appuser

# Expose the port the app runs on
EXPOSE $PORT

# Add health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:$PORT/health || exit 1

# Run the application
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port $PORT"]
```

### .dockerignore

```dockerignore
# === Git ===
.git
.gitignore
.gitattributes

# === CI/CD ===
.github
.gitlab-ci.yml
Jenkinsfile

# === Python ===
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# === Virtual Environments ===
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# === Testing ===
.tox/
.coverage
.coverage.*
.cache
.pytest_cache/
nosetests.xml
coverage.xml
*.cover
.hypothesis/

# === IDEs ===
.vscode/
.idea/
*.swp
*.swo
*~
.spyderproject
.spyproject

# === OS ===
.DS_Store
.DS_Store?
._*
.Spotlight-V100
.Trashes
ehthumbs.db
Thumbs.db

# === Documentation ===
*.md
docs/
README*

# === Development Files ===
docker-compose*.yml
Dockerfile*
requirements-dev.txt
.pre-commit-config.yaml

# === Logs ===
*.log
logs/

# === Temporary files ===
tmp/
temp/
```

### docker-compose.yml

```yaml
version: '3.8'

services:
  app:
    build:
      context: .
      dockerfile: Dockerfile
      target: runtime
    ports:
      - "8000:8000"
    environment:
      - ENVIRONMENT=development
      - PORT=8000
    volumes:
      # Mount source code for development (read-only)
      - ./app:/app/app:ro
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
    depends_on:
      - db
      - redis

  # Database service
  db:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: myapp_dev
      POSTGRES_USER: dev_user
      POSTGRES_PASSWORD: dev_password
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./scripts/init-db.sql:/docker-entrypoint-initdb.d/init.sql:ro
    restart: unless-stopped
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U dev_user -d myapp_dev"]
      interval: 30s
      timeout: 10s
      retries: 3

  # Cache service
  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 30s
      timeout: 10s
      retries: 3

volumes:
  postgres_data:
  redis_data:

# Development network
networks:
  default:
    name: myapp_dev_network
```

### 完整 GitHub Actions Workflow

```yaml
name: Complete CI/CD Pipeline with Docker

on:
  push:
    branches: [main, develop]
    tags: ['v*']
  pull_request:
    branches: [main]

env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}
  PYTHON_VERSION: '3.11'

jobs:
  # Job 1: Code Quality
  quality-check:
    name: Code Quality Check
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v4
        with:
          python-version: ${{ env.PYTHON_VERSION }}
      - name: Install tools
        run: |
          pip install flake8 black isort mypy
      - name: Run quality checks
        run: |
          flake8 app tests
          black --check app tests
          isort --check-only app tests

  # Job 2: Security Scan
  security-scan:
    name: Security Analysis
    needs: quality-check
    runs-on: ubuntu-latest
    permissions:
      security-events: write
      contents: read
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v4
        with:
          python-version: ${{ env.PYTHON_VERSION }}

      # CodeQL Analysis
      - name: Initialize CodeQL
        uses: github/codeql-action/init@v3
        with:
          languages: python
          queries: security-extended

      - name: Perform CodeQL Analysis
        uses: github/codeql-action/analyze@v3

      # bandit Security Scan
      - name: Run bandit
        run: |
          pip install bandit[toml]
          bandit -r app -f json -o bandit-report.json
          bandit -r app

  # Job 3: Tests
  test:
    name: Run Tests
    needs: security-scan
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v4
        with:
          python-version: ${{ env.PYTHON_VERSION }}
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install pytest pytest-cov httpx
      - name: Run tests
        run: |
          pytest --cov=app --cov-report=xml -v
      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          file: ./coverage.xml

  # Job 4: Build and Push Docker Image
  build-and-push:
    name: Build Docker Image
    needs: [test]
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write
    outputs:
      image-digest: ${{ steps.build.outputs.digest }}
      image-tags: ${{ steps.meta.outputs.tags }}

    steps:
    - name: Checkout code
      uses: actions/checkout@v4

    # Set up Docker Buildx with advanced features
    - name: Set up Docker Buildx
      uses: docker/setup-buildx-action@v3
      with:
        platforms: linux/amd64,linux/arm64

    # Login to GitHub Container Registry
    - name: Login to Container Registry
      if: github.event_name != 'pull_request'
      uses: docker/login-action@v3
      with:
        registry: ${{ env.REGISTRY }}
        username: ${{ github.actor }}
        password: ${{ secrets.GITHUB_TOKEN }}

    # Extract metadata for tags and labels
    - name: Extract metadata
      id: meta
      uses: docker/metadata-action@v5
      with:
        images: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}
        tags: |
          type=ref,event=branch
          type=ref,event=pr
          type=semver,pattern={{version}}
          type=semver,pattern={{major}}.{{minor}}
          type=sha,prefix={{branch}}-,format=short
          type=raw,value=latest,enable={{is_default_branch}}

    # Build and push Docker image
    - name: Build and push Docker image
      id: build
      uses: docker/build-push-action@v5
      with:
        context: .
        platforms: linux/amd64,linux/arm64
        push: ${{ github.event_name != 'pull_request' }}
        tags: ${{ steps.meta.outputs.tags }}
        labels: ${{ steps.meta.outputs.labels }}
        cache-from: type=gha
        cache-to: type=gha,mode=max
        provenance: false  # 避免多平台構建問題

    # Generate summary
    - name: Generate build summary
      run: |
        echo "## 🐳 Docker Image Build Summary" >> $GITHUB_STEP_SUMMARY
        echo "" >> $GITHUB_STEP_SUMMARY
        echo "**Repository:** \`${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}\`" >> $GITHUB_STEP_SUMMARY
        echo "**Digest:** \`${{ steps.build.outputs.digest }}\`" >> $GITHUB_STEP_SUMMARY
        echo "" >> $GITHUB_STEP_SUMMARY
        echo "**Tags:**" >> $GITHUB_STEP_SUMMARY
        echo '${{ steps.meta.outputs.tags }}' | sed 's/^/- `/' | sed 's/$/`/' >> $GITHUB_STEP_SUMMARY

  # Job 5: Container Security Scan (Optional)
  container-scan:
    name: Container Security Scan
    needs: build-and-push
    if: github.event_name != 'pull_request'
    runs-on: ubuntu-latest
    steps:
    - name: Run Trivy vulnerability scanner
      uses: aquasecurity/trivy-action@master
      with:
        image-ref: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:${{ github.sha }}
        format: 'sarif'
        output: 'trivy-results.sarif'

    - name: Upload Trivy scan results
      uses: github/codeql-action/upload-sarif@v3
      with:
        sarif_file: 'trivy-results.sarif'
```

---

## 🔍 驗證與除錯

### 本機測試完整流程

**1. 構建映像**：
```bash
# 構建映像
docker build -t my-fastapi-app:latest .

# 查看映像大小
docker images my-fastapi-app

# 檢查映像層
docker history my-fastapi-app:latest
```

**2. 運行容器**：
```bash
# 運行容器
docker run -d -p 8000:8000 --name my-app my-fastapi-app:latest

# 檢查容器狀態
docker ps

# 查看日誌
docker logs my-app

# 測試健康檢查
docker exec my-app curl -f http://localhost:8000/health
```

**3. 測試應用**：
```bash
# 基本測試
curl http://localhost:8000/
curl http://localhost:8000/health
curl http://localhost:8000/users/123

# 負載測試（可選）
ab -n 1000 -c 10 http://localhost:8000/health
```

**4. 使用 docker-compose**：
```bash
# 啟動完整服務
docker-compose up -d

# 查看服務狀態
docker-compose ps

# 查看日誌
docker-compose logs app

# 停止服務
docker-compose down
```

### 優化與除錯

**映像大小優化**：
```bash
# 比較不同 base image 的大小
docker build -f Dockerfile.python-slim -t app:slim .
docker build -f Dockerfile.python-alpine -t app:alpine .
docker build -f Dockerfile.distroless -t app:distroless .

docker images | grep app
```

**構建快取分析**：
```bash
# 查看構建快取使用情況
docker buildx du

# 清理構建快取
docker buildx prune
```

**安全掃描**：
```bash
# 使用 Trivy 掃描映像
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock \
    aquasec/trivy image my-fastapi-app:latest

# 使用 Docker Scout (新)
docker scout quickview my-fastapi-app:latest
docker scout cves my-fastapi-app:latest
```

### 常見問題與解決

**問題 1：映像太大**
```
映像大小超過 1GB
```

**解決方案**：
```dockerfile
# 使用更小的 base image
FROM python:3.11-alpine AS runtime

# 清理 apt cache
RUN apt-get update && apt-get install -y curl \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# 使用 .dockerignore 排除不必要檔案
```

**問題 2：權限問題**
```
Permission denied when running container
```

**解決方案**：
```dockerfile
# 確保檔案擁有者正確
COPY --chown=appuser:appuser app/ ./app/

# 檢查工作目錄權限
RUN chown -R appuser:appuser /app
```

**問題 3：健康檢查失敗**
```
Health check failing: curl: command not found
```

**解決方案**：
```dockerfile
# 確保 curl 已安裝
RUN apt-get update && apt-get install -y curl

# 或使用 Python 內建功能
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')"
```

---

## 🌟 延伸挑戰

### 挑戰 1：多階段優化

建立更精細的多階段構建：

```dockerfile
# Stage 1: 依賴下載
FROM python:3.11 AS dependencies
WORKDIR /app
COPY requirements.txt .
RUN pip download -r requirements.txt -d /app/packages

# Stage 2: 依賴安裝
FROM python:3.11 AS builder
WORKDIR /app
COPY --from=dependencies /app/packages /app/packages
COPY requirements.txt .
RUN pip install --user --no-index --find-links /app/packages -r requirements.txt

# Stage 3: 執行環境
FROM python:3.11-slim AS runtime
# ... 剩餘配置
```

### 挑戰 2：Distroless 映像

使用 Google 的 distroless 映像提升安全性：

```dockerfile
FROM gcr.io/distroless/python3-debian11
COPY --from=builder /root/.local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY app/ /app/
WORKDIR /app
EXPOSE 8000
CMD ["app.main:app"]
```

### 挑戰 3：BuildKit 最佳化

使用 BuildKit 的進階功能：

```dockerfile
# syntax=docker/dockerfile:1.4
FROM python:3.11 AS builder

# 使用快取掛載
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install --user -r requirements.txt

# 使用 bind mount 避免複製
RUN --mount=type=bind,source=requirements.txt,target=/tmp/requirements.txt \
    pip install --user -r /tmp/requirements.txt
```

### 挑戰 4：映像簽名和驗證

加入映像簽名流程：

```yaml
- name: Install cosign
  uses: sigstore/cosign-installer@v3

- name: Sign container image
  run: |
    cosign sign --yes ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}@${{ steps.build.outputs.digest }}
  env:
    COSIGN_EXPERIMENTAL: 1
```

---

## 📖 知識回顧

完成這個情境題後，你應該學會：

### 核心概念
- ✅ 容器化的價值（環境一致性）
- ✅ Docker 映像的分層架構
- ✅ 多階段構建的優勢
- ✅ 容器安全最佳實踐

### 實戰技能
- ✅ 編寫生產級別的 Dockerfile
- ✅ 設計 .dockerignore 最佳化構建
- ✅ 在 CI/CD 中整合 Docker 構建
- ✅ 使用 GitHub Container Registry

### 最佳實踐
- ✅ 最小化映像大小
- ✅ 使用非 root 使用者
- ✅ 實作健康檢查
- ✅ 有效利用構建快取

### 進階概念
- ✅ 多平台映像構建
- ✅ 容器安全掃描
- ✅ 映像標籤策略
- ✅ BuildKit 最佳化技巧

---

## 📝 學習筆記範本

```markdown
## B04 學習筆記

### 完成時間
[填寫]

### Docker 概念理解
- **容器 vs 虛擬機**：[你的理解]
- **映像 vs 容器**：[你的理解]
- **層級架構**：[你的理解]

### Dockerfile 最佳實踐
1. **多階段構建**：[優勢和應用場景]
2. **快取最佳化**：[策略和技巧]
3. **安全性考量**：[非 root 使用者、最小權限]

### 遇到的問題
1. [問題描述]
   - 解決方案：[...]
2. [問題描述]
   - 解決方案：[...]

### 映像最佳化成果
- **原始大小**：[...]
- **最佳化後大小**：[...]
- **減少比例**：[...]

### 關鍵學習點
1. 環境一致性的重要性：[...]
2. 容器化的安全考量：[...]
3. CI/CD 整合的技巧：[...]

### 應用到實際專案的計畫
- [ ] 為現有專案建立 Dockerfile
- [ ] 設定自動化構建流程
- [ ] 整合容器安全掃描

### 下一步
- [ ] 完成挑戰 1
- [ ] 進入 B05
```

---

**恭喜完成 B04！** 你已經掌握了 Docker 容器化的核心技能。接下來前往 `B05_配置依賴掃描.md`，學習自動化的依賴管理和安全監控。