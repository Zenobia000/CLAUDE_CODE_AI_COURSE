# Claude Code 情境驅動學習法：像學 Linux 一樣掌握 AI 編程

## 🎯 學習哲學：從「背指令」到「解決問題」

### Linux 學習者的痛點與啟示

**初學者的錯誤學習方式**：
```bash
# 死記硬背指令
ls -la    # 列出檔案
cd        # 切換目錄
grep      # 搜尋文字
...
# 結果：記不住，不會組合，遇到實際問題不知道用什麼
```

**高手的學習方式**：
```bash
# 情境：我要找出所有包含 "error" 的日誌檔案並統計數量

# 思考過程：
# 1. 找檔案 → find
# 2. 找內容 → grep
# 3. 統計 → wc

# 組合使用
find /var/log -name "*.log" -exec grep -l "error" {} \; | wc -l

# 記憶點：透過解決實際問題，自然記住指令組合
```

### Claude Code 的學習困境

**傳統教學方式（❌）**：
```markdown
## 指令清單
- /help - 顯示幫助
- /agents - 管理代理人
- /mcp - MCP 伺服器
- /output-style - 設定輸出風格
- /memory - 編輯記憶
...

學員：看完就忘，不知道什麼時候用什麼
```

**情境驅動教學（✅）**：
```markdown
## 情境1：團隊新人 onboarding

問題：新同事加入，需要快速理解 10 萬行的舊專案

解決路徑：
1. 用 Gemini CLI 載入整個 codebase (@.)
2. 用 /agents:code-analyzer 分析架構
3. 用 /output-style:onboarding-doc 生成新人文檔
4. 用 /memory 記錄關鍵發現

自然記住：
- Gemini CLI 適合大範圍分析
- /agents 可以切換專門任務
- /output-style 控制文檔格式
- /memory 累積知識
```

---

## 📖 情境金字塔：漸進式難度設計

### Level 1：單一情境（理解單個指令）

**目標**：建立指令與場景的直接連結

#### 情境 1.1：混亂的專案資料夾需要整理

**背景**：
```
downloads/
├── report_final.pdf
├── report_final_v2.pdf
├── report_FINAL.pdf
├── code.py
├── test.py
├── random_notes.txt
├── meeting_2024.mp3
└── [50 個類似的混亂檔案...]
```

**需求**：按類型分類並移除重複檔案

**第一反應（新手）**：
"我該用什麼指令？`/help` 嗎？"

**引導思考**：
1. **這是什麼類型的任務？** → 檔案操作
2. **Claude 能直接操作檔案嗎？** → 能（透過 Bash 工具）
3. **我需要 Claude 做什麼？** → 分析 → 規劃 → 執行

**解決過程**：

```bash
# Step 1：進入 Claude Code
claude

# Step 2：描述問題（不需要知道指令）
提示詞：
請整理 ./downloads 資料夾：
1. 按檔案類型分類（pdf/py/txt/mp3等）
2. 找出重複檔案（檔名相似或內容相同）
3. 給我整理建議，等我確認後執行

# Claude 的回應：
我會這樣做：

[分析階段]
正在掃描 ./downloads...
發現：
- 15 個 PDF 檔案（3 組疑似重複）
- 8 個 Python 檔案
- 22 個文字檔案
- 5 個音訊檔案

[規劃階段]
建議的資料夾結構：
downloads/
├── documents/
│   └── reports/
│       ├── report_final_v2.pdf  ← 最新版本
│       └── [保留這個，刪除其他2個]
├── code/
│   ├── code.py
│   └── test.py
├── notes/
└── audio/

是否執行？(y/n)

# 你輸入 y 後執行...
```

**學到的指令（自然記憶）**：
- ✅ 不需要記指令，只需描述問題
- ✅ Claude 會主動規劃並等待確認
- ✅ `/clear` 可以重置對話（如果需要重新開始）

---

#### 情境 1.2：快速理解陌生專案

**背景**：
你剛接手一個 React 專案，完全不熟悉程式碼結構

