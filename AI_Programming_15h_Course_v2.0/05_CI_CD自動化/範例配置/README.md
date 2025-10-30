# Workflow 範本庫

## 📚 範本總覽

本目錄包含 4 個生產級別的 GitHub Actions workflow 範本,可直接使用或客製化。

| 範本 | 用途 | 適用專案 | 執行時間 |
|------|------|---------|---------|
| `basic-test.yml` | 基礎測試管線 | 所有專案 | 1-2 分鐘 |
| `security-scan.yml` | 安全掃描 | 生產專案 | 3-5 分鐘 |
| `docker-build-deploy.yml` | 容器化部署 | Docker 專案 | 5-10 分鐘 |
| `full-pipeline.yml` | 完整管線 | 企業級專案 | 10-15 分鐘 |

---

## 🚀 快速使用

### 步驟 1：選擇範本

根據你的需求選擇適合的範本：

```
只需要測試？
  → basic-test.yml

需要安全掃描？
  → security-scan.yml

使用 Docker？
  → docker-build-deploy.yml

需要完整流程？
  → full-pipeline.yml
```

### 步驟 2：複製到專案

```bash
# 在你的專案根目錄
mkdir -p .github/workflows

# 複製範本（以 basic-test.yml 為例）
cp path/to/basic-test.yml .github/workflows/test.yml
```

### 步驟 3：客製化

根據你的專案修改：
- Python 版本
- 依賴檔案路徑
- 測試命令
- 分支名稱

### 步驟 4：提交並測試

```bash
git add .github/workflows/test.yml
git commit -m "ci: add automated workflow"
git push

# 前往 GitHub Actions tab 查看執行結果
```

---

## 📝 範本詳細說明

### 1. basic-test.yml - 基礎測試管線

**用途**：為專案建立最基本的自動化測試

**包含功能**：
- ✅ 自動化測試執行
- ✅ Pip 快取
- ✅ 測試報告

**適用場景**：
- 新專案起步
- 只需要基本測試
- 學習 CI/CD

**客製化要點**：
```yaml
# 修改 Python 版本
python-version: '3.11'  # 改成你的版本

# 修改測試命令
run: pytest             # 改成 npm test, go test 等

# 修改觸發分支
branches: [main]        # 改成你的主分支名稱
```

### 2. security-scan.yml - 安全掃描管線

**用途**：完整的三層安全掃描

**包含功能**：
- ✅ CodeQL 靜態分析
- ✅ Snyk 依賴掃描
- ✅ Trivy 容器掃描
- ✅ 自動上傳結果到 GitHub Security

**適用場景**：
- 生產環境專案
- 處理敏感資料
- 需要安全合規

**前置需求**：
```
1. Snyk Token（免費註冊）
   - 註冊：https://snyk.io
   - 取得 API Token
   - 在 GitHub 設定 Secret: SNYK_TOKEN

2. Docker（如果需要容器掃描）
   - 確保專案有 Dockerfile
```

**客製化要點**：
```yaml
# 修改掃描嚴重度閾值
severity-threshold: high  # critical, high, medium, low

# 排除特定路徑
paths-ignore:
  - 'tests/**'
  - 'docs/**'
```

### 3. docker-build-deploy.yml - 容器化部署管線

**用途**：建立 Docker 映像並部署

**包含功能**：
- ✅ 多階段建立優化
- ✅ 映像快取
- ✅ 映像掃描
- ✅ 推送到 Container Registry
- ✅ 部署到 Kubernetes

**適用場景**：
- 使用 Docker 的專案
- 微服務架構
- Kubernetes 部署

**前置需求**：
```
1. Container Registry
   - GitHub Container Registry（推薦,免費）
   - Docker Hub
   - AWS ECR / Azure ACR / GCP GCR

2. Kubernetes（如果需要部署）
   - 集群訪問憑證
   - kubectl 配置
```

**客製化要點**：
```yaml
# 修改 registry
REGISTRY: ghcr.io       # 改成你的 registry

# 修改映像標籤策略
tags: |
  type=ref,event=branch
  type=semver,pattern={{version}}

# 修改 Kubernetes manifests
manifests: |
  k8s/deployment.yml    # 改成你的路徑
```

### 4. full-pipeline.yml - 完整 CI/CD 管線

**用途**：企業級完整流程

**包含功能**：
- ✅ 並行執行（lint, test, security）
- ✅ 測試覆蓋率檢查
- ✅ 多層次安全掃描
- ✅ Docker 建立與推送
- ✅ 多環境部署（dev, staging, prod）
- ✅ 自動回退機制
- ✅ Slack/Discord 通知

