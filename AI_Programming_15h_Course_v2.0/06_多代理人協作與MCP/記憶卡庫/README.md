# 記憶卡庫 - MCP 與多代理人協作

## 📇 記憶卡架構

本記憶卡庫包含 **100+ 張情境式記憶卡**，涵蓋 MCP 配置、多代理人協作、工作流程編排等核心知識。

### 六大類記憶卡

1. **MCP 核心概念**（20 張）
2. **MCP 配置與除錯**（25 張）
3. **Agent 切換策略**（15 張）
4. **工作流程編排**（25 張）
5. **錯誤處理**（10 張）
6. **實戰場景**（15 張）

---

## 🎯 設計理念

### 情境式 > 定義式

**錯誤示範** ❌：
```
Q: 什麼是 MCP？
A: Model Context Protocol，是 AI 與外部系統溝通的協議。
```

**正確示範** ✅：
```
Q: 【情境】你想讓 Claude Code 自動從 GitHub 讀取 issues 並分析，
   而不是每次都手動複製貼上。你應該使用什麼技術？

A: 【解決方案】使用 MCP（Model Context Protocol）

   【步驟】
   1. 配置 GitHub MCP（.claude/mcp-config.json）
   2. 提供 GitHub Token
   3. 重啟 Claude Code
   4. 直接對話：「分析這個 repo 的 issues」

   【關鍵點】
   - MCP 讓 AI 可以主動調用外部 API
   - 像 Linux 的 mount，將外部系統「掛載」到 Claude
   - 一次配置，之後都能使用

   【來源】理論 6.1
```

---

## 📚 Category 1：MCP 核心概念（20 張）

### 卡片 1-1：MCP 的本質

```
Q: 【情境】你的同事問：「MCP 跟普通的 REST API 有什麼不同？
   我為什麼要用 MCP 而不是直接寫 API 調用？」

A: 【五個核心差異】

   1. **主動 vs 被動**
      - REST API：你寫程式碼調用
      - MCP：AI 主動探索調用

   2. **單次 vs 多輪**
      - REST API：調用一次就結束
      - MCP：AI 可以多輪探索

   3. **靜態 vs 動態**
      - REST API：功能預先定義
      - MCP：AI 動態選擇功能

   4. **單一 vs 組合**
      - REST API：需要膠水程式碼整合
      - MCP：原生支援多 MCP 協同

   5. **開發者中心 vs AI 中心**
      - REST API：為開發者設計
      - MCP：為 AI 設計

   【類比】
   REST API = 你是司機，手動開車
   MCP = AI 是司機，自動駕駛

   【來源】理論 6.1
```

### 卡片 1-2：MCP 配置結構

```
Q: 【情境】你需要配置 GitHub MCP，但不知道 .claude/mcp-config.json
   應該怎麼寫。請說明配置檔的基本結構。

A: 【配置檔結構】

   {
     "mcpServers": {
       "server-name": {
         "command": "執行指令",
         "args": ["參數1", "參數2"],
         "env": {
           "環境變數名": "環境變數值"
         }
       }
     }
   }

   【GitHub MCP 範例】
   {
     "mcpServers": {
       "github": {
         "command": "npx",
         "args": ["-y", "@modelcontextprotocol/server-github"],
         "env": {
           "GITHUB_TOKEN": "ghp_xxxx"
         }
       }
     }
   }

   【關鍵點】
   - mcpServers：必須的頂層鍵
   - command：通常是 npx（Node.js）或 python
   - args：MCP server 的套件名稱
   - env：敏感資訊（API keys）

   【來源】理論 6.1
```

### 卡片 1-3：MCP 安全第一原則

```
Q: 【情境】你配置了 GitHub MCP 後，準備上傳到 Git。
   同事提醒你：「等等！你的配置檔有安全問題！」
   請列出 MCP 配置的安全檢查清單。

A: 【安全檢查清單】

   配置前：
   ☐ Token 有設定過期時間嗎？
   ☐ 權限是最小化的嗎？（只給需要的權限）
   ☐ .gitignore 有包含 .claude/mcp-config.json 嗎？
   ☐ 有定期輪換計畫嗎？

   配置中：
   ☐ JSON 格式正確嗎？
   ☐ 環境變數有正確設定嗎？
   ☐ 敏感資訊有遮罩嗎（log 中）？

   配置後：
   ☐ 測試連線成功嗎？
   ☐ Token 有正確的權限嗎？
   ☐ 錯誤日誌有記錄嗎？

   【絕對禁止】
   ❌ 把 token 寫在程式碼裡
   ❌ 上傳 mcp-config.json 到 Git
   ❌ 給超過必要的權限
   ❌ 使用永久 token

   【來源】理論 6.1
```

---

## 📚 Category 2：MCP 配置與除錯（25 張）

### 卡片 2-1：GitHub Token 取得

