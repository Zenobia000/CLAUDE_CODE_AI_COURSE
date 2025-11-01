# C05：Monorepo 管線設計 ⭐

## 📋 情境資訊

**難度等級**：⭐⭐ 組合級
**預估時間**：2-2.5 小時
**核心技能**：Monorepo 策略、變更檢測、並行構建、依賴管理
**前置知識**：基礎級 B01-B06、組合級 C03-C04

---

## 🎯 情境背景

你是一家中型科技公司的 DevOps Lead,公司決定將所有專案遷移到 Monorepo 架構。

**公司現況**：
- 產品：SaaS 企業管理平台
- 技術棧：
  - Frontend: React + TypeScript (3 個應用)
  - Backend: Node.js + NestJS (5 個微服務)
  - Shared: 10+ 共享套件（UI 元件、工具函數、型別定義）
- 團隊：30 個工程師
- Repository: 從 20+ 個分散 repo 合併到 1 個 Monorepo

**痛點**：

```bash
# 現有問題報告
日期：2024-10-25

問題 1：構建時間爆炸
- 每次 push 都構建所有專案（30 分鐘）
- 即使只修改一個共享套件中的一個 typo
- CI 成本從 $200/月增加到 $2000/月

問題 2：依賴地獄
- 共享套件版本不一致
- A 專案用 utils@1.0，B 專案用 utils@2.0
- 循環依賴未被發現
- 更新一個套件導致多個專案 build 失敗

問題 3：測試混亂
- 不知道哪些測試需要執行
- 測試時間從 5 分鐘增加到 45 分鐘
- 經常因為不相關的測試失敗而阻擋部署

問題 4：部署協調困難
- 多個微服務需要同時更新
- 不知道哪些服務需要重新部署
- API 版本不相容導致生產環境故障
```

**CTO 的要求**：
> 「我們需要一個智能的 Monorepo CI/CD 系統。只構建和測試有變更的專案，自動處理依賴關係，並行執行以提升速度。目標是將 CI 時間降低到 5 分鐘以內，成本降低 70%。」

**你的任務**：
設計並實作高效的 Monorepo CI/CD 管線，包括：
- 智能變更檢測（只構建變更的專案）
- 依賴圖分析（自動檢測 affected packages）
- 並行構建策略（最大化 CI 效率）
- 版本管理（自動化 changelog 和 versioning）
- 協調部署（正確的服務更新順序）

---

## 📦 專案結構

```
monorepo/
├── apps/
│   ├── web-admin/              # 管理後台（React）
│   │   ├── package.json
│   │   ├── src/
│   │   └── tsconfig.json
│   │
│   ├── web-customer/           # 客戶端（React）
│   │   ├── package.json
│   │   └── src/
│   │
│   ├── mobile-app/             # 行動應用（React Native）
│   │   ├── package.json
│   │   └── src/
│   │
│   ├── api-gateway/            # API Gateway（NestJS）
│   │   ├── package.json
│   │   └── src/
│   │
│   ├── user-service/           # 用戶服務（NestJS）
│   │   ├── package.json
│   │   └── src/
│   │
│   ├── payment-service/        # 支付服務（NestJS）
│   │   ├── package.json
│   │   └── src/
│   │
│   ├── notification-service/   # 通知服務（NestJS）
│   │   ├── package.json
│   │   └── src/
│   │
│   └── analytics-service/      # 分析服務（NestJS）
│       ├── package.json
│       └── src/
│
├── packages/
│   ├── ui-components/          # UI 元件庫
│   │   ├── package.json
│   │   ├── src/
│   │   └── README.md
│   │
│   ├── utils/                  # 工具函數
│   │   ├── package.json
│   │   └── src/
│   │
│   ├── types/                  # TypeScript 型別定義
│   │   ├── package.json
│   │   └── src/
│   │
│   ├── constants/              # 常數定義
│   │   ├── package.json
│   │   └── src/
│   │
│   ├── api-client/             # API 客戶端
│   │   ├── package.json
│   │   └── src/
│   │
│   └── test-utils/             # 測試工具
│       ├── package.json
│       └── src/
│
├── tools/
│   ├── scripts/
│   │   ├── affected-check.js   # 變更檢測腳本
│   │   ├── build-order.js      # 構建順序計算
│   │   └── version-bump.js     # 版本管理
│   │
│   └── github-actions/         # 自訂 GitHub Actions
│       ├── affected-apps/
│       └── parallel-build/
│
├── .github/
│   ├── workflows/
│   │   ├── ci.yml              # 主 CI 管線
│   │   ├── deploy.yml          # 部署管線
│   │   └── release.yml         # 發布管線
│   │
│   └── actions/
│
├── package.json                 # Root package.json
├── pnpm-workspace.yaml         # PNPM workspace 配置
├── turbo.json                  # Turborepo 配置
├── nx.json                     # Nx 配置（可選）
└── README.md
```

