# E01：企業級完整 DevOps 管線 🔥

## 📋 情境資訊

**難度等級**：⭐⭐⭐ 複雜級
**預估時間**：4-6 小時
**核心技能**：完整 DevOps 流程、多團隊協作、企業級安全、合規性、多雲部署
**前置知識**：所有基礎級 + 所有組合級情境

---

## 🎯 情境背景

你是一家快速成長的 SaaS 獨角獸公司（估值 $1B+）的 DevOps 架構師。公司經過 5 年發展,技術棧已經非常複雜,現在需要重新設計整個 DevOps 管線以支持未來 3 年的業務增長。

**公司規模**：
- **員工**：120 個工程師（分佈在 8 個國家）
- **產品**：企業級 SaaS 平台（類似 Salesforce）
- **客戶**：500+ 企業客戶,包含 50 家 Fortune 500
- **流量**：1M+ DAU,5TB+ 數據處理/天
- **收入**：$50M ARR,正在籌備 IPO

**技術架構**：
```
前端：
├── Web Admin（React + TypeScript）
├── Web Customer Portal（Next.js）
├── Mobile Apps（React Native）
└── Chrome Extension（JavaScript）

後端：
├── API Gateway（Kong + Lua）
├── 15 個微服務（Node.js + Python + Go）
├── 消息佇列（Kafka）
├── 快取（Redis Cluster）
├── 搜尋（Elasticsearch）
└── 數據倉庫（Snowflake）

基礎設施：
├── AWS（主要）
├── GCP（災難恢復）
├── Kubernetes（EKS + GKE）
├── Terraform（IaC）
└── Vault（Secret 管理）

團隊結構：
├── Frontend Team（20 人）
├── Backend Team（40 人）
├── Platform Team（15 人）
├── Data Team（10 人）
├── DevOps Team（你 + 5 人）
├── Security Team（10 人）
└── QA Team（20 人）
```

**當前痛點（災難性問題）**：

```bash
# 問題 1：部署混亂（每週 3 次生產事故）
──────────────────────────────────────
事故報告 #234
日期：2024-10-20
停機時間：6 小時
影響客戶：350 家
損失：$500,000（SLA 賠償）

根本原因：
1. 15 個微服務版本不相容
2. 部署順序錯誤導致級聯失敗
3. 回退失敗（回退腳本未測試）
4. 監控不足（40 分鐘才發現問題）

# 問題 2：合規性危機（即將失去最大客戶）
──────────────────────────────────────
合規審計結果：FAIL
- SOC 2 Type II：不合格
- GDPR：12 項違規
- HIPAA：未通過
- PCI DSS：Level 1 失敗

客戶威脅：
- 最大客戶（$5M/年）威脅終止合約
- 3 家 Fortune 500 暫停採購
- 新客戶要求完整合規證明

# 問題 3：CI/CD 效率極低
──────────────────────────────────────
構建統計（上週）：
- 平均 CI 時間：45 分鐘
- 平均部署時間：2 小時
- 失敗率：35%
- 每天阻擋的 PR：~20 個
- 工程師等待時間浪費：480 人時/週

成本問題：
- GitHub Actions 帳單：$8,000/月
- 構建失敗浪費：$12,000/月
- 總 CI/CD 成本：$20,000/月

# 問題 4：安全漏洞頻發
──────────────────────────────────────
安全掃描結果：
- Critical 漏洞：127 個
- High 漏洞：456 個
- 依賴過時：342 個套件
- 容器基礎鏡像漏洞：89 個
- Secrets 洩漏：23 次（過去 3 個月）

近期安全事件：
- API 密鑰洩漏到公開 GitHub repo
- SQL 注入漏洞被利用
- 資料外洩（50,000 用戶）
- 罰金：$2M（GDPR）
```

**CEO 緊急會議記錄**：
> 「我們正處於公司歷史上最關鍵的時刻。IPO 審計團隊發現我們的 DevOps 流程存在重大風險。投資銀行明確表示，如果我們不能在 6 個月內建立企業級的 DevOps 體系，IPO 計劃將被推遲，這意味著損失數億美元的市值。
>
> 我需要你在 **3 個月內**完成以下目標：
> 1. 建立符合 SOC 2、GDPR、HIPAA 的完整 DevOps 管線
> 2. 部署成功率達到 99.9%
> 3. CI/CD 時間減少 70%
> 4. 所有 Critical/High 漏洞清零
> 5. 建立完整的災難恢復體系
> 6. 多雲架構（AWS + GCP）
> 7. 完整的審計追蹤
>
> 預算：$200,000（軟體 + 基礎設施）
> 團隊：你可以從公司內部調配資源
>
> 失敗不是選項。公司的未來取決於此。」

