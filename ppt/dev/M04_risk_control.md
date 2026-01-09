# M04. 風險控制學 (Risk Control)

## Slide 4.1: The Risk Control Matrix

**核心概念**：並非所有 AI 生成的代碼都需要同等審查。將資源集中在高風險區域。

**矩陣分級**:
*   🔴 **Red Zone (高風險/高影響)**:
    *   *Scope*: Auth (認證), Payments (金流), Core Business Logic (核心邏輯), Security Config (資安配置).
    *   *Action*: **100% Human Review** + Automated Tests + Security Audit.
*   🟡 **Yellow Zone (中風險)**:
    *   *Scope*: UI Components, Data Transformation, API Integration.
    *   *Action*: Visual Check (看一眼 UI) + Spot Check (抽查邏輯).
*   🟢 **Green Zone (低風險)**:
    *   *Scope*: Unit Tests, Documentation, Comments, Mock Data.
    *   *Action*: **Fast Pass** (快速通過，依賴 Linter 檢查即可).

> 🤖 **AI Generation Prompt**:
> - **Visual Style**: Safety Dashboard / Heatmap.
> - **Layout**: 3-Zone Traffic Light System.
> - **Key Elements**:
>   - **Top (Red)**: Stop Sign symbol. Text: "Critical Path". Icon: Shield/Lock.
>   - **Middle (Yellow)**: Yield Sign symbol. Text: "Visual Logic". Icon: Eye.
>   - **Bottom (Green)**: Go Sign symbol. Text: "Boilerplate". Icon: Fast Forward >>.
>   - Arrows indicating the speed of workflow for each zone (Slow vs Fast).

---

## Slide 4.2: Common Vibe Vulnerabilities

**核心概念**：AI 的盲點就是你的風險。認識 AI 常犯的幾種 "Vibe Errors"。

**三大漏洞**:
1.  **The Auth Gap (權限真空)**:
    *   *Scenario*: AI 完美生成了登入前端頁面，但後端 API 忘記檢查 Session Token。
    *   *Fix*: 檢查所有 API Route 是否有 Middleware 保護。
2.  **Slopsquatting (供應鏈幻覺)**:
    *   *Scenario*: AI 建議安裝一個名字很像但不存在的 npm 套件 (如 `react-use-auth-v2`)，這可能被駭客搶註並植入惡意代碼。
    *   *Fix*: 安裝前務必去 npm/pypi 確認套件真實性。
3.  **The Logic Loop (邏輯死循環)**:
    *   *Scenario*: AI 不斷修改同一段代碼來修復 Bug，但每次都產生新的 Bug，陷入無效迴圈。
    *   *Fix*: 停止對話，Reset Context，人工介入分析 Root Cause。

> 🤖 **AI Generation Prompt**:
> - **Visual Style**: Cybersecurity Warning, glitch art aesthetic.
> - **Layout**: Three Warning Cards.
> - **Key Elements**:
>   - **Card 1 (Auth Gap)**: An open door with a "Do Not Enter" sign that is falling off.
>   - **Card 2 (Slopsquatting)**: A package box that looks suspicious (maybe a skull logo subtly hidden).
>   - **Card 3 (Logic Loop)**: An Ouroboros (snake eating tail) or an infinite loop symbol, looking distressed.
> - **Colors**: Black, Neon Green, Warning Orange.

---

## Slide 4.3: The Vibe Check List (Pre-flight)

**核心概念**：起飛前的檢查清單 (Pre-flight Checklist)。在 `git commit` 之前必做的檢查。

**Checklist Items**:
*   [ ] **Security**: 代碼中是否有 Hardcoded Secrets (API Keys, Passwords)? -> 改用 `.env`。
*   [ ] **Injection**: SQL 查詢是否使用參數化 (Parameterized)? XSS 是否防護?
*   [ ] **Dependency**: 新引入的套件是否必要且安全?
*   [ ] **Logic**: 是否處理了 Edge Cases (空值, 錯誤狀態)?
*   [ ] **Style**: 是否符合 `CLAUDE.md` 定義的風格? (讓 Linter 幫你做)

> 🤖 **AI Generation Prompt**:
> - **Visual Style**: Aviation/Pilot theme, professional and rigorous.
> - **Layout**: Clipboard Checklist on a desk.
> - **Key Elements**:
>   - A clipboard with a paper list. Items have checkmarks.
>   - A pilot's hand holding a pen, hovering over the list.
>   - Background: A cockpit view or a "Ready for Takeoff" runway.
>   - Text overlay: "Clear for Takeoff".

