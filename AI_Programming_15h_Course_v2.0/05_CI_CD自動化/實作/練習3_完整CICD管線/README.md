# 實作練習 3：完整 CI/CD 管線（端到端）

## 📋 練習概述

**練習目標**：整合測試、安全掃描、Docker 構建、自動部署，建立完整的端到端 CI/CD 管線

**預估時間**：3-4 小時

**難度等級**：⭐⭐⭐⭐ 進階綜合

**前置知識**：
- 完成練習 1（基礎 CI 工作流程）
- 完成練習 2（安全掃描管線）
- 理解 Docker 基礎
- 了解基本的雲端部署概念

---

## 🎯 學習目標

完成本練習後，你將能夠：

1. ✅ 整合完整的 CI/CD 管線（測試 → 掃描 → 構建 → 部署）
2. ✅ 實現多環境部署策略（開發/測試/生產）
3. ✅ 配置自動化回退機制
4. ✅ 建立監控和通知系統
5. ✅ 理解企業級 DevOps 最佳實踐

---

## 🏗️ 完整管線架構

```
觸發事件（Push/PR）
    ↓
┌───────────────────────────────────────┐
│  Stage 1: 程式碼品質檢查（並行）        │
├───────────────────────────────────────┤
│  ✓ Lint（black, flake8）              │
│  ✓ 單元測試（pytest）                  │
│  ✓ 測試覆蓋率                          │
└───────────────────────────────────────┘
    ↓（全部通過才繼續）
┌───────────────────────────────────────┐
│  Stage 2: 安全掃描（並行）             │
├───────────────────────────────────────┤
│  ✓ CodeQL 靜態分析                    │
│  ✓ Snyk 依賴掃描                      │
│  ✓ Gitleaks 密鑰掃描                  │
└───────────────────────────────────────┘
    ↓（無高危漏洞才繼續）
┌───────────────────────────────────────┐
│  Stage 3: Docker 構建與掃描            │
├───────────────────────────────────────┤
│  ✓ 構建 Docker 映像                   │
│  ✓ Trivy 容器掃描                     │
│  ✓ 推送到 Registry                    │
└───────────────────────────────────────┘
    ↓（main 分支才繼續）
┌───────────────────────────────────────┐
│  Stage 4: 部署（分環境）               │
├───────────────────────────────────────┤
│  ✓ 開發環境（自動）                    │
│  ✓ 測試環境（自動）                    │
│  ✓ 生產環境（需要審批）                │
└───────────────────────────────────────┘
    ↓
┌───────────────────────────────────────┐
│  Stage 5: 部署後驗證                   │
├───────────────────────────────────────┤
│  ✓ 健康檢查                            │
│  ✓ 煙霧測試（Smoke Tests）             │
│  ✓ 監控告警                            │
└───────────────────────────────────────┘
```

---

## 📂 專案結構

```
練習3_完整CICD管線/
├── README.md（本文件）
├── app/                      # FastAPI 應用（完整版）
│   ├── main.py
│   ├── models.py
│   ├── database.py
│   ├── config.py            # 環境配置
│   └── health.py            # 健康檢查端點
├── tests/
│   ├── unit/                # 單元測試
│   ├── integration/         # 整合測試
│   └── smoke/               # 煙霧測試（部署後）
├── .github/
│   └── workflows/
│       ├── ci.yml           # 持續整合
│       ├── cd.yml           # 持續部署
│       └── rollback.yml     # 回退流程
├── deployment/              # 部署配置
│   ├── dev/                 # 開發環境
│   │   ├── docker-compose.yml
│   │   └── .env.example
│   ├── staging/             # 測試環境
│   └── production/          # 生產環境
├── scripts/
│   ├── health-check.sh      # 健康檢查腳本
│   ├── smoke-test.sh        # 煙霧測試腳本
│   └── rollback.sh          # 回退腳本
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── 參考解答/
│   ├── 完整專案代碼/
│   ├── .github/workflows/
│   └── 部署指南.md
└── 評量標準.md
```

---

## 🚀 練習步驟

### 第 1 步：建立多環境配置（45 分鐘）

#### 1.1 設計環境配置

創建 `app/config.py`，支援多環境配置：

**提示詞（給 Claude Code）**：

```
請幫我建立 app/config.py，實現多環境配置管理：

需求：
1. 支援三個環境：development、staging、production
2. 使用環境變數控制配置
3. 包含以下配置項：
   - 資料庫連線字串
   - API 密鑰（從環境變數讀取）
   - 日誌等級
   - CORS 設定
   - 功能開關（feature flags）

4. 使用 pydantic BaseSettings 管理配置
5. 提供配置驗證機制
```