**適用場景**：
- 企業級專案
- 多人協作團隊
- 需要完整治理

**執行流程**：
```
Trigger
  │
  ├─── Lint (並行)
  ├─── Test (並行)
  └─── Security Scan (並行)
  │
  └─── Build Docker Image
       │
       ├─── Deploy to Dev (自動)
       ├─── Deploy to Staging (需批准)
       └─── Deploy to Production (需批准)
            │
            └─── Health Check → Rollback if failed
```

**客製化要點**：
```yaml
# 修改環境配置
environments:
  dev:
    url: https://dev.example.com
  staging:
    url: https://staging.example.com
  prod:
    url: https://example.com

# 修改通知設定
SLACK_WEBHOOK: ${{ secrets.SLACK_WEBHOOK }}
```

---

## ⚙️ 通用配置項目

### 環境變數設定

所有範本都支援環境變數配置：

```yaml
# Workflow 層級（所有 jobs 共享）
env:
  PYTHON_VERSION: '3.11'
  NODE_VERSION: '18'

# Job 層級
jobs:
  test:
    env:
      DATABASE_URL: ${{ secrets.DATABASE_URL }}

# Step 層級
steps:
  - name: Run tests
    env:
      LOG_LEVEL: debug
    run: pytest
```

### Secrets 管理

在 GitHub 設定 Secrets：
```
Settings → Secrets and variables → Actions → New repository secret
```

常用 Secrets：
```
# 資料庫
DATABASE_URL

# API Keys
SNYK_TOKEN
CODECOV_TOKEN

# 部署
KUBE_CONFIG
AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY

# 通知
SLACK_WEBHOOK
DISCORD_WEBHOOK
```

### 快取策略

所有範本都使用快取加速：

```yaml
# Python pip 快取
- uses: actions/cache@v3
  with:
    path: ~/.cache/pip
    key: ${{ runner.os }}-pip-${{ hashFiles('requirements.txt') }}

# Node.js npm 快取
- uses: actions/cache@v3
  with:
    path: node_modules
    key: ${{ runner.os }}-node-${{ hashFiles('package-lock.json') }}

# Docker 層快取
- uses: docker/build-push-action@v4
  with:
    cache-from: type=gha
    cache-to: type=gha,mode=max
```

---

## 🎯 使用建議

### 新手建議

1. **從簡單開始**：先使用 `basic-test.yml`
2. **逐步加入功能**：測試通過後,加入安全掃描
3. **理解再客製化**：確保理解每個部分的作用
4. **善用 AI**：用 Claude 幫助理解和客製化

### 進階建議

1. **組合使用**：可以同時使用多個範本
   ```
   .github/workflows/
   ├── test.yml          (基於 basic-test.yml)
   ├── security.yml      (基於 security-scan.yml)
   └── deploy.yml        (基於 docker-build-deploy.yml)
   ```

2. **建立可重用 workflow**：
   ```yaml
   # .github/workflows/reusable-test.yml
   on:
     workflow_call:
       inputs:
         python-version:
           required: true
           type: string
   ```

3. **使用 workflow_dispatch**：手動觸發
   ```yaml
   on:
     workflow_dispatch:
       inputs:
         environment:
           description: 'Target environment'
           required: true
           default: 'staging'
   ```

---

## 🔧 故障排除

### 常見問題

**Q1：workflow 執行失敗**
```
A：
1. 查看具體失敗的 step
2. 複製錯誤訊息
3. 問 Claude：「GitHub Actions 失敗，錯誤：[貼上錯誤]」
```

**Q2：快取沒有生效**
```
A：
1. 檢查 key 是否包含正確的檔案 hash
2. 第一次執行會建立快取
3. 第二次執行才會使用快取
```

**Q3：Secret 讀不到**
```
A：
1. 確認 Secret 名稱正確（大小寫敏感）
2. 確認 Secret 已在 GitHub 設定
3. 確認在正確的 repository 設定
```

**Q4：部署權限不足**
```
A：
1. 檢查 workflow permissions
2. 加入必要的權限：
   permissions:
     contents: read
     packages: write
```

---

## 📚 參考資源

### 官方文件
- [GitHub Actions 文件](https://docs.github.com/en/actions)
- [Workflow 語法](https://docs.github.com/en/actions/reference/workflow-syntax-for-github-actions)
- [Actions Marketplace](https://github.com/marketplace?type=actions)

### 學習路徑
- 理論 5.1：GitHub Actions 整合
- 理論 5.2：安全掃描與自動修復
- 理論 5.3：自動化部署策略

---

**選擇範本,開始建立你的 CI/CD 管線！**
