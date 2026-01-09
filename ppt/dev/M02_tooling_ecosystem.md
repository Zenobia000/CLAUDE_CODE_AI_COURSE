# M02. 工具生態與泛化邏輯 (Tooling & Generalization)

## Slide 2.1: The Vibe Coding Tool Spectrum

**核心概念**：沒有最好的工具，只有最適合場景的工具。學會選擇 "Task-Tool Fit"。

**三大類別光譜**:
1.  **IDE Integrated (編輯器整合型)**
    *   *Tools*: **Cursor**, **Windsurf**
    *   *Pros*: 深度整合 DX (開發者體驗) 佳，適合精細修改 (Surgical Edits)。
    *   *Cons*: 受限於單一視窗，難以綜觀全局。
2.  **CLI Agent (終端代理型)**
    *   *Tools*: **Claude Code**, **Aider**, **Gemini CLI**
    *   *Pros*: 系統級權限，批次處理能力強，適合大型重構 (Refactoring)。
    *   *Cons*: 學習曲線較高，無圖形介面。
3.  **Cloud Hosted (全託管型)**
    *   *Tools*: **Replit Agent**, **v0.dev**, **Bolt.new**
    *   *Pros*: 零配置 (Zero Config)，開箱即用，適合 0->1 快速原型。
    *   *Cons*: 環境封閉，難以客製化工具鏈。

> 🤖 **AI Generation Prompt**:
> - **Visual Style**: Tech Ecosystem Map, clean and categorized.
> - **Layout**: Venn Diagram or Horizontal Spectrum.
> - **Key Elements**:
>   - **Left (CLI)**: Icon of a Terminal prompt `>_`. Keywords: "Power", "Control".
>   - **Center (IDE)**: Icon of a Code Editor window. Keywords: "Balance", "Flow".
>   - **Right (Cloud)**: Icon of a Cloud. Keywords: "Speed", "Convenience".
>   - Place tool logos (Cursor, Claude, Replit) in their respective areas.
> - **Color Coding**: Purple for CLI, Blue for IDE, Green for Cloud.

---

## Slide 2.2: The Model Intelligence Matrix

**核心概念**：依照任務難度選擇對應的模型「大腦」。不要用牛刀殺雞，也不要用殺雞刀屠牛。

**模型三大類**:
*   **🧠 Reasoning Models (思考型)**
    *   *Examples*: **o3-mini**, **Gemini 1.5 Pro**
    *   *特點*: 慢思考 (Chain of Thought)，邏輯強，價格高。
    *   *用途*: 架構設計, 複雜除錯, Root Cause Analysis。
*   **⚡ Standard Models (直覺型)**
    *   *Examples*: **Claude 3.5 Sonnet**, **GPT-4o**
    *   *特點*: 速度與品質的平衡點，表現最穩定。
    *   *用途*: 日常編碼, UI 生成, 文檔撰寫。
*   **💰 Budget Models (經濟型)**
    *   *Examples*: **Gemini Flash**, **Claude Haiku**
    *   *特點*: 極快，便宜，巨大的 Context Window。
    *   *用途*: 全庫檢索, 簡單翻譯, 日誌分析 (Log Analysis)。

> 🤖 **AI Generation Prompt**:
> - **Visual Style**: Strategic Matrix/Chart, clear quadrants.
> - **Layout**: 2D Plot (X-axis: Cost/Latency, Y-axis: Intelligence/Reasoning).
> - **Key Elements**:
>   - **Top Left (Reasoning)**: Icon of a Brain. High Intelligence, High Cost. Label: "The Architect".
>   - **Center (Standard)**: Icon of a Lightning Bolt. Balanced. Label: "The Workhorse".
>   - **Bottom Right (Budget)**: Icon of a Coin or Stack of Papers. Low Cost, High Volume. Label: "The Intern".
> - **Annotations**: Small arrows pointing to suggested use cases (e.g., "Debug" -> Brain, "Logs" -> Intern).

---

## Slide 2.3: Platform Agnostic Primitives

**核心概念**：工具會變，但底層原語 (Primitives) 不變。掌握這些，你可以適應任何新工具。

**四大通用原語對照表**:

| 原語 (Primitive) | 定義 (Definition) | Claude Code | Cursor | Windsurf |
| :--- | :--- | :--- | :--- | :--- |
| **Memory (記憶)** | 專案級別的長期規則 | `CLAUDE.md` | `.cursorrules` | `.windsurfrules` |
| **Context (上下文)** | 餵食當前任務資訊 | `/add` | `@Files` | `@Context` |
| **Planning (規劃)** | 拆解複雜任務步驟 | `/bug` | `Composer` | `Cascade` |
| **Control (控制)** | 設定行為邊界與權限 | `Permissions` | `.cursorignore` | - |

> 💡 **教學重點**: 不要背指令，要理解「我現在需要給 AI 記憶」，然後去找該工具對應的指令。

> 🤖 **AI Generation Prompt**:
> - **Visual Style**: Rosetta Stone concept, linking abstract concepts to concrete tools.
> - **Layout**: Layered Cake or Abstract Connections.
> - **Key Elements**:
>   - **Bottom Layer (The Primitives)**: Large, solid blocks labeled "Memory", "Context", "Planning".
>   - **Top Layer (The Tools)**: Floating icons of Claude, Cursor, Windsurf.
>   - **Connectors**: Lines connecting the tools down to the same underlying primitives, showing that they all rely on the same foundation.
> - **Metaphor**: "Same Engine, Different Chassis".