#### 1.2 建立部署配置檔案

為每個環境創建 docker-compose.yml：

**提示詞（給 Claude Code）**：

```
請幫我建立三個環境的 docker-compose.yml：

1. deployment/dev/docker-compose.yml
   - 開發環境配置
   - 啟用熱重載
   - 掛載本地代碼
   - 使用 SQLite

2. deployment/staging/docker-compose.yml
   - 測試環境配置
   - 使用 PostgreSQL
   - 模擬生產環境

3. deployment/production/docker-compose.yml
   - 生產環境配置
   - 資源限制
   - 健康檢查
   - 重啟策略
```

**檢查點**：
- [ ] 三個環境配置完成
- [ ] 本地可以啟動開發環境
- [ ] 配置使用環境變數（無硬編碼）

---

### 第 2 步：建立 CI 管線（60 分鐘）

#### 2.1 整合練習 1 和 2 的內容

創建 `.github/workflows/ci.yml`，整合測試和安全掃描：

**提示詞（給 Claude Code）**：

```
請幫我建立 .github/workflows/ci.yml，整合以下功能：

需求：
1. 觸發條件：
   - 所有 push 和 pull request
   - 支援手動觸發（workflow_dispatch）

2. Jobs 結構（並行執行）：

   Job 1: lint
   - black 格式檢查
   - flake8 風格檢查
   - isort import 排序

   Job 2: test
   - pytest 單元測試
   - 產生覆蓋率報告
   - 上傳覆蓋率到 Codecov

   Job 3: security-scan
   - CodeQL 靜態分析
   - Snyk 依賴掃描
   - Gitleaks 密鑰掃描

3. Job 4: build（依賴前三個 jobs 通過）
   - 構建 Docker 映像
   - Trivy 容器掃描
   - 標記映像（使用 git SHA）
   - 推送到 GitHub Container Registry

4. 優化：
   - 使用 cache 加速（pip、Docker layer）
   - 顯示執行時間
   - 清晰的錯誤訊息
```

#### 2.2 配置 GitHub Container Registry

設定推送 Docker 映像到 GHCR：

```bash
# 設定 GitHub Token 權限
# Settings > Actions > General > Workflow permissions
# 選擇 "Read and write permissions"
```

**檢查點**：
- [ ] CI 管線成功執行
- [ ] 所有檢查並行執行
- [ ] Docker 映像成功推送到 GHCR
- [ ] 執行時間 < 10 分鐘

---

### 第 3 步：建立 CD 管線（90 分鐘）

#### 3.1 自動部署到開發/測試環境

創建 `.github/workflows/cd.yml`：

**提示詞（給 Claude Code）**：

```
請幫我建立 .github/workflows/cd.yml，實現多環境部署：

需求：
1. 觸發條件：
   - CI 管線成功完成
   - 只在 main 分支
   - workflow_run 觸發

2. Jobs 結構（串行執行）：

   Job 1: deploy-dev
   - 部署到開發環境
   - 使用最新的 Docker 映像
   - 執行健康檢查
   - 執行煙霧測試

   Job 2: deploy-staging（依賴 deploy-dev）
   - 部署到測試環境
   - 執行整合測試
   - 執行完整的煙霧測試

   Job 3: deploy-production（依賴 deploy-staging）
   - 需要手動審批（environment protection rules）
   - 使用藍綠部署策略
   - 執行健康檢查
   - 失敗時自動回退

3. 部署方式：
   - 使用 docker-compose（或你選擇的方式）
   - SSH 到遠端伺服器（或使用雲端服務 API）
   - 更新容器
   - 驗證部署

注意：請提供模擬部署的方案（如果沒有真實伺服器）
```

#### 3.2 設定環境保護規則

在 GitHub 配置生產環境審批：

```
Settings > Environments > New environment
名稱：production
勾選：Required reviewers
添加：你的 GitHub 帳號
```

**檢查點**：
- [ ] 開發環境自動部署成功
- [ ] 測試環境自動部署成功
- [ ] 生產環境需要審批
- [ ] 部署後健康檢查通過

---

### 第 4 步：實現健康檢查和煙霧測試（30 分鐘）

#### 4.1 建立健康檢查端點

在 `app/health.py` 實現健康檢查：