**檔案結構**：
```
react-app/
├── src/
│   ├── components/  [50 個元件]
│   ├── hooks/       [20 個自訂 hooks]
│   ├── pages/       [15 個頁面]
│   ├── utils/
│   └── api/
├── package.json
└── [其他設定檔...]
```

**需求**：30 分鐘內掌握專案架構

**錯誤做法**：
```bash
# 開始一個個檔案看...
cat src/components/Header.jsx
cat src/components/Footer.jsx
...
# 看了 1 小時還是一頭霧水
```

**正確做法（使用 Claude Code）**：

```bash
# Step 1：載入專案上下文
claude --add-dir ./react-app/src

# Step 2：用 /context 檢查已載入的內容
claude /context

# 輸出：
上下文使用情況：
├─ 程式碼檔案：85,000 tokens (42.5%)
├─ 專案記憶：0 tokens (0%)
└─ 總計：85,000 / 200,000 tokens

# Step 3：快速理解
提示詞：
請分析這個 React 專案，告訴我：
1. 專案的主要功能是什麼？
2. 核心元件有哪些？它們的職責是什麼？
3. 資料流向如何？（Props/Context/Redux?）
4. 有哪些外部 API 整合？
5. 如果我要添加一個新頁面，應該修改哪些檔案？

給我一個結構化的 onboarding 文檔。

# Claude 自動分析並生成：
# 1. 專案概述
# 2. 架構圖（文字版）
# 3. 核心元件導覽
# 4. 開發指南
```

**遇到問題：上下文太大怎麼辦？**

```bash
# 發現 /context 顯示 95% 已使用

# 學習新指令：/compact
claude /compact

# 壓縮後：
上下文使用情況：
├─ 對話歷史：15,000 tokens (7.5%)  ← 壓縮了！
├─ 程式碼檔案：85,000 tokens (42.5%)
└─ 總計：100,000 / 200,000 tokens

# 記憶點：
# /compact 就像 Linux 的 tar -czf，壓縮內容但保留重點
```

**學到的指令組合（自然記憶）**：
- ✅ `--add-dir` 載入專案目錄
- ✅ `/context` 檢查上下文使用量（就像 `df -h` 檢查硬碟）
- ✅ `/compact` 壓縮上下文（就像清理快取）

---

### Level 2：組合情境（多指令協同）

**目標**：理解指令之間的協作關係

#### 情境 2.1：為開源專案貢獻 - 完整流程

**背景**：
你想為一個 Python 開源專案貢獻程式碼，但：
- 不熟悉專案結構
- 不知道編碼規範
- 需要寫測試
- 需要通過 CI/CD

**完整流程（會用到 7+ 個指令）**：

