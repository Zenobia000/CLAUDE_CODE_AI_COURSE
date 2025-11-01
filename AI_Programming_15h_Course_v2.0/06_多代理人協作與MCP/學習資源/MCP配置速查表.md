# MCP 配置速查表 - 常見 MCP 快速配置參考

## 📋 使用說明

這不是完整文檔，而是**快速配置模板庫**。

**使用情境**：
- ✅ 第一次配置某個 MCP
- ✅ 忘記配置格式需要快速查閱
- ✅ 需要參考安全配置實踐
- ✅ 多 MCP 整合配置

**不適用**：
- ❌ 深入理解 MCP 原理 → 請閱讀 `6.1_MCP協議深入.md`
- ❌ 故障排除 → 請參考 `常見問題解決方案.md`

---

## 配置文件位置

```bash
# 配置檔位置（必須）
.claude/mcp-config.json

# 環境變數檔（可選，推薦）
.env

# ⚠️ 重要：配置後必須重啟 Claude Code
```

---

## 快速配置模板

### 1. GitHub MCP

**適用場景**：存取 GitHub repositories、issues、PRs

```json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_TOKEN": "ghp_your_token_here"
      }
    }
  }
}
```

**Token 權限需求**：
- 最小權限：`public_repo`（公開 repo）
- 私人 repo：`repo`（完整控制）
- Issue 管理：`repo`
- PR 操作：`repo`

**Token 取得**：
```
GitHub Settings → Developer settings → Personal access tokens →
Tokens (classic) → Generate new token
```

**測試指令**：
```
User: "列出我的 GitHub repositories"
User: "創建一個名為 test 的 issue"
```

---

### 2. Database MCP (PostgreSQL)

**適用場景**：查詢、分析資料庫數據

```json
{
  "mcpServers": {
    "database": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-postgres"],
      "env": {
        "DATABASE_URL": "postgresql://username:password@localhost:5432/dbname"
      }
    }
  }
}
```

**🔒 安全最佳實踐**：

**方法 A：只讀帳號（推薦）**
```sql
-- 創建專用只讀帳號
CREATE USER claude_readonly WITH PASSWORD 'secure_password';

-- 僅授予 SELECT 權限
GRANT CONNECT ON DATABASE your_db TO claude_readonly;
GRANT USAGE ON SCHEMA public TO claude_readonly;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO claude_readonly;

-- 未來新表自動授權
ALTER DEFAULT PRIVILEGES IN SCHEMA public
GRANT SELECT ON TABLES TO claude_readonly;
```

**方法 B：使用環境變數**
```json
{
  "mcpServers": {
    "database": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-postgres"],
      "env": {
        "DATABASE_URL": "${DATABASE_URL}"
      }
    }
  }
}
```

配合 `.env` 檔案：
```bash
# .env
DATABASE_URL=postgresql://claude_readonly:secure_password@localhost:5432/mydb
```

**測試指令**：
```
User: "查詢 users 資料表的總數"
User: "分析最近 7 天的訂單趨勢"
```

---

### 3. Database MCP (MySQL)

**適用場景**：MySQL/MariaDB 資料庫操作

```json
{
  "mcpServers": {
    "mysql": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-mysql"],
      "env": {
        "MYSQL_HOST": "localhost",
        "MYSQL_PORT": "3306",
        "MYSQL_USER": "claude_readonly",
        "MYSQL_PASSWORD": "secure_password",
        "MYSQL_DATABASE": "your_database"
      }
    }
  }
}
```

**只讀帳號建立**：
```sql
-- 創建只讀用戶
CREATE USER 'claude_readonly'@'localhost' IDENTIFIED BY 'secure_password';

-- 授予 SELECT 權限
GRANT SELECT ON your_database.* TO 'claude_readonly'@'localhost';

-- 套用權限
FLUSH PRIVILEGES;
```

---

### 4. Slack MCP

**適用場景**：發送通知、讀取訊息、管理 channels

```json
{
  "mcpServers": {
    "slack": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-slack"],
      "env": {
        "SLACK_BOT_TOKEN": "xoxb-your-bot-token",
        "SLACK_USER_TOKEN": "xoxp-your-user-token"
      }
    }
  }
}
```

**Token 取得步驟**：

1. **創建 Slack App**
   - 前往 https://api.slack.com/apps
   - 點擊 "Create New App" → "From scratch"
   - 命名並選擇 workspace

