# Agent 切換決策樹 - 何時切換、為何切換、切換到誰

## 📋 使用說明

這不是 Agent 功能列表，而是**決策流程圖**。

**解決的問題**：
- 何時應該切換 Agent？
- 應該切換到哪個 Agent？
- 切換的成本與收益如何權衡？
- 如何避免不必要的切換？

**不是用來**：
- ❌ 查詢 Agent 有哪些功能 → 參考 Claude Code 官方文檔
- ❌ 學習如何切換 → 參考 `B05_基礎Agent切換.md`

---

## 核心決策流程

### 第一層：是否需要切換？

```
當前任務遇到問題
    ↓
問題 1：預設 Agent 能否解決？
├─ 是 → 繼續使用，不需切換 ✅
└─ 否 ↓

問題 2：問題是否需要專業領域知識？
├─ 否 → 可能是提示不清楚，重新描述任務 ✅
└─ 是 ↓

問題 3：任務是否複雜且重要？
├─ 否 → 切換成本 > 收益，不值得切換 ✅
└─ 是 ↓

✅ 值得切換到專業 Agent
```

### 第二層：切換到哪個 Agent？

```
需要切換 Agent
    ↓
任務類型判斷：

程式碼品質問題
├─ 需要深度分析？ → code-expert
├─ 需要審查？ → reviewer
├─ 需要除錯？ → debugger
└─ 需要效能優化？ → performance-optimizer

系統設計問題
├─ 架構設計？ → architect
├─ 資料庫設計？ → architect
└─ API 設計？ → architect

安全問題
└─ 任何安全相關 → security-auditor

測試問題
└─ 測試策略/實作 → test-engineer

資料分析問題
└─ 數據分析/視覺化 → data-analyst

文檔問題
└─ 技術寫作 → tech-writer

運維問題
└─ 部署/監控 → devops-engineer
```

---

## Agent 決策矩陣

| 情境 | 判斷標準 | 推薦 Agent | 優先級 |
|-----|---------|-----------|--------|
| 程式碼架構設計 | 需要高層設計決策 | `architect` | ⭐⭐⭐⭐⭐ |
| 程式碼深度分析 | 複雜邏輯理解 | `code-expert` | ⭐⭐⭐⭐ |
| 程式碼審查 | PR review、品質檢查 | `reviewer` | ⭐⭐⭐⭐ |
| Bug 修復 | 找不到根本原因 | `debugger` | ⭐⭐⭐⭐ |
| 安全審計 | 任何安全相關 | `security-auditor` | ⭐⭐⭐⭐⭐ |
| 效能優化 | 效能瓶頸分析 | `performance-optimizer` | ⭐⭐⭐ |
| 測試策略 | 設計測試案例 | `test-engineer` | ⭐⭐⭐⭐ |
| 資料分析 | SQL 優化、報表 | `data-analyst` | ⭐⭐⭐⭐ |
| 技術文檔 | API 文檔、README | `tech-writer` | ⭐⭐⭐ |
| DevOps | 部署、監控 | `devops-engineer` | ⭐⭐⭐ |

**優先級說明**：
- ⭐⭐⭐⭐⭐：強烈建議切換，品質差異顯著
- ⭐⭐⭐⭐：建議切換，品質有明顯提升
- ⭐⭐⭐：可選切換，視任務複雜度決定

---

## 詳細決策樹

### 情境 1：程式碼品質問題

```
程式碼有問題
    ↓
問題類型？

1️⃣ 不理解程式碼邏輯
    ↓
    複雜度高嗎？
    ├─ 是 → /agents:code-expert
    │   「深入分析這段程式碼的執行流程和設計意圖」
    └─ 否 → 預設 Agent 即可

2️⃣ 程式碼需要審查
    ↓
    重要程度？
    ├─ 生產環境/關鍵功能 → /agents:reviewer
    │   「從程式碼品質、最佳實踐、潛在問題三方面審查」
    └─ 一般功能 → 預設 Agent 即可

3️⃣ 有 Bug 但找不到原因
    ↓
    調試時間？
    ├─ 已超過 30 分鐘 → /agents:debugger
    │   「系統性分析可能的根本原因」
    └─ 剛開始調試 → 預設 Agent 先嘗試

4️⃣ 效能不佳
    ↓
    影響範圍？
    ├─ 關鍵路徑/用戶體驗受影響 → /agents:performance-optimizer
    │   「識別效能瓶頸並提供優化方案」
    └─ 次要功能 → 預設 Agent 即可
```