```bash
# ===== 階段 1：專案理解 =====

# Step 1：初始化 Claude 專案記憶
cd /path/to/opensource-project
claude /init

# 生成 CLAUDE.md 模板

# Step 2：載入專案並分析
claude --add-dir ./src --add-dir ./tests

提示詞：
請幫我理解這個專案：
1. 主要功能
2. 目錄結構
3. 依賴關係

然後將關鍵資訊寫入 CLAUDE.md

# Claude 分析後自動更新 CLAUDE.md：
# - 技術棧：Python 3.10, FastAPI, PostgreSQL
# - 架構原則：Clean Architecture, DDD
# - 編碼規範：Black, mypy, pytest


# ===== 階段 2：發現可貢獻的 Issue =====

# Step 3：使用 GitHub MCP（如果已配置）
claude /mcp

# 查看 MCP 狀態，確認 GitHub MCP 已連接

提示詞：
使用 GitHub MCP 列出這個專案的 "good first issue"

# 假設選擇了 Issue #123：添加用戶頭像上傳功能


# ===== 階段 3：開發新功能（TDD 方式） =====

# Step 4：使用 code-reviewer agent 先審查現有程式碼風格
claude /agents:code-reviewer

提示詞：
請分析 src/users/ 下的程式碼風格，包括：
- 命名規範
- 檔案組織方式
- 測試寫法

# Claude 分析並記錄風格要點...

# Step 5：切換到 test-generator agent
claude /agents:test-generator

提示詞：
根據 Issue #123 的需求，先生成測試案例：
功能：用戶頭像上傳
- 支援 JPG, PNG
- 最大 5MB
- 自動調整為 200x200
- 儲存到 S3

請使用專案現有的測試風格。

# Claude 生成 test_avatar_upload.py（紅燈階段）


# ===== 階段 4：實作功能 =====

# Step 6：切換回一般模式，實作功能
claude /agents:off  # 關閉 agent 模式

提示詞：
現在請實作頭像上傳功能，讓剛才的測試通過（綠燈）。
遵循 CLAUDE.md 中記錄的編碼規範。

# Claude 生成實作程式碼...


# ===== 階段 5：程式碼審查 =====

# Step 7：自我審查
claude /review src/users/avatar_upload.py

# Claude 進行程式碼審查，提出改進建議

# Step 8：安全審查
claude /security-review src/users/avatar_upload.py

# 發現潛在的檔案上傳漏洞，Claude 提供修復方案


# ===== 階段 6：文檔更新 =====

# Step 9：使用自訂輸出風格生成 API 文檔
claude /output-style:api-documentation

提示詞：
為新增的頭像上傳 API 生成文檔，格式要符合專案現有的 API 文檔風格。

# Claude 生成並添加到 docs/api.md


# ===== 階段 7：提交 PR =====

# Step 10：讓 Claude 幫忙寫 commit message 和 PR 描述
提示詞：
請根據以下變更，生成：
1. Git commit message（遵循 Conventional Commits）
2. Pull Request 描述

變更內容：
- 添加用戶頭像上傳功能
- 包含完整測試
- 更新 API 文檔

# Claude 生成：
# Commit: feat(users): add avatar upload functionality (#123)
# PR 描述：包含變更摘要、測試覆蓋、截圖等


# ===== 階段 8：保存專案知識 =====

# Step 11：更新專案記憶
claude /memory

# 手動添加：
## 常見問題
### 問題：頭像上傳失敗
解決方案：檢查 S3 權限配置...
```

**這個情境中學到的指令組合（有機記憶）**：

| 指令 | 場景關聯 | 記憶技巧 |
|------|---------|---------|
| `/init` | 開始新專案 | 就像 `git init` |
| `--add-dir` | 載入程式碼 | 就像 `source` 載入設定 |
| `/mcp` | 整合外部工具 | 就像 `apt install` 安裝套件 |
| `/agents:xxx` | 切換專家模式 | 就像 `su` 切換使用者 |
| `/review` | 程式碼審查 | 就像 `lint` 檢查 |
| `/security-review` | 安全掃描 | 就像 `nmap` 掃描漏洞 |
| `/output-style` | 格式化輸出 | 就像 `jq` 格式化 JSON |
| `/memory` | 保存知識 | 就像 `.bashrc` 保存設定 |

**關鍵頓悟時刻**：
> "原來這些指令不是孤立的！就像 Linux 的管道（pipe），
> Claude Code 的指令也可以串成完整的工作流程！"

---

#### 情境 2.2：救火任務 - 生產環境出錯

**背景**：
週五晚上 8 點，生產環境突然大量錯誤，你需要：
1. 快速定位問題
2. 找出錯誤原因
3. 提供修復方案
4. 寫事後報告

**時間壓力下的指令組合**：

