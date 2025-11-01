# C04：後端 API 完整管線建立 ⭐

## 📋 情境資訊

**難度等級**：⭐⭐ 組合級
**預估時間**：2-2.5 小時
**核心技能**：完整後端 CI/CD、API 測試、資料庫遷移、文檔生成
**前置知識**：基礎級 B01-B06 全部完成

---

## 🎯 情境背景

你是一家快速成長的 SaaS 公司的後端技術 Lead，負責為核心 API 服務建立企業級的 CI/CD 管線。

**公司現況**：
- 產品：B2B 專案管理平台（類似 Asana/Jira）
- 團隊：8 個後端工程師
- 技術棧：FastAPI + PostgreSQL + Redis + Celery
- 客戶：50+ 企業客戶，20,000+ MAU

**上個月的慘痛教訓**：

```bash
# 生產環境故障報告 #247
日期：2024-10-15
持續時間：4 小時
影響用戶：15,000
經濟損失：$80,000（SLA 賠償）

時間軸：
14:00 - 部署新版本 v2.5.0 到生產環境
14:15 - 開始收到大量 500 錯誤告警
14:20 - 發現資料庫遷移腳本有 bug（刪除了重要欄位）
14:25 - 嘗試回退，但回退腳本失敗
14:30 - 緊急停止服務，手動修復資料庫
18:00 - 服務恢復

根本原因分析：
1. ❌ 資料庫遷移沒有在 CI 中測試
2. ❌ API 整合測試不完整（未覆蓋關鍵流程）
3. ❌ 沒有 API 文檔（客戶端團隊不知道 breaking change）
4. ❌ 部署沒有灰度策略（一次影響所有用戶）
5. ❌ 回退計劃未經測試

客戶反應：
- 3 家企業客戶威脅取消合約
- NPS 分數從 72 下降到 45
- 大量負評湧入 G2/Capterra
```

**CTO 的緊急會議**：
> 「這種事情不能再發生了。我們需要一套完整的後端 CI/CD 管線，涵蓋從單元測試到資料庫遷移驗證，再到 API 文檔生成的所有環節。我們的目標是：**任何進入生產環境的代碼都經過自動化驗證，部署成功率達到 99.9%**。」

**你的任務**：
設計並實作完整的後端 API CI/CD 管線，包括：
- 多層次自動化測試（單元 + 整合 + API + 負載）
- 資料庫遷移安全驗證
- API 文檔自動生成與版本管理
- 容器化構建與優化
- 多環境部署策略（dev/staging/prod）
- 完整的監控與告警

---

## 📦 專案結構

這是一個複雜的企業級 API 專案：