**你的任務**：
從零開始設計並實施企業級的完整 DevOps 管線,涵蓋從程式碼提交到生產部署的所有環節,確保滿足所有合規性要求,同時大幅提升效率和可靠性。

---

## 📂 專案結構

```
enterprise-devops/
├── .github/
│   ├── workflows/
│   │   ├── ci-frontend.yml
│   │   ├── ci-backend.yml
│   │   ├── ci-platform.yml
│   │   ├── security-scan.yml
│   │   ├── compliance-check.yml
│   │   ├── deploy-staging.yml
│   │   ├── deploy-production.yml
│   │   ├── disaster-recovery-drill.yml
│   │   └── release.yml
│   │
│   ├── actions/
│   │   ├── security-scan/
│   │   ├── compliance-check/
│   │   ├── deploy-service/
│   │   └── rollback/
│   │
│   └── CODEOWNERS
│
├── infrastructure/
│   ├── terraform/
│   │   ├── aws/
│   │   │   ├── eks/
│   │   │   ├── rds/
│   │   │   ├── s3/
│   │   │   └── vpc/
│   │   │
│   │   ├── gcp/
│   │   │   ├── gke/
│   │   │   └── cloud-sql/
│   │   │
│   │   └── modules/
│   │
│   ├── kubernetes/
│   │   ├── base/
│   │   ├── overlays/
│   │   │   ├── dev/
│   │   │   ├── staging/
│   │   │   └── production/
│   │   │
│   │   └── helm/
│   │
│   └── monitoring/
│       ├── prometheus/
│       ├── grafana/
│       └── alerts/
│
├── services/
│   ├── api-gateway/
│   ├── auth-service/
│   ├── user-service/
│   ├── payment-service/
│   ├── notification-service/
│   └── ... (10 more services)
│
├── frontend/
│   ├── web-admin/
│   ├── web-customer/
│   └── mobile-app/
│
├── docs/
│   ├── compliance/
│   │   ├── SOC2-controls.md
│   │   ├── GDPR-compliance.md
│   │   ├── HIPAA-safeguards.md
│   │   └── PCI-DSS-requirements.md
│   │
│   ├── runbooks/
│   │   ├── deployment.md
│   │   ├── rollback.md
│   │   ├── disaster-recovery.md
│   │   └── incident-response.md
│   │
│   └── architecture/
│       ├── system-design.md
│       ├── security-architecture.md
│       └── disaster-recovery-plan.md
│
├── scripts/
│   ├── compliance/
│   ├── security/
│   └── automation/
│
└── tests/
    ├── e2e/
    ├── integration/
    ├── performance/
    └── security/
```

---

## 🎬 情境展開

### 階段 1：架構設計與規劃（1 小時）

**任務**：設計完整的 DevOps 架構,涵蓋所有需求。

#### 1.1 DevOps 成熟度評估

**當前狀態評估矩陣**：
```
維度               | 當前狀態 | 目標狀態 | 差距
-------------------|---------|---------|-----
自動化程度         | Level 2 | Level 5 | 3 levels
部署頻率           | 2x/週   | 10x/天  | 50x
變更前置時間       | 2 週    | 4 小時  | 84%
MTTR（平均恢復時間）| 6 小時  | 5 分鐘  | 98.6%
變更失敗率         | 35%     | < 1%    | 97%
安全漏洞修復時間   | 30 天   | 24 小時 | 99%
合規性覆蓋率       | 30%     | 100%    | 70%
```

#### 1.2 技術選型決策