---

## 🎬 情境展開

### 階段 1：變更檢測與依賴圖分析（30 分鐘）

**任務**：實現智能變更檢測，只構建受影響的專案。

#### 1. Turbo repo 配置（`turbo.json`）

```json
{
  "$schema": "https://turbo.build/schema.json",
  "pipeline": {
    "build": {
      "dependsOn": ["^build"],
      "outputs": ["dist/**", ".next/**"]
    },
    "test": {
      "dependsOn": ["build"],
      "outputs": ["coverage/**"]
    },
    "lint": {
      "outputs": []
    },
    "type-check": {
      "outputs": []
    },
    "deploy": {
      "dependsOn": ["build", "test"],
      "outputs": []
    }
  },
  "globalDependencies": [".env", "tsconfig.json"]
}
```

#### 2. 變更檢測腳本（`tools/scripts/affected-check.js`）

```javascript
#!/usr/bin/env node
/**
 * 檢測受影響的專案
 * 基於 git diff 和依賴圖分析
 */
const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

function getChangedFiles(base = 'origin/main') {
  const output = execSync(`git diff --name-only ${base}...HEAD`, {
    encoding: 'utf-8'
  });
  return output.trim().split('\n').filter(Boolean);
}

function getPackageDependencies(packagePath) {
  const pkgJson = JSON.parse(
    fs.readFileSync(path.join(packagePath, 'package.json'), 'utf-8')
  );

  const deps = {
    ...pkgJson.dependencies,
    ...pkgJson.devDependencies
  };

  // 只返回 monorepo 內部的依賴
  return Object.keys(deps).filter(dep => dep.startsWith('@company/'));
}

function buildDependencyGraph() {
  const graph = new Map();

  // 掃描所有 apps 和 packages
  const workspaces = [
    ...fs.readdirSync('apps').map(dir => `apps/${dir}`),
    ...fs.readdirSync('packages').map(dir => `packages/${dir}`)
  ];

  for (const workspace of workspaces) {
    const pkgPath = path.join(process.cwd(), workspace);
    if (!fs.existsSync(path.join(pkgPath, 'package.json'))) continue;

    const deps = getPackageDependencies(pkgPath);
    graph.set(workspace, deps);
  }

  return graph;
}

function getAffectedProjects(changedFiles) {
  const graph = buildDependencyGraph();
  const affected = new Set();

  // 1. 直接修改的專案
  for (const file of changedFiles) {
    const [type, project] = file.split('/');
    if ((type === 'apps' || type === 'packages') && project) {
      affected.add(`${type}/${project}`);
    }
  }

  // 2. 依賴受影響專案的其他專案
  let previousSize = 0;
  while (affected.size !== previousSize) {
    previousSize = affected.size;

    for (const [project, deps] of graph.entries()) {
      for (const dep of deps) {
        const depProject = dep.replace('@company/', 'packages/');
        if (affected.has(depProject)) {
          affected.add(project);
        }
      }
    }
  }

  return Array.from(affected);
}

function main() {
  const changedFiles = getChangedFiles();

  if (changedFiles.length === 0) {
    console.log('No changes detected');
    process.exit(0);
  }

  console.log(`Changed files (${changedFiles.length}):`);
  changedFiles.forEach(file => console.log(`  - ${file}`));

  const affectedProjects = getAffectedProjects(changedFiles);

  console.log(`\nAffected projects (${affectedProjects.length}):`);
  affectedProjects.forEach(proj => console.log(`  - ${proj}`));

  // 輸出為 JSON 供 GitHub Actions 使用
  const output = {
    apps: affectedProjects.filter(p => p.startsWith('apps/')),
    packages: affectedProjects.filter(p => p.startsWith('packages/'))
  };

  fs.writeFileSync(
    'affected-projects.json',
    JSON.stringify(output, null, 2)
  );

  console.log('\nOutput written to affected-projects.json');
}

main();
```