```
project-mgmt-api/
├── app/
│   ├── __init__.py
│   ├── main.py                    # FastAPI 應用入口
│   ├── config.py                  # 配置管理
│   ├── database.py                # 資料庫連接
│   ├── dependencies.py            # 依賴注入
│   │
│   ├── models/                    # SQLAlchemy Models
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── project.py
│   │   ├── task.py
│   │   └── comment.py
│   │
│   ├── schemas/                   # Pydantic Schemas
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── project.py
│   │   ├── task.py
│   │   └── comment.py
│   │
│   ├── routers/                   # API Routes
│   │   ├── __init__.py
│   │   ├── auth.py               # 認證相關
│   │   ├── users.py              # 用戶管理
│   │   ├── projects.py           # 專案管理
│   │   ├── tasks.py              # 任務管理
│   │   └── comments.py           # 評論功能
│   │
│   ├── services/                  # 業務邏輯
│   │   ├── __init__.py
│   │   ├── auth_service.py
│   │   ├── project_service.py
│   │   └── task_service.py
│   │
│   └── utils/                     # 工具函數
│       ├── __init__.py
│       ├── auth.py
│       ├── pagination.py
│       └── validators.py
│
├── alembic/                       # 資料庫遷移
│   ├── versions/
│   │   ├── 001_initial_schema.py
│   │   ├── 002_add_projects.py
│   │   └── 003_add_tasks.py
│   ├── env.py
│   └── script.py.mako
│
├── tests/
│   ├── __init__.py
│   ├── conftest.py               # pytest 配置
│   │
│   ├── unit/                     # 單元測試
│   │   ├── test_services/
│   │   ├── test_utils/
│   │   └── test_models/
│   │
│   ├── integration/              # 整合測試
│   │   ├── test_database/
│   │   └── test_redis/
│   │
│   ├── api/                      # API 測試
│   │   ├── test_auth.py
│   │   ├── test_projects.py
│   │   └── test_tasks.py
│   │
│   └── load/                     # 負載測試
│       ├── locustfile.py
│       └── load_test_config.py
│
├── migrations/                    # 自訂遷移腳本
│   ├── seed_data.py
│   └── rollback_scripts/
│
├── scripts/                       # 自動化腳本
│   ├── run_migrations.sh
│   ├── health_check.sh
│   └── generate_docs.sh
│
├── .github/
│   ├── workflows/
│   │   ├── ci.yml               # CI 管線
│   │   ├── deploy-dev.yml       # Dev 部署
│   │   ├── deploy-staging.yml   # Staging 部署
│   │   └── deploy-prod.yml      # Prod 部署
│   │
│   └── actions/                  # 自訂 Actions
│       └── migration-test/
│
├── docs/
│   ├── api/                      # 自動生成的 API 文檔
│   ├── architecture.md
│   └── deployment.md
│
├── docker/
│   ├── Dockerfile
│   ├── Dockerfile.dev
│   └── docker-compose.yml
│
├── requirements.txt
├── requirements-dev.txt
├── alembic.ini
├── pytest.ini
└── README.md
```

---

## 🎬 情境展開

### 階段 1：多層次測試金字塔（30 分鐘）

**任務**：建立完整的測試體系。

#### 測試金字塔設計

```
           /\
          /  \  E2E Tests (5%)
         /----\
        / API  \ API Tests (15%)
       /--------\
      /Integration\ Integration Tests (30%)
     /------------\
    / Unit Tests   \ Unit Tests (50%)
   /----------------\
```

**具體實作**：

**1. 單元測試範例**（`tests/unit/test_services/test_project_service.py`）

```python
import pytest
from unittest.mock import Mock, patch
from app.services.project_service import ProjectService
from app.models.project import Project

class TestProjectService:
    @pytest.fixture
    def project_service(self):
        return ProjectService()

    @pytest.fixture
    def mock_db(self):
        return Mock()

    def test_create_project_success(self, project_service, mock_db):
        # Arrange
        project_data = {
            "name": "Test Project",
            "description": "Test Description",
            "owner_id": 1
        }

        # Act
        result = project_service.create_project(mock_db, project_data)

        # Assert
        assert result.name == "Test Project"
        mock_db.add.assert_called_once()
        mock_db.commit.assert_called_once()

    def test_create_project_duplicate_name(self, project_service, mock_db):
        # 測試重複專案名稱處理
        pass

    def test_get_project_by_id_not_found(self, project_service, mock_db):
        # 測試專案不存在的情況
        pass
```

**2. 整合測試範例**（`tests/integration/test_database/test_project_crud.py`）

```python
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.base import Base
from app.models.project import Project
from app.models.user import User

class TestProjectDatabaseIntegration:
    @pytest.fixture(scope="function")
    def test_db(self):
        # 使用測試資料庫
        engine = create_engine("postgresql://test:test@localhost:5432/test_db")
        Base.metadata.create_all(engine)
        SessionLocal = sessionmaker(bind=engine)
        db = SessionLocal()

        yield db

        db.close()
        Base.metadata.drop_all(engine)

    def test_create_project_with_owner(self, test_db):
        # 測試建立專案及關聯用戶
        user = User(email="test@example.com", username="testuser")
        test_db.add(user)
        test_db.commit()

        project = Project(name="Test Project", owner_id=user.id)
        test_db.add(project)
        test_db.commit()

        assert project.id is not None
        assert project.owner.email == "test@example.com"

    def test_cascade_delete_project_tasks(self, test_db):
        # 測試級聯刪除
        pass
```