**提示詞（給 Claude Code）**：

```
請幫我建立 app/health.py，實現完整的健康檢查：

需求：
1. GET /health 端點：
   - 檢查應用狀態
   - 檢查資料庫連線
   - 檢查外部依賴（如果有）
   - 返回詳細的健康報告

2. 回應格式：
{
  "status": "healthy",
  "version": "1.0.0",
  "checks": {
    "database": "ok",
    "dependencies": "ok"
  },
  "timestamp": "2024-01-01T00:00:00Z"
}

3. 狀態碼：
   - 200：所有檢查通過
   - 503：任何檢查失敗
```

#### 4.2 建立煙霧測試腳本

創建 `scripts/smoke-test.sh`：

**提示詞（給 Claude Code）**：

```
請幫我建立 scripts/smoke-test.sh，執行部署後的煙霧測試：

需求：
1. 測試項目：
   - 健康檢查端點回應 200
   - 主要 API 端點可訪問
   - 資料庫連線正常
   - 回應時間 < 1 秒

2. 失敗處理：
   - 任何測試失敗時，返回非零狀態碼
   - 輸出詳細的錯誤訊息
   - 重試機制（最多 3 次）

3. 環境變數：
   - API_URL：要測試的 API 網址
   - TIMEOUT：超時時間（預設 30 秒）
```

**檢查點**：
- [ ] 健康檢查端點正常運作
- [ ] 煙霧測試可以成功執行
- [ ] 測試失敗時正確報錯

---

### 第 5 步：實現回退機制（45 分鐘）

#### 5.1 建立回退 workflow

創建 `.github/workflows/rollback.yml`：

**提示詞（給 Claude Code）**：

```
請幫我建立 .github/workflows/rollback.yml，實現緊急回退：

需求：
1. 觸發方式：
   - 手動觸發（workflow_dispatch）
   - 輸入參數：環境（dev/staging/production）
   - 輸入參數：目標版本（Docker 映像 tag）

2. 回退流程：
   - 驗證目標版本存在
   - 部署指定版本
   - 執行健康檢查
   - 通知團隊

3. 安全措施：
   - 生產環境回退需要二次確認
   - 記錄回退原因
   - 自動建立事件報告
```

#### 5.2 建立回退腳本

創建 `scripts/rollback.sh`：

**提示詞（給 Claude Code）**：

```
請幫我建立 scripts/rollback.sh，執行回退操作：

需求：
1. 功能：
   - 停止當前版本
   - 啟動目標版本
   - 驗證回退成功

2. 參數：
   - 環境名稱
   - 目標版本號

3. 安全檢查：
   - 確認目標版本存在
   - 備份當前狀態
   - 驗證回退成功
```

**檢查點**：
- [ ] 回退 workflow 可以手動觸發
- [ ] 能夠回退到任意歷史版本
- [ ] 回退後健康檢查通過

---

### 第 6 步：加入監控和通知（30 分鐘）

#### 6.1 整合 Slack 通知

**提示詞（給 Claude Code）**：

```
請幫我在 .github/workflows/cd.yml 加入 Slack 通知：

需求：
1. 通知時機：
   - 部署開始
   - 部署成功
   - 部署失敗
   - 回退發生

2. 通知內容：
   - 環境名稱
   - 版本號
   - 部署者
   - 狀態（成功/失敗）
   - 相關連結（GitHub Actions、部署 URL）

3. 使用 slackapi/slack-github-action
   - SLACK_WEBHOOK_URL 從 secrets 讀取
```

#### 6.2 加入 GitHub Status 徽章

在專案 README.md 加入狀態徽章：

```markdown
![CI](https://github.com/你的帳號/你的專案/workflows/CI/badge.svg)
![CD](https://github.com/你的帳號/你的專案/workflows/CD/badge.svg)
![Security](https://github.com/你的帳號/你的專案/workflows/Security/badge.svg)
```

**檢查點**：
- [ ] Slack 通知正常運作
- [ ] 徽章顯示正確狀態
- [ ] 通知訊息清晰明確

---

## 🎯 完成標準

完成本練習後，你的完整 CI/CD 管線應該滿足：

### ✅ 核心功能（80 分）

- [ ] **完整的 CI 管線**：測試 + 掃描 + 構建
- [ ] **多環境部署**：開發、測試、生產三環境
- [ ] **自動化部署**：main 分支自動部署到開發/測試
- [ ] **部署驗證**：健康檢查 + 煙霧測試
- [ ] **回退機制**：可以快速回退到任意版本