**核心工具鏈**：
```yaml
工具選型矩陣:
  CI/CD:
    primary: GitHub Actions
    backup: GitLab CI
    reasoning: >
      - 與 GitHub 深度整合
      - 豐富的 marketplace
      - 彈性計價
      - 符合 SOC 2 要求

  容器編排:
    primary: Kubernetes (EKS + GKE)
    version: 1.28+
    reasoning: >
      - 業界標準
      - 多雲支持
      - 強大的生態系統

  基礎設施即代碼:
    tool: Terraform
    version: 1.5+
    state_backend: S3 + DynamoDB
    reasoning: >
      - 多雲支持
      - 模組化
      - 狀態管理

  Secret 管理:
    tool: HashiCorp Vault
    deployment: Kubernetes Operator
    reasoning: >
      - 企業級安全
      - 審計日誌
      - 動態 Secret

  監控與告警:
    metrics: Prometheus + Grafana
    logs: ELK Stack
    traces: Jaeger
    apm: Datadog
    reasoning: >
      - 全方位可觀測性
      - 符合合規要求

  安全掃描:
    sast: CodeQL + Semgrep
    sca: Snyk + Dependabot
    container: Trivy + Grype
    secrets: GitGuardian
    reasoning: >
      - 多層次防禦
      - 自動化修復
      - 合規報告
```

#### 1.3 架構設計文檔

建立完整的架構設計文檔（`docs/architecture/devops-architecture.md`）：

```markdown
# Enterprise DevOps Architecture

## 1. 總體架構

```
開發者 →  Git Push
           ↓
    ┌─────────────────────────────┐
    │   GitHub（Source Control）   │
    └─────────────────────────────┘
           ↓
    ┌─────────────────────────────┐
    │   CI Pipeline                │
    │   - Build                    │
    │   - Test（Unit/Integration） │
    │   - Security Scan            │
    │   - Compliance Check         │
    └─────────────────────────────┘
           ↓（Artifact）
    ┌─────────────────────────────┐
    │   Artifact Registry          │
    │   - GHCR（容器鏡像）         │
    │   - S3（其他 artifacts）     │
    └─────────────────────────────┘
           ↓
    ┌─────────────────────────────┐
    │   CD Pipeline                │
    │   - Deploy to Staging        │
    │   - E2E Tests                │
    │   - Security Validation      │
    │   - Manual Approval          │
    │   - Deploy to Production     │
    └─────────────────────────────┘
           ↓
    ┌─────────────────────────────┐
    │   Multi-Cloud Production     │
    │   - AWS（Primary）           │
    │   - GCP（DR）                │
    │   - Kubernetes               │
    └─────────────────────────────┘
           ↓
    ┌─────────────────────────────┐
    │   Monitoring & Alerting      │
    │   - Metrics（Prometheus）    │
    │   - Logs（ELK）              │
    │   - Traces（Jaeger）         │
    │   - Incidents（PagerDuty）   │
    └─────────────────────────────┘
```

## 2. 安全架構

```
┌─────────────────────────────────────┐
│        Security Layers              │
├─────────────────────────────────────┤
│ 1. Source Code Security             │
│    - Branch Protection               │
│    - Code Signing                    │
│    - Secret Scanning                 │
├─────────────────────────────────────┤
│ 2. Build Security                    │
│    - Verified Base Images            │
│    - SBOM Generation                 │
│    - Image Signing                   │
├─────────────────────────────────────┤
│ 3. Runtime Security                  │
│    - Network Policies                │
│    - Pod Security Standards          │
│    - Runtime Threat Detection        │
├─────────────────────────────────────┤
│ 4. Data Security                     │
│    - Encryption at Rest              │
│    - Encryption in Transit           │
│    - Key Rotation                    │
└─────────────────────────────────────┘
```

## 3. 合規性架構

每個控制點都對應具體的合規要求：

| 控制點 | SOC 2 | GDPR | HIPAA | PCI DSS |
|--------|-------|------|-------|---------|
| 代碼審查 | CC6.1 | Art.32 | §164.308 | Req.6.3 |
| 安全掃描 | CC7.2 | Art.32 | §164.308 | Req.6.2 |
| 訪問控制 | CC6.2 | Art.32 | §164.312 | Req.7.1 |
| 審計日誌 | CC5.2 | Art.30 | §164.312 | Req.10.1 |
| 加密 | CC6.7 | Art.32 | §164.312 | Req.3.4 |
| 備份 | CC8.1 | Art.32 | §164.308 | Req.9.5 |
```

**檢查點 1.1**：
- [ ] 架構設計文檔完成
- [ ] 技術選型有充分理由
- [ ] 合規性映射清晰
- [ ] 團隊審查通過

---

### 階段 2：核心 CI 管線建設（2 小時）

**任務**：建立企業級的 CI 管線,滿足速度、安全、合規的要求。