**3. API 測試範例**（`tests/api/test_projects.py`）

```python
import pytest
from fastapi.testclient import TestClient
from app.main import app

class TestProjectsAPI:
    @pytest.fixture
    def client(self):
        return TestClient(app)

    @pytest.fixture
    def auth_headers(self, client):
        # 登入並取得 token
        response = client.post("/auth/login", json={
            "email": "test@example.com",
            "password": "testpass"
        })
        token = response.json()["access_token"]
        return {"Authorization": f"Bearer {token}"}

    def test_create_project_success(self, client, auth_headers):
        # Act
        response = client.post(
            "/api/v1/projects",
            headers=auth_headers,
            json={
                "name": "New Project",
                "description": "Project Description"
            }
        )

        # Assert
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "New Project"
        assert "id" in data
        assert "created_at" in data

    def test_get_projects_pagination(self, client, auth_headers):
        # 測試分頁功能
        response = client.get(
            "/api/v1/projects?page=1&size=10",
            headers=auth_headers
        )

        assert response.status_code == 200
        data = response.json()
        assert "items" in data
        assert "total" in data
        assert "page" in data

    def test_create_project_unauthorized(self, client):
        # 測試未授權訪問
        response = client.post(
            "/api/v1/projects",
            json={"name": "Project"}
        )

        assert response.status_code == 401
```

**4. 負載測試範例**（`tests/load/locustfile.py`）

```python
from locust import HttpUser, task, between

class ProjectManagementUser(HttpUser):
    wait_time = between(1, 3)

    def on_start(self):
        # 登入獲取 token
        response = self.client.post("/auth/login", json={
            "email": "loadtest@example.com",
            "password": "testpass"
        })
        self.token = response.json()["access_token"]
        self.headers = {"Authorization": f"Bearer {self.token}"}

    @task(3)
    def get_projects(self):
        self.client.get("/api/v1/projects", headers=self.headers)

    @task(2)
    def create_project(self):
        self.client.post(
            "/api/v1/projects",
            headers=self.headers,
            json={
                "name": "Load Test Project",
                "description": "Testing load"
            }
        )

    @task(1)
    def get_project_details(self):
        self.client.get("/api/v1/projects/1", headers=self.headers)
```

**CI Workflow 配置**（`.github/workflows/ci.yml`）

```yaml
name: Backend API CI

on:
  push:
    branches: ['**']
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest

    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_USER: test
          POSTGRES_PASSWORD: test
          POSTGRES_DB: test_db
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5

      redis:
        image: redis:7
        options: >-
          --health-cmd "redis-cli ping"
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5

    steps:
      - uses: actions/checkout@v4

      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
          cache: 'pip'

      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install -r requirements-dev.txt

      - name: Run unit tests
        run: |
          pytest tests/unit/ -v --cov=app --cov-report=xml --cov-report=html
        env:
          DATABASE_URL: postgresql://test:test@localhost:5432/test_db
          REDIS_URL: redis://localhost:6379

      - name: Run integration tests
        run: |
          pytest tests/integration/ -v
        env:
          DATABASE_URL: postgresql://test:test@localhost:5432/test_db
          REDIS_URL: redis://localhost:6379

      - name: Run API tests
        run: |
          pytest tests/api/ -v
        env:
          DATABASE_URL: postgresql://test:test@localhost:5432/test_db
          REDIS_URL: redis://localhost:6379

      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          files: ./coverage.xml
          fail_ci_if_error: true
```

**檢查點 1**：
- [ ] 單元測試覆蓋率 ≥ 70%
- [ ] 整合測試覆蓋關鍵業務邏輯
- [ ] API 測試覆蓋所有端點
- [ ] 所有測試都通過

---

### 階段 2：資料庫遷移安全驗證（25 分鐘）

**任務**：確保資料庫遷移的安全性和可回退性。

#### 遷移測試策略

**1. 遷移腳本範例**（`alembic/versions/004_add_status_column.py`）

