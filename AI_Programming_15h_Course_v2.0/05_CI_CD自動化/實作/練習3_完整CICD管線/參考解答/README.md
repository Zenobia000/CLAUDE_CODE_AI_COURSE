# 參考解答：練習 3 - 完整 CI/CD 管線（端到端）

## 📋 說明

這是練習 3 的參考解答，展示如何建立企業級的端到端 CI/CD 管線。

**重要提示**：
- ⚠️ 這是最複雜的練習，建議先完成練習 1 和 2
- ⚠️ 參考解答提供一種實現方式，實際部署需根據環境調整
- ⚠️ 重點理解架構設計思路，而非死記配置細節

---

## 🏗️ 架構總覽

```
[Git Push] → [CI Pipeline] → [CD Pipeline] → [Production]
     ↓
  [Trigger]
     ↓
┌────────────────────────────────────────┐
│  CI: Continuous Integration            │
├────────────────────────────────────────┤
│  1. Lint (parallel)                    │
│  2. Test (parallel)                    │
│  3. Security Scan (parallel)           │
│  4. Build Docker (after 1-3 pass)      │
│  5. Container Scan (Trivy)             │
└────────────────────────────────────────┘
     ↓ (CI Success)
┌────────────────────────────────────────┐
│  CD: Continuous Deployment             │
├────────────────────────────────────────┤
│  1. Deploy to Dev (auto)               │
│     └─ Health Check                    │
│     └─ Smoke Tests                     │
│  2. Deploy to Staging (auto)           │
│     └─ Health Check                    │
│     └─ Integration Tests               │
│  3. Deploy to Production (manual)      │
│     └─ Approval Required ⚠️             │
│     └─ Health Check                    │
│     └─ Smoke Tests                     │
│     └─ Auto Rollback if failed         │
└────────────────────────────────────────┘
```

---

## 📂 專案結構

```
參考解答/
├── README.md（本文件）
├── 部署指南.md              # 完整部署文檔
├── app/                     # FastAPI 應用
│   ├── main.py
│   ├── config.py           # 多環境配置
│   ├── health.py           # 健康檢查
│   └── models.py
├── tests/
│   ├── unit/               # 單元測試
│   ├── integration/        # 整合測試
│   └── smoke/              # 煙霧測試
├── deployment/             # 部署配置
│   ├── dev/
│   │   ├── docker-compose.yml
│   │   └── .env.example
│   ├── staging/
│   │   ├── docker-compose.yml
│   │   └── .env.example
│   └── production/
│       ├── docker-compose.yml
│       └── .env.example
├── scripts/
│   ├── health-check.sh     # 健康檢查腳本
│   ├── smoke-test.sh       # 煙霧測試腳本
│   └── rollback.sh         # 回退腳本
├── .github/workflows/
│   ├── ci.yml              # 持續整合
│   ├── cd.yml              # 持續部署
│   └── rollback.yml        # 回退流程
├── Dockerfile
└── docker-compose.yml
```

---

## 🎯 核心設計決策

### 1. CI 與 CD 分離

**為什麼分成兩個 workflows？**

```yaml
# ci.yml - 持續整合
on:
  push:
  pull_request:

# cd.yml - 持續部署
on:
  workflow_run:
    workflows: ["CI"]
    types: [completed]
    branches: [main]
```

**理由**：
- **職責分離**：CI 負責驗證代碼品質，CD 負責部署
- **觸發條件不同**：CI 每次 push/PR 都執行，CD 只在 main 分支且 CI 成功後執行
- **權限隔離**：CD 需要更高權限（部署權限），分離更安全
- **更好的可見性**：GitHub Actions 中可以清楚看到 CI 和 CD 的狀態

---

### 2. 多環境配置策略

**環境變數管理**（`app/config.py`）：

```python
from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    # 環境標識
    environment: str = "development"

    # 應用配置
    app_name: str = "My FastAPI App"
    debug: bool = False

    # 資料庫
    database_url: str

    # 外部服務
    api_key: str
    redis_url: str | None = None

    # 功能開關
    enable_feature_x: bool = False

    class Config:
        env_file = ".env"
        case_sensitive = False

@lru_cache()
def get_settings():
    return Settings()

# 使用範例
settings = get_settings()
```