#### 2.1 統一 CI 框架

建立可重用的 CI 框架（`.github/workflows/reusable-ci.yml`）：

```yaml
name: Reusable CI Pipeline

on:
  workflow_call:
    inputs:
      service_name:
        required: true
        type: string
      language:
        required: true
        type: string  # node, python, go
      test_command:
        required: true
        type: string
      build_command:
        required: false
        type: string
    outputs:
      image_tag:
        description: "Built image tag"
        value: ${{ jobs.build.outputs.image_tag }}
      security_passed:
        description: "Security scan passed"
        value: ${{ jobs.security.outputs.passed }}

jobs:
  # Job 1: 程式碼品質檢查
  code-quality:
    runs-on: ubuntu-latest
    timeout-minutes: 10

    steps:
      - uses: actions/checkout@v4

      - name: Setup environment
        uses: ./.github/actions/setup-${{ inputs.language }}

      - name: Lint
        run: |
          case "${{ inputs.language }}" in
            node)
              npm run lint
              ;;
            python)
              ruff check .
              black --check .
              ;;
            go)
              golangci-lint run
              ;;
          esac

      - name: Type check
        if: inputs.language == 'node' || inputs.language == 'python'
        run: |
          case "${{ inputs.language }}" in
            node)
              npm run type-check
              ;;
            python)
              mypy .
              ;;
          esac

  # Job 2: 測試
  test:
    runs-on: ubuntu-latest
    timeout-minutes: 20

    strategy:
      matrix:
        test-type: [unit, integration]

    steps:
      - uses: actions/checkout@v4

      - name: Setup environment
        uses: ./.github/actions/setup-${{ inputs.language }}

      - name: Run ${{ matrix.test-type }} tests
        run: ${{ inputs.test_command }} --test-type=${{ matrix.test-type }}

      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          flags: ${{ matrix.test-type }}

  # Job 3: 安全掃描
  security:
    runs-on: ubuntu-latest
    outputs:
      passed: ${{ steps.evaluate.outputs.passed }}

    steps:
      - uses: actions/checkout@v4

      - name: Run Semgrep
        uses: returntocorp/semgrep-action@v1
        with:
          config: r/security-audit

      - name: Dependency scan
        uses: snyk/actions@master
        with:
          command: test
          args: --severity-threshold=high
        env:
          SNYK_TOKEN: ${{ secrets.SNYK_TOKEN }}

      - name: Secret scanning
        uses: trufflesecurity/trufflehog@main
        with:
          path: ./
          base: ${{ github.event.repository.default_branch }}
          head: HEAD

      - name: Evaluate security
        id: evaluate
        run: |
          # 檢查是否有 Critical/High 漏洞
          if [ "${{ steps.snyk.outcome }}" == "failure" ]; then
            echo "passed=false" >> $GITHUB_OUTPUT
            exit 1
          fi
          echo "passed=true" >> $GITHUB_OUTPUT

  # Job 4: 構建
  build:
    needs: [code-quality, test, security]
    runs-on: ubuntu-latest
    outputs:
      image_tag: ${{ steps.meta.outputs.tags }}

    steps:
      - uses: actions/checkout@v4

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Log in to GHCR
        uses: docker/login-action@v3
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Docker meta
        id: meta
        uses: docker/metadata-action@v5
        with:
          images: ghcr.io/${{ github.repository }}/${{ inputs.service_name }}
          tags: |
            type=sha,prefix={{branch}}-
            type=semver,pattern={{version}}
            type=semver,pattern={{major}}.{{minor}}

      - name: Build and push
        uses: docker/build-push-action@v5
        with:
          context: ./services/${{ inputs.service_name }}
          push: true
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
          cache-from: type=gha
          cache-to: type=gha,mode=max
          build-args: |
            BUILD_DATE=${{ github.event.repository.updated_at }}
            VCS_REF=${{ github.sha }}

      - name: Sign image
        uses: sigstore/cosign-installer@main
        run: |
          cosign sign --key cosign.key \
            ${{ steps.meta.outputs.tags }}
        env:
          COSIGN_PASSWORD: ${{ secrets.COSIGN_PASSWORD }}

      - name: Generate SBOM
        uses: anchore/sbom-action@v0
        with:
          image: ${{ steps.meta.outputs.tags }}
          format: spdx-json
          output-file: sbom.spdx.json

      - name: Scan image
        uses: aquasecurity/trivy-action@master
        with:
          image-ref: ${{ steps.meta.outputs.tags }}
          format: 'sarif'
          output: 'trivy-results.sarif'
          severity: 'CRITICAL,HIGH'
          exit-code: '1'

      - name: Upload SARIF
        uses: github/codeql-action/upload-sarif@v2
        if: always()
        with:
          sarif_file: 'trivy-results.sarif'

  # Job 5: 合規性檢查
  compliance:
    needs: [build]
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: SOC 2 控制檢查
        run: python scripts/compliance/check_soc2.py

      - name: GDPR 合規檢查
        run: python scripts/compliance/check_gdpr.py

      - name: 生成合規報告
        run: |
          python scripts/compliance/generate_report.py \
            --output compliance-report.pdf

      - name: Upload report
        uses: actions/upload-artifact@v3
        with:
          name: compliance-report
          path: compliance-report.pdf

  # Job 6: 通知
  notify:
    needs: [build, compliance]
    if: always()
    runs-on: ubuntu-latest

    steps:
      - name: Send Slack notification
        uses: 8398a7/action-slack@v3
        with:
          status: ${{ job.status }}
          text: |
            CI Pipeline for ${{ inputs.service_name }}
            Result: ${{ job.status }}
            Commit: ${{ github.sha }}
            Author: ${{ github.actor }}
          webhook_url: ${{ secrets.SLACK_WEBHOOK }}
```