### 情境 2：系統設計問題

```
需要設計系統
    ↓
設計層次？

1️⃣ 高層架構設計
    ✅ 強烈建議：/agents:architect
    「設計 [系統名稱] 的整體架構，考慮：
     - 可擴展性
     - 可維護性
     - 技術選型」

2️⃣ 資料庫設計
    ↓
    複雜度？
    ├─ 多表關聯/複雜查詢 → /agents:architect
    │   「設計資料庫 schema，優化查詢效能」
    └─ 簡單 CRUD → 預設 Agent 或 data-analyst

3️⃣ API 設計
    ↓
    重要程度？
    ├─ 公開 API/需要長期維護 → /agents:architect
    │   「設計 RESTful API，確保向後相容」
    └─ 內部 API/簡單介面 → 預設 Agent 即可

4️⃣ 模組設計
    ↓
    複雜度？
    ├─ 多模組交互/複雜依賴 → /agents:architect
    │   「設計模組結構，減少耦合」
    └─ 單一模組 → 預設 Agent 即可
```

### 情境 3：安全問題

```
涉及安全
    ↓
⚠️ 任何安全相關都應該切換

✅ 強烈建議：/agents:security-auditor

1️⃣ 安全審計
    「對 [程式碼/系統] 進行全面安全審計：
     - SQL injection
     - XSS
     - CSRF
     - 權限控制
     - 資料洩漏」

2️⃣ 安全漏洞分析
    「分析這個潛在漏洞的嚴重程度和修復方案」

3️⃣ 安全配置審查
    「檢查這些配置是否符合安全最佳實踐」

❌ 不推薦：
使用預設 Agent 處理安全問題
（可能遺漏關鍵漏洞）
```

### 情境 4：測試問題

```
需要測試
    ↓
測試類型？

1️⃣ 測試策略設計
    ✅ 推薦：/agents:test-engineer
    「為 [功能] 設計測試策略：
     - 單元測試
     - 整合測試
     - E2E 測試」

2️⃣ 測試案例設計
    ↓
    覆蓋率要求？
    ├─ 關鍵功能/高覆蓋率要求 → /agents:test-engineer
    │   「設計全面的測試案例，包含邊界情況」
    └─ 一般功能 → 預設 Agent 即可

3️⃣ 測試程式碼撰寫
    ↓
    複雜度？
    ├─ Mock 複雜/非同步測試 → /agents:test-engineer
    └─ 簡單單元測試 → 預設 Agent 即可
```

### 情境 5：資料分析問題

```
需要分析資料
    ↓
分析類型？

1️⃣ SQL 查詢優化
    ✅ 推薦：/agents:data-analyst
    「優化這個 SQL 查詢的效能」

2️⃣ 資料報表生成
    ✅ 推薦：/agents:data-analyst
    「從資料庫生成週報，包含：
     - 趨勢圖表
     - 關鍵指標
     - 洞察分析」

3️⃣ 資料視覺化
    ✅ 推薦：/agents:data-analyst
    「將這些資料視覺化，選擇合適的圖表類型」

4️⃣ 簡單資料查詢
    ❌ 不需要切換
    預設 Agent 即可
```

### 情境 6：文檔撰寫