**環境配置檔案**：

```bash
# deployment/dev/.env
ENVIRONMENT=development
DEBUG=true
DATABASE_URL=sqlite:///./dev.db
API_KEY=dev_key_12345
ENABLE_FEATURE_X=true

# deployment/production/.env
ENVIRONMENT=production
DEBUG=false
DATABASE_URL=postgresql://prod_db_url
API_KEY=${SECRET_API_KEY}  # 從 secrets 注入
ENABLE_FEATURE_X=false
```

**為什麼這樣設計**：
- 使用 Pydantic Settings：類型安全、自動驗證
- 環境變數優先：12-factor app 原則
- 預設值：開發環境友好
- `lru_cache`：避免重複讀取配置

---

### 3. 健康檢查端點設計

**`app/health.py`**：

```python
from fastapi import APIRouter, HTTPException, status
from datetime import datetime
from . import database, external_services

router = APIRouter()

@router.get("/health")
async def health_check():
    """
    完整的健康檢查端點
    檢查項目：
    1. 應用狀態
    2. 資料庫連線
    3. 外部依賴（Redis、API 等）
    """
    checks = {}
    overall_healthy = True

    # 檢查資料庫
    try:
        await database.ping()
        checks["database"] = {"status": "ok"}
    except Exception as e:
        checks["database"] = {"status": "error", "message": str(e)}
        overall_healthy = False

    # 檢查 Redis（如果有）
    try:
        if external_services.redis:
            await external_services.redis.ping()
            checks["redis"] = {"status": "ok"}
    except Exception as e:
        checks["redis"] = {"status": "error", "message": str(e)}
        # Redis 是可選的，不影響整體健康

    response = {
        "status": "healthy" if overall_healthy else "unhealthy",
        "version": "1.0.0",
        "environment": settings.environment,
        "timestamp": datetime.utcnow().isoformat(),
        "checks": checks
    }

    if not overall_healthy:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=response
        )

    return response

@router.get("/health/liveness")
async def liveness():
    """
    存活探測（Kubernetes liveness probe）
    只檢查應用是否還活著，不檢查依賴
    """
    return {"status": "alive"}

@router.get("/health/readiness")
async def readiness():
    """
    就緒探測（Kubernetes readiness probe）
    檢查應用是否準備好接收流量
    """
    # 與 health_check 相同的邏輯
    return await health_check()
```

**為什麼需要三種健康檢查**：
- `/health`：完整檢查，部署後驗證用
- `/health/liveness`：存活探測，Kubernetes 用它判斷是否重啟容器
- `/health/readiness`：就緒探測，Kubernetes 用它判斷是否加入負載均衡

---

### 4. 煙霧測試設計

**`scripts/smoke-test.sh`**：

```bash
#!/bin/bash
set -e

# 配置
API_URL="${API_URL:-http://localhost:8000}"
TIMEOUT=30
RETRY_COUNT=10
RETRY_DELAY=5

echo "🧪 Running smoke tests against $API_URL"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# 輔助函數：帶重試的 HTTP 請求
function http_get() {
    local url=$1
    local expected_code=${2:-200}

    for i in $(seq 1 $RETRY_COUNT); do
        response_code=$(curl -s -o /dev/null -w "%{http_code}" --max-time $TIMEOUT "$url" || echo "000")

        if [ "$response_code" = "$expected_code" ]; then
            echo "✅ $url (HTTP $response_code)"
            return 0
        fi

        echo "⏳ Attempt $i/$RETRY_COUNT failed (HTTP $response_code), retrying in ${RETRY_DELAY}s..."
        sleep $RETRY_DELAY
    done

    echo "❌ $url failed after $RETRY_COUNT attempts"
    return 1
}

# 測試 1：健康檢查
echo ""
echo "Test 1: Health Check"
http_get "$API_URL/health"

# 測試 2：主頁
echo ""
echo "Test 2: Homepage"
http_get "$API_URL/"

# 測試 3：API 端點
echo ""
echo "Test 3: API Endpoint"
response=$(curl -s "$API_URL/api/items/1")
if echo "$response" | jq -e '.id' > /dev/null 2>&1; then
    echo "✅ API endpoint returns valid JSON"
else
    echo "❌ API endpoint response invalid"
    exit 1
fi

# 測試 4：回應時間
echo ""
echo "Test 4: Response Time"
time_total=$(curl -o /dev/null -s -w '%{time_total}\n' "$API_URL/")
if (( $(echo "$time_total < 2.0" | bc -l) )); then
    echo "✅ Response time: ${time_total}s (< 2s)"
else
    echo "⚠️  Response time: ${time_total}s (> 2s, consider optimization)"
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🎉 All smoke tests passed!"
```

