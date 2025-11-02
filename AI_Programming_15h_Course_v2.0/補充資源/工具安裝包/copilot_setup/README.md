# GitHub Copilot 安裝與配置指南

> AI 程式碼補全助手完整設定教學

---

## 📋 前置要求

### 系統要求
- **GitHub 帳號**: 需要有效的 GitHub 帳號
- **訂閱方案**: Copilot Individual、Business 或 Enterprise
- **IDE**: VS Code、JetBrains IDE、Neovim 或 Visual Studio

### 訂閱選項

| 方案 | 價格 | 適用對象 |
|------|------|---------|
| **Individual** | $10/月 或 $100/年 | 個人開發者 |
| **Business** | $19/月/用戶 | 企業團隊 |
| **Enterprise** | 客製報價 | 大型組織 |
| **免費試用** | 30 天 | 首次使用者 |
| **學生/教師** | 免費 | 經驗證的學生/教師 |

---

## 🎓 學生免費方案

### 申請步驟

1. **驗證學生身份**
   - 前往 [GitHub Education](https://education.github.com/)
   - 點擊 **Get benefits**
   - 上傳學生證或在學證明
   - 等待驗證（通常 1-3 天）

2. **啟用 Copilot**
   - 驗證通過後，前往 [GitHub Copilot](https://github.com/features/copilot)
   - 點擊 **Start free trial**
   - 選擇 **Education** 方案

3. **確認啟用**
   - 檢查 [Settings > Copilot](https://github.com/settings/copilot)
   - 狀態應顯示 **Active**

---

## 🚀 安裝步驟

### VS Code 安裝（推薦）

#### 1. 安裝擴充套件

```bash
# 方法 1: 透過 VS Code Marketplace
# 1. 開啟 VS Code
# 2. 按 Ctrl+Shift+X (Windows/Linux) 或 Cmd+Shift+X (macOS)
# 3. 搜尋 "GitHub Copilot"
# 4. 點擊 Install

# 方法 2: 使用指令列
code --install-extension GitHub.copilot
code --install-extension GitHub.copilot-chat
```

#### 2. 登入 GitHub 帳號

1. 安裝完成後，VS Code 右下角會提示登入
2. 點擊 **Sign in to GitHub**
3. 瀏覽器會開啟授權頁面
4. 點擊 **Authorize GitHub Copilot**
5. 返回 VS Code，確認已登入

#### 3. 驗證安裝

1. 開啟任何程式碼檔案（如 `.js`, `.py`）
2. 開始輸入註解或程式碼
3. 應該會看到灰色的建議文字
4. 按 **Tab** 接受建議

---

### JetBrains IDE 安裝

支援的 IDE：
- IntelliJ IDEA
- PyCharm
- WebStorm
- PhpStorm
- GoLand
- Rider

#### 安裝步驟

1. **開啟 IDE**
2. **前往 Settings/Preferences**
   - Windows/Linux: `File > Settings`
   - macOS: `IntelliJ IDEA > Preferences`

3. **安裝外掛**
   - 選擇 `Plugins`
   - 搜尋 `GitHub Copilot`
   - 點擊 `Install`
   - 重啟 IDE

4. **登入 GitHub**
   - 重啟後會提示登入
   - 按照指示完成授權

---

### Neovim 安裝（進階）

#### 使用 vim-plug

```vim
" 在 init.vim 或 .vimrc 中加入
Plug 'github/copilot.vim'

" 安裝
:PlugInstall
```

#### 使用 packer.nvim

```lua
-- 在 packer 配置中加入
use 'github/copilot.vim'

-- 安裝
:PackerSync
```

#### 設定與登入

```vim
" 登入 GitHub
:Copilot setup

" 啟用 Copilot
:Copilot enable
```

---

## 🔧 基本配置

### VS Code 設定

#### 開啟 Settings.json

按 `Ctrl+Shift+P` (Windows/Linux) 或 `Cmd+Shift+P` (macOS)，輸入 **Preferences: Open Settings (JSON)**

#### 推薦配置

```json
{
  // Copilot 基本設定
  "github.copilot.enable": {
    "*": true,
    "yaml": false,
    "plaintext": false,
    "markdown": false
  },

  // 啟用 Copilot Chat
  "github.copilot.chat.enabled": true,

  // 建議觸發設定
  "editor.inlineSuggest.enabled": true,
  "editor.quickSuggestions": {
    "comments": false,
    "strings": true,
    "other": true
  },

  // 自動補全延遲（毫秒）
  "editor.quickSuggestionsDelay": 10,

  // 顯示多個建議選項
  "github.copilot.editor.enableAutoCompletions": true
}
```

---

## 🎯 基本使用

### 接受建議

| 操作 | Windows/Linux | macOS |
|------|---------------|-------|
| **接受整個建議** | `Tab` | `Tab` |
| **接受單字** | `Ctrl + →` | `Cmd + →` |
| **下一個建議** | `Alt + ]` | `Option + ]` |
| **上一個建議** | `Alt + [` | `Option + [` |
| **開啟 Copilot** | `Ctrl + Enter` | `Cmd + Enter` |

### Copilot Chat（對話模式）

| 操作 | 快捷鍵 (Windows/Linux) | 快捷鍵 (macOS) |
|------|----------------------|----------------|
| **開啟 Chat** | `Ctrl + Shift + I` | `Cmd + Shift + I` |
| **快速提問** | `Ctrl + I` | `Cmd + I` |

---

## 💡 使用技巧

### 技巧 1: 撰寫有效的註解

**❌ 不好的註解**:
```python
# function
def process():
    pass
```

**✅ 好的註解**:
```python
# Parse JSON configuration file and validate required fields
# Returns: dict with validated config or raises ValueError
def parse_config(file_path: str) -> dict:
    # Copilot 會生成完整的實作
```

### 技巧 2: 使用範例引導

```javascript
// Example: convert date string to ISO format
// Input: "2024-01-15" -> Output: "2024-01-15T00:00:00.000Z"
function formatDate(dateString) {
    // Copilot 會根據範例生成正確的轉換邏輯
}
```

### 技巧 3: 逐步引導複雜邏輯

```python
class UserAuthentication:
    """
    Handle user authentication with JWT tokens

    Features:
    - Login with email/password
    - Generate JWT token
    - Validate token
    - Refresh expired tokens
    """

    def __init__(self, secret_key: str):
        # Copilot 會生成建構函數

    def login(self, email: str, password: str) -> dict:
        # Step 1: Validate email format
        # Step 2: Check user exists in database
        # Step 3: Verify password hash
        # Step 4: Generate JWT token
        # Step 5: Return token and user info
        pass
```

### 技巧 4: 利用 Copilot Chat

**程式碼解釋**:
```
選取程式碼 → 右鍵 → Copilot → Explain This
```

**產生測試**:
```
選取函數 → 右鍵 → Copilot → Generate Tests
```

**修正錯誤**:
```
選取錯誤程式碼 → 右鍵 → Copilot → Fix This
```

---

## 🛠️ 進階設定

### 排除特定檔案或目錄

建立 `.copilotignore` 檔案：

```
# 排除敏感資料
.env
secrets.json
*.key

# 排除設定檔
*.config.js
webpack.config.js

# 排除測試資料
test/fixtures/
__mocks__/
```

### 自訂語言支援

```json
{
  "github.copilot.advanced": {
    "length": 500,
    "temperature": "",
    "top_p": 1,
    "stops": {
      "*": ["\n\n\n"]
    },
    "indentationMode": {
      "python": true,
      "javascript": false
    }
  }
}
```

### 團隊策略設定（Enterprise）

```json
{
  "github.copilot.inlineSuggest.enable": true,
  "github.copilot.advanced": {
    "authProvider": "github-enterprise",
    "allowedOrganizations": ["your-org"]
  }
}
```

---

## 🐛 常見問題排解

### 問題 1: 無法登入

**症狀**: 點擊登入後無反應

**解決方法**:
1. 檢查網路連線
2. 清除 VS Code 快取：
   ```bash
   # Windows
   rd /s /q %APPDATA%\Code\Cache

   # macOS/Linux
   rm -rf ~/.vscode/extensions/github.copilot-*
   ```
3. 重新安裝擴充套件

### 問題 2: 沒有建議出現

**症狀**: 輸入程式碼沒有任何建議

**解決方法**:
1. 檢查 Copilot 狀態（右下角圖示）
2. 確認檔案類型是否支援
3. 檢查設定：
   ```json
   {
     "editor.inlineSuggest.enabled": true,
     "github.copilot.enable": {
       "*": true
     }
   }
   ```

### 問題 3: 建議品質不佳

**症狀**: 建議的程式碼不符合需求

**解決方法**:
1. 改善註解描述（更具體、更詳細）
2. 提供範例輸入/輸出
3. 使用 Copilot Chat 進行對話式互動
4. 在檔案頂部提供上下文註解

### 問題 4: 訂閱過期

**症狀**: `Your Copilot subscription has expired`

**解決方法**:
1. 前往 [GitHub Billing](https://github.com/settings/billing)
2. 檢查訂閱狀態
3. 更新付款方式或重新訂閱

---

## 📊 使用統計與監控

### 查看使用情況

1. **VS Code 狀態列**
   - 右下角 Copilot 圖示
   - 點擊查看今日接受/拒絕建議數

2. **GitHub Dashboard**
   - 前往 [GitHub Settings > Copilot](https://github.com/settings/copilot)
   - 查看詳細使用統計

### 效能監控

```json
{
  "github.copilot.advanced": {
    "debug.overrideEngine": "copilot-codex",
    "debug.showScores": true,
    "debug.testOverrideProxyUrl": ""
  }
}
```

---

## 🔐 安全性與隱私

### 資料隱私政策

1. **程式碼片段收集**
   - Copilot 會收集上下文程式碼用於建議
   - 僅在當前工作階段使用
   - 不會儲存在 GitHub 伺服器

2. **組織設定**（Business/Enterprise）
   ```
   允許管理員控制：
   - 是否允許使用 Copilot
   - 是否收集遙測資料
   - 是否允許公開程式碼建議
   ```

3. **隱私保護**
   - 敏感檔案加入 `.copilotignore`
   - 使用組織級別的存取控制
   - 定期審查建議程式碼

### 最佳實踐

```markdown
✅ DO:
- 審查所有 Copilot 建議的程式碼
- 在敏感專案中排除機密檔案
- 理解建議程式碼的運作原理
- 使用 Copilot 作為輔助工具，非替代品

❌ DON'T:
- 直接接受所有建議而不審查
- 在包含機密資料的檔案中使用
- 依賴 Copilot 處理安全性關鍵邏輯
- 忽視程式碼品質和測試
```

---

## 📚 學習資源

### 官方資源
- [GitHub Copilot 官方文檔](https://docs.github.com/copilot)
- [Copilot Labs](https://githubnext.com/projects/copilot-labs/)
- [使用案例展示](https://github.com/features/copilot#examples)

### 社群資源
- [Copilot Discord](https://discord.gg/github)
- [GitHub Community Forum](https://github.community/)
- [YouTube 教學頻道](https://www.youtube.com/github)

### 進階學習
- **提示工程技巧** (Prompt Engineering)
- **AI 輔助 TDD** (Test-Driven Development with AI)
- **程式碼審查工作流程** (Code Review Workflow)

---

## 🔄 更新與維護

### 檢查更新

```bash
# VS Code 會自動更新擴充套件
# 手動檢查：Extensions 面板 → 更新按鈕

# 檢查 Copilot 版本
code --list-extensions --show-versions | grep copilot
```

### 解除安裝

```bash
# VS Code
code --uninstall-extension GitHub.copilot
code --uninstall-extension GitHub.copilot-chat

# 清除快取
# Windows
rd /s /q %APPDATA%\Code\User\globalStorage\github.copilot

# macOS/Linux
rm -rf ~/.config/Code/User/globalStorage/github.copilot
```

---

## 💰 費用管理

### 訂閱管理

1. **查看當前訂閱**
   - [GitHub Settings > Billing](https://github.com/settings/billing)

2. **取消訂閱**
   - Billing 頁面 → Copilot → Cancel subscription
   - 可使用到當前計費週期結束

3. **變更方案**
   - Individual ↔ Business 可隨時切換
   - 按比例計費

---

**安裝完成後，請參考課程 Module 2 學習如何有效使用 GitHub Copilot！** 🚀
