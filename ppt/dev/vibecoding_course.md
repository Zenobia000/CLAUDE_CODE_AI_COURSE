# Vibe Coding 架構師速成課程設計 (0 -> 1)

**版本**：2.1 (Refined for Teaching)
**目標受眾**：從零開始希望掌握 AI 協作開發底層邏輯的開發者
**核心哲學**：不教特定工具的操作（How），教 AI 協作的物理學（Why）。讓學習者能將技能泛化到 Claude Code, Cursor, Windsurf 等任何平台。

---

## 🧭 課程導航

本課程分為六大模組，總計約 15 小時。每個模組由多個教學單元（Slides）組成，循序漸進地構建你的 AI 架構師思維。

| 模組 | 主題 | 關鍵概念 | 實戰產出 |
| :--- | :--- | :--- | :--- |
| **M01** | **典範轉移** | 經理思維、L1-L4 分級 | AI 員工手冊 |
| **M02** | **工具生態** | IDE/CLI/Cloud、模型矩陣 | 個人工具鏈配置 |
| **M03** | **上下文工程** | 專案憲法、Token 經濟學 | `CLAUDE.md` 規範檔 |
| **M04** | **風險控制** | 幻覺防禦、供應鏈安全 | Vibe Check 清單 |
| **M05** | **實戰演練** | MVP 快速原型、除錯迴圈 | 迷你 Trello 應用 |
| **M06** | **未來價值** | 洞察、品味、擴散 | 個人職涯護城河 |

---

## 📚 M01. 典範轉移 (The Paradigm Shift)

### Slide 1.1: 從編碼者到架構師
**核心概念**：打破「AI 是更強 Google」的迷思。
*   **舊思維**：我是駕駛，AI 是導航。我必須手握方向盤。
*   **新思維**：我是產品經理 (PM)，AI 是初級開發者。我負責定義需求與驗收。
*   **關鍵轉變**：
    *   Writer (撰寫者) -> Reviewer (審閱者)
    *   Executor (執行者) -> Specifier (規格制定者)

### Slide 1.2: 什麼是 Vibe Coding？
**核心概念**：跟著感覺寫 (Coding on vibes)，但背後有嚴謹的邏輯。
*   **定義**：一種以「自然語言意圖」驅動開發，將「實作細節」外包給 AI 的開發模式。
*   **核心公式**：
    > 產出品質 = (AI 能力 × 上下文清晰度) ÷ 熵 (隨機性)
*   **目標**：降低熵值，提高上下文清晰度，最大化 AI 產出。

### Slide 1.3: 雙重性原則 (Duality Principle)
**核心概念**：根據風險與成本，動態切換工作模式。
*   **🏖️ 週末模式 (Weekend Mode)**：
    *   適用：L0-L1 應用、個人玩具專案、概念驗證。
    *   心態：完全信任 (Full Trust)，追求速度。
    *   特徵：不看 Code，只看結果。
*   **🏢 工程模式 (Engineering Mode)**：
    *   適用：L3-L4 應用、生產環境、團隊協作。
    *   心態：零信任 (Zero Trust)，追求穩健。
    *   特徵：逐行審查，要求測試與型別安全。

### Slide 1.4: AI 自主性分級 (Levels of Autonomy)
**核心概念**：理解你手上的工具處於哪個等級。
*   **L1: Chat (單次問答)** - ChatGPT, Claude Web
    *   特徵：一問一答，無記憶，無檔案權限。
*   **L2: Copilot (結對編程)** - Cursor Tab, GitHub Copilot
    *   特徵：即時補完，感知當前檔案上下文。
*   **L3: Agentic (系統化運作)** - Claude Code, Windsurf Cascade
    *   特徵：多步驟執行，讀寫檔案系統，自我修正。(目前主流)
*   **L4: Multi-Agent (多代理協作)** - MetaGPT, AutoGen
    *   特徵：角色分工 (PM/Dev/QA)，自主決策。

---

## 📚 M02. 工具生態與泛化邏輯 (Tooling & Generalization)

### Slide 2.1: Vibe Coding 工具光譜
**核心概念**：沒有最好的工具，只有最適合場景的工具。
*   **編輯器整合型 (IDE)**：Cursor, Windsurf
    *   優勢：深度整合上下文，DX 體驗佳。
    *   場景：精細修改、日常開發。