**為什麼這樣設計**：
- **重試機制**：新部署的服務可能需要幾秒啟動
- **超時設置**：避免無限等待
- **清晰的輸出**：便於調試
- **返回值**：失敗時返回非零（workflow 會識別）

---

### 5. 部署策略：藍綠部署

**為什麼選擇藍綠部署**：

| 部署策略 | 停機時間 | 回退速度 | 資源成本 | 複雜度 |
|---------|---------|---------|---------|--------|
| 直接部署 | 有 | 慢 | 低 | 低 |
| 滾動更新 | 無 | 中 | 中 | 中 |
| **藍綠部署** | **無** | **快** | **高** | **中** |
| 金絲雀發布 | 無 | 中 | 中 | 高 |

**藍綠部署流程**：

```
當前狀態：Green 環境在運行

1. 部署到 Blue 環境
   docker-compose -f docker-compose.blue.yml up -d

2. 健康檢查 Blue 環境
   ./scripts/health-check.sh http://blue.example.com

3. 煙霧測試 Blue 環境
   ./scripts/smoke-test.sh http://blue.example.com

4. 切換流量到 Blue
   # 更新 Nginx/ALB 配置
   ./scripts/switch-to-blue.sh

5. 保留 Green 環境（作為回退選項）
   # 5-10 分鐘後，確認無問題才關閉 Green
```

**Nginx 配置範例**：

```nginx
# /etc/nginx/conf.d/app.conf

upstream app {
    server blue.internal:8000;   # 當前流量指向 Blue
    # server green.internal:8000;  # Green 待命
}

server {
    listen 80;
    server_name app.example.com;

    location / {
        proxy_pass http://app;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

**切換腳本** (`scripts/switch-to-blue.sh`):

```bash
#!/bin/bash
# 藍綠切換腳本

TARGET=$1  # blue 或 green

echo "Switching traffic to $TARGET environment..."

# 更新 Nginx 配置
sed -i "s/server .*.internal:8000;/server $TARGET.internal:8000;/" /etc/nginx/conf.d/app.conf

# 重載 Nginx
nginx -t && nginx -s reload

echo "Traffic switched to $TARGET successfully"
```

---

### 6. 自動回退機制

**CD Workflow 中的自動回退**：

```yaml
deploy-production:
  environment: production
  steps:
    # 記錄當前版本
    - name: Save current version
      run: |
        echo "PREVIOUS_VERSION=$(docker ps --format '{{.Image}}' | grep app | head -1)" >> $GITHUB_ENV

    # 部署新版本
    - name: Deploy new version
      id: deploy
      run: ./scripts/deploy.sh production ${{ github.sha }}

    # 健康檢查（帶重試）
    - name: Health check with auto-rollback
      id: health_check
      run: |
        if ! ./scripts/health-check.sh https://prod.example.com; then
          echo "❌ Health check failed, triggering rollback..."
          echo "ROLLBACK_NEEDED=true" >> $GITHUB_OUTPUT
        else
          echo "✅ Health check passed"
        fi

    # 自動回退
    - name: Auto rollback on failure
      if: steps.health_check.outputs.ROLLBACK_NEEDED == 'true'
      run: |
        echo "Rolling back to previous version: $PREVIOUS_VERSION"
        ./scripts/rollback.sh production $PREVIOUS_VERSION

    # 驗證回退成功
    - name: Verify rollback
      if: steps.health_check.outputs.ROLLBACK_NEEDED == 'true'
      run: |
        if ! ./scripts/health-check.sh https://prod.example.com; then
          echo "❌ Rollback verification failed! Manual intervention required!"
          exit 1
        fi
        echo "✅ Rollback successful"

    # 通知團隊
    - name: Notify on rollback
      if: steps.health_check.outputs.ROLLBACK_NEEDED == 'true'
      uses: slackapi/slack-github-action@v1
      with:
        webhook-url: ${{ secrets.SLACK_WEBHOOK }}
        payload: |
          {
            "text": "🚨 Auto rollback triggered in Production",
            "blocks": [
              {
                "type": "section",
                "text": {
                  "type": "mrkdwn",
                  "text": "*Deployment failed and rolled back*\nFailed version: `${{ github.sha }}`\nRolled back to: `${{ env.PREVIOUS_VERSION }}`"
                }
              }
            ]
          }