### ✅ 進階功能（100 分）

- [ ] **環境保護**：生產環境需要審批
- [ ] **並行優化**：CI 階段並行執行（< 10 分鐘）
- [ ] **失敗處理**：自動回退機制
- [ ] **監控通知**：Slack/Email 通知
- [ ] **完整文檔**：部署指南、回退手冊

### ✅ 企業級標準（120 分）

- [ ] **藍綠部署**：零停機時間部署
- [ ] **金絲雀發布**：漸進式流量切換
- [ ] **完整監控**：整合 Prometheus/Grafana
- [ ] **自動化回退**：健康檢查失敗自動回退
- [ ] **合規記錄**：完整的部署審計日誌

---

## 🔍 自我檢查清單

### CI 階段

- [ ] Lint、Test、Security 並行執行
- [ ] 所有檢查通過才能構建 Docker
- [ ] Docker 映像標記包含版本資訊
- [ ] CI 執行時間 < 10 分鐘

### CD 階段

- [ ] 開發環境自動部署
- [ ] 測試環境自動部署
- [ ] 生產環境需要審批
- [ ] 部署後自動執行煙霧測試

### 可靠性

- [ ] 部署失敗時有清晰的錯誤訊息
- [ ] 可以快速回退（< 5 分鐘）
- [ ] 有完整的部署日誌
- [ ] 監控和告警正常運作

---

## 💡 學習重點

### DevOps 最佳實踐

1. **自動化一切**
   - 測試自動化
   - 部署自動化
   - 回退自動化

2. **快速失敗**
   - 盡早發現問題
   - 清晰的錯誤訊息
   - 快速修復機制

3. **漸進式發布**
   - 開發 → 測試 → 生產
   - 小步快跑
   - 降低風險

4. **可觀測性**
   - 完整的日誌
   - 健康檢查
   - 監控告警

### 部署策略對比

| 策略 | 停機時間 | 回退速度 | 複雜度 | 成本 |
|------|---------|---------|--------|------|
| 直接部署 | 有 | 慢 | 低 | 低 |
| 藍綠部署 | 無 | 快 | 中 | 高（雙倍資源）|
| 金絲雀發布 | 無 | 中 | 高 | 中 |
| 滾動更新 | 無 | 中 | 中 | 中 |

---

## 📚 延伸學習

完成基礎練習後，可以嘗試：

1. **整合 Kubernetes**
   - 使用 Helm charts
   - 實現滾動更新
   - 配置自動擴展

2. **加入效能測試**
   - 使用 k6 或 Locust
   - 部署前執行負載測試
   - 設定效能基準線

3. **實現功能開關**
   - 使用 LaunchDarkly 或 Unleash
   - 漸進式功能發布
   - A/B 測試

4. **建立災難恢復**
   - 資料備份策略
   - 跨區域部署
   - 災難恢復演練

---

## 🆘 需要協助？

### 常見問題

**Q1: 部署失敗但沒有錯誤訊息？**

A: 檢查：
- GitHub Actions 日誌
- 應用程式日誌
- Docker 容器日誌
- 健康檢查端點回應

**Q2: 如何在沒有真實伺服器的情況下練習？**

A: 方案：
- 使用 GitHub Actions 的 runner 作為「部署目標」
- 使用免費的雲端服務（Railway、Render、Fly.io）
- 使用 Docker Compose 模擬多環境

**Q3: 如何測試回退功能？**

A: 步驟：
1. 部署版本 v1.0
2. 部署版本 v2.0（故意引入 bug）
3. 觸發回退到 v1.0
4. 驗證回退成功

---

## ✅ 完成後的下一步

完成本練習後，你已經掌握了企業級 CI/CD 管線的建立！

**下一步建議**：

1. **應用到實際專案**
   - 為你的專案建立完整管線
   - 根據專案需求調整策略

2. **深入學習**
   - Kubernetes 進階應用
   - GitOps（ArgoCD、Flux）
   - 服務網格（Istio、Linkerd）

3. **分享經驗**
   - 寫部落格記錄學習過程
   - 在團隊中推廣 DevOps 實踐

---

**恭喜你完成所有練習！** 🎉

你已經掌握了：
- ✅ 自動化測試管線
- ✅ 多層次安全掃描
- ✅ 容器化構建
- ✅ 多環境部署
- ✅ 監控和回退

這些技能將極大提升你的開發效率和代碼品質！