#### 3. CI Workflow 整合（`.github/workflows/ci.yml`）

```yaml
name: Monorepo CI

on:
  push:
    branches: ['**']
  pull_request:
    branches: [main]

jobs:
  # Job 1: 檢測變更
  detect-changes:
    runs-on: ubuntu-latest
    outputs:
      apps: ${{ steps.affected.outputs.apps }}
      packages: ${{ steps.affected.outputs.packages }}
      has_changes: ${{ steps.affected.outputs.has_changes }}

    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0  # 需要完整歷史記錄進行 diff

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'

      - name: Install pnpm
        uses: pnpm/action-setup@v2
        with:
          version: 8

      - name: Detect affected projects
        id: affected
        run: |
          node tools/scripts/affected-check.js

          if [ -f affected-projects.json ]; then
            APPS=$(jq -c '.apps' affected-projects.json)
            PACKAGES=$(jq -c '.packages' affected-projects.json)

            echo "apps=$APPS" >> $GITHUB_OUTPUT
            echo "packages=$PACKAGES" >> $GITHUB_OUTPUT
            echo "has_changes=true" >> $GITHUB_OUTPUT
          else
            echo "has_changes=false" >> $GITHUB_OUTPUT
          fi

      - name: Upload affected projects
        uses: actions/upload-artifact@v3
        with:
          name: affected-projects
          path: affected-projects.json

  # Job 2: 構建共享套件（並行）
  build-packages:
    needs: detect-changes
    if: needs.detect-changes.outputs.has_changes == 'true'
    runs-on: ubuntu-latest

    strategy:
      matrix:
        package: ${{ fromJson(needs.detect-changes.outputs.packages) }}

    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'pnpm'

      - name: Install dependencies
        run: pnpm install --frozen-lockfile

      - name: Build package
        run: pnpm --filter "./${{ matrix.package }}" build

      - name: Test package
        run: pnpm --filter "./${{ matrix.package }}" test

      - name: Upload build artifacts
        uses: actions/upload-artifact@v3
        with:
          name: ${{ matrix.package }}-dist
          path: ${{ matrix.package }}/dist

  # Job 3: 構建應用（依賴 packages）
  build-apps:
    needs: [detect-changes, build-packages]
    if: needs.detect-changes.outputs.has_changes == 'true'
    runs-on: ubuntu-latest

    strategy:
      matrix:
        app: ${{ fromJson(needs.detect-changes.outputs.apps) }}

    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'pnpm'

      - name: Download package artifacts
        uses: actions/download-artifact@v3
        with:
          path: artifacts

      - name: Install dependencies
        run: pnpm install --frozen-lockfile

      - name: Build app
        run: pnpm --filter "./${{ matrix.app }}" build

      - name: Test app
        run: pnpm --filter "./${{ matrix.app }}" test

      - name: Lint app
        run: pnpm --filter "./${{ matrix.app }}" lint

      - name: Type check
        run: pnpm --filter "./${{ matrix.app }}" type-check
```

**檢查點 1**：
- [ ] 變更檢測腳本能正確識別受影響專案
- [ ] 依賴圖分析正確
- [ ] 只有受影響的專案被構建和測試
- [ ] CI 時間顯著減少（> 70%）

---

### 階段 2：並行構建優化（25 分鐘）

**任務**：使用 Turborepo 實現最大化並行構建。

#### 1. Turborepo 進階配置（`turbo.json`）