#### 2.2 服務特定 CI（範例：auth-service）

`.github/workflows/ci-auth-service.yml`：
```yaml
name: CI - Auth Service

on:
  push:
    branches: ['**']
    paths:
      - 'services/auth-service/**'
      - '.github/workflows/ci-auth-service.yml'
  pull_request:
    branches: [main]
    paths:
      - 'services/auth-service/**'

jobs:
  ci:
    uses: ./.github/workflows/reusable-ci.yml
    with:
      service_name: auth-service
      language: node
      test_command: npm run test
      build_command: npm run build
    secrets: inherit
```

#### 2.3 並行執行策略

`.github/workflows/ci-all-services.yml`：
```yaml
name: CI - All Services

on:
  push:
    branches: [main]

jobs:
  detect-changes:
    runs-on: ubuntu-latest
    outputs:
      services: ${{ steps.changes.outputs.services }}

    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Detect changed services
        id: changes
        run: |
          CHANGED_SERVICES=$(git diff --name-only HEAD~1 HEAD | \
            grep '^services/' | \
            cut -d/ -f2 | \
            sort -u | \
            jq -R -s -c 'split("\n")[:-1]')

          echo "services=$CHANGED_SERVICES" >> $GITHUB_OUTPUT

  ci-services:
    needs: detect-changes
    if: needs.detect-changes.outputs.services != '[]'

    strategy:
      matrix:
        service: ${{ fromJson(needs.detect-changes.outputs.services) }}
      max-parallel: 5  # 最多 5 個服務並行構建

    uses: ./.github/workflows/reusable-ci.yml
    with:
      service_name: ${{ matrix.service }}
      language: node  # 根據實際情況調整
      test_command: npm run test
    secrets: inherit
```

**檢查點 2.1**：
- [ ] 可重用 CI 框架建立
- [ ] 所有服務整合 CI
- [ ] 並行構建正常運作
- [ ] CI 時間 < 15 分鐘

---

### 階段 3：企業級安全與合規（1.5 小時）

**任務**：建立符合 SOC 2、GDPR、HIPAA、PCI DSS 的完整安全與合規體系。

#### 3.1 SOC 2 控制實施

建立自動化的 SOC 2 控制檢查（`scripts/compliance/check_soc2.py`）：

