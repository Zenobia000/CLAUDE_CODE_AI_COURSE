# MCP 配置範本庫

## 📦 範本總覽

本目錄提供 **即用型 MCP 配置範本**，涵蓋最常用的 MCP servers 及其組合場景。

### 範本列表

| 範本檔案 | 描述 | 適用場景 | 難度 |
|---------|------|---------|------|
| `github-mcp.json` | GitHub MCP 基礎配置 | 程式碼管理、Issue 追蹤 | ★☆☆ |
| `database-mcp.json` | PostgreSQL/MySQL 配置 | 資料查詢、報表生成 | ★★☆ |
| `slack-notion-mcp.json` | Slack + Notion 整合 | 團隊協作、知識管理 | ★★★ |
| `full-stack-dev.json` | 完整開發環境配置 | 全端開發、DevOps | ★★★★ |

---

## 🚀 快速開始

### Step 1：選擇範本

根據你的需求選擇對應的範本：

**個人開發者**：
- `github-mcp.json`：管理個人專案

**資料分析師**：
- `database-mcp.json`：查詢資料庫資料

**團隊協作**：
- `slack-notion-mcp.json`：自動化通知與文檔管理

**全端工程師**：
- `full-stack-dev.json`：完整的開發工具鏈

### Step 2：複製範本

```bash
# 複製到你的專案目錄
cp mcp_templates/github-mcp.json /path/to/your/project/.claude/mcp-config.json
```

### Step 3：填入你的 API Keys

```json
{
  "mcpServers": {
    "github": {
      "env": {
        "GITHUB_TOKEN": "ghp_YOUR_TOKEN_HERE"  // 替換成你的 token
      }
    }
  }
}
```

### Step 4：重啟 Claude Code

```bash
# CLI
claude

# VSCode Extension
# 重新載入 VSCode 或重啟 Extension
```

---

## 📖 範本詳細說明

### 1. github-mcp.json

**功能**：
- 存取 GitHub repositories
- 管理 issues 和 pull requests
- 查看 commits 和 branches
- 搜尋程式碼

**取得 Token**：
1. 前往 https://github.com/settings/tokens
2. 點擊 "Generate new token (classic)"
3. 選擇 scopes：
   - `repo`（完整存取）
   - `read:user`（讀取用戶資訊）
4. 複製 token

**權限建議**：
- **開發環境**：`repo` + `read:user`
- **生產環境**：只給需要的最小權限

**使用範例**：
```
User: "列出我的所有 repositories"
User: "這個 repo 有哪些 open issues？"
User: "幫我創建一個 issue：修復登入 bug"
```

---

### 2. database-mcp.json

**功能**：
- 執行 SQL 查詢
- 查看 table schema
- 分析資料
- 生成報表

**連線字串格式**：

**PostgreSQL**：
```
postgresql://[user]:[password]@[host]:[port]/[database]
```

**MySQL**：
```
mysql://[user]:[password]@[host]:[port]/[database]
```

**安全建議**：
1. 創建唯讀帳號
2. 只授予 SELECT 權限
3. 限制可存取的 tables
4. 使用 SSL 連線

**創建唯讀帳號**：

```sql
-- PostgreSQL
CREATE USER readonly WITH PASSWORD 'secure_password';
GRANT CONNECT ON DATABASE mydb TO readonly;
GRANT USAGE ON SCHEMA public TO readonly;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO readonly;

-- MySQL
CREATE USER 'readonly'@'%' IDENTIFIED BY 'secure_password';
GRANT SELECT ON mydb.* TO 'readonly'@'%';
FLUSH PRIVILEGES;
```

**使用範例**：
```
User: "查詢最近 7 天的用戶註冊數"
User: "哪些用戶最活躍？"
User: "生成本月的業務報表"
```

---

### 3. slack-notion-mcp.json

**功能組合**：

**Slack MCP**：
- 發送訊息到 channel
- 上傳檔案
- 管理 threads
- 讀取歷史訊息

**Notion MCP**：
- 創建 pages
- 更新內容
- 查詢 database
- 管理 blocks

**取得 Slack Token**：
1. 前往 https://api.slack.com/apps
2. 創建 App
3. 啟用 Bots 功能
4. 安裝 App 到 Workspace
5. 複製 Bot User OAuth Token（以 `xoxb-` 開頭）

**取得 Notion API Key**：
1. 前往 https://www.notion.so/my-integrations
2. 創建 Integration
3. 授權給需要存取的 Pages
4. 複製 Internal Integration Token（以 `secret_` 開頭）

**適用場景**：
- 自動化週報發送
- 會議記錄自動歸檔
- 通知自動儲存
- 知識庫同步

**使用範例**：
```
User: "生成週報並發送到 Slack #engineering，同時儲存到 Notion"
User: "把今天的討論記錄整理成 Notion 頁面"
```

---

### 4. full-stack-dev.json

**完整工具鏈**：
- GitHub MCP（程式碼管理）
- Database MCP（資料存取）
- Slack MCP（團隊通知）
- Notion MCP（文檔管理）
- File System MCP（本地檔案）

**適用場景**：
- 全端開發
- DevOps 自動化
- 企業級專案
- 團隊協作