*   **終端代理型 (CLI)**：Claude Code, Aider
    *   優勢：系統級權限，批次處理能力強。
    *   場景：大型重構、跨檔案分析、自動化腳本。
*   **全託管型 (Cloud)**：Replit Agent, v0.dev
    *   優勢：零配置，開箱即用。
    *   場景：從零到一 (0->1) 快速原型。

### Slide 2.2: 模型智商矩陣 (The Model Matrix)
**核心概念**：依照任務難度選擇對應的模型「大腦」。
*   **🧠 思考型 (Reasoning)**：o3, Gemini 1.5 Pro
    *   特點：慢思考，邏輯強，貴。
    *   用途：架構設計、複雜除錯、Root Cause Analysis。
*   **⚡ 直覺型 (Standard)**：Claude 3.5 Sonnet, GPT-4o
    *   特點：平衡，速度快，表現穩。
    *   用途：日常編碼、UI 生成、文檔撰寫。
*   **💰 經濟型 (Budget)**：Gemini Flash, Claude Haiku
    *   特點：極快，便宜，上下文窗口大。
    *   用途：全庫檢索、簡單翻譯、日誌分析。

### Slide 2.3: Task-Model Fit 決策框架
**核心概念**：殺雞焉用牛刀，反之亦然。
*   **決策流程**：
    1.  任務是否需要高度邏輯推理？(是 -> Reasoning)
    2.  任務是否涉及大量文本閱讀？(是 -> Budget)
    3.  任務是否為標準編碼工作？(是 -> Standard)
*   **反模式**：
    *   用 Flash 寫複雜演算法 (邏輯崩潰)。
    *   用 o1 翻譯 100 頁文檔 (錢包崩潰)。

### Slide 2.4: 跨平台通用原語 (Platform Agnostic Primitives)
**核心概念**：掌握底層邏輯，無視工具變遷。
*   **記憶 (Memory)**：`CLAUDE.md`, `.cursorrules` - 定義規則。
*   **上下文 (Context)**：`@Files`, `/add` - 餵食資訊。
*   **控制 (Control)**：`y/n`, `.cursorignore` - 設定邊界。
*   **規劃 (Planning)**：`Composer`, `/bug` - 拆解任務。

---

## 📚 M03. 上下文工程 (Context Engineering)

### Slide 3.1: 上下文漂移 (Context Drift)
**核心概念**：AI 的記憶是短暫且昂貴的。
*   **現象**：對話越長，AI 越笨。開始忘記一開始的設定。
*   **原因**：Token Window 限制，注意力機制分散。
*   **解法**：將關鍵資訊從「對話流 (Ephemeral)」固化到「檔案系統 (Persistent)」。

### Slide 3.2: 專案憲法體系 (The Constitution)
**核心概念**：建立專案的最高指導原則。
*   **`CLAUDE.md` / `AGENTS.md`**：
    *   **Tech Stack**：明確定義使用的庫與版本 (e.g., React 18, Tailwind 3.4)。
    *   **Coding Style**：命名慣例、資料夾結構、錯誤處理規範。
*   **`SPEC.md`**：任務規格書。
    *   定義「做什麼 (What)」與「驗收標準 (Acceptance Criteria)」。
*   **`.cursorrules`**：特定工具的角色設定。

### Slide 3.3: Token 經濟學與資訊分層
**核心概念**：垃圾進，垃圾出 (GIGO)。優化成本與品質。
*   **資訊分層**：
    1.  **核心層** (Core)：憲法、當前任務 (必讀)。
    2.  **參考層** (Reference)：相關代碼片段、API 文件 (按需讀取)。
    3.  **雜訊層** (Noise)：`node_modules`, `dist`, logs (過濾)。
*   **`.gitignore` for AI**：確保 AI 不會浪費 Token 讀取無用檔案。

---

## 📚 M04. 風險控制學 (Risk Control)

### Slide 4.1: 風險控制矩陣
**核心概念**：並非所有 AI 生成的代碼都需要同等審查。
*   **🔴 紅區 (Red Zone)**：核心邏輯、資安模組、金流。
    *   策略：100% 人工審查 + 自動化測試。
*   **🟡 黃區 (Yellow Zone)**：UI 組件、資料轉換。
    *   策略：視覺檢查 + 抽樣審查。