```python
"""add status column to projects

Revision ID: 004
Revises: 003
Create Date: 2024-10-30

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers
revision = '004'
down_revision = '003'

def upgrade():
    # 1. 添加新欄位（允許 NULL）
    op.add_column('projects',
        sa.Column('status', sa.String(20), nullable=True)
    )

    # 2. 更新現有資料（設定預設值）
    op.execute("""
        UPDATE projects
        SET status = 'active'
        WHERE status IS NULL
    """)

    # 3. 設定為 NOT NULL
    op.alter_column('projects', 'status', nullable=False)

    # 4. 建立索引
    op.create_index('idx_projects_status', 'projects', ['status'])

def downgrade():
    # 回退步驟（必須與 upgrade 相反）
    op.drop_index('idx_projects_status')
    op.drop_column('projects', 'status')
```

**2. 遷移測試腳本**（`.github/actions/migration-test/action.yml`）

```yaml
name: 'Test Database Migration'
description: 'Test migration upgrade and downgrade'

runs:
  using: 'composite'
  steps:
    - name: Setup test database
      shell: bash
      run: |
        docker run -d \
          --name migration-test-db \
          -e POSTGRES_USER=test \
          -e POSTGRES_PASSWORD=test \
          -e POSTGRES_DB=test_db \
          -p 5433:5432 \
          postgres:15

        # 等待資料庫啟動
        sleep 5

    - name: Run migrations
      shell: bash
      run: |
        export DATABASE_URL=postgresql://test:test@localhost:5433/test_db

        # 1. 執行所有遷移
        alembic upgrade head

        # 2. 驗證遷移結果
        python scripts/verify_migration.py

        # 3. 回退一個版本
        alembic downgrade -1

        # 4. 再次升級
        alembic upgrade head

        # 5. 驗證資料完整性
        python scripts/verify_data_integrity.py

    - name: Cleanup
      shell: bash
      if: always()
      run: |
        docker stop migration-test-db
        docker rm migration-test-db
```

**3. 遷移驗證腳本**（`scripts/verify_migration.py`）

```python
import sys
from sqlalchemy import create_engine, inspect
from app.config import settings

def verify_schema():
    """驗證資料庫 schema 是否符合預期"""
    engine = create_engine(settings.DATABASE_URL)
    inspector = inspect(engine)

    # 檢查必要的表格
    required_tables = ['users', 'projects', 'tasks', 'comments']
    existing_tables = inspector.get_table_names()

    for table in required_tables:
        if table not in existing_tables:
            print(f"❌ Missing table: {table}")
            return False

    # 檢查關鍵欄位
    projects_columns = [col['name'] for col in inspector.get_columns('projects')]
    required_columns = ['id', 'name', 'description', 'owner_id', 'status', 'created_at']

    for column in required_columns:
        if column not in projects_columns:
            print(f"❌ Missing column in projects: {column}")
            return False

    # 檢查索引
    projects_indexes = inspector.get_indexes('projects')
    if not any(idx['name'] == 'idx_projects_status' for idx in projects_indexes):
        print("❌ Missing index: idx_projects_status")
        return False

    print("✅ Schema verification passed")
    return True

if __name__ == "__main__":
    success = verify_schema()
    sys.exit(0 if success else 1)
```

**CI Workflow 整合**（在 `.github/workflows/ci.yml` 中添加）

```yaml
  migration-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          pip install alembic psycopg2-binary sqlalchemy

      - name: Test migrations
        uses: ./.github/actions/migration-test
```

**檢查點 2**：
- [ ] 遷移腳本能成功升級
- [ ] 遷移腳本能成功回退
- [ ] Schema 驗證通過
- [ ] 資料完整性檢查通過

---

### 階段 3：API 文檔自動生成（20 分鐘）

**任務**：自動生成 OpenAPI 文檔並進行版本管理。

**1. FastAPI 文檔增強**（`app/main.py`）

```python
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi

app = FastAPI(
    title="Project Management API",
    description="Enterprise-grade project management system",
    version="2.5.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title="Project Management API",
        version="2.5.0",
        description="""
        ## 核心功能
        - 用戶管理與認證
        - 專案管理
        - 任務追蹤
        - 評論系統

        ## 認證方式
        使用 Bearer Token（JWT）

        ## 速率限制
        - 未認證：100 requests/hour
        - 已認證：1000 requests/hour
        """,
        routes=app.routes,
    )

    # 添加安全 scheme
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT"
        }
    }

    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi
```