**環境變數管理**：

```bash
# .env 檔案（不要上傳到 Git！）
GITHUB_TOKEN=ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
POSTGRES_CONNECTION_STRING=postgresql://readonly:password@localhost:5432/mydb
SLACK_BOT_TOKEN=xoxb-your-bot-token
SLACK_TEAM_ID=T01234567
NOTION_API_KEY=secret_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

**載入環境變數**：
```bash
# Linux/Mac
export $(cat .env | xargs)

# Windows
# 手動設定環境變數，或使用 PowerShell：
Get-Content .env | ForEach-Object {
    $name, $value = $_.split('=')
    Set-Item -Path "Env:$name" -Value $value
}
```

**使用範例**：
```
User: "執行完整的 CI/CD 流程：
1. 從 GitHub 獲取最新程式碼
2. 執行測試
3. 查詢 Database 驗證資料
4. 發送結果到 Slack
5. 更新 Notion 文檔"
```

---

## 🔒 安全最佳實踐

### 1. 絕不上傳 API Keys 到 Git

**必須加入 .gitignore**：
```bash
# .gitignore
.claude/mcp-config.json
.env
secrets/
*.key
*.pem
```

### 2. 使用環境變數

**推薦做法**：
```json
{
  "mcpServers": {
    "github": {
      "env": {
        "GITHUB_TOKEN": "${GITHUB_TOKEN}"  // 從環境變數讀取
      }
    }
  }
}
```

### 3. 定期輪換 Token

**建議輪換週期**：
- 生產環境：30-60 天
- 開發環境：90 天
- 個人專案：180 天

### 4. 權限最小化

**原則**：
- 只給必要的權限
- 不給修改權限（如果只需讀取）
- 限制可存取的資源範圍

**範例**：
```sql
-- 只給 SELECT 權限，不給 INSERT/UPDATE/DELETE
GRANT SELECT ON database.* TO 'user'@'host';
```

---

## 🛠️ 故障排除

### 問題 1：MCP 連線失敗

**症狀**：
```
Error: Unable to connect to MCP server
```

**診斷步驟**：
```bash
# 1. 檢查 JSON 格式
cat .claude/mcp-config.json | jq .

# 2. 檢查 MCP server 是否可執行
npx -y @modelcontextprotocol/server-github

# 3. 檢查環境變數
echo $GITHUB_TOKEN

# 4. 測試 API
curl -H "Authorization: token $GITHUB_TOKEN" https://api.github.com/user
```

### 問題 2：授權失敗

**症狀**：
```
Error: 401 Unauthorized
```

**解決方案**：
1. 確認 token 沒有過期
2. 確認 token 有所需的權限
3. 確認 token 格式正確（包含前綴，如 `ghp_`）

### 問題 3：功能找不到

**症狀**：
```
Error: Function 'list_issues' not found
```

**解決方案**：
```bash
# 更新 MCP server 到最新版本
npm update @modelcontextprotocol/server-github

# 重啟 Claude Code
```

---

## 📊 範本比較

| 特性 | GitHub | Database | Slack+Notion | Full Stack |
|-----|--------|----------|--------------|------------|
| **配置複雜度** | 低 | 中 | 高 | 很高 |
| **設定時間** | 5 分鐘 | 10 分鐘 | 15 分鐘 | 30 分鐘 |
| **適用場景** | 程式碼管理 | 資料分析 | 團隊協作 | 全端開發 |
| **MCP 數量** | 1 | 1 | 2 | 5 |
| **權限管理** | 簡單 | 中等 | 複雜 | 很複雜 |
| **維護成本** | 低 | 中 | 中 | 高 |

---

## 🎯 客製化指南

### 新增自訂 MCP

**步驟**：
1. 找到對應的 MCP server（或自己開發）
2. 在 `mcpServers` 加入新的配置
3. 填入必要的環境變數
4. 測試連線

**範例**：新增 Weather API MCP
```json
{
  "mcpServers": {
    "github": { /* 現有配置 */ },
    "weather": {
      "command": "python",
      "args": ["/path/to/weather_mcp_server.py"],
      "env": {
        "WEATHER_API_KEY": "your_api_key"
      }
    }
  }
}
```

### 修改現有配置

**範例**：只允許 File System MCP 存取特定目錄
```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "/home/user/projects",      // 允許的目錄 1
        "/home/user/documents"       // 允許的目錄 2
      ]
    }
  }
}
```

---

## 📚 延伸閱讀

- **MCP 協議深入**：`../理論/6.1_MCP協議深入.md`
- **多代理人編排**：`../理論/6.2_多代理人編排實戰.md`
- **實戰情境**：`../情境題庫/`
- **官方文檔**：https://github.com/anthropics/anthropic-mcp-servers

---

## 🤝 貢獻範本

如果你開發了新的 MCP 配置範本，歡迎貢獻！

**範本要求**：
- 包含詳細的註解
- 提供完整的取得 API key 步驟
- 說明適用場景
- 提供使用範例
- 遵守安全最佳實踐

---

**開始使用這些範本，快速建立你的 MCP 環境！** 🚀

記住：
> 好的配置是自動化的基礎。
> 花時間正確配置一次，之後就能享受自動化的便利。