```
Q: 【情境】你需要配置 GitHub MCP，但不知道如何取得 Personal Access Token。
   請說明完整的步驟。

A: 【取得步驟】

   1. 登入 GitHub
   2. 前往 Settings → Developer settings → Personal access tokens
      → Tokens (classic)
   3. 點擊 "Generate new token"
   4. 選擇 Scopes（權限）：
      - repo：存取 repositories
      - read:user：讀取用戶資訊
      - read:org：讀取組織資訊（如需要）
   5. 設定過期時間（建議 90 天）
   6. 複製 token（只會顯示一次！）

   【權限建議】
   - 只讀：repo:status + public_repo
   - 讀寫 issues：repo + write:issues
   - 完全控制：repo（謹慎使用）

   【安全提醒】
   - Token 以 ghp_ 開頭
   - 立即儲存到密碼管理器
   - 絕不上傳到 Git
   - 定期輪換（90 天）

   【來源】理論 6.1
```

### 卡片 2-2：MCP 連線失敗診斷

```
Q: 【情境】你配置了 GitHub MCP，但 Claude Code 報錯：
   "Unable to connect to MCP server 'github'"
   請說明診斷流程。

A: 【診斷步驟】

   Step 1：檢查 JSON 格式
   ```bash
   cat .claude/mcp-config.json | jq .
   ```
   如果報錯 → JSON 格式有誤（逗號、引號）

   Step 2：檢查 MCP server 是否可執行
   ```bash
   npx -y @modelcontextprotocol/server-github
   ```
   如果失敗 → 網路問題或套件不存在

   Step 3：檢查環境變數
   ```bash
   echo $GITHUB_TOKEN
   ```
   如果空白 → 環境變數未設定

   Step 4：測試 API
   ```bash
   curl -H "Authorization: token $GITHUB_TOKEN" \
        https://api.github.com/user
   ```
   如果 401 → Token 無效
   如果 403 → 權限不足

   Step 5：檢查 Claude Code 日誌
   查看詳細錯誤訊息

   【常見原因】
   1. JSON 格式錯誤（90%）
   2. Token 過期或無效（5%）
   3. 網路連線問題（3%）
   4. MCP server 版本問題（2%）

   【來源】理論 6.1
```

---

## 📚 Category 3：Agent 切換策略（15 張）

### 卡片 3-1：何時應該切換 Agent

```
Q: 【情境】你正在審查一段程式碼，預設 Agent 的建議太籠統。
   請說明何時應該切換 Agent，以及如何判斷切換到哪個 Agent。

A: 【決策樹】

   任務複雜度 < 簡單？
   ├─ 是 → 使用預設 Agent（code-expert）
   └─ 否 → 任務需要專業知識？
       ├─ 安全相關 → security-auditor
       ├─ 效能問題 → performance-optimizer
       ├─ 測試相關 → test-engineer
       ├─ 架構設計 → architect
       ├─ 程式碼審查 → reviewer
       └─ 資料分析 → data-analyst

   【切換指令】
   /agents:security-auditor

   【經驗法則】
   - 簡單任務：不切換（成本 > 收益）
   - 中等任務：視情況切換
   - 複雜任務：一定要切換

   【範例】
   任務：審查登入功能
   ├─ 預設 Agent → "程式碼看起來不錯"
   └─ security-auditor → "發現 3 個安全問題：
                           1. 密碼未加密
                           2. 沒有 rate limiting
                           3. Session 未設定過期"

   【來源】理論 6.2
```

---

## 📚 Category 4：工作流程編排（25 張）

### 卡片 4-1：四種編排模式選擇

```
Q: 【情境】你需要設計一個自動化流程：從 GitHub 讀取 issues，
   從 Database 查詢數據，生成報告，發送到 Slack，儲存到 Notion。
   請選擇合適的編排模式並說明原因。

A: 【分析】

   任務分解：
   1. 從 GitHub 讀取 issues
   2. 從 Database 查詢數據
   3. 生成報告
   4. 發送到 Slack
   5. 儲存到 Notion

   【選擇編排模式】

   階段 1：並行（Parallel）
   ├─ GitHub 讀取
   └─ Database 查詢
   原因：兩個任務獨立，可以同時執行，節省時間

   階段 2：串行（Sequential）
   └─ 生成報告
   原因：需要等待階段 1 的資料

   階段 3：並行（Parallel）
   ├─ 發送到 Slack
   └─ 儲存到 Notion
   原因：兩個任務獨立，可以同時執行

   【時間估算】
   - 全串行：2s + 3s + 2s + 1s + 1s = 9s
   - 混合模式：max(2s,3s) + 2s + max(1s,1s) = 3s + 2s + 1s = 6s
   - 節省：3s（33%）

   【來源】理論 6.2
```

### 卡片 4-2：錯誤處理策略