**2. API 端點文檔範例**（`app/routers/projects.py`）

```python
from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.project import ProjectCreate, ProjectResponse, ProjectList

router = APIRouter(prefix="/api/v1/projects", tags=["Projects"])

@router.post(
    "/",
    response_model=ProjectResponse,
    status_code=status.HTTP_201_CREATED,
    summary="建立新專案",
    description="""
    建立一個新的專案。

    **權限要求**：需要認證

    **請求範例**：
    ```json
    {
        "name": "Website Redesign",
        "description": "Complete redesign of company website"
    }
    ```

    **注意事項**：
    - 專案名稱必須唯一
    - 名稱長度 3-100 字元
    - 建立者自動成為專案擁有者
    """,
    responses={
        201: {"description": "專案建立成功"},
        400: {"description": "請求參數錯誤"},
        401: {"description": "未授權"},
        409: {"description": "專案名稱已存在"}
    }
)
async def create_project(
    project: ProjectCreate,
    current_user = Depends(get_current_user)
):
    # 實作邏輯
    pass

@router.get(
    "/",
    response_model=ProjectList,
    summary="查詢專案列表",
    description="獲取當前用戶的所有專案（支援分頁和過濾）"
)
async def get_projects(
    page: int = Query(1, ge=1, description="頁碼"),
    size: int = Query(10, ge=1, le=100, description="每頁數量"),
    status: Optional[str] = Query(None, description="專案狀態過濾"),
    current_user = Depends(get_current_user)
):
    # 實作邏輯
    pass
```

**3. 文檔生成與部署**（`scripts/generate_docs.sh`）

```bash
#!/bin/bash
set -e

echo "🔧 Generating API documentation..."

# 1. 啟動 API server（背景執行）
uvicorn app.main:app --host 0.0.0.0 --port 8000 &
SERVER_PID=$!

# 等待服務啟動
sleep 5

# 2. 下載 OpenAPI spec
curl http://localhost:8000/openapi.json > docs/api/openapi.json

# 3. 生成 Markdown 文檔
npx @openapitools/openapi-generator-cli generate \
  -i docs/api/openapi.json \
  -g markdown \
  -o docs/api/markdown

# 4. 生成 HTML 文檔
npx redoc-cli bundle docs/api/openapi.json \
  -o docs/api/index.html \
  --options.theme.colors.primary.main=#1976d2

# 5. 停止服務
kill $SERVER_PID

echo "✅ Documentation generated successfully"
echo "   - OpenAPI spec: docs/api/openapi.json"
echo "   - Markdown: docs/api/markdown/"
echo "   - HTML: docs/api/index.html"
```

**CI Workflow 整合**

```yaml
  generate-docs:
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'

    steps:
      - uses: actions/checkout@v4

      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          npm install -g @openapitools/openapi-generator-cli redoc-cli

      - name: Generate documentation
        run: bash scripts/generate_docs.sh

      - name: Deploy to GitHub Pages
        uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./docs/api
          destination_dir: api/v2.5.0
```

**檢查點 3**：
- [ ] OpenAPI 文檔自動生成
- [ ] 所有端點都有詳細說明
- [ ] 文檔部署到 GitHub Pages
- [ ] 支援多版本文檔

---

### 階段 4：容器化與多環境部署（25 分鐘）

**任務**：建立優化的容器映像和多環境部署策略。

**1. 多階段 Dockerfile**（`docker/Dockerfile`）

```dockerfile
# Stage 1: Build stage
FROM python:3.11-slim as builder

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Stage 2: Runtime stage
FROM python:3.11-slim

WORKDIR /app

# Install runtime dependencies only
RUN apt-get update && apt-get install -y \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy installed packages from builder
COPY --from=builder /root/.local /root/.local

# Copy application code
COPY app/ ./app/
COPY alembic/ ./alembic/
COPY alembic.ini .

# Create non-root user
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Make sure scripts are in PATH
ENV PATH=/root/.local/bin:$PATH

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**2. 部署 Workflow - Development**（`.github/workflows/deploy-dev.yml`）

```yaml
name: Deploy to Development