*   **🟢 綠區 (Green Zone)**：測試資料、文件、註解。
    *   策略：快速通過。

### Slide 4.2: 常見 Vibe 漏洞 (Vibe Vulnerabilities)
**核心概念**：AI 的盲點就是你的風險。
*   **Auth Gap**：生成了前端登入頁面，但後端 API 沒有驗證 Token。
*   **Slopsquatting (供應鏈幻覺)**：AI 建議安裝一個不存在的 npm 套件 (可能被攻擊者搶註)。
*   **Logic Loop**：AI 陷入無效修復的死循環，不斷修改同一段代碼但無法解決問題。

### Slide 4.3: Vibe Check 清單
**核心概念**：起飛前的檢查清單 (Pre-flight Checklist)。
1.  **安全性**：有無 Hardcoded Secrets? SQL Injection?
2.  **依賴性**：新引入的套件是否存在？是否必要？
3.  **邏輯性**：是否處理了邊界情況 (Edge Cases)？
4.  **一致性**：是否符合 `CLAUDE.md` 定義的風格？

---

## 📚 M05. 實戰演練 (Hands-on Lab)

### Slide 5.1: 實戰心法
**核心概念**：實踐是檢驗真理的唯一標準。
*   **目標**：在 1 小時內，從零打造一個功能完整的應用。
*   **流程**：
    1.  **Initiate**：建立 `CLAUDE.md` 與 `SPEC.md`。
    2.  **Plan**：讓 AI 拆解任務步驟。
    3.  **Execute**：執行 L3 Agent 進行開發。
    4.  **Verify**：人工驗收與除錯。

### Slide 5.2: Lab 1 - 迷你 Trello (Kanban)
**任務**：建立一個可拖拉的看板應用。
*   **技術棧**：React, Tailwind CSS, DnD Kit。
*   **學習點**：
    *   如何描述 UI 互動需求。
    *   如何處理狀態管理 (State Management)。
    *   體驗 Cursor Composer 或 Claude Code 的多檔案修改能力。

### Slide 5.3: Lab 2 - 天氣儀表板 (API Integration)
**任務**：串接公開氣象 API，顯示即時天氣。
*   **技術棧**：Next.js, Server Actions, OpenWeatherMap API。
*   **學習點**：
    *   處理非同步資料 (Async/Await)。
    *   錯誤處理 (Error Handling) 與 Loading 狀態。
    *   **除錯演練**：故意引入 Bug，訓練「餵食錯誤訊息」的技巧。

---

## 📚 M06. 後軟體時代的價值 (Future Value)

### Slide 6.1: 軟體的終結
**核心概念**：軟體從「資產」變成「消耗品」。
*   **趨勢**：軟體開發邊際成本趨近於零。
*   **未來**：每個人都能根據當下需求，生成一次性的軟體工具。
*   **影響**：純粹的「編碼 (Coding)」技能迅速貶值。

### Slide 6.2: 開發者的三大新價值
**核心概念**：當 AI 能解決 How，人類的價值在於 What 和 Why。
1.  **💡 洞察力 (Insight)**：
    *   發現真正的問題。定義值得解決的需求。
2.  **🎨 品味 (Taste)**：
    *   從無數 AI 生成方案中，辨別出「好」的那一個。
    *   對 UX、架構美學的鑑賞力。
3.  **📢 擴散力 (Distribution)**：
    *   溝通、說服、影響力。讓你的解決方案被採用。

### Slide 6.3: 建立職涯護城河
**核心概念**：成為 AI 的指揮官，而非 AI 的競爭者。
*   **策略**：
    *   深耕 Domain Knowledge (領域知識)。
    *   培養系統架構思維。
    *   建立個人品牌與信任資產。
*   **結論**：不會被 AI 取代，而是被「善用 AI 的人」取代。

---

## 📝 附錄：通用架構原語對照表

| 底層原語 | Claude Code | Cursor | Windsurf | Copilot |
| :--- | :--- | :--- | :--- | :--- |
| **記憶** | `CLAUDE.md` | `.cursorrules` | `.windsurfrules` | Instructions |
| **上下文** | `/add` | `@Files` | `@Context` | `#File` |
| **規劃** | `/bug` | Composer | Cascade | Workspace |