```
Q: 【情境】你的自動化週報系統中，GitHub MCP 調用失敗（rate limit exceeded）。
   請設計錯誤處理策略。

A: 【錯誤等級分類】

   Level 1：可恢復錯誤
   - Rate limit → 等待重試
   - 網路暫時中斷 → 重試 3 次
   - 資料暫時不可用 → 使用快取

   Level 2：可降級錯誤
   - 非關鍵資料缺失 → 標註並繼續
   - 部分功能失敗 → 使用替代方案
   - 效能問題 → 使用簡化流程

   Level 3：致命錯誤
   - 認證失敗 → 立即停止
   - 所有 MCP 都失敗 → 終止流程
   - 關鍵資料完全缺失 → 無法繼續

   【針對 Rate Limit 的處理】

   Step 1：檢測錯誤
   ```
   Error: GitHub API rate limit exceeded
   ```

   Step 2：等待重試
   ```
   等待 60 秒後重試（rate limit 通常 1 小時重置）
   ```

   Step 3：使用快取
   ```
   如果仍失敗，使用快取的資料
   在週報中標註「使用快取資料」
   ```

   Step 4：通知管理員
   ```
   發送 Slack 通知：
   「週報生成使用快取資料，請檢查 GitHub API quota」
   ```

   【來源】理論 6.2
```

---

## 📚 Category 5：錯誤處理（10 張）

### 卡片 5-1：重試機制設計

```
Q: 【情境】MCP 調用偶爾會因為網路問題失敗。
   請設計一個重試機制。

A: 【重試策略】

   【Exponential Backoff（指數退避）】
   ```
   第 1 次失敗 → 等待 2 秒重試
   第 2 次失敗 → 等待 4 秒重試
   第 3 次失敗 → 等待 8 秒重試
   第 4 次失敗 → 放棄
   ```

   【實作指令】
   ```
   User: "獲取 GitHub issues，如果失敗，重試 3 次，
         每次等待時間加倍（2s, 4s, 8s）"
   ```

   【關鍵點】
   1. 最多重試 3 次（避免無限重試）
   2. 指數退避（避免瞬間大量請求）
   3. 記錄每次重試（便於除錯）
   4. 最後失敗要有降級方案

   【何時應該重試】
   ✓ 網路暫時中斷
   ✓ 服務暫時不可用（503）
   ✓ Rate limit（需要等待更久）

   【何時不應該重試】
   ✗ 認證失敗（401）
   ✗ 權限不足（403）
   ✗ 資源不存在（404）
   ✗ 請求格式錯誤（400）

   【來源】理論 6.2
```

---

## 📚 Category 6：實戰場景（15 張）

### 卡片 6-1：自動化週報系統設計

```
Q: 【情境】你需要設計一個自動化週報系統，每週一早上 9 點自動執行：
   從 GitHub 獲取 issues → 從 Database 查詢指標 → 生成週報 →
   發 Slack → 存 Notion。請設計完整的工作流程。

A: 【系統架構】

   涉及 MCP：
   - GitHub MCP
   - Database MCP
   - Slack MCP
   - Notion MCP

   涉及 Agent：
   - data-analyst（資料分析）
   - tech-writer（報告撰寫）

   【工作流程】

   階段 1：資料獲取（並行）⏱ ~3 分鐘
   ├─ GitHub MCP：獲取本週 issues/PRs
   └─ Database MCP：查詢關鍵指標

   階段 2：報告生成（串行）⏱ ~3 分鐘
   ├─ data-analyst：整合資料並分析
   └─ tech-writer：生成週報文檔

   階段 3：分發（並行）⏱ ~2 分鐘
   ├─ Slack MCP：發送到 #engineering
   └─ Notion MCP：儲存到週報 database

   總時間：~8 分鐘

   【自動化觸發】
   ```bash
   # crontab
   0 9 * * 1 /path/to/generate-weekly-report.sh
   ```

   【錯誤處理】
   - GitHub rate limit → 使用快取資料
   - Database 超時 → 使用簡化查詢
   - Slack 失敗 → 儲存為本地檔案

   【來源】理論 6.2，情境 C01
```

---

## 🎯 使用建議

### 學習階段

**第 1 週**：MCP 核心概念 + 配置與除錯
- 重點：理解 MCP 的本質
- 目標：能獨立配置 3 個 MCP

**第 2 週**：Agent 切換 + 工作流程編排
- 重點：掌握編排模式
- 目標：能設計 2-MCP 協同流程

**第 3 週**：錯誤處理 + 實戰場景
- 重點：建立完整系統
- 目標：能處理企業級任務

### 複習策略

**間隔重複**：
- Day 1：學習新卡片
- Day 3：第一次複習
- Day 7：第二次複習
- Day 14：第三次複習
- Day 30：第四次複習

**主動回憶**：
- 看到問題（Q），先自己回答
- 再看答案（A），對比差異
- 標記不熟的卡片，增加複習頻率

---

## 📥 如何使用

### 方式 1：Anki 導入

1. 安裝 Anki：https://apps.ankiweb.net/
2. 導入記憶卡檔案（如有提供 .apkg）
3. 每天複習 20 張新卡 + 50 張舊卡

### 方式 2：自製實體卡片

1. 列印問題在正面，答案在背面
2. 使用盒子分類（不熟/熟悉/精通）
3. 定期複習不熟的卡片

### 方式 3：數位筆記

1. 複製到 Notion/Obsidian
2. 加入你自己的理解和範例
3. 與實作練習結合

---

**開始你的記憶卡學習之旅！** 🚀

記住：
> 記憶卡不是背誦工具，而是思考觸發器。
> 每次複習都是重新思考和理解的過程。