on:
  push:
    branches:
      - 'feature/**'
      - develop

jobs:
  deploy-dev:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Build Docker image
        run: |
          docker build -f docker/Dockerfile -t project-api:dev-${{ github.sha }} .

      - name: Run database migrations
        run: |
          docker run --rm \
            -e DATABASE_URL=${{ secrets.DEV_DATABASE_URL }} \
            project-api:dev-${{ github.sha }} \
            alembic upgrade head

      - name: Deploy to Railway (Dev)
        uses: bervProject/railway-deploy@main
        with:
          railway_token: ${{ secrets.RAILWAY_DEV_TOKEN }}
          service: project-api-dev

      - name: Health check
        run: |
          sleep 10
          curl -f https://project-api-dev.railway.app/health || exit 1

      - name: Run smoke tests
        run: |
          curl -f https://project-api-dev.railway.app/api/v1/projects || exit 1
```

**3. 部署 Workflow - Staging**（`.github/workflows/deploy-staging.yml`）

```yaml
name: Deploy to Staging

on:
  push:
    branches: [main]

jobs:
  deploy-staging:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Run all tests
        run: |
          # 確保所有測試通過
          docker-compose -f docker-compose.test.yml up --abort-on-container-exit

      - name: Build and push Docker image
        run: |
          echo ${{ secrets.GHCR_TOKEN }} | docker login ghcr.io -u ${{ github.actor }} --password-stdin
          docker build -f docker/Dockerfile -t ghcr.io/${{ github.repository }}:staging-${{ github.sha }} .
          docker push ghcr.io/${{ github.repository }}:staging-${{ github.sha }}

      - name: Deploy to Staging
        run: |
          # 使用 Railway CLI 部署
          railway up --service project-api-staging --environment staging

      - name: Run integration tests against staging
        run: |
          pytest tests/api/ --base-url=https://project-api-staging.railway.app

      - name: Performance test
        run: |
          locust -f tests/load/locustfile.py \
            --host=https://project-api-staging.railway.app \
            --users=50 --spawn-rate=10 --run-time=2m \
            --headless --only-summary

      - name: Notify team
        uses: 8398a7/action-slack@v3
        with:
          status: ${{ job.status }}
          text: 'Staging deployment completed'
          webhook_url: ${{ secrets.SLACK_WEBHOOK }}
```

**4. 部署 Workflow - Production**（`.github/workflows/deploy-prod.yml`）

```yaml
name: Deploy to Production

on:
  workflow_dispatch:
    inputs:
      version:
        description: 'Version to deploy'
        required: true

jobs:
  deploy-production:
    runs-on: ubuntu-latest
    environment:
      name: production
      url: https://api.projectmgmt.com

    steps:
      - uses: actions/checkout@v4
        with:
          ref: ${{ github.event.inputs.version }}

      - name: Security scan
        run: |
          # 生產環境部署前最後一次安全掃描
          docker build -f docker/Dockerfile -t project-api:prod .
          trivy image --severity HIGH,CRITICAL --exit-code 1 project-api:prod

      - name: Backup database
        run: |
          # 部署前備份資料庫
          pg_dump ${{ secrets.PROD_DATABASE_URL }} > backup_$(date +%Y%m%d_%H%M%S).sql
          # 上傳到 S3
          aws s3 cp backup_*.sql s3://project-backups/

      - name: Deploy to Production (Blue-Green)
        run: |
          # 部署到 Green 環境
          railway up --service project-api-green --environment production

          # 等待健康檢查
          for i in {1..30}; do
            if curl -f https://green.api.projectmgmt.com/health; then
              echo "Green environment is healthy"
              break
            fi
            sleep 10
          done

          # 切換流量到 Green
          railway service update project-api --environment production --active-service green

          # 保留 Blue 環境 10 分鐘以便快速回退
          sleep 600

      - name: Verify production
        run: |
          # 驗證生產環境
          pytest tests/api/test_critical_flows.py \
            --base-url=https://api.projectmgmt.com

      - name: Rollback on failure
        if: failure()
        run: |
          echo "Deployment failed. Rolling back..."
          railway service update project-api --environment production --active-service blue

      - name: Create release notes
        if: success()
        run: |
          gh release create v${{ github.event.inputs.version }} \
            --title "Release v${{ github.event.inputs.version }}" \
            --notes-file CHANGELOG.md