```bash
# T+0 分鐘：收到告警

# 快速啟動 Claude，載入相關程式碼
claude --add-dir ./src/payment

提示詞：
緊急！生產環境報錯：
```
PaymentProcessingError: Transaction timeout after 30s
Frequency: 500+ errors/min
Started: 2025-01-15 20:00 UTC
```

請幫我：
1. 分析可能的原因（基於已載入的 payment 模組）
2. 檢查最近的程式碼變更
3. 提供臨時緩解方案
4. 提供根本修復方案

# T+2 分鐘：Claude 分析

Claude 回應：
[緊急分析]
可能原因：
1. 資料庫連線池耗盡（最可能）
2. 第三方支付 API 超時
3. Redis 快取失效

[最近變更]
檢測到 PR #456 在 19:45 部署：
- 修改了資料庫查詢邏輯
- 未添加連線池超時設定

[臨時緩解]
立即執行：
1. 增加連線池大小到 50
2. 添加斷路器（Circuit Breaker）

[根本修復]
需要添加：
1. 連線池超時設定
2. 資料庫查詢優化
3. 監控告警


# T+5 分鐘：使用 /bashes 平行執行多個任務

# 終端 1：監控日誌
claude /bashes

提示詞：
請在背景執行：
tail -f /var/log/payment.log | grep "timeout"

# 終端 2：檢查資料庫連線
提示詞：
執行：
psql -c "SELECT count(*) FROM pg_stat_activity WHERE state = 'active';"


# T+10 分鐘：生成修復腳本

提示詞：
基於分析結果，生成：
1. 緊急修復的配置檔（增加連線池）
2. 資料庫查詢優化的 SQL
3. 部署腳本

# Claude 生成修復方案...


# T+30 分鐘：問題解決，寫事後報告

# 使用 /output-style 生成正式報告
claude /output-style:incident-report

提示詞：
請生成完整的事後報告（Post-mortem），包括：
- 時間線
- 根本原因分析（5 Whys）
- 影響範圍
- 緩解措施
- 預防措施
- 行動項目

基於今晚的緊急處理過程。

# Claude 生成專業的事後報告...


# T+45 分鐘：更新專案記憶，避免下次再犯

claude /memory

# 添加到 CLAUDE.md：
## 常見問題
### 問題：支付交易超時
根本原因：資料庫連線池設定不當
預防措施：
- 所有資料庫操作添加超時設定
- 連線池大小依據負載測試調整
- 部署前進行負載測試

相關 PR：#456
事後報告：docs/incidents/2025-01-15-payment-timeout.md
```

**救火過程中學到的指令（壓力記憶）**：

| 指令 | 救火用途 | 為什麼記得住 |
|------|---------|-------------|
| `--add-dir` | 快速載入相關程式碼 | 救火第一步 |
| `/bashes` | 平行執行多個監控任務 | 就像同時開多個終端 |
| `/output-style` | 生成正式報告 | 事後必須交報告 |
| `/memory` | 記錄教訓 | 絕不想再踩同樣的坑 |

**記憶點**：
> "就像 Linux 救火時會用 `top` + `netstat` + `tail -f log`，
> Claude Code 也可以同時執行多個任務！"

---

### Level 3：複雜情境（工作流程編排）

**目標**：設計自己的自動化工作流程

#### 情境 3.1：技術部落格自動化系統

**需求**：
從寫程式碼到發布部落格文章的完整自動化

**情境拆解**：

```bash
# ===== 週一：開發新功能 =====

# 你實作了一個很酷的功能：Redis 快取裝飾器

# 1. 先用 TDD 方式完成開發（使用之前學的流程）

# 2. 開發完成後，想分享到部落格

提示詞：
我剛完成了一個 Redis 快取裝飾器的實作，
請幫我執行以下自動化流程：

[分析階段]
1. 分析 src/cache/redis_decorator.py 的程式碼
2. 提取核心概念和亮點

[內容創作階段]
3. 使用 tech-blogger agent
4. 使用 blog-article 輸出風格
5. 生成一篇技術部落格文章，包含：
   - 引言（為什麼需要這個功能）
   - 技術實作解析
   - 完整程式碼範例
   - 使用場景
   - 效能測試結果
   - 結論

[SEO 優化階段]
6. 生成 SEO 友好的：
   - 標題（3 個候選）
   - Meta 描述
   - 標籤

[多平台發布階段]
7. 使用 Medium MCP 發布到 Medium
8. 使用 DevTo MCP 發布到 Dev.to
9. 使用 Twitter MCP 發推文宣傳

[記錄階段]
10. 將文章資訊記錄到 CLAUDE.md 的「已發布文章」區塊

請開始執行。
```

**Claude 的執行（自動編排）**：