```json
{
  "$schema": "https://turbo.build/schema.json",
  "globalDependencies": [".env", "tsconfig.json"],
  "pipeline": {
    "build": {
      "dependsOn": ["^build"],
      "outputs": ["dist/**", ".next/**", "build/**"],
      "cache": true
    },
    "test": {
      "dependsOn": ["build"],
      "outputs": ["coverage/**"],
      "cache": true
    },
    "lint": {
      "cache": true,
      "outputs": []
    },
    "type-check": {
      "cache": true,
      "outputs": []
    },
    "deploy": {
      "dependsOn": ["build", "test", "lint"],
      "cache": false
    }
  },
  "remoteCache": {
    "enabled": true
  }
}
```

#### 2. GitHub Actions 遠端快取配置

```yaml
# .github/workflows/ci.yml（優化版）
name: Monorepo CI (Optimized)

on:
  push:
    branches: ['**']
  pull_request:
    branches: [main]

jobs:
  ci:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'

      - name: Install pnpm
        uses: pnpm/action-setup@v2
        with:
          version: 8

      - name: Get pnpm store directory
        id: pnpm-cache
        run: echo "pnpm_cache_dir=$(pnpm store path)" >> $GITHUB_OUTPUT

      - name: Setup pnpm cache
        uses: actions/cache@v3
        with:
          path: ${{ steps.pnpm-cache.outputs.pnpm_cache_dir }}
          key: ${{ runner.os }}-pnpm-store-${{ hashFiles('**/pnpm-lock.yaml') }}
          restore-keys: |
            ${{ runner.os }}-pnpm-store-

      - name: Install dependencies
        run: pnpm install --frozen-lockfile

      - name: Setup Turborepo cache
        uses: actions/cache@v3
        with:
          path: .turbo
          key: ${{ runner.os }}-turbo-${{ github.sha }}
          restore-keys: |
            ${{ runner.os }}-turbo-

      - name: Build all affected projects
        run: |
          pnpm turbo run build \
            --filter="...[origin/main]" \
            --cache-dir=.turbo

      - name: Test all affected projects
        run: |
          pnpm turbo run test \
            --filter="...[origin/main]" \
            --cache-dir=.turbo

      - name: Lint all affected projects
        run: |
          pnpm turbo run lint \
            --filter="...[origin/main]" \
            --cache-dir=.turbo

      - name: Generate build report
        run: |
          pnpm turbo run build --dry-run=json > turbo-summary.json

      - name: Upload turbo summary
        uses: actions/upload-artifact@v3
        with:
          name: turbo-summary
          path: turbo-summary.json

      - name: Comment PR with build stats
        if: github.event_name == 'pull_request'
        uses: actions/github-script@v6
        with:
          script: |
            const fs = require('fs');
            const summary = JSON.parse(fs.readFileSync('turbo-summary.json', 'utf8'));

            const taskCount = summary.tasks.length;
            const cachedCount = summary.tasks.filter(t => t.cache?.status === 'HIT').length;
            const cacheHitRate = ((cachedCount / taskCount) * 100).toFixed(1);

            const comment = `## 🚀 Turborepo Build Summary

            - **Total tasks**: ${taskCount}
            - **Cached tasks**: ${cachedCount}
            - **Cache hit rate**: ${cacheHitRate}%
            - **Total time saved**: ${summary.timeSaved || 'N/A'}

            ### Task Execution
            ${summary.tasks.map(t => `- ${t.taskId}: ${t.execution.duration}ms`).join('\n')}
            `;

            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: comment
            });
```

#### 3. 構建效能監控（`tools/scripts/analyze-build-time.js`）