```
需要寫文檔
    ↓
文檔類型？

1️⃣ API 文檔
    ↓
    重要程度？
    ├─ 公開 API/需要專業呈現 → /agents:tech-writer
    │   「撰寫專業的 API 文檔，包含範例」
    └─ 內部 API → 預設 Agent 即可

2️⃣ README / 使用指南
    ↓
    受眾？
    ├─ 外部用戶/需要高品質 → /agents:tech-writer
    │   「撰寫清晰易懂的使用指南」
    └─ 內部開發者 → 預設 Agent 即可

3️⃣ 技術決策文檔
    ✅ 推薦：/agents:architect + tech-writer
    先讓 architect 整理決策，再讓 tech-writer 撰寫

4️⃣ 程式碼註解
    ❌ 不需要切換
    預設 Agent 即可
```

### 情境 7：DevOps 問題

```
部署/維運問題
    ↓
問題類型？

1️⃣ 部署策略設計
    ✅ 推薦：/agents:devops-engineer
    「設計 CI/CD 流程，包含：
     - 自動化測試
     - 建置策略
     - 部署策略
     - 回滾機制」

2️⃣ 監控告警設置
    ✅ 推薦：/agents:devops-engineer
    「設計監控指標和告警規則」

3️⃣ 容器化配置
    ↓
    複雜度？
    ├─ 多容器編排/複雜網路 → /agents:devops-engineer
    └─ 簡單 Dockerfile → 預設 Agent 即可

4️⃣ 簡單部署腳本
    ❌ 不需要切換
    預設 Agent 即可
```

---

## 成本與收益分析

### 切換成本

**時間成本**：
- 切換指令：10 秒
- 重新說明上下文：1-2 分鐘
- Agent 分析時間：可能稍長

**總計**：約 2-5 分鐘

### 切換收益

| 情境 | 預設 Agent 品質 | 專業 Agent 品質 | 收益 |
|-----|---------------|----------------|-----|
| 安全審計 | ⭐⭐ (可能遺漏) | ⭐⭐⭐⭐⭐ (全面) | 極高 |
| 架構設計 | ⭐⭐⭐ (可用) | ⭐⭐⭐⭐⭐ (專業) | 很高 |
| 程式碼審查 | ⭐⭐⭐ (基本) | ⭐⭐⭐⭐⭐ (深入) | 很高 |
| Bug 調試 | ⭐⭐⭐ (常見問題) | ⭐⭐⭐⭐ (系統性) | 高 |
| 測試設計 | ⭐⭐⭐ (基本) | ⭐⭐⭐⭐ (全面) | 高 |
| 資料分析 | ⭐⭐⭐ (簡單查詢) | ⭐⭐⭐⭐ (優化+洞察) | 中高 |
| API 文檔 | ⭐⭐⭐ (可讀) | ⭐⭐⭐⭐ (專業) | 中 |
| 簡單 CRUD | ⭐⭐⭐⭐ (足夠) | ⭐⭐⭐⭐ (無差異) | 低 |

### 決策建議

```
收益極高（安全、架構）
    → 必須切換

收益很高（審查、測試）
    → 任務重要時切換

收益高（調試、資料分析）
    → 任務複雜時切換

收益中（文檔）
    → 視受眾決定

收益低（簡單任務）
    → 不需切換
```

---

## 實戰案例

### 案例 1：登入功能開發

```
階段 1：架構設計
✅ 切換到 architect
User: "/agents:architect
      設計用戶登入系統，考慮：
      - JWT vs Session
      - 多因素驗證
      - 密碼策略"

階段 2：安全審查
✅ 切換到 security-auditor
User: "/agents:security-auditor
      審查登入實作的安全性"

階段 3：單元測試
❌ 不需要切換（簡單測試）
User: "為 login() 函數寫單元測試"

階段 4：整合測試
✅ 切換到 test-engineer（複雜測試）
User: "/agents:test-engineer
      設計登入流程的整合測試，
      包含 Mock 和邊界情況"
```

**總計切換**：3 次
**價值**：架構合理 + 安全可靠 + 測試完整

---

### 案例 2：效能優化

