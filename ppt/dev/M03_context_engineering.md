# M03. 上下文工程 (Context Engineering)

## Slide 3.1: Context Drift (上下文漂移)

**核心概念**：AI 的記憶是短暫且昂貴的。對話越長，AI 越笨。

**漂移現象 (The Drift)**:
*   當對話歷史 (Chat History) 超過 Context Window 時，最早的資訊（如你的專案設定）會被截斷 (Truncated)。
*   即使未截斷，過多的雜訊 (Noise) 會導致注意力機制 (Attention Mechanism) 分散，產生幻覺。

**解決方案**:
*   **Ephemeral (短暫)**: Chat 視窗中的對話，隨用隨丟。
*   **Persistent (持久)**: 將關鍵規則移至檔案系統 (`CLAUDE.md`)，確保每次對話 AI 都能重新讀取最正確的設定。

> 🤖 **AI Generation Prompt**:
> - **Visual Style**: Conceptual Illustration, focused on memory and time.
> - **Layout**: Before & After comparison.
> - **Key Elements**:
>   - **Left (Drift)**: A robot trying to hold too many falling papers, looking confused. Papers at the bottom are fading away (fading memory).
>   - **Right (Anchored)**: A robot calmly reading from a solid stone tablet or book labeled "CLAUDE.md", ignoring the flying papers around it.
> - **Color**: Fade from gray/misty (drift) to solid sharp blue (anchored).

---

## Slide 3.2: The Project Constitution (CLAUDE.md)

**核心概念**：建立專案的最高指導原則。這不是給人看的，是給 AI 看的。

**憲法結構 (The Anatomy)**:
1.  **Tech Stack (技術棧)**:
    *   *Rule*: 明確指定版本。 e.g., "React 18", "Tailwind 3.4" (避免 AI 使用過時語法)。
2.  **Coding Style (風格指南)**:
    *   *Rule*: "Functional Components only", "Use Zod for validation", "Early return pattern".
3.  **Behavioral Rules (行為準則)**:
    *   *Rule*: "Always write tests before implementation", "Think step-by-step".

> 💡 **實用技巧**: 像寫程式一樣維護你的 `CLAUDE.md`，它是你 AI 團隊的 "Source of Truth"。

> 🤖 **AI Generation Prompt**:
> - **Visual Style**: Legal/Documentary style but modernized.
> - **Layout**: Document Anatomy Breakdown.
> - **Key Elements**:
>   - A central document icon labeled "CLAUDE.md" or "System Prompt".
>   - Callout lines pointing to different sections of the document:
>     - "Tech Stack" -> Icon: Tech Logos (React, Python).
>     - "Style Guide" -> Icon: Paintbrush or Ruler.
>     - "Rules" -> Icon: Gavel or Shield.
>   - Background: Subtle code syntax highlighting pattern.

---

## Slide 3.3: Token Economics & Info Layering

**核心概念**：垃圾進，垃圾出 (GIGO)。優化你的 Prompt 成本與品質。

**資訊分層策略 (Information Layering)**:
1.  **Core Layer (核心層)**:
    *   *Content*: `CLAUDE.md`, 當前任務目標。
    *   *Policy*: **Always Include** (必讀)。
2.  **Reference Layer (參考層)**:
    *   *Content*: 相關代碼片段, API 文件, 資料庫 Schema。
    *   *Policy*: **On Demand** (按需讀取，用 `@File` 引用)。
3.  **Noise Layer (雜訊層)**:
    *   *Content*: `node_modules`, `dist`, `logs`, `lock files`.
    *   *Policy*: **Exclude** (使用 `.gitignore` 或 `.cursorignore` 排除)。

> 🤖 **AI Generation Prompt**:
> - **Visual Style**: Infographic, concentric circles or funnel.
> - **Layout**: Target/Bullseye Diagram.
> - **Key Elements**:
>   - **Center (Bullseye)**: Bright Red, label "Core Context" (High Value).
>   - **Middle Ring**: Blue, label "Reference" (On Demand).
>   - **Outer Ring**: Gray/Faded, label "Noise" (Ignore).
>   - Icons of gold coins stacked in the center, and trash bins in the outer ring.
> - **Metaphor**: Signal vs. Noise.