2. **設定權限（OAuth & Permissions）**
   - Bot Token Scopes（必需）：
     - `channels:read`
     - `chat:write`
     - `users:read`
   - User Token Scopes（可選，讀取歷史訊息用）：
     - `channels:history`
     - `search:read`

3. **安裝到 workspace**
   - 點擊 "Install to Workspace"
   - 授權
   - 複製 **Bot User OAuth Token**（xoxb-...）

**測試指令**：
```
User: "發送 'Hello from Claude' 到 #general"
User: "列出所有 channels"
```

---

### 5. Notion MCP

**適用場景**：管理 Notion pages 和 databases

```json
{
  "mcpServers": {
    "notion": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-notion"],
      "env": {
        "NOTION_TOKEN": "secret_your_notion_integration_token"
      }
    }
  }
}
```

**Integration 設定**：

1. **創建 Integration**
   - 前往 https://www.notion.so/my-integrations
   - 點擊 "New integration"
   - 命名（例如：Claude Code Integration）
   - 選擇 workspace

2. **授予權限**
   - 預設權限（Read, Update, Insert）
   - 複製 **Internal Integration Token**

3. **分享頁面給 Integration**
   - 打開要給 Claude 存取的 Notion 頁面
   - 點擊右上角 "Share"
   - 搜尋你的 Integration 名稱
   - 點擊 "Invite"

**測試指令**：
```
User: "列出我的 Notion pages"
User: "在 '每日筆記' database 創建一個新條目"
```

---

### 6. File System MCP

**適用場景**：本地檔案操作（讀取、搜尋、分析）

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem"],
      "env": {
        "ALLOWED_DIRECTORIES": "/path/to/workspace,/path/to/documents"
      }
    }
  }
}
```

**🔒 安全配置**：

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem"],
      "env": {
        "ALLOWED_DIRECTORIES": "/home/user/projects",
        "READONLY": "true"  // 僅允許讀取
      }
    }
  }
}
```

**Windows 路徑**：
```json
"ALLOWED_DIRECTORIES": "C:\\Users\\YourName\\Projects,D:\\Documents"
```

**測試指令**：
```
User: "分析 /path/to/workspace 中所有 Python 檔案"
User: "搜尋包含 'TODO' 的所有檔案"
```

---

## 多 MCP 配置範例

### 範例 1：完整開發環境

```json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_TOKEN": "${GITHUB_TOKEN}"
      }
    },
    "database": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-postgres"],
      "env": {
        "DATABASE_URL": "${DATABASE_URL}"
      }
    },
    "slack": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-slack"],
      "env": {
        "SLACK_BOT_TOKEN": "${SLACK_BOT_TOKEN}"
      }
    },
    "notion": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-notion"],
      "env": {
        "NOTION_TOKEN": "${NOTION_TOKEN}"
      }
    }
  }
}
```

**對應 .env 檔案**：
```bash
# .env（絕不提交到 Git！）
GITHUB_TOKEN=ghp_xxxxxxxxxxxxxxxxxx
DATABASE_URL=postgresql://user:pass@localhost:5432/db
SLACK_BOT_TOKEN=xoxb-xxxxxxxxxxxx
NOTION_TOKEN=secret_xxxxxxxxxxxx
```

**安全檢查清單**：
- [ ] `.env` 已加入 `.gitignore`
- [ ] 資料庫使用只讀帳號
- [ ] Token 僅授予必要權限
- [ ] 定期輪換 tokens
- [ ] 不在配置檔中硬編碼 secrets

---

### 範例 2：知識管理系統

適用情境：團隊知識庫自動化

```json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_TOKEN": "${GITHUB_TOKEN}"
      }
    },
    "notion": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-notion"],
      "env": {
        "NOTION_TOKEN": "${NOTION_TOKEN}"
      }
    },
    "slack": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-slack"],
      "env": {
        "SLACK_BOT_TOKEN": "${SLACK_BOT_TOKEN}"
      }
    },
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem"],
      "env": {
        "ALLOWED_DIRECTORIES": "${WORKSPACE_PATH}"
      }
    }
  }
}
```

**使用情境**：
- GitHub Wiki → Notion 自動同步
- Slack 重要對話 → Notion 歸檔
- 本地文檔 → Notion 統一管理

---

### 範例 3：DevOps 自動化

適用情境：CI/CD 與監控

```json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_TOKEN": "${GITHUB_TOKEN}"
      }
    },
    "database": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-postgres"],
      "env": {
        "DATABASE_URL": "${DATABASE_URL}"
      }
    },
    "slack": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-slack"],
      "env": {
        "SLACK_BOT_TOKEN": "${SLACK_BOT_TOKEN}"
      }
    }
  }
}
```