```

**為什麼自動回退重要**：
- **快速恢復**：無需人工介入，降低 MTTR（平均恢復時間）
- **降低風險**：即使深夜部署出問題也能自動恢復
- **保護生產**：健康檢查失敗 → 自動回退，而非讓故障持續

---

## 🔧 關鍵配置檔案

### 1. CI Workflow (`.github/workflows/ci.yml`)

**重點**：
- 並行執行（lint, test, security）
- 使用 `needs` 控制依賴
- Docker 構建使用 cache
- 容器掃描（Trivy）

### 2. CD Workflow (`.github/workflows/cd.yml`)

**重點**：
- 環境保護規則（production 需審批）
- 健康檢查與煙霧測試
- 自動回退機制
- Slack 通知

### 3. Rollback Workflow (`.github/workflows/rollback.yml`)

**重點**：
- 手動觸發（workflow_dispatch）
- 輸入參數：環境、版本、原因
- 驗證回退成功

---

## 📊 執行時間優化

### 優化前
```
Total: ~18 分鐘
├─ Lint: 2 分鐘（串行）
├─ Test: 3 分鐘（串行，等待 Lint）
├─ Security: 4 分鐘（串行，等待 Test）
├─ Build: 8 分鐘（等待前三者）
└─ Deploy: 1 分鐘
```

### 優化後
```
Total: ~10 分鐘
├─ Lint, Test, Security: 4 分鐘（並行）
├─ Build: 5 分鐘（Docker cache）
└─ Deploy: 1 分鐘

節省: 44% 時間
```

**優化技巧**：
1. 並行執行獨立 jobs
2. 使用 pip cache 和 Docker cache
3. 減少不必要的步驟
4. 使用更快的 actions（如 setup-python@v4 的內建 cache）

---

## 💡 學習重點

### 1. CI/CD 不是「自動化部署」，是「可靠的自動化交付」

**區別**：
- ❌ 自動化部署：代碼 push → 直接上生產
- ✅ 可靠的 CI/CD：代碼 → 測試 → 掃描 → 審批 → 部署 → 驗證 → 回退（如果失敗）

### 2. 每個環境都很重要

- **Dev**：快速迭代，發現基本問題
- **Staging**：模擬生產，發現整合問題
- **Production**：真實用戶，零容忍故障

### 3. 健康檢查是關鍵

**不要**只檢查 HTTP 200：
```bash
# ❌ 不夠
curl http://app/

# ✅ 完整檢查
curl http://app/health  # 檢查應用 + 資料庫 + 外部依賴
```

### 4. 回退比部署更重要

- 部署可以慢慢做（有審批）
- 回退必須快（故障時爭分奪秒）
- 設計時優先考慮「如何回退」

---

## 🎯 自我檢查

完成練習後，驗證：

- [ ] CI 管線包含測試、掃描、構建
- [ ] 三個環境配置完整
- [ ] 健康檢查實現並測試
- [ ] 煙霧測試腳本可執行
- [ ] 生產環境需要審批
- [ ] 可以手動觸發回退
- [ ] 自動回退機制生效（進階）
- [ ] 有監控和通知

---

## 📚 延伸學習

- Kubernetes 部署（進階）
- GitOps（ArgoCD、Flux）
- Observability（日誌、指標、追蹤）
- 災難恢復演練

---

**恭喜你完成最複雜的練習！** 🎉

你現在掌握了企業級 CI/CD 管線的核心技能！