```
[步驟 1-2：分析程式碼]
✓ 已分析 redis_decorator.py
✓ 核心亮點：支援動態 TTL、自動序列化、錯誤處理

[步驟 3-5：生成文章]
✓ 切換到 tech-blogger agent
✓ 應用 blog-article 輸出風格
✓ 文章已生成（1800 字）

預覽前 200 字：
---
# Redis 快取裝飾器：讓你的 API 快 10 倍的秘密武器

還記得上次你的 API 因為資料庫查詢太慢被老闆罵嗎？
今天分享一個簡單但超實用的解決方案...
---

是否繼續？(y/n)

# 你輸入 y

[步驟 6：SEO 優化]
標題候選：
1. "Redis 快取裝飾器：讓你的 Python API 快 10 倍"
2. "從 0 到 1 實作生產級 Redis 快取裝飾器"
3. "Python Redis 快取最佳實踐：裝飾器模式深入解析"

請選擇（1-3）或自訂：

# 你選擇 1

[步驟 7-9：多平台發布]
✓ Medium 文章已發布：https://medium.com/@you/...
✓ Dev.to 文章已發布：https://dev.to/you/...
✓ 推文已發送：https://twitter.com/you/status/...

[步驟 10：記錄]
✓ 已更新 CLAUDE.md

[完成摘要]
- 文章字數：1800
- 程式碼範例：3 個
- 圖表：1 個（架構圖）
- 發布平台：Medium, Dev.to, Twitter
- 預估閱讀時間：8 分鐘
```

**學到的進階概念**：

1. **工作流程編排（Workflow Orchestration）**
   - 一次提示詞串聯 10 個步驟
   - 每個步驟自動執行
   - 中間可以人工確認

2. **Agent 自動切換**
   - Claude 自動判斷何時切換 agent
   - 不需要手動執行 `/agents:xxx`

3. **MCP 整合**
   - 一次整合多個平台
   - 自動化發布流程

**記憶技巧**：
> "就像 Linux 的 cron job + shell script，
> 可以把常用的流程自動化！"

---

## 🎓 學習路徑設計：漸進式挑戰

### 第1週：基礎情境（熟悉環境）

**每日一情境**：

| 天 | 情境 | 學習目標 | 核心指令 |
|----|------|---------|---------|
| 1 | 整理混亂的資料夾 | 基本操作 | 無（只用自然語言） |
| 2 | 快速理解新專案 | 上下文管理 | `--add-dir`, `/context` |
| 3 | 生成專案文檔 | 輸出控制 | `/output-style` |
| 4 | 批量重命名檔案 | Bash 整合 | `/bashes` |
| 5 | 為程式碼添加註解 | 程式碼理解 | 基本提示詞 |
| 6 | 整合測試 | 整合挑戰 | 前 5 天的組合 |
| 7 | 複習與總結 | 知識固化 | `/memory` |

**評量方式**：
- 不是「你記得指令嗎？」
- 而是「給你一個新情境，你能解決嗎？」

---

### 第2週：組合情境（建立連結）

**每日情境題**：

```markdown
## 情境題 2.1：開源貢獻完整流程
時間：2 小時
目標：從理解專案到提交 PR

檢查點：
□ 已載入專案並理解架構
□ 已找到並選擇 Issue
□ 已寫測試（紅燈）
□ 已實作功能（綠燈）
□ 已通過程式碼審查
□ 已更新文檔
□ 已提交 PR

你會用到的指令（不提前告訴，讓學員自己發現）：
- /init, --add-dir, /context
- /agents:xxx
- /review, /security-review
- /output-style
- /memory
```

**學習日誌範本**：

```markdown
# 情境 2.1 學習日誌

## 遇到的問題
1. 問題：上下文太大，超過限制
   解決：使用 /compact 壓縮
   學到：定期壓縮是必要的

2. 問題：不知道專案的編碼規範
   解決：先用 /agents:code-reviewer 分析現有程式碼
   學到：agent 可以學習專案風格

## 指令使用記錄
```bash
/init              # 初始化專案
--add-dir ./src    # 載入程式碼
/compact           # 壓縮上下文
/agents:code-reviewer  # 分析風格
/review            # 自我審查
```

## 頓悟時刻
原來 /agents 不只是切換模式，更像是「召喚專家」！
```