```python
#!/usr/bin/env python3
"""
SOC 2 Trust Service Criteria 自動化檢查
"""
import sys
import json
from typing import Dict, List, Tuple

class SOC2Checker:
    def __init__(self):
        self.results = []
        self.passed = 0
        self.failed = 0

    def check_cc6_1_code_review(self) -> Tuple[bool, str]:
        """CC6.1: 系統變更需要授權和審查"""
        # 檢查 CODEOWNERS 檔案存在
        if not os.path.exists('.github/CODEOWNERS'):
            return False, "CODEOWNERS file not found"

        # 檢查分支保護規則
        response = requests.get(
            f"https://api.github.com/repos/{REPO}/branches/main/protection",
            headers={"Authorization": f"token {GITHUB_TOKEN}"}
        )

        if response.status_code != 200:
            return False, "Branch protection not enabled"

        protection = response.json()

        # 必須要求 PR 審查
        if not protection.get('required_pull_request_reviews'):
            return False, "PR reviews not required"

        # 必須要求至少 2 個審查者
        if protection['required_pull_request_reviews']['required_approving_review_count'] < 2:
            return False, "At least 2 reviewers required"

        return True, "Code review controls in place"

    def check_cc6_6_access_control(self) -> Tuple[bool, str]:
        """CC6.6: 訪問控制和身份驗證"""
        # 檢查是否使用 SSO
        response = requests.get(
            f"https://api.github.com/orgs/{ORG}",
            headers={"Authorization": f"token {GITHUB_TOKEN}"}
        )

        org = response.json()

        if not org.get('has_organization_projects'):
            return False, "SSO not configured"

        # 檢查 2FA
        if not org.get('two_factor_requirement_enabled'):
            return False, "2FA not enforced"

        return True, "Access controls configured"

    def check_cc7_2_security_monitoring(self) -> Tuple[bool, str]:
        """CC7.2: 系統監控與異常檢測"""
        # 檢查是否有監控設置
        monitors_file = 'infrastructure/monitoring/alerts/rules.yml'

        if not os.path.exists(monitors_file):
            return False, "Monitoring rules not found"

        with open(monitors_file) as f:
            rules = yaml.safe_load(f)

        required_alerts = [
            'DeploymentFailed',
            'HighErrorRate',
            'SecurityVulnerabilityDetected',
            'UnauthorizedAccess'
        ]

        existing_alerts = [rule['alert'] for group in rules['groups']
                          for rule in group['rules']]

        missing = set(required_alerts) - set(existing_alerts)

        if missing:
            return False, f"Missing alerts: {', '.join(missing)}"

        return True, "Security monitoring configured"

    def check_cc8_1_backup_recovery(self) -> Tuple[bool, str]:
        """CC8.1: 資料備份與恢復"""
        # 檢查備份策略文檔
        if not os.path.exists('docs/runbooks/disaster-recovery.md'):
            return False, "Disaster recovery plan not found"

        # 檢查是否有自動化備份 workflow
        backup_workflow = '.github/workflows/backup.yml'

        if not os.path.exists(backup_workflow):
            return False, "Automated backup not configured"

        # 檢查最近一次災難恢復演練
        drill_file = 'docs/compliance/last-dr-drill.json'

        if os.path.exists(drill_file):
            with open(drill_file) as f:
                drill = json.load(f)

            last_drill = datetime.fromisoformat(drill['date'])
            if (datetime.now() - last_drill).days > 90:
                return False, "DR drill not performed in last 90 days"

        return True, "Backup and recovery controls in place"

    def run_all_checks(self) -> bool:
        """執行所有 SOC 2 檢查"""
        checks = [
            ("CC6.1", "Code Review", self.check_cc6_1_code_review),
            ("CC6.6", "Access Control", self.check_cc6_6_access_control),
            ("CC7.2", "Security Monitoring", self.check_cc7_2_security_monitoring),
            ("CC8.1", "Backup & Recovery", self.check_cc8_1_backup_recovery),
        ]

        print("=" * 60)
        print("SOC 2 Trust Service Criteria - Automated Checks")
        print("=" * 60)

        for code, name, check_func in checks:
            passed, message = check_func()

            status = "✅ PASS" if passed else "❌ FAIL"
            print(f"\n[{code}] {name}")
            print(f"Status: {status}")
            print(f"Details: {message}")

            self.results.append({
                "code": code,
                "name": name,
                "passed": passed,
                "message": message
            })

            if passed:
                self.passed += 1
            else:
                self.failed += 1

        print("\n" + "=" * 60)
        print(f"Results: {self.passed} passed, {self.failed} failed")
        print("=" * 60)

        # 生成報告
        with open('soc2-compliance-report.json', 'w') as f:
            json.dump({
                "timestamp": datetime.now().isoformat(),
                "results": self.results,
                "summary": {
                    "passed": self.passed,
                    "failed": self.failed,
                    "compliance_rate": f"{(self.passed / len(checks)) * 100:.1f}%"
                }
            }, f, indent=2)

        return self.failed == 0

if __name__ == "__main__":
    checker = SOC2Checker()
    success = checker.run_all_checks()
    sys.exit(0 if success else 1)
```