**自動化工作流程**：
- GitHub PR 創建 → 自動觸發 CI
- 測試失敗 → 分析 Database logs → Slack 警報
- 部署成功 → 更新 Notion 文檔

---

## 環境變數最佳實踐

### ✅ 推薦做法

**1. 使用 .env 檔案**
```bash
# .env
GITHUB_TOKEN=ghp_xxx
DATABASE_URL=postgresql://...
SLACK_BOT_TOKEN=xoxb-...
```

**2. .gitignore 防止洩漏**
```gitignore
# .gitignore
.env
.claude/mcp-config.json
*.secret
secrets/
```

**3. 提供範本檔案**
```bash
# .env.example（可提交到 Git）
GITHUB_TOKEN=your_github_token_here
DATABASE_URL=postgresql://user:password@host:port/database
SLACK_BOT_TOKEN=your_slack_bot_token
NOTION_TOKEN=your_notion_integration_token
```

**4. 團隊協作指南**

在 README.md 加入：
```markdown
## 環境設定

1. 複製環境變數範本：
   ```bash
   cp .env.example .env
   ```

2. 編輯 `.env`，填入你的實際 tokens

3. 重啟 Claude Code
```

---

### ❌ 不要做的事

**1. 硬編碼 Tokens**
```json
❌ "GITHUB_TOKEN": "ghp_actual_token_here"
✅ "GITHUB_TOKEN": "${GITHUB_TOKEN}"
```

**2. 提交 Secrets 到 Git**
```bash
❌ git add .env
❌ git add .claude/mcp-config.json
```

**3. 使用生產環境 Tokens 開發**
```bash
❌ DATABASE_URL=postgresql://admin:prod_password@prod.db
✅ DATABASE_URL=postgresql://readonly:dev_password@localhost
```

**4. 忽略權限最小化**
```bash
❌ 資料庫 admin 權限
✅ 只讀帳號，僅授予 SELECT
```

---

## 故障排除快速檢查

### MCP 配置後沒反應？

```bash
# 1. 檢查檔案是否存在
ls -la .claude/mcp-config.json

# 2. 驗證 JSON 格式
cat .claude/mcp-config.json | jq .

# 3. 檢查環境變數
echo $GITHUB_TOKEN

# 4. 重啟 Claude Code（必須！）
```

### Token 權限不足？

```
Error: 403 Forbidden
→ 檢查 Token 權限範圍
→ 重新生成 Token 並更新配置
→ 重啟 Claude Code
```

### 連線超時？

```
Error: Connection timeout
→ 檢查網路連線
→ 檢查防火牆設定
→ 確認 Database/API 服務是否正常運行
```

**詳細故障排除** → 參考 `常見問題解決方案.md`

---

## 配置驗證清單

在使用 MCP 之前，確認：

- [ ] 配置檔位於正確位置（`.claude/mcp-config.json`）
- [ ] JSON 格式正確（可用 `jq` 驗證）
- [ ] Tokens 有效且權限足夠
- [ ] 環境變數正確設定
- [ ] 敏感資料未硬編碼
- [ ] `.env` 已加入 `.gitignore`
- [ ] 已重啟 Claude Code
- [ ] 測試指令可正常執行

---

## 快速測試指令集

配置完成後，使用以下指令測試：

```
# GitHub MCP
User: "列出我的 GitHub repositories"

# Database MCP
User: "顯示資料庫中的所有表格"

# Slack MCP
User: "列出所有 Slack channels"

# Notion MCP
User: "顯示我的 Notion pages"

# File System MCP
User: "列出 workspace 目錄中的所有 Python 檔案"
```

**如果都成功 → 配置完成！🎉**

---

## 下一步

- **遇到問題？** → 查閱 `常見問題解決方案.md`
- **需要更複雜的工作流程？** → 參考 `工作流程編排模式庫.md`
- **想了解安全最佳實踐？** → 閱讀 `安全與治理檢查清單.md`
- **實戰案例？** → 查看 `情境題庫/` 中的實作範例

---

**提醒**：
> 配置 MCP 只是開始
> 真正的價值在於工作流程編排
> 繼續探索情境題庫中的實戰案例！

**安全第一**：
> 永遠不要在程式碼中硬編碼 secrets
> 使用環境變數 + .gitignore
> 權限最小化原則