```javascript
#!/usr/bin/env node
/**
 * 分析構建時間並生成報告
 */
const fs = require('fs');

function analyzeBuildPerformance() {
  const summary = JSON.parse(fs.readFileSync('turbo-summary.json', 'utf8'));

  const stats = {
    totalTasks: summary.tasks.length,
    cachedTasks: summary.tasks.filter(t => t.cache?.status === 'HIT').length,
    executedTasks: summary.tasks.filter(t => t.execution).length,
    totalTime: summary.tasks.reduce((sum, t) => sum + (t.execution?.duration || 0), 0),
    slowestTasks: summary.tasks
      .filter(t => t.execution)
      .sort((a, b) => b.execution.duration - a.execution.duration)
      .slice(0, 10)
      .map(t => ({
        task: t.taskId,
        duration: `${(t.execution.duration / 1000).toFixed(2)}s`
      }))
  };

  console.log('📊 Build Performance Analysis');
  console.log('============================');
  console.log(`Total Tasks: ${stats.totalTasks}`);
  console.log(`Cached: ${stats.cachedTasks} (${((stats.cachedTasks / stats.totalTasks) * 100).toFixed(1)}%)`);
  console.log(`Executed: ${stats.executedTasks}`);
  console.log(`Total Time: ${(stats.totalTime / 1000).toFixed(2)}s`);
  console.log('\n🐌 Slowest Tasks:');
  stats.slowestTasks.forEach((t, i) => {
    console.log(`${i + 1}. ${t.task}: ${t.duration}`);
  });

  return stats;
}

analyzeBuildPerformance();
```

**檢查點 2**：
- [ ] Turborepo 快取正常運作
- [ ] 快取命中率 > 80%（第二次構建）
- [ ] 並行執行多個任務
- [ ] 構建時間 < 5 分鐘

---

### 階段 3：版本管理與發布（20 分鐘）

**任務**：自動化版本管理和 changelog 生成。

#### 1. Changesets 配置（`.changeset/config.json`）

```json
{
  "$schema": "https://unpkg.com/@changesets/config@2.3.0/schema.json",
  "changelog": "@changesets/cli/changelog",
  "commit": false,
  "fixed": [],
  "linked": [],
  "access": "public",
  "baseBranch": "main",
  "updateInternalDependencies": "patch",
  "ignore": ["@company/test-utils"]
}
```

#### 2. 發布 Workflow（`.github/workflows/release.yml`）

```yaml
name: Release

on:
  push:
    branches: [main]

concurrency: ${{ github.workflow }}-${{ github.ref }}

jobs:
  release:
    name: Release
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'

      - name: Install pnpm
        uses: pnpm/action-setup@v2
        with:
          version: 8

      - name: Install dependencies
        run: pnpm install --frozen-lockfile

      - name: Build all packages
        run: pnpm turbo run build

      - name: Create Release Pull Request or Publish
        id: changesets
        uses: changesets/action@v1
        with:
          publish: pnpm changeset publish
          version: pnpm changeset version
          commit: 'chore: version packages'
          title: 'chore: version packages'
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          NPM_TOKEN: ${{ secrets.NPM_TOKEN }}

      - name: Send Slack notification
        if: steps.changesets.outputs.published == 'true'
        uses: 8398a7/action-slack@v3
        with:
          status: custom
          custom_payload: |
            {
              text: `🎉 New version published!`,
              attachments: [{
                color: 'good',
                fields: [
                  {
                    title: 'Packages',
                    value: '${{ steps.changesets.outputs.publishedPackages }}',
                    short: false
                  }
                ]
              }]
            }
        env:
          SLACK_WEBHOOK_URL: ${{ secrets.SLACK_WEBHOOK }}
```

**檢查點 3**：
- [ ] Changesets 正確配置
- [ ] 版本自動更新
- [ ] Changelog 自動生成
- [ ] 發布通知發送成功

---

### 階段 4：協調部署（25 分鐘）

**任務**：根據依賴關係協調多個服務的部署順序。

#### 1. 部署順序計算（`tools/scripts/build-order.js`）