#### 3.2 GDPR 合規檢查

建立 GDPR 自動化檢查（`scripts/compliance/check_gdpr.py`）：

```python
#!/usr/bin/env python3
"""
GDPR Article 32 - Security of Processing 自動化檢查
"""
import sys
from typing import List, Dict

class GDPRChecker:
    def check_encryption_at_rest(self) -> Tuple[bool, str]:
        """檢查靜態加密"""
        # 檢查資料庫加密設定
        terraform_files = glob.glob('infrastructure/terraform/**/*.tf', recursive=True)

        encryption_found = False
        for tf_file in terraform_files:
            with open(tf_file) as f:
                content = f.read()

                # 檢查 RDS 加密
                if 'resource "aws_db_instance"' in content:
                    if 'storage_encrypted = true' in content:
                        encryption_found = True
                    else:
                        return False, f"Database encryption not enabled in {tf_file}"

        return True, "Encryption at rest enabled"

    def check_encryption_in_transit(self) -> Tuple[bool, str]:
        """檢查傳輸加密"""
        # 檢查 Kubernetes Ingress TLS 設定
        k8s_files = glob.glob('infrastructure/kubernetes/**/*.yaml', recursive=True)

        for k8s_file in k8s_files:
            with open(k8s_file) as f:
                docs = yaml.safe_load_all(f)

                for doc in docs:
                    if doc.get('kind') == 'Ingress':
                        if 'tls' not in doc.get('spec', {}):
                            return False, f"TLS not configured in {k8s_file}"

        return True, "Encryption in transit enabled"

    def check_data_retention(self) -> Tuple[bool, str]:
        """檢查資料保留政策"""
        policy_file = 'docs/compliance/data-retention-policy.md'

        if not os.path.exists(policy_file):
            return False, "Data retention policy not found"

        # 檢查是否有自動化資料刪除機制
        # (實際實作會檢查資料庫中的 TTL 設定等)

        return True, "Data retention policy in place"

    def check_audit_logging(self) -> Tuple[bool, str]:
        """檢查審計日誌"""
        # 檢查是否啟用 CloudTrail（AWS）
        # 檢查是否啟用 Cloud Audit Logs（GCP）
        # 檢查 Kubernetes audit logging

        k8s_audit_config = 'infrastructure/kubernetes/audit-policy.yaml'

        if not os.path.exists(k8s_audit_config):
            return False, "Kubernetes audit policy not found"

        return True, "Audit logging enabled"

    def check_right_to_erasure(self) -> Tuple[bool, str]:
        """檢查「被遺忘權」實施"""
        # 檢查是否有資料刪除 API
        api_files = glob.glob('services/*/src/routes/**/*.js', recursive=True)

        erasure_endpoint_found = False
        for api_file in api_files:
            with open(api_file) as f:
                content = f.read()

                if 'DELETE' in content and '/users/' in content:
                    erasure_endpoint_found = True
                    break

        if not erasure_endpoint_found:
            return False, "User data deletion endpoint not found"

        return True, "Right to erasure implemented"

    def run_all_checks(self) -> bool:
        """執行所有 GDPR 檢查"""
        checks = [
            ("Art.32(1)(a)", "Encryption at Rest", self.check_encryption_at_rest),
            ("Art.32(1)(a)", "Encryption in Transit", self.check_encryption_in_transit),
            ("Art.5(1)(e)", "Data Retention", self.check_data_retention),
            ("Art.30", "Audit Logging", self.check_audit_logging),
            ("Art.17", "Right to Erasure", self.check_right_to_erasure),
        ]

        print("=" * 60)
        print("GDPR Compliance - Automated Checks")
        print("=" * 60)

        passed = 0
        failed = 0

        for article, name, check_func in checks:
            result, message = check_func()

            status = "✅ PASS" if result else "❌ FAIL"
            print(f"\n[{article}] {name}")
            print(f"Status: {status}")
            print(f"Details: {message}")

            if result:
                passed += 1
            else:
                failed += 1

        print("\n" + "=" * 60)
        print(f"Results: {passed} passed, {failed} failed")
        print("=" * 60)

        return failed == 0

if __name__ == "__main__":
    checker = GDPRChecker()
    success = checker.run_all_checks()
    sys.exit(0 if success else 1)
```

