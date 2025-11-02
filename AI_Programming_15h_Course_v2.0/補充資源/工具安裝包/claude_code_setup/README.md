# Claude Code 安裝與配置指南

> Claude Code CLI 工具完整安裝步驟

---

## 📋 前置要求

### 系統要求
- **作業系統**: Windows 10/11, macOS, Linux
- **Node.js**: 18.x 或更高版本
- **Claude 帳號**: 需要有效的 Anthropic 帳號

### 檢查環境

```bash
# 檢查 Node.js 版本
node --version

# 檢查 npm 版本
npm --version
```

---

## 🚀 安裝步驟

### 方法 1: NPM 安裝（推薦）

```bash
# 全域安裝 Claude Code
npm install -g @anthropic-ai/claude-code

# 驗證安裝
claude --version
```

### 方法 2: 使用 npx（無需全域安裝）

```bash
# 直接使用 npx 執行
npx @anthropic-ai/claude-code

# 首次使用會自動下載
```

---

## 🔑 設定 API Key

### 取得 API Key

1. 前往 [Anthropic Console](https://console.anthropic.com/)
2. 登入或註冊帳號
3. 導航至 **API Keys** 頁面
4. 點擊 **Create Key** 建立新的 API Key
5. 複製並安全保存此 Key

### 配置 API Key

**方法 1: 環境變數（推薦）**

```bash
# Windows (PowerShell)
$env:ANTHROPIC_API_KEY="your-api-key-here"

# Windows (CMD)
set ANTHROPIC_API_KEY=your-api-key-here

# macOS/Linux (Bash)
export ANTHROPIC_API_KEY="your-api-key-here"
```

**方法 2: .env 檔案**

在專案根目錄建立 `.env` 檔案：

```env
ANTHROPIC_API_KEY=your-api-key-here
```

**方法 3: 使用 `claude login` 指令**

```bash
# 互動式登入
claude login

# 按照提示輸入 API Key
```

---

## ✅ 驗證安裝

```bash
# 檢查版本
claude --version

# 檢查連線狀態
claude status

# 執行簡單測試
claude "Hello, Claude!"
```

預期輸出：

```
Claude Code v1.x.x
Connected to Claude API
Model: claude-sonnet-4-5
```

---

## 🛠️ 基本配置

### 設定預設模型

```bash
# 設定使用 Sonnet 4.5 (推薦)
claude config set model claude-sonnet-4-5

# 查看當前配置
claude config list
```

### 設定工作目錄

```bash
# 設定預設專案目錄
claude config set workspace ~/projects

# 查看配置
claude config get workspace
```

### 設定 Proxy（如需要）

```bash
# 設定 HTTP Proxy
claude config set proxy http://proxy.example.com:8080

# 設定 HTTPS Proxy
claude config set https-proxy https://proxy.example.com:8443
```

---

## 🔧 進階設定

### 自訂 CLAUDE.md

在專案根目錄建立 `CLAUDE.md` 檔案：

```markdown
# Project Instructions for Claude

## Project Overview
This is a [project description].

## Code Style
- Use TypeScript
- Follow ESLint rules
- Write tests for all features

## Commands
- `npm run dev`: Start development server
- `npm run build`: Build for production
```

### 設定 .claudeignore

類似 `.gitignore`，排除不需要 Claude 分析的檔案：

```
# .claudeignore
node_modules/
dist/
build/
*.log
.env
```

---

## 🎯 快速開始範例

### 範例 1: 程式碼審查

```bash
# 進入專案目錄
cd ~/projects/my-app

# 要求 Claude 審查程式碼
claude "Review the codebase and suggest improvements"
```

### 範例 2: 生成測試

```bash
# 為特定檔案生成測試
claude "Generate unit tests for src/utils/auth.ts"
```

### 範例 3: 除錯協助

```bash
# 分析錯誤
claude "Debug the error in logs/error.log"
```

---

## 🐛 常見問題排解

### 問題 1: API Key 無效

**症狀**: `Error: Invalid API key`

**解決方法**:
1. 檢查 API Key 是否正確複製（無多餘空格）
2. 確認 API Key 尚未過期
3. 重新生成新的 API Key

### 問題 2: 網路連線錯誤

**症狀**: `Error: Network timeout`

**解決方法**:
```bash
# 檢查網路連線
ping api.anthropic.com

# 設定 Proxy（如在公司網路）
claude config set proxy http://proxy.company.com:8080

# 增加 timeout 時間
claude config set timeout 60000
```

### 問題 3: 指令找不到

**症狀**: `'claude' is not recognized`

**解決方法**:
```bash
# Windows: 檢查環境變數 PATH
echo %PATH%

# macOS/Linux: 檢查 PATH
echo $PATH

# 重新安裝
npm uninstall -g @anthropic-ai/claude-code
npm install -g @anthropic-ai/claude-code
```

### 問題 4: 權限不足（Windows）

**症狀**: `Error: EPERM operation not permitted`

**解決方法**:
```powershell
# 以管理員身份執行 PowerShell
# 設定執行政策
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# 重新安裝
npm install -g @anthropic-ai/claude-code
```

---

## 📚 學習資源

### 官方文檔
- [Claude Code 官方文檔](https://docs.anthropic.com/claude-code)
- [API 參考文檔](https://docs.anthropic.com/api)

### 教學影片
- 官方快速入門影片
- 社群教學資源

### 社群資源
- [Claude Code GitHub](https://github.com/anthropics/claude-code)
- [Discord 社群](https://discord.gg/anthropic)
- [論壇討論](https://community.anthropic.com/)

---

## 🔄 更新與維護

### 檢查更新

```bash
# 檢查是否有新版本
npm outdated -g @anthropic-ai/claude-code

# 更新到最新版本
npm update -g @anthropic-ai/claude-code
```

### 解除安裝

```bash
# 解除安裝 Claude Code
npm uninstall -g @anthropic-ai/claude-code

# 清除配置檔案（可選）
rm -rf ~/.claude
```

---

## 💡 使用技巧

### 技巧 1: 使用 .claude/ 目錄組織提示詞

```
project/
├── .claude/
│   ├── commands/
│   │   ├── review.md       # /review 指令
│   │   └── test.md         # /test 指令
│   └── CLAUDE.md           # 專案級指令
```

### 技巧 2: 搭配 Git Hooks

```bash
# .git/hooks/pre-commit
#!/bin/bash
claude "Review staged changes and check for issues"
```

### 技巧 3: 整合到 CI/CD

```yaml
# .github/workflows/claude-review.yml
name: Claude Code Review
on: [pull_request]
jobs:
  review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run Claude Review
        run: npx @anthropic-ai/claude-code "Review this PR"
```

---

## 🔐 安全性建議

1. **絕不提交 API Key 到版本控制**
   - 使用環境變數
   - 確保 `.env` 在 `.gitignore` 中

2. **定期輪換 API Key**
   - 每 90 天更換一次
   - 懷疑洩漏時立即更換

3. **限制 API Key 權限**
   - 僅授予必要的權限
   - 為不同專案使用不同 Key

4. **監控使用情況**
   - 定期檢查 API 使用量
   - 設定使用上限警告

---

**安裝完成後，請參考課程 Module 2 開始學習 Claude Code 的核心功能！** 🚀