```javascript
#!/usr/bin/env node
/**
 * 計算服務部署順序
 * 基於依賴圖進行拓撲排序
 */
const fs = require('fs');

function topologicalSort(graph) {
  const visited = new Set();
  const result = [];

  function visit(node) {
    if (visited.has(node)) return;
    visited.add(node);

    const deps = graph.get(node) || [];
    for (const dep of deps) {
      visit(dep);
    }

    result.push(node);
  }

  for (const node of graph.keys()) {
    visit(node);
  }

  return result;
}

function getDeploymentOrder() {
  const affected = JSON.parse(
    fs.readFileSync('affected-projects.json', 'utf8')
  );

  // 構建依賴圖（這裡簡化處理）
  const graph = new Map([
    ['apps/user-service', []],
    ['apps/payment-service', ['apps/user-service']],
    ['apps/notification-service', ['apps/user-service']],
    ['apps/api-gateway', ['apps/user-service', 'apps/payment-service']],
    ['apps/web-admin', ['apps/api-gateway']],
    ['apps/web-customer', ['apps/api-gateway']]
  ]);

  const affectedApps = affected.apps.filter(app => graph.has(app));
  const order = topologicalSort(graph).filter(app => affectedApps.includes(app));

  console.log('🚀 Deployment Order:');
  order.forEach((app, index) => {
    console.log(`${index + 1}. ${app}`);
  });

  return order;
}

getDeploymentOrder();
```

#### 2. 協調部署 Workflow（`.github/workflows/deploy.yml`）

```yaml
name: Deploy

on:
  workflow_dispatch:
    inputs:
      environment:
        description: 'Environment'
        required: true
        type: choice
        options:
          - staging
          - production

jobs:
  detect-affected:
    runs-on: ubuntu-latest
    outputs:
      deployment_order: ${{ steps.order.outputs.deployment_order }}

    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Detect affected projects
        run: node tools/scripts/affected-check.js

      - name: Calculate deployment order
        id: order
        run: |
          ORDER=$(node tools/scripts/build-order.js | jq -R -s -c 'split("\n")[:-1]')
          echo "deployment_order=$ORDER" >> $GITHUB_OUTPUT

  deploy-services:
    needs: detect-affected
    runs-on: ubuntu-latest

    strategy:
      matrix:
        service: ${{ fromJson(needs.detect-affected.outputs.deployment_order) }}
      max-parallel: 1  # 按順序部署

    steps:
      - uses: actions/checkout@v4

      - name: Deploy ${{ matrix.service }}
        run: |
          echo "Deploying ${{ matrix.service }} to ${{ inputs.environment }}"
          # 實際部署邏輯

      - name: Health check
        run: |
          # 等待服務健康
          sleep 30
          # 執行健康檢查

      - name: Smoke test
        run: |
          # 執行煙霧測試
```

**檢查點 4**：
- [ ] 部署順序正確計算
- [ ] 按照依賴順序部署
- [ ] 每個服務部署後進行驗證
- [ ] 部署失敗自動停止

---

## 🎯 學習檢查點

完成所有階段後，驗證以下能力：

### 技術能力
- [ ] 實現了智能變更檢測
- [ ] 建立了依賴圖分析系統
- [ ] 配置了並行構建策略
- [ ] 整合了遠端快取
- [ ] 實現了自動版本管理
- [ ] 建立了協調部署機制

### 效能指標
- [ ] CI 時間減少 > 70%
- [ ] 快取命中率 > 80%
- [ ] 構建時間 < 5 分鐘
- [ ] 部署成功率 > 95%

### 成本優化
- [ ] CI 成本降低 > 60%
- [ ] 不必要的構建減少 > 80%

---

## 💡 延伸挑戰

### 挑戰 1：智能測試選擇
- 只執行受影響程式碼的測試
- 使用 Jest 的 `--onlyChanged` 功能
- 進一步減少 CI 時間

### 挑戰 2：增量構建
- 實現真正的增量構建
- 只編譯變更的檔案
- 使用 SWC 或 esbuild 加速

### 挑戰 3：動態並行度
- 根據 CI 機器資源動態調整並行數
- 優化任務排程
- 最大化資源利用率

---

## 📚 參考資源

### 工具
- [Turborepo](https://turbo.build/)
- [Nx](https://nx.dev/)
- [Changesets](https://github.com/changesets/changesets)
- [PNPM Workspace](https://pnpm.io/workspaces)

### 最佳實踐
- [Monorepo Best Practices](https://monorepo.tools/)
- [Google's Monorepo Strategy](https://research.google/pubs/pub45424/)

---

**下一步**：完成這個情境後，你已經掌握了 Monorepo 的完整 CI/CD 策略。接下來可以挑戰 **C06：容器化應用管線** 或 **E01：企業級完整 DevOps 管線**！