```
問題：API 回應慢

階段 1：初步診斷
❌ 不需要切換
User: "分析這個 API 為什麼慢"
Claude: "可能是 SQL N+1 查詢問題"

階段 2：SQL 優化
✅ 切換到 data-analyst
User: "/agents:data-analyst
      優化這個查詢，消除 N+1 問題"

階段 3：程式碼優化
✅ 切換到 performance-optimizer
User: "/agents:performance-optimizer
      優化這段程式碼的效能"

階段 4：驗證效能
❌ 不需要切換
User: "撰寫效能測試腳本"
```

**總計切換**：2 次
**價值**：專業優化方案

---

### 案例 3：不應該切換的情境

```
❌ 錯誤：過度切換

User: "/agents:code-expert
      幫我寫一個簡單的 hello world"

分析：
- 任務極簡單
- 預設 Agent 完全勝任
- 切換成本 > 收益
- 浪費時間

✅ 正確：

User: "寫一個 hello world 程式"
```

---

## 切換最佳實踐

### ✅ 好的切換模式

**1. 明確說明上下文**
```
User: "/agents:security-auditor

我開發了一個用戶註冊 API（user_register.py），
請進行安全審計，重點檢查：
- SQL injection
- 密碼儲存
- Input validation"
```

**2. 階段性切換**
```
架構設計 → architect
安全審查 → security-auditor
效能優化 → performance-optimizer
```

**3. 適時切回預設**
```
複雜任務完成後，簡單任務切回預設 Agent：

User: "/agents:default"
```

---

### ❌ 不好的切換模式

**1. 頻繁無意義切換**
```
❌ User: "/agents:code-expert"
   User: "寫 hello world"
   User: "/agents:architect"
   User: "加一行註解"
```

**2. 不提供上下文**
```
❌ User: "/agents:security-auditor"
   User: "審查程式碼"

（Claude 不知道要審查什麼）
```

**3. 簡單任務用專業 Agent**
```
❌ User: "/agents:architect"
   User: "幫我改個變數名稱"
```

---

## 快速決策檢查清單

切換前問自己：

- [ ] 任務是否複雜？（否 → 不切換）
- [ ] 任務是否重要？（否 → 不切換）
- [ ] 預設 Agent 是否能勝任？（是 → 不切換）
- [ ] 需要專業領域知識？（是 → 考慮切換）
- [ ] 品質差異是否顯著？（是 → 切換）
- [ ] 切換成本是否值得？（是 → 切換）

**如果 3 個以上 ✅ → 切換**
**如果 2 個以下 ✅ → 不切換**

---

## Agent 能力圖譜

```
           深度分析能力
                ↑
    code-expert │ architect
                │
    reviewer ───┼─── security-auditor
                │
                │
專業廣度 ←──────┼──────→ 領域專精
                │
    debugger ───┼─── test-engineer
                │
performance-    │ data-analyst
optimizer       │
                ↓
           實作執行能力
```

**使用建議**：
- **左上角 Agent（深度+廣度）**：複雜任務優先
- **右上角 Agent（深度+專精）**：關鍵領域必用
- **下方 Agent（執行導向）**：明確目標時使用

---

## 總結：何時切換決策口訣

```
安全問題 → 必切換（security-auditor）
架構設計 → 必切換（architect）
審查調試 → 看複雜度（reviewer / debugger）
測試資料 → 看重要性（test-engineer / data-analyst）
文檔運維 → 看受眾（tech-writer / devops-engineer）
簡單任務 → 不切換（預設 Agent）
```

**記住**：
> 不是所有任務都需要專業 Agent
> 預設 Agent 已經很強大
> 切換是為了解決特定領域的複雜問題
> 而不是為了切換而切換

---

## 下一步

- **實際練習** → 查看 `B05_基礎Agent切換.md` 情境題
- **進階應用** → 查看 `工作流程編排模式庫.md` 中的 Agent 協同模式
- **疑難排解** → 如果 Agent 切換沒有明顯效果，檢查是否提供足夠上下文