```

**檢查點 4**：
- [ ] Docker 映像大小 < 200MB
- [ ] Development 自動部署成功
- [ ] Staging 部署包含完整驗證
- [ ] Production 使用 Blue-Green 部署
- [ ] 部署失敗自動回退

---

## 🎯 學習檢查點

完成所有階段後，驗證以下能力：

### 技術能力
- [ ] 建立了完整的測試金字塔（單元 + 整合 + API + 負載）
- [ ] 實現了安全的資料庫遷移流程
- [ ] 自動生成並部署了 API 文檔
- [ ] 優化了 Docker 映像大小
- [ ] 實現了多環境部署策略
- [ ] 建立了自動回退機制

### 品質指標
- [ ] 測試覆蓋率 ≥ 80%
- [ ] 所有 API 端點都有文檔
- [ ] 容器映像無 Critical 漏洞
- [ ] 部署成功率 > 95%
- [ ] 部署時間 < 10 分鐘

### 最佳實踐
- [ ] 遵循 12-Factor App 原則
- [ ] 使用環境變數管理配置
- [ ] 實現健康檢查端點
- [ ] 記錄詳細的部署日誌
- [ ] 建立災難恢復計劃

---

## 💡 延伸挑戰

想進一步提升？嘗試這些進階任務：

### 挑戰 1：金絲雀部署（Canary Deployment）
- 先部署到 5% 流量
- 監控錯誤率和延遲
- 逐步增加到 100%
- 異常時自動回退

### 挑戰 2：資料庫零停機遷移
- 使用雙寫策略
- 實現向後相容的 Schema 變更
- 驗證資料一致性

### 挑戰 3：完整監控體系
- 整合 Prometheus + Grafana
- 設定關鍵指標告警
- 建立 SLO/SLI 指標
- 實現分散式追蹤（Jaeger）

### 挑戰 4：成本優化
- 優化 CI 執行時間（< 5 分鐘）
- 減少 Docker 映像大小（< 100MB）
- 實現構建快取策略

---

## 📚 參考資源

### 官方文檔
- [FastAPI 文檔](https://fastapi.tiangolo.com/)
- [Alembic 文檔](https://alembic.sqlalchemy.org/)
- [Pytest 文檔](https://docs.pytest.org/)
- [Locust 文檔](https://docs.locust.io/)

### 最佳實踐
- [The Twelve-Factor App](https://12factor.net/)
- [API 設計最佳實踐](https://swagger.io/resources/articles/best-practices-in-api-design/)
- [Database Migration Best Practices](https://www.prisma.io/dataguide/types/relational/migration-best-practices)

### 工具
- [OpenAPI Generator](https://openapi-generator.tech/)
- [ReDoc](https://github.com/Redocly/redoc)
- [Railway](https://railway.app/)

---

## 🎓 反思問題

完成情境後，思考以下問題：

1. **測試策略**：為什麼需要多層次的測試金字塔？每一層的測試目標是什麼？

2. **遷移風險**：如何確保資料庫遷移的安全性？如果遷移失敗了如何快速恢復？

3. **文檔維護**：自動生成的文檔如何確保與實際 API 行為一致？

4. **部署策略**：Blue-Green 部署和 Canary 部署有什麼區別？什麼情況下使用哪種策略？

5. **監控指標**：對於 API 服務，哪些指標是最關鍵的？如何設定合理的告警閾值？

---

**下一步**：完成這個情境後，你已經掌握了後端 API 的完整 CI/CD 流程。接下來可以挑戰 **C05：Monorepo 管線設計** 或 **E01：企業級完整 DevOps 管線**！