---

### 第3週：複雜情境（實戰演練）

**專案驅動學習**：

```markdown
## 專案：建立個人知識管理系統

### 需求
1. 從多個來源收集資訊（網頁、PDF、影片）
2. 自動萃取關鍵知識
3. 分類整理
4. 生成筆記
5. 同步到 Notion
6. 定期生成週報

### 你需要掌握的技能
□ MCP 伺服器配置（Notion, Web）
□ 自訂 Agent（knowledge-curator）
□ 自訂輸出風格（note-template）
□ 工作流程編排
□ 排程自動化

### 學習方式
不是：「先學會所有指令再開始」
而是：「遇到問題，查文檔，解決，記錄」

就像學 Linux：
- 遇到檔案權限問題 → 查 chmod
- 遇到進程管理問題 → 查 ps, kill
- 遇到網路問題 → 查 netstat, curl
```

---

## 📚 記憶卡系統：Anki 式複習

### 情境卡片範本

**正面（情境）**：
```
情境：生產環境突然大量 500 錯誤

需要：
1. 快速查看最近的部署
2. 檢查日誌檔案
3. 找出錯誤的程式碼行
4. 生成事後報告

你會用到哪些 Claude Code 功能？
```

**背面（解決方案）**：
```bash
# 方案

1. 查看 Git 歷史
提示詞：請列出最近 24 小時的 git commits

2. 平行監控日誌
claude /bashes
提示詞：tail -f /var/log/app.log | grep "ERROR"

3. 快速定位錯誤程式碼
提示詞：根據錯誤堆疊，找出對應的程式碼並解釋問題

4. 生成報告
claude /output-style:incident-report

關鍵：不需要記指令名稱，記住「解決問題的思路」
```

---

## 🎯 評量方式：實戰考核

### 不是這樣考：
```
問：/agents 指令的作用是什麼？
答：管理 AI 代理人
```

### 而是這樣考：
```
情境：
你的團隊需要建立統一的程式碼審查流程。
要求：
1. 所有 PR 必須經過安全掃描
2. 程式碼風格必須符合團隊規範
3. 必須有測試覆蓋
4. 生成審查報告

請設計並實作這個流程。

評分標準：
□ 能識別需要哪些 agents (30%)
□ 正確配置 output-style (20%)
□ 整合 CI/CD (20%)
□ 流程完整性 (30%)
```

---

## 💡 學習訣竅總結

### Linux 學習法類比

| Linux 概念 | Claude Code 概念 | 記憶連結 |
|-----------|----------------|---------|
| `man` 命令 | `/help` | 查手冊 |
| 管道 `|` | 工作流程編排 | 串聯處理 |
| 別名 `alias` | 自訂 `/command` | 快捷方式 |
| `.bashrc` | `CLAUDE.md` | 持久化設定 |
| 環境變數 | `/memory` | 保存狀態 |
| `cron` | 自動化工作流程 | 定時任務 |
| `sudo` | `/agents` | 切換權限/角色 |

### 記憶三原則

1. **情境第一，指令第二**
   - 不要背「/agents 是什麼」
   - 而要記「需要專家時用 /agents」

2. **問題驅動學習**
   - 遇到問題 → 查文檔 → 解決 → 記錄
   - 不要「預習所有指令」

3. **建立個人知識庫**
   - 用 `/memory` 記錄每次的解決方案
   - 下次遇到類似問題，先查自己的記錄

### 學習檢查清單

**新手階段**：
- □ 能用自然語言描述問題讓 Claude 理解
- □ 知道何時使用 `/context` 檢查狀態
- □ 遇到錯誤會查 `/help`

**進階階段**：
- □ 能組合 2-3 個指令解決複雜問題
- □ 理解不同 agents 的適用場景
- □ 會配置基本的 MCP 整合

**高手階段**：
- □ 能設計完整的自動化工作流程
- □ 創建自訂的 agents 和 output-styles
- □ 將 Claude Code 整合到團隊流程

---

**下一步**：
選擇一個實際問題，用情境驅動學習法解決它！
記住：最好的學習，就是實戰。