#### 3.3 合規 Workflow 整合

`.github/workflows/compliance-check.yml`：
```yaml
name: Compliance Check

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
  schedule:
    - cron: '0 0 * * 0'  # 每週日執行

jobs:
  compliance:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          pip install pyyaml requests

      - name: SOC 2 Compliance Check
        run: python scripts/compliance/check_soc2.py

      - name: GDPR Compliance Check
        run: python scripts/compliance/check_gdpr.py

      - name: HIPAA Compliance Check
        run: python scripts/compliance/check_hipaa.py

      - name: PCI DSS Compliance Check
        run: python scripts/compliance/check_pci_dss.py

      - name: Generate consolidated report
        run: python scripts/compliance/generate_consolidated_report.py

      - name: Upload compliance reports
        uses: actions/upload-artifact@v3
        with:
          name: compliance-reports
          path: |
            soc2-compliance-report.json
            gdpr-compliance-report.json
            hipaa-compliance-report.json
            pci-dss-compliance-report.json
            consolidated-compliance-report.pdf

      - name: Send compliance report to stakeholders
        if: github.event_name == 'schedule'
        run: |
          # 發送到 Slack #compliance 頻道
          # 發送到 security@company.com
          # 上傳到合規管理平台
```

**檢查點 3.1**：
- [ ] SOC 2 自動化檢查完成
- [ ] GDPR 自動化檢查完成
- [ ] HIPAA 自動化檢查完成
- [ ] PCI DSS 自動化檢查完成
- [ ] 所有合規檢查通過

---

（由於篇幅限制,這裡只展示了部分核心內容。完整情境會繼續包含以下階段：）

### 階段 4：多雲部署架構（1 小時）
- AWS 主要部署（EKS）
- GCP 災難恢復（GKE）
- Terraform 多雲基礎設施
- 跨雲資料同步

### 階段 5：監控與可觀測性（45 分鐘）
- Prometheus + Grafana 監控
- ELK Stack 日誌聚合
- Jaeger 分散式追蹤
- PagerDuty 告警整合

### 階段 6：災難恢復與業務連續性（30 分鐘）
- RTO/RPO 定義
- 自動化災難恢復流程
- 定期演練機制
- 跨區域 failover

---

## 🎯 最終交付物

完成所有階段後,你應該擁有：

### 技術交付物
- [ ] 完整的 CI/CD 管線（15+ workflows）
- [ ] 企業級安全掃描體系
- [ ] 自動化合規檢查系統
- [ ] 多雲部署架構
- [ ] 完整的監控與告警
- [ ] 災難恢復計劃與演練

### 文檔交付物
- [ ] DevOps 架構設計文檔
- [ ] 安全架構文檔
- [ ] 合規性映射文檔
- [ ] 運維手冊（10+ runbooks）
- [ ] 災難恢復計劃
- [ ] 培訓材料

### 業務成果
- [ ] 部署成功率 > 99.9%
- [ ] CI/CD 時間減少 > 70%
- [ ] 所有 Critical/High 漏洞清零
- [ ] SOC 2、GDPR、HIPAA、PCI DSS 合規
- [ ] RTO < 10 分鐘,RPO < 5 分鐘
- [ ] 成本降低 > 40%

---

## 💡 進階挑戰

### 挑戰 1：AI 驅動的 DevOps
- 使用機器學習預測部署風險
- 自動化根本原因分析
- 智能告警降噪

### 挑戰 2：FinOps 優化
- 雲成本可視化
- 資源使用優化
- 成本歸因分析

### 挑戰 3：平台工程
- 建立內部開發者平台（IDP）
- 自助服務門戶
- 黃金路徑（Golden Path）

---

## 📚 參考資源

- [DORA State of DevOps Report](https://dora.dev/)
- [SOC 2 Controls](https://www.aicpa.org/interestareas/frc/assuranceadvisoryservices/sorhome)
- [GDPR Official Text](https://gdpr.eu/)
- [NIST Cybersecurity Framework](https://www.nist.gov/cyberframework)
- [The DevOps Handbook](https://itrevolution.com/product/the-devops-handbook/)

---

**恭喜！** 如果你成功完成這個企業級 DevOps 管線,你已經具備了領導大型組織 DevOps 轉型的能力。接下來可以挑戰 **E02：微服務架構 CI/CD**！
