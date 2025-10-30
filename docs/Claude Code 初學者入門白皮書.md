# Claude Code 初學者入門白皮書：AI 程式設計的完整指南

## 目錄

1. [Claude Code 簡介](#claude-code-簡介)
2. [快速開始](#快速開始)
3. [核心命令全覽](#核心命令全覽)
4. [功能詳解與使用場景](#功能詳解與使用場景)
5. [快捷鍵與操作技巧](#快捷鍵與操作技巧)
6. [上下文管理與記憶系統](#上下文管理與記憶系統)
7. [整合與擴展](#整合與擴展)
8. [最佳實踐與工作流程](#最佳實踐與工作流程)
9. [常見問題與故障排除](#常見問題與故障排除)
10. [進階學習路徑](#進階學習路徑)

---

## Claude Code 簡介

### 什麼是 Claude Code？

Claude Code 是由 Anthropic 開發的 AI 程式設計助手，以命令列（CLI）為核心的代理人式協作工具。與傳統 IDE 內建的 AI 助手不同，Claude Code 採用顯式、有狀態的上下文管理方式，賦予開發者極高的控制權，使其能夠執行複雜的多檔案重構、跨專案分析和系統級任務規劃。

### 核心特性

- **命令列原生設計**：專為 CLI 環境優化，無需依賴 IDE
- **顯式上下文管理**：透過檔案系統互動構建和管理上下文
- **狀態持久化**：支援跨會話的記憶管理和專案配置
- **代理人協作**：可整合多個 AI 工具和 MCP（Model Context Protocol）伺服器
- **強大的程式碼分析**：能夠理解大型程式碼庫並執行複雜重構

### 與其他工具的區別

| 特性 | Claude Code | GitHub Copilot | Gemini CLI |
|------|-------------|----------------|------------|
| 核心定位 | CLI 代理人協作者 | IDE 內建助手 | CLI 代理人協作者 |
| 上下文管理 | 顯式、有狀態 | 隱式、即時 | 巨量記憶體上下文 |
| 最佳場景 | 複雜重構、系統設計 | 日常編碼、即時補全 | 程式碼庫分析、一次性載入 |

---

## 快速開始

### 安裝 Claude Code

#### 系統要求

- macOS、Linux 或 Windows（WSL 推薦）
- Node.js 18+ 或 Python 3.8+
- 網際網路連線（用於 API 呼叫）

#### 安裝步驟

1. **使用 npm 安裝**（推薦）
```bash
npm install -g @anthropic-ai/claude-code
```

2. **使用 pip 安裝**
```bash
pip install claude-code
```

3. **驗證安裝**
```bash
claude --version
```

### 首次使用：登入與配置

#### 1. 登入帳號

```bash
claude /login
```

按照提示輸入您的 Anthropic API 金鑰，或使用瀏覽器進行 OAuth 認證。

> **提示**：如圖 `help - 显示帮助.png` 所示，您隨時可以使用 `/help` 命令查看所有可用命令的完整列表。

#### 2. 初始化專案記憶

```bash
claude /init
```

這將在當前目錄生成一個 `CLAUDE.md` 檔案，用於儲存專案的長期記憶。

#### 3. 添加工作目錄

```bash
claude --add-dir ./src
```

將您的主要程式碼目錄添加到 Claude 的上下文範圍中。

### 第一個程式設計任務

讓我們從一個簡單的範例開始：

```bash
claude
```

進入互動模式後，嘗試：

```
請幫我建立一個 Python 函數，計算斐波那契數列的第 n 項，並包含完整的單元測試
```

Claude Code 將：
1. 生成符合您專案風格的程式碼
2. 創建對應的測試檔案
3. 根據您的 `CLAUDE.md` 配置調整輸出格式

---

## 核心命令全覽

### 基礎命令

#### `/help` - 顯示幫助

顯示所有可用命令的完整列表和說明。建議初學者首先執行此命令熟悉功能。

![帮助命令界面](ref_img/help%20-%20%E6%98%BE%E7%A4%BA%E5%B8%AE%E5%8A%A9.png)

![帮助命令界面2](ref_img/help%20-%20%E6%98%BE%E7%A4%BA%E5%B8%AE%E5%8A%A92.png)

```bash
claude /help
```

#### `/clear` (或 `/reset`) - 清除對話歷史

清除當前會話的對話歷史，重新開始一個全新的上下文。

**使用時機**：
- 會話變得太長，需要重新整理
- 上下文變得混亂或不相關
- 開始一個全新的主題討論

```bash
claude /clear
```

#### `/exit` (或 `/quit`) - 退出 REPL

退出 Claude Code 的互動式 REPL 環境。

```bash
claude /exit
```

### 上下文管理命令

#### `/compact` - 壓縮上下文

壓縮當前對話歷史，保留關鍵資訊並移除冗餘內容，以節省上下文空間。

![压缩上下文功能](ref_img/compact%20-%20%E5%8E%8B%E7%BC%A9%E4%B8%8A%E4%B8%8B%E6%96%87.png)

**使用時機**：
- 會話歷史過長，接近上下文限制
- 對話中包含大量冗餘或臨時資訊
- 需要保持關鍵上下文但不佔用過多 token

```bash
claude /compact
```

#### `/context` - 視覺化上下文使用

顯示當前上下文的詳細使用情況，包括：
- 已使用的 token 數量
- 上下文窗口大小
- 各類內容的佔用比例

![上下文使用可视化](ref_img/context%20-%20%E5%8F%AF%E8%A7%86%E5%8C%96%E4%B8%8A%E4%B8%8B%E6%96%87%E4%BD%BF%E7%94%A8.png)

```bash
claude /context
```

**輸出範例**：
```
上下文使用情況：
├─ 對話歷史：45,231 tokens (22.6%)
├─ 程式碼檔案：120,450 tokens (60.2%)
├─ 專案記憶：25,000 tokens (12.5%)
└─ 系統提示：9,319 tokens (4.7%)

總計：199,000 / 200,000 tokens
```

### 專案記憶管理

#### `/memory` - 編輯記憶檔案

編輯專案的記憶檔案，用於儲存長期知識、架構決策和最佳實踐。

![编辑记忆文件](ref_img/memory%20-%20%E7%BC%96%E8%BE%91%E8%AE%B0%E5%BF%86%E6%96%87%E4%BB%B6.png)

![编辑记忆文件2](ref_img/memory%20-%20%E7%BC%96%E8%BE%91%E8%AE%B0%E5%BF%86%E6%96%87%E4%BB%B62.png)

```bash
claude /memory
```

**記憶檔案用途**：
- 儲存專案架構決策
- 記錄編碼規範和風格指南
- 保存常見問題的解決方案
- 定義 API 契約和介面規範

#### `/init` - 初始化專案記憶檔案

為新專案生成初始的 `CLAUDE.md` 檔案模板。

```bash
claude /init
```

### 配置與設定

#### `/config` (或 `/theme`) - 打開配置面板

打開配置面板，自訂 Claude Code 的外觀和行為設定。

![配置面板](ref_img/config%20%28theme%29%20-%20%E6%89%93%E5%BC%80%E9%85%8D%E7%BD%AE%E9%9D%A2%E6%9D%BF.png)

**可配置項目**：
- 主題色彩
- 輸出格式
- 預設模型
- 快捷鍵綁定
- 檔案過濾規則

```bash
claude /config
```

#### `/output-style` - 設置輸出樣式

設定 Claude 回應的輸出格式和風格。

![设置输出样式](ref_img/output-style%20-%20%E8%AE%BE%E7%BD%AE%E8%BE%93%E5%87%BA%E6%A0%B7%E5%BC%8F.png)

**可用的輸出樣式**：
- `detailed`：詳細說明
- `concise`：簡潔版本
- `code-focused`：程式碼優先
- `explanation-first`：解釋優先

```bash
claude /output-style detailed
```

#### `/output-style:new` - 創建自訂樣式

創建符合您個人或團隊偏好的自訂輸出樣式。

```bash
claude /output-style:new my-custom-style
```

### 模型管理

#### `/model` - 切換 AI 模型

在不同版本的 Claude 模型之間切換，以適應不同的任務需求。

![切换AI模型](ref_img/model%20-%20%E5%88%87%E6%8D%A2%20AI%20%E6%A8%A1%E5%9E%8B.png)

**可用模型**：
- `claude-3-5-sonnet`：平衡性能與速度（推薦日常使用）
- `claude-3-opus`：最強能力，適用複雜任務
- `claude-3-haiku`：最快速度，適用簡單任務

```bash
claude /model claude-3-5-sonnet
```

**選擇建議**：
- **日常開發**：使用 `claude-3-5-sonnet`
- **複雜架構設計**：使用 `claude-3-opus`
- **快速原型**：使用 `claude-3-haiku`

### 代理與擴展

#### `/agents` - 管理代理配置

管理多個 AI 代理人的配置，實現分工協作。

![管理代理配置](ref_img/agents%20-%20%E7%AE%A1%E7%90%86%E4%BB%A3%E7%90%86%E9%85%8D%E7%BD%AE.png)

**使用場景**：
- 設定專門的程式碼審查代理人
- 配置安全掃描代理人
- 建立測試生成代理人

```bash
claude /agents
```

#### `/mcp` - 管理 MCP 伺服器

管理 Model Context Protocol (MCP) 伺服器，擴展 Claude Code 的能力。

**MCP 伺服器範例**：
- GitHub 整合
- 資料庫連接
- 雲端服務 API
- 自訂工具

```bash
claude /mcp
```

### 終端與基礎設施

#### `/bashes` - 管理後台 Bash 終端

管理多個背景執行的 Bash 終端會話，用於執行長時間運行的任務。

![管理后台Bash终端](ref_img/bashes%20-%20%E7%AE%A1%E7%90%86%E5%90%8E%E5%8F%B0%20Bash%20%E7%BB%88%E7%AB%AF.png)

**使用場景**：
- 並行執行多個測試套件
- 監控長期運行的程序
- 執行構建和部署任務

```bash
claude /bashes
```

### 整合功能

#### `/ide` - 管理 IDE 整合

配置 Claude Code 與各種 IDE 的整合設定。

![管理IDE集成](ref_img/ide%20-%20%E7%AE%A1%E7%90%86%20IDE%20%E9%9B%86%E6%88%90.png)

**支援的 IDE**：
- Visual Studio Code
- JetBrains 系列（IntelliJ、PyCharm 等）
- Neovim
- Emacs

```bash
claude /ide
```

#### `/install-github-app` - 設置 GitHub Actions

配置 Claude Code 的 GitHub Actions 整合，實現自動化程式碼審查。

![设置GitHub Actions](ref_img/install-github-app%20-%20%E8%AE%BE%E7%BD%AE%20GitHub%20Actions.png)

**功能**：
- 自動 PR 評論
- 程式碼品質檢查
- 安全漏洞掃描

```bash
claude /install-github-app
```

#### `/pr-comments` - 獲取 PR 評論

獲取指定 Pull Request 的審查評論摘要。

![获取PR评论](ref_img/pr-comments%20-%20%E8%8E%B7%E5%8F%96%20PR%20%E8%AF%84%E8%AE%BA.png)

```bash
claude /pr-comments #123
```

### 狀態與診斷

#### `/status` - 顯示狀態資訊

顯示 Claude Code 的當前狀態，包括：
- 連接狀態
- API 配額使用情況
- 當前活動的會話

![显示状态信息](ref_img/status%20-%20%E6%98%BE%E7%A4%BA%E7%8A%B6%E6%80%81%E4%BF%A1%E6%81%AF.png)

```bash
claude /status
```

#### `/cost` - 顯示會話成本

顯示當前會話的 API 使用成本估算。

![显示会话成本](ref_img/cost%20-%20%E6%98%BE%E7%A4%BA%E4%BC%9A%E8%AF%9D%E6%88%90%E6%9C%AC.png)

```bash
claude /cost
```

**輸出範例**：
```
當前會話成本：
├─ 輸入 tokens：45,231 ($0.015)
├─ 輸出 tokens：12,450 ($0.045)
└─ 總計：$0.06
```

#### `/doctor` - 診斷安裝問題

診斷並修復 Claude Code 的安裝和配置問題。

![诊断安装问题](ref_img/doctor%20-%20%E8%AF%8A%E6%96%AD%E5%AE%89%E8%A3%85%E9%97%AE%E9%A2%98.png)

**常見問題**：
- API 金鑰配置錯誤
- 網路連線問題
- 依賴套件缺失

```bash
claude /doctor
```

### 權限管理

#### `/permissions` - 管理工具權限

管理 Claude Code 可以執行的工具和命令的權限設定。

![管理工具权限](ref_img/permissions%20-%20%E7%AE%A1%E7%90%86%E5%B7%A5%E5%85%B7%E6%9D%83%E9%99%90.png)

![管理工具权限2](ref_img/permissions%20-%20%E7%AE%A1%E7%90%86%E5%B7%A5%E5%85%B7%E6%9D%83%E9%99%902.png)

![管理工具权限3](ref_img/permissions%20-%20%E7%AE%A1%E7%90%86%E5%B7%A5%E5%85%B7%E6%9D%83%E9%99%903.png)

![管理工具权限4](ref_img/permissions%20-%20%E7%AE%A1%E7%90%86%E5%B7%A5%E5%85%B7%E6%9D%83%E9%99%904.png)

**權限類型**：
- **允許**：無條件允許執行
- **詢問**：執行前需使用者確認
- **拒絕**：禁止執行

```bash
claude /permissions
```

**安全建議**：
- 對 `rm -rf` 等高風險命令設為「詢問」或「拒絕」
- 對檔案讀寫操作保持謹慎
- 定期審查權限設定

### 狀態列與介面

#### `/statusline` - 配置狀態列

自訂終端狀態列的顯示內容和格式。

![配置状态栏](ref_img/statusline%20-%20%E9%85%8D%E7%BD%AE%E7%8A%B6%E6%80%81%E6%A0%8F.png)

![配置状态栏2](ref_img/statusline%20-%20%E9%85%8D%E7%BD%AE%E7%8A%B6%E6%80%81%E6%A0%8F2.png)

**可顯示資訊**：
- 當前模型
- Token 使用量
- 會話持續時間
- 網路狀態

```bash
claude /statusline
```

### 其他實用命令

#### `/export` - 匯出對話記錄

將當前會話匯出為 Markdown、JSON 或其他格式。

![导出对话记录](ref_img/export%20-%20%E5%AF%BC%E5%87%BA%E5%AF%B9%E8%AF%9D%E8%AE%B0%E5%BD%95.png)

```bash
claude /export conversation.md
```

#### `/release-notes` - 查看更新日誌

查看 Claude Code 的最新更新和功能變更。

![查看更新日志](ref_img/release-notes%20-%20%E6%9F%A5%E7%9C%8B%E6%9B%B4%E6%96%B0%E6%97%A5%E5%BF%97.png)

```bash
claude /release-notes
```

#### `/review` - 程式碼審查

對指定檔案或目錄進行程式碼審查。

```bash
claude /review ./src/utils.py
```

#### `/security-review` - 安全審查

進行 Convowiz 級別的安全審查，檢查潛在的安全漏洞。

```bash
claude /security-review ./src
```

#### `/hooks` - 管理鉤子配置

配置預執行和後執行鉤子，自動化工作流程。

![管理钩子配置](ref_img/hooks%20-%20%E7%AE%A1%E7%90%86%E9%92%A9%E5%AD%90%E9%85%8D%E7%BD%AE.png)

**鉤子類型**：
- 預執行：在 Claude 執行前運行（如格式化檢查）
- 後執行：在 Claude 執行後運行（如自動測試）

```bash
claude /hooks
```

#### `/vim` - 切換 Vim 模式

切換到 Vim 風格的編輯模式，適用於熟悉 Vim 的使用者。

```bash
claude /vim
```

#### `/terminal-setup` - 配置換行快捷鍵

配置多行輸入的快捷鍵（Windows 使用 Shift+Enter，Linux 使用 \ + Enter）。

![配置换行快捷键](ref_img/terminal-setup%20-%20%E9%85%8D%E7%BD%AE%E6%8D%A2%E8%A1%8C%E5%BF%AB%E6%8D%B7%E9%94%AE%EF%BC%88Shift%2BEnter%EF%BC%89.png)

```bash
claude /terminal-setup
```

> **Linux/WSL 提示**：在 Linux 系統上，您可以直接按 `\` 再按 `Enter` 來換行輸入。

#### `/add-dir` - 添加新工作目錄

將目錄添加到 Claude Code 的上下文範圍。

```bash
claude --add-dir ./src
claude --add-dir ./tests
```

#### `/upgrade` - 升級到 Max 版本

升級到 Claude Code Max 版本，獲得更多功能和更高的 API 配額。

```bash
claude /upgrade
```

#### `/login` - 登入帳號

登入您的 Anthropic 帳號。

```bash
claude /login
```

#### `/logout` - 登出帳號

登出當前帳號。

```bash
claude /logout
```

#### `/migrate-installer` - 遷移安裝方式

遷移不同安裝方式之間的配置和資料。

```bash
claude /migrate-installer
```

#### `/resume` - 恢復對話

恢復之前中斷的對話會話。

```bash
claude /resume session-id
```

#### `/bug` - 提交反饋

 الامارة對問題或提交功能建議。

```bash
claude /bug
```

---

## 功能詳解與使用場景

### 1. 上下文管理：建立 AI 的「心智模型」

#### 為什麼上下文管理很重要？

Claude Code 的核心優勢在於其顯式的上下文管理。與 IDE 內建的工具不同，Claude Code 要求您明確指定哪些檔案和目錄應該被納入上下文，這使得您可以精確控制 AI 對專案的理解。

#### 實作步驟

**步驟 1：初始化專案記憶**

```bash
cd /path/to/your/project
claude /init
```

這會創建 `CLAUDE.md` 檔案，您應該在其中記錄：
- 專案概述和目標
- 技術棧和框架
- 編碼風格和規範
- 架構決策和設計原則
- 常見問題和解決方案

**步驟 2：添加關鍵目錄**

```bash
claude --add-dir ./src
claude --add-dir ./tests
claude --add-dir ./docs
```

**步驟 3：定期更新記憶**

當專案發生重大變更時，使用 `/memory` 命令更新 `CLAUDE.md`：

```bash
claude /memory
```

### 2. 複雜重構：受控的多檔案修改

#### 工作流程：探索 → 規劃 → 編碼 → 驗證

**場景**：需要將專案中的 API 版本從 v1 升級到 v2

```bash
claude
```

**步驟 1：探索（Explore）**

```
請分析 src/api/v1/ 目錄下的所有檔案，找出所有 API 端點的定義和使用方式
```

讓 Claude 先理解現狀，不要急於修改。

**步驟 2：規劃（Plan）**

```
基於剛才的分析，請制定一個詳細的遷移計劃，包括：
1. 需要修改的檔案列表
2. 每個檔案的修改內容
3. 潛在的破壞性變更
4. 回退方案
```

**步驟 3：編碼（Code）**

在審核並批准計劃後：

```
請按照剛才制定的計劃，執行 API v1 到 v2 的遷移，並在每個重要步驟後暫停，等待我的確認
```

**步驟 4：驗證（Verify）**

```
請生成測試腳本來驗證遷移是否成功，確保所有 API 端點都正常工作
```

### 3. 程式碼審查：自動化品質檢查

使用 `/review` 命令進行程式碼審查：

```bash
claude /review ./src/auth.py
```

Claude Code 會檢查：
- 程式碼風格一致性
- 潛在的邏輯錯誤
- 安全漏洞
- 效能問題
- 可維護性

**整合到 CI/CD**：

使用 `/install-github-app` 配置自動化審查，讓每次 PR 都自動觸發程式碼審查。

### 4. 安全審查：主動防禦

```bash
claude /security-review ./src
```

Claude Code 會檢查常見的安全問題：
- SQL 注入漏洞
- XSS 攻擊風險
- 敏感資料洩露
- 不安全的依賴套件
- 權限控制缺陷

---

## 快捷鍵與操作技巧

### 基礎操作快捷鍵

| 快捷鍵 | 功能 | 說明 |
|--------|------|------|
| `Ctrl+C` | 取消當前輸入或中斷生成 | 停止 Claude 正在執行的任務 |
| `Ctrl+D` | 退出當前會話 | 等同於 `/exit` 命令 |
| `Ctrl+L` | 清除終端螢幕 | 不影響對話歷史 |
| `Ctrl+R` | 反向搜尋歷史命令 | 搜尋之前的輸入 |
| `↑` / `↓` | 瀏覽輸入歷史 | 快速重複之前的命令 |
| `Esc + Esc` | 編輯上一條訊息 | 修改最後發送的內容 |
| `Option + Enter` (Mac) | 多行輸入 | 在輸入框中換行 |
| `Shift + Enter` (Windows) | 多行輸入 | 在輸入框中換行 |
| `\ + Enter` (Linux/WSL) | 強制換行 | 在 Linux 系統上換行輸入 |

### 互動模式快捷鍵

| 快捷鍵 | 功能 |
|--------|------|
| `Shift + TAB` | 開啟 Plan 模式（Claude 會先制定計劃） |
| `Shift + TAB` ×2 | 開啟思考模式（顯示 Claude 的思考過程） |
| `! + Bash 命令` | 執行 Bash 命令（例如：`!ls -la`） |
| `## + 內容` | 添加專案記憶（快速更新記憶） |

### Vim 模式快捷鍵

啟用 Vim 模式後（`/vim`），可以使用標準 Vim 快捷鍵：

| 快捷鍵 | 功能 |
|--------|------|
| `Esc` | 退出插入模式 |
| `i` | 進入插入模式（游標位置） |
| `a` | 進入插入模式（游標後一位） |
| `h`/`j`/`k`/`l` | 移動游標（左/下/上/右） |
| `w`/`e`/`b` | 移動單詞位置 |
| `0` / `$` | 移動到行首/行尾 |
| `gg` / `G` | 移動到檔案開頭/末尾 |
| `x` | 刪除當前字元 |
| `dd` | 刪除當前行 |
| `cw` | 修改當前單詞 |

### 高效工作流程技巧

#### 1. 使用 Plan 模式進行複雜任務

在處理複雜任務前，按 `Shift + TAB` 進入 Plan 模式，讓 Claude 先制定詳細計劃，您審核後再執行。

 Cela évite les modifications inattendues et vous donne un contrôle total sur le processus.

#### 2. 批量操作多個檔案

```bash
claude --add-dir ./src --add-dir ./tests
```

一次性添加多個目錄，Claude 會同時考慮所有上下文。

#### 3. 使用 `##` 快速更新記憶

在對話中直接使用 `##` 語法添加記憶，無需打開編輯器：

```
## 專案使用 Python 3.10+，所有字串格式化必須使用 f-string
```

#### 4. 組合使用命令

```bash
claude /compact && claude /context
```

壓縮上下文後立即檢查使用情況。

---

## 上下文管理與記憶系統

### 理解上下文窗口

Claude Code 使用有限的上下文窗口（約 20 萬 tokens，依模型而定）。有效管理上下文是高效使用 Claude Code 的關鍵。

#### 上下文組成

```
總上下文 = 系統提示 + 對話歷史 + 程式碼檔案 + 專案記憶 + 工具輸出
```

#### 監控上下文使用

定期使用 `/context` 檢查：

```bash
claude /context
```

**最佳實踐**：
- 保持上下文使用率在 70% 以下
- 當超過 80% 的名義容量時，使用 `/compact` 壓縮
- 定期清理過時的對話歷史

### 專案記憶（CLAUDE.md）的最佳實踐

#### 記憶檔案結構建議

```markdown
# 專案名稱

## 概述
簡要描述專案的目的和核心功能。

## 技術棧
- Python 3.10+
- FastAPI
- PostgreSQL
- Docker

## 架構原則
1. 所有 API 必須包含完整的 OpenAPI 文檔
2. 資料庫查詢必須使用參數化查詢
3. 所有錯誤必須記錄到集中式日誌系統 grader:gradescope

## 編碼規範
- 使用 Black 進行程式碼格式化
- 類型提示是必需的
- 所有函數必須包含 docstring

## 常見問題
### 問題 1：資料庫連線失敗
解決方案：檢查環境變數 DATABASE_URL 是否正確設定

## API 契約
### 使用者認證
- 端點：POST /api/v1/auth/login
- 請求格式：{ "username": string, "password": string }
- 回應格式：{ "token": string, "expires_in": int }
```

#### 記憶更新策略

1. **初始設定**：使用 `/init` 生成模板後，填入基礎資訊
2. **漸進式更新**：在開發過程中，遇到重要決策時立即更新
3. **定期審查**：每週或每個迭代週期審查一次，移除過時資訊

#### 使用 `/memory` 編輯

```bash
claude /memory
```

這會打開預設編輯器，讓您編輯 `CLAUDE.md`。儲存後，Claude 會自動重新載入。

### 上下文壓縮策略

當上下文接近上限時：

1. **識別冗餘內容**：
   - 重複的程式碼片段
   - 已解決的問題討論
   - 臨時測試程式碼

2. **執行壓縮**：
   ```bash
   claude /compact
   ```

3. **驗證關鍵資訊保留**：
   ```bash
   claude /context
   ```

### 跨會話的狀態持久化

Claude Code 支援透過記憶系統實現跨會話的知識積累：

1. **在會話中學習**：Claude 會在對話中學習專案的特定知識
2. **保存到記憶**：使用 `/memory` 將重要知識持久化
3. **下次會話使用**：新會話會自動載入 Freund 記憶檔案

---

## 整合與擴展

### IDE 整合

#### Visual Studio Code

1. 安裝 Claude Code 擴展
2. 配置設定：

```json
{
  "claude.code.apiKey": "your-api-key",
  "claude.code.model": "claude-3-5-sonnet",
  "claude.code.autoAddDir": true
}
```

3. 使用 `Cmd/Ctrl + Shift + P` 打開命令面板，搜尋 "Claude Code"

#### JetBrains IDE

類似地安裝對應擴展並配置 API 金鑰。

### GitHub Actions 整合

#### 設定自動化程式碼審查

1. 安裝 GitHub App：
```bash
claude /install-github-app
```

2. 在 `.github/workflows/claude-review.yml` 中配置：

```yaml
name: Claude Code Review

on:
  pull_request:
    types: [opened, synchronize]

jobs:
  review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: anthropics/claude-code-action@v1
        with:
          api-key: ${{ secrets.CLAUDE_API_KEY }}
          trigger: '@claude review'
```

3. 在 PR 描述中使用 `@claude review` 觸發審查

### MCP 伺服器整合

#### 添加 GitHub MCP 伺服器

```bash
claude /mcp
```

選擇 "Add Server"，輸入 GitHub MCP 伺服器配置。

#### 自訂 MCP 伺服器

您可以創建自己的 MCP 伺服器來擴展 Claude Code 的功能，例如：
- 連接到內部資料庫
- 整合自訂工具
- 訪問特定的 API

### 鉤子（Hooks）系統

#### 配置預執行鉤子

```bash
claude /hooks
```

**範例：格式化檢查**

```yaml
pre-execute:
  - command: black --check .
    on-failure: warn
```

#### 配置後執行鉤子

**範例：自動執行測試**

```yaml
post-execute:
  - command: pytest tests/
    on-failure: error
```

---

## 最佳實踐與工作流程

### 日常開發工作流程

#### 1. 早晨啟動流程

```bash
# 1. 檢查狀態
claude /status

# 2. 更新專案記憶（如有需要）
claude /memory

# 3. 檢查上下文使用
claude /context

# 4. 開始工作
claude --add-dir ./src
```

#### 2. 新功能開發流程

**階段 1：需求分析**
```
請分析這個功能需求：[描述需求]
找出所有相關的現有程式碼和需要考慮的邊界條件
```

**階段 2：設計規劃**
```
基於分析結果，請制定實現計劃，包括：
1. 需要創建的檔案
2. 需要修改的檔案
3. 需要新增的測試
4. 潛在風險和緩解措施
```

**階段 3：實作**
```
請按照計劃實作功能，並在每個重要里程碑暫停等待確認
```

**階段 4：測試與驗證**
```
請生成完整的單元測試和整合測試
```

#### 3. 重構工作流程

**原則**：小步快跑，頻繁驗證

1. **探索階段**：全面分析需要重構的程式碼
2. **規劃階段**：制定詳細的重構計劃
3. **增量執行**：分小批次進行，每批次後驗證
4. **測試保護**：確保有足夠的測試覆蓋

### 團隊協作最佳實踐

#### 1. 標準化 CLAUDE.md 模板

為團隊創建統一的 `CLAUDE.md` 模板，確保所有成員使用一致的配置。

#### 2. 共享記憶片段

將通用的架構決策和最佳實踐保存在團隊共享的記憶檔案中。

#### 3. 程式碼審查規範

制定使用 Claude Code 進行程式碼審查的標準流程：
- 何時使用自動審查
- 審查標準
- 如何處理審查意見

### 效能優化技巧

#### 1. 精確的上下文範圍

只添加必要的目錄，避免包含：
- `node_modules/`
- `.git/`
- 大型二進制檔案
- 自動生成的檔案

#### 2. 使用適當的模型

- 簡單任務 → `claude-3-haiku`（更快、更便宜）
- 日常開發 → `claude-3-5-sonnet`（平衡）
- 複雜架構 → `claude-3-opus`（最強能力）

#### 3. 批量操作

將相關的請求合併為一個會話，而非多次短會話。

#### 4. 定期清理

定期使用 `/compact` 清理冗餘上下文，保持會話健康。

### 安全最佳實踐

#### 1. API 金鑰管理

- 使用環境變數儲存 API 金鑰
- 永遠不要將 API 金鑰提交到版本控制
- 定期輪換 API 金鑰

#### 2. 權限最小化

使用 `/permissions` 設定嚴格權限：
- 高風險命令設為「詢問」
- 禁止執行破壞性操作
- 定期審查權限設定

#### 3. 程式碼審查

永遠不要直接接受 Claude 生成的程式碼：
- 仔細審查所有變更
- 執行完整的測試套件
- 進行安全審查

#### 4. 敏感資訊保護

- 不要在對話中包含敏感資訊（密碼、API 金鑰等）
- 使用 `.claudeignore` 排除敏感檔案

---

## 常見問題與故障排除

### 安裝與配置問題

#### Q1: 安裝後無法啟動

**症狀**：執行 `claude` 命令無反應或報錯

**解決方案**：
1. 檢查 Node.js/Python 版本是否符合要求
2. 執行 `/doctor` 進行診斷：
   ```bash
   claude /doctor
   ```
3. 檢查網路連線
4. 驗證 API 金鑰是否正確設定

#### Q2: API 金鑰錯誤

**症狀**：提示 "Invalid API key" 或認證失敗

**解決方案**：
1. 確認 API 金鑰格式正確
2. 檢查 API 金鑰是否有足夠的配額
3. 重新登入：
   ```bash
   claude /logout
   claude /login
   ```

### 使用問題

#### Q3: 上下文超出限制

**症狀**：提示 "Context window exceeded"

**解決方案**：
1. 檢查當前使用情況：
   ```bash
   claude /context
   ```
2. 壓縮上下文：
   ```bash
   claude /compact
   ```
3. 移除不必要的目錄
4. 開始新的會話

#### Q4: Claude 生成錯誤的程式碼

**症狀**：生成的程式碼不符合專案規範或包含錯誤

**解決方案**：
1. 檢查 `CLAUDE.md` 是否包含足夠的專案資訊
2. 使用更詳細的提示，明確指定要求
3. 使用 Plan 模式先審核計劃
4. 啟用思考模式（`Shift + TAB` ×2）查看推理過程

#### Q5: 回應速度慢

**症狀**：Claude 回應時間過長

**解決方案**：
1. 切換到更快的模型（如 `claude-3-haiku`）
2. 減少上下文大小
3. 檢查網路連線
4. 使用 `/status` 檢查服務狀態

### 整合問題

#### Q6: IDE 整合不工作

**症狀**：IDE 擴展無法連接到 Claude Code

**解決方案**：
1. 檢查 IDE 擴展是否正確安裝
2. 驗證 API 金鑰配置
3. 檢查擴展日誌
4. 重新載入 IDE

#### Q7: GitHub Actions 整合失敗

**症狀**：自動審查未觸發或失敗

**解決方案**：
1. 檢查 GitHub App 是否正確安裝
2. 驗證工作流程 YAML 語法
3. 檢查 Secrets 配置
4. 查看 GitHub Actions 日誌

### 效能問題

#### Q8: Token 使用量過高

**症狀**：API 成本超出預期

**解決方案**：
1. 使用 `/cost` 監控使用情況
2. 選擇更便宜的模型（如 `claude-3-haiku`）
3. 減少上下文大小
4. 使用 `/compact` 定期清理

#### Q9: 會話變慢

**症狀**：會話時間越長，回應越慢

**解決方案**：
1. 定期使用 `/compact` 壓縮上下文
2. 開始新的會話
3. 移除不必要的歷史記錄

---

## 進階學習路徑

### 初級 → 中級

#### 階段 1：掌握基礎命令（1-2 週）

**目標**：熟練使用所有核心命令

**練習任務**：
1. 完成所有 `/help` 列出的命令體驗
2. 為一個小專案設定完整的記憶系統
3. 執行一次完整的程式碼審查

#### 階段 2：上下文管理（2-3 週）

**目標**：高效管理上下文和記憶

**練習任務**：
1. 為中等規模專案建立完整的 `CLAUDE.md`
2. 執行一次複雜的多檔案重構
3. 實現跨會話的知識積累

### 中級 → 進階

#### 階段 3：工作流程自動化（3-4 週）

**目標**：整合 Claude Code 到開發工作流程

**練習任務**：
1. 設定 GitHub Actions 自動審查
2. 配置鉤子系統實現自動化測試
3. 創建自訂 MCP 伺服器

#### 階段 4：團隊協作（持續）

**目標**：在團隊環境中推廣 Claude Code

**任務**：
1. 制定團隊使用規範
2. 建立共享記憶庫
3. 培訓團隊成員

### 進階 → 專家

#### 階段 5：自訂擴展與整合

**目標**：深度客製化 Claude Code

**學習內容**：
1. MCP 協議深入理解
2. 創建複雜的 MCP 伺服器
3. 整合內部工具和系統

#### 階段 6：最佳實踐貢獻

**目標**：成為 Claude Code 社群貢獻者

**活動**：
1. 分享使用經驗
2. 貢獻開源專案
3. 幫助其他使用者

---

## 附錄

### A. 命令速查表

| 命令 | 功能 | 使用頻率 |
|------|------|----------|
| `/help` | 顯示幫助 | ⭐⭐⭐ |
| `/clear` | 清除對話 | ⭐⭐⭐ |
| `/compact` | 壓縮上下文 | ⭐⭐ |
| `/context` | 查看上下文 | ⭐⭐ |
| `/memory` | 編輯記憶 | ⭐⭐⭐ |
| `/model` | 切換模型 | ⭐⭐ |
| `/review` | 程式碼審查 | ⭐⭐⭐ |
| `/status` | 查看狀態 | ⭐ |
| `/cost` | 查看成本 | ⭐⭐ |
| `/permissions` | 管理權限 | ⭐ |

### B. 推薦資源

#### 官方文檔
- [Claude Code 官方文檔](https://docs.anthropic.com/en/docs/claude-code/overview)
- [Anthropic API 文檔](https://docs.anthropic.com/)

#### 社群資源
- Anthropic Discord 社群
- Reddit r/ClaudeCode
- GitHub Discussions

#### 相關工具
- GitHub Copilot（IDE 整合）
- Gemini CLI（替代 CLI 工具）

### C. 範例 CLAUDE.md 模板

```markdown
# [專案名稱]

## 專案概述
[描述專案的目的、目標用戶、核心功能]

## 技術棧
- **語言**：[Python 3.10+, JavaScript ES2020+, etc.]
- **框架**：[FastAPI, React, etc.]
- **資料庫**：[PostgreSQL, MongoDB, etc.]
- **工具**：[Docker, Kubernetes, etc.]

## 專案結構
```
project/
├── src/          # 主要原始碼
├── tests/        # 測試檔案
├── docs/         # 文檔
└── scripts/      # 腳本
```

## 架構原則
1. [原則 1]
2. [原則 2]
3. [原則 3]

## 編碼規範
- **格式化工具**：[Black, Prettier, etc.]
- **Linter**：[Pylint, ESLint, etc.]
- **類型檢查**：[mypy, TypeScript, etc.]
- **命名約定**：[說明命名規範]

## API 設計規範
- [API 設計原則]
- [錯誤處理標準]
- [認證與授權方式]

## 測試策略
- [單元測試要求]
- [整合測試要求]
- [測試覆蓋率目標]

## 常見問題與解決方案
### 問題 1：[問題描述]
**解決方案**：[解決步驟]

## 部署與運維
- [部署流程]
- [環境配置]
- [監控與日誌]

## 待辦事項與已知問題
- [ ] [待辦項目 1]
- [ ] [待辦項目 2]

## 參考資源
- [相關文檔連結]
- [架構決策記錄]
```

### D. 故障排除檢查清單

#### 安裝問題
- [ ] Node.js/Python 版本符合要求
- [ ] 網路連線正常
- [ ] API 金鑰正確設定
- [ ] 執行 `/doctor` 無錯誤

#### 使用問題
- [ ] 上下文未超出限制
- [ ] 記憶檔案格式正確
- [ ] 權限設定合理
- [ ] 模型選擇適當

#### 整合問題
- [ ] IDE 擴展正確安裝
- [ ] GitHub App 正確配置
- [ ] 工作流程語法正確
- [ ] Secrets 正確設定

---

## 結語

恭喜您完成了 Claude Code 初學者入門白皮書的學習！這份文件涵蓋了從基礎使用到進階應用的完整內容。

### 下一步建議

1. **實踐練習**：選擇一個真實專案，應用所學知識
2. **社群參與**：加入 Claude Code 社群，與其他使用者交流
3. **持續學習**：關注更新日誌（`/release-notes`），學習新功能
4. **分享經驗**：將您的使用經驗分享給團隊和社群

### 記住核心原則

- **顯式優於隱式**：明確指定上下文和需求
- **驗證永遠重要**：永遠審查 AI 生成的程式碼
- **持續改進**：定期更新記憶和配置
- **安全第一**：嚴格管理權限和敏感資訊

祝您使用 Claude Code 愉快，編程效率倍增！

---

**版本**：1.0  
**最後更新**：2025年1月  
**參考資料**：
- [Claude Code 官方文檔](https://docs.anthropic.com/en/docs/claude-code/overview)
- [CSDN：Claude Code 快捷鍵介紹](https://blog.csdn.net/Dontla/article/details/150591506)

---

*本白皮書基於 Claude Code 的最新功能和最佳實踐編寫。如有疑問或建議，歡迎提供反饋。*
