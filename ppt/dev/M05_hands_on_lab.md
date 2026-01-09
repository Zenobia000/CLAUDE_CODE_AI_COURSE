# M05. 實戰演練 (Hands-on Lab)

## Slide 5.1: The Vibe Coding Workflow: IPEV


**核心概念**：Vibe Coding 不是隨機嘗試，而是結構化的循環。我們使用 **IPEV 框架** 來確保每次生成都在軌道上。

**IPEV 執行迴圈**:
1.  **Initiate (啟動)**: 設定邊界。
    *   *Action*: 建立 `CLAUDE.md` (憲法) 與 `.cursorrules`。
    *   *Why*: 防止 AI 使用錯誤的技術棧或風格。
2.  **Plan (規劃)**: 定義路徑。
    *   *Action*: 撰寫 `SPEC.md` 或使用 `/bug` 指令讓 AI 分析。
    *   *Why*: 讓 AI 理解 "Done" 的定義。
3.  **Execute (執行)**: 代理人運作。
    *   *Action*: 使用 Agent (L3) 執行多步驟任務。
    *   *Why*: 讓 AI 處理繁瑣的檔案操作。
4.  **Verify (驗證)**: 人類審查。
    *   *Action*: 運行測試、檢查 UI、Vibe Check。
    *   *Why*: AI 會幻覺，人類負責驗收。

> 💡 **關鍵心法**: "Don't write code. Write specifications." (不要寫代碼，寫規格。)

> 🤖 **AI Generation Prompt**:
> - **Visual Style**: Modern Corporate Tech, clean and structured.
> - **Layout**: Circular Process Diagram (Cycle).
> - **Color Palette**: Claude Orange (#FF6B35) for active steps, Slate Grey (#2C2B29) for text, Off-white (#F5F4F2) background.
> - **Key Elements**: 
>   - Four distinct nodes arranged in a clockwise circle: Initiate, Plan, Execute, Verify.
>   - Icons for each node: 
>     - Initiate: A constitution scroll or flag.
>     - Plan: A compass or blueprint.
>     - Execute: A robot arm or gear.
>     - Verify: A magnifying glass or checkmark shield.
>   - Connectors should be arrows indicating flow.
>   - Center of the circle contains text: "The Vibe Loop".

---

## Slide 5.2: Lab 01 - The Reactive Interface (Kanban)


**任務目標**：在 20 分鐘內建立一個功能完整的 Trello 仿製品。
**適用模式**：🏖️ Weekend Mode (L1/L2 Trust)

**技術棧**:
*   Framework: React + Vite
*   Styling: Tailwind CSS
*   Interaction: `@dnd-kit/core` (Drag & Drop)

**學習重點**:
1.  **UI 描述技巧**:
    *   ❌ "做一個好看的看板"
    *   ✅ "建立一個三欄式看板 (To Do, In Progress, Done)，使用玻璃擬態風格 (Glassmorphism)，卡片要有陰影與圓角。"
2.  **狀態管理 (State Management)**:
    *   讓 AI 處理複雜的 Drag & Drop 狀態邏輯，你只負責定義 "拖拉後資料要怎麼存"。
3.  **迭代修正**:
    *   當 UI 跑版時，截圖餵給 AI："修正這個邊距，參考這張圖的間距。"

> 🚀 **Challenge**: 嘗試不寫一行 CSS，全靠 Prompt 調整樣式。

> 🤖 **AI Generation Prompt**:
> - **Visual Style**: Product Showcase, sleek and vibrant.
> - **Layout**: Split Screen / Before & After conceptualization.
> - **Key Elements**: 
>   - Left Side: A text bubble showing the "Prompt" (e.g., "Create a glassmorphism kanban board...").
>   - Right Side: A high-fidelity mockup of the resulting Kanban Board UI.
>   - The UI should look modern: frosted glass effects, soft shadows, vibrant accent colors tags on cards.
>   - A magical sparkle effect connecting the prompt to the UI.
> - **Typography**: Monospace font for the Prompt, Sans-serif for the UI labels.

---

## Slide 5.3: Lab 02 - The Resilient System (Weather API)


**任務目標**：串接真實世界數據，處理不可預期的錯誤。
**適用模式**：🏢 Engineering Mode (L3 Zero Trust)

**技術棧**:
*   Framework: Next.js (App Router)
*   Data: OpenWeatherMap API
*   Validation: Zod

**學習重點**:
1.  **非同步邏輯 (Async Logic)**:
    *   如何讓 AI 正確處理 `Loading`, `Error`, `Success` 三種狀態。
2.  **錯誤邊界 (Error Boundaries)**:
    *   Prompt: "如果 API 回傳 404 或 500，請顯示一個優雅的錯誤組件，並提供重試按鈕。"
3.  **防禦性編程**:
    *   使用 Zod 驗證 API 回傳的資料結構，防止因 API 改版導致前端崩潰。

> 🛡️ **Vibe Check**: 檢查 AI 是否將 API Key 硬編碼 (Hardcoded) 在代碼中？要求它使用 `.env`。

> 🤖 **AI Generation Prompt**:
> - **Visual Style**: Technical Architecture, isometric and detailed.
> - **Layout**: Data Flow Diagram.
> - **Color Palette**: Cool Blues and Teals (representing data/cloud), with Red accents for Error states.
> - **Key Elements**: 
>   - Left: A User Interface block showing a "Weather Card".
>   - Right: A Cloud icon representing the External API.
>   - Middle: Connecting pipes/lines representing data flow.
>   - Visual representation of "Filters" or "Shields" on the lines (representing Zod validation and Error Handling).
>   - A floating "Environment Variable" lock icon indicating security.

---

## Slide 5.4: The Art of AI Debugging


**核心概念**：當 AI 犯錯時，不要修代碼，修 Prompt。

**除錯決策樹**:
1.  **是語法錯誤 (Syntax Error)?**
    *   👉 直接貼 Error Log 給 AI，通常能秒解。
2.  **是邏輯錯誤 (Logic Error)?**
    *   👉 不要只說 "壞了"。描述 "預期行為" vs "實際行為"。
    *   *Prompt*: "我點擊按鈕時預期會彈出視窗，但實際上什麼都沒發生，這是 console log..."
3.  **是鬼打牆 (Looping)?**
    *   👉 **Stop!** 回退版本 (`git checkout`)，切換模型 (Claude -> GPT 或反之)，或是重寫 Prompt 的上下文。

> 💡 **金句**: "Debugging is just explaining the problem to the AI until it understands."

> 🤖 **AI Generation Prompt**:
> - **Visual Style**: Abstract Decision Map, clean dark mode aesthetic.
> - **Layout**: Flowchart / Decision Tree.
> - **Key Elements**: 
>   - Start node: "Bug Found 🐛".
>   - Three branches: 
>     1. "Syntax" -> Icon: Copy/Paste -> Result: ✅
>     2. "Logic" -> Icon: Speak Bubble (Explain) -> Result: ✅
>     3. "Looping" -> Icon: Stop Sign 🛑 -> Action: "Reset Context / Switch Model".
>   - Use neon distinct colors for paths (e.g., Green for Syntax, Yellow for Logic, Red for Looping).