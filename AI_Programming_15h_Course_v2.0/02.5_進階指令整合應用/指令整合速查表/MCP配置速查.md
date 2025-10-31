# MCP 配置速查表

## 🌐 MCP (Model Context Protocol) 概述

MCP 讓 Claude Code 能夠與外部系統和工具進行無縫整合，是平台能力的核心基礎。

---

## 🚀 快速啟動

### 基本 MCP 指令
```bash
claude --mcp-list           # 列出已配置的 MCP servers
claude --mcp-check          # 檢查 MCP 配置狀態
claude --mcp-reset          # 重置 MCP 配置
claude --mcp-help           # MCP 幫助資訊
```

### 配置檔案位置
```bash
# 主配置檔案
~/.config/claude/config.json

# 備份位置
~/.claude/mcp_config.json
```

---

## 📁 檔案系統 MCP

### 基本配置
```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem"],
      "env": {
        "HOME": "${HOME}"
      }
    }
  }
}
```

### 常用操作
```bash
# 檔案瀏覽
"請列出 ./src 目錄下的所有檔案"

# 檔案讀取
"讀取 config.yaml 的內容"

# 檔案創建
"在 ./docs 目錄下創建 API.md 檔案"

# 檔案搜尋
"搜尋包含 'TODO' 的所有 Python 檔案"

# 目錄操作
"創建專案目錄結構：
src/
├── api/
├── models/
└── utils/"
```

### 安全設定
```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem"],
      "env": {
        "HOME": "${HOME}",
        "ALLOWED_PATHS": "/home/user/projects,/tmp",
        "DENIED_PATHS": "/etc,/root"
      }
    }
  }
}
```

---

## 🔍 網路搜尋 MCP

### 基本配置
```json
{
  "mcpServers": {
    "search": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-search"],
      "env": {
        "SEARCH_API_KEY": "${SEARCH_API_KEY}"
      }
    }
  }
}
```

### 常用搜尋操作
```bash
# 技術資訊搜尋
"搜尋 'Python 3.12 新功能'"

# 程式設計問題
"搜尋 'FastAPI vs Flask 效能比較'"

# 官方文檔
"搜尋 'Claude Code MCP 官方文檔'"

# 最新資訊
"搜尋 2024 年最新的 JavaScript 框架趨勢"
```

### 搜尋策略
```bash
# 精確搜尋
"搜尋確切的錯誤訊息：'TypeError: unsupported operand'"

# 範圍搜尋
"在 GitHub 上搜尋 Python 的機器學習專案"

# 時間範圍
"搜尋最近一年內的 React 18 教學"
```

---

## 💾 資料庫 MCP

### PostgreSQL 配置
```json
{
  "mcpServers": {
    "postgres": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-postgres"],
      "env": {
        "POSTGRES_CONNECTION_STRING": "postgresql://user:password@localhost:5432/dbname"
      }
    }
  }
}
```

### SQLite 配置
```json
{
  "mcpServers": {
    "sqlite": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-sqlite"],
      "env": {
        "SQLITE_DB_PATH": "./data/app.db"
      }
    }
  }
}
```

### 資料庫操作範例
```bash
# 查詢資料
"查詢 users 表中的所有記錄"

# 複雜查詢
"查詢過去一週內註冊的活躍用戶"

# 資料分析
"分析訂單表的月度趨勢"

# 結構查詢
"顯示 products 表的結構"
```

---

## 🐙 GitHub MCP

### 基本配置
```json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "${GITHUB_TOKEN}"
      }
    }
  }
}
```

### GitHub 操作
```bash
# Repository 資訊
"獲取 myproject repository 的基本資訊"

# Issues 管理
"列出所有開放的 issues"
"創建新 issue：修復登入問題"

# Pull Requests
"檢查待審查的 PR"
"創建 PR 將 feature-branch 合併到 main"

# 程式碼檢索
"搜尋 repository 中包含 'authentication' 的檔案"

# 統計資訊
"獲取過去一個月的提交統計"
```

---

## 💬 Slack MCP

### 基本配置
```json
{
  "mcpServers": {
    "slack": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-slack"],
      "env": {
        "SLACK_BOT_TOKEN": "${SLACK_BOT_TOKEN}",
        "SLACK_APP_TOKEN": "${SLACK_APP_TOKEN}"
      }
    }
  }
}
```

### Slack 操作
```bash
# 發送訊息
"發送訊息到 #dev-team 頻道：部署完成"

# 檔案分享
"分享 report.pdf 到 #general 頻道"

# 狀態更新
"更新我的狀態為：正在開發新功能"

# 頻道管理
"列出所有可用的頻道"
```

---

## 📧 Email MCP

### 基本配置
```json
{
  "mcpServers": {
    "email": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-email"],
      "env": {
        "EMAIL_PROVIDER": "gmail",
        "EMAIL_USERNAME": "${EMAIL_USERNAME}",
        "EMAIL_PASSWORD": "${EMAIL_APP_PASSWORD}"
      }
    }
  }
}
```

### Email 操作
```bash
# 檢查郵件
"檢查最新的 10 封郵件"

# 發送郵件
"發送郵件給團隊：專案進度更新"

# 郵件搜尋
"搜尋包含 '發票' 的郵件"

# 附件處理
"下載最新郵件的附件"
```

---

## 🔧 自訂 MCP Server

### 基本結構
```python
# custom_mcp_server.py
from mcp import Server, types
import asyncio

server = Server("custom-tool")

@server.list_tools()
async def list_tools() -> list[types.Tool]:
    return [
        types.Tool(
            name="custom_function",
            description="自訂功能說明",
            inputSchema={
                "type": "object",
                "properties": {
                    "param": {"type": "string"}
                }
            }
        )
    ]

@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[types.TextContent]:
    if name == "custom_function":
        result = custom_logic(arguments["param"])
        return [types.TextContent(type="text", text=result)]

if __name__ == "__main__":
    asyncio.run(server.run())
```

### 配置自訂 MCP
```json
{
  "mcpServers": {
    "custom": {
      "command": "python",
      "args": ["./custom_mcp_server.py"],
      "env": {
        "CUSTOM_CONFIG": "value"
      }
    }
  }
}
```

---

## 🔄 MCP 工作流程整合

### 多 MCP 協作範例
```bash
# 完整的專案報告流程
"請執行以下工作流程：
1. 使用 GitHub MCP 獲取專案統計
2. 使用檔案系統 MCP 分析程式碼結構
3. 使用搜尋 MCP 查找相關最佳實踐
4. 整合所有資訊生成專案報告
5. 使用 Slack MCP 發送報告給團隊"
```

### 資料處理管線
```bash
# 資料收集到分析的完整流程
"建立資料處理管線：
1. 從資料庫 MCP 提取原始資料
2. 使用檔案系統 MCP 保存處理結果
3. 使用 Email MCP 發送分析報告
4. 使用 GitHub MCP 更新專案文檔"
```

---

## ⚠️ 故障排除

### 常見錯誤

#### 1. MCP Server 啟動失敗
```bash
錯誤：Connection refused

解決方案：
1. 檢查 Node.js 是否已安裝
   node --version

2. 檢查 MCP server 套件
   npm list -g | grep @modelcontextprotocol

3. 重新安裝
   npm install -g @modelcontextprotocol/server-filesystem
```

#### 2. 認證失敗
```bash
錯誤：Authentication failed

解決方案：
1. 檢查環境變數
   echo $GITHUB_TOKEN

2. 驗證權限
   curl -H "Authorization: token $GITHUB_TOKEN" https://api.github.com/user

3. 重新生成 Token
```

#### 3. 權限問題
```bash
錯誤：Permission denied

解決方案：
1. 檢查檔案權限
   ls -la ~/.config/claude/

2. 修正權限
   chmod 600 ~/.config/claude/config.json

3. 檢查目錄權限
   chmod 755 ~/.config/claude/
```

### 診斷指令
```bash
# 檢查 MCP 狀態
claude --mcp-check

# 檢查配置檔案
cat ~/.config/claude/config.json | jq .

# 測試特定 MCP
claude --mcp-test filesystem

# 查看錯誤日誌
cat ~/.claude/logs/mcp.log
```

---

## 🛡️ 安全最佳實踐

### 1. API Key 管理
```bash
# 使用環境變數
export GITHUB_TOKEN="your_token_here"
export SLACK_BOT_TOKEN="xoxb-your-token"

# 配置檔案中使用變數引用
"GITHUB_PERSONAL_ACCESS_TOKEN": "${GITHUB_TOKEN}"
```

### 2. 權限最小化
```json
{
  "mcpServers": {
    "filesystem": {
      "env": {
        "ALLOWED_PATHS": "/home/user/projects",
        "MAX_FILE_SIZE": "10MB",
        "READONLY_MODE": "false"
      }
    }
  }
}
```

### 3. 網路安全
```json
{
  "mcpServers": {
    "search": {
      "env": {
        "ALLOWED_DOMAINS": "github.com,stackoverflow.com",
        "RATE_LIMIT": "100/hour"
      }
    }
  }
}
```

---

## 📊 MCP 效能監控

### 效能指標
```bash
# 查看 MCP 效能統計
claude --mcp-stats

# 常見指標
- 連接時間
- 請求回應時間
- 錯誤率
- 資源使用量
```

### 優化建議
```bash
# 連接池配置
"MAX_CONNECTIONS": "10"

# 快取設定
"CACHE_TTL": "300"

# 超時設定
"REQUEST_TIMEOUT": "30"
```

---

## 🔗 社群 MCP Servers

### 官方 MCP Servers
- `@modelcontextprotocol/server-filesystem` - 檔案系統操作
- `@modelcontextprotocol/server-github` - GitHub 整合
- `@modelcontextprotocol/server-postgres` - PostgreSQL 資料庫
- `@modelcontextprotocol/server-sqlite` - SQLite 資料庫
- `@modelcontextprotocol/server-slack` - Slack 整合

### 社群 MCP Servers
- `mcp-server-notion` - Notion 整合
- `mcp-server-jira` - JIRA 專案管理
- `mcp-server-docker` - Docker 容器管理
- `mcp-server-aws` - AWS 服務整合

### 安裝社群 MCP
```bash
# 從 npm 安裝
npm install -g mcp-server-notion

# 從 GitHub 安裝
git clone https://github.com/user/custom-mcp-server
cd custom-mcp-server
npm install
npm run build
```

---

## 🎯 MCP 使用最佳實踐

### 1. 漸進式配置
```bash
# 第一步：配置基礎 MCP
- filesystem (檔案操作)
- search (資訊搜尋)

# 第二步：添加開發工具
- github (版本控制)
- database (資料存取)

# 第三步：整合團隊工具
- slack (團隊溝通)
- email (外部溝通)
```

### 2. 工作流程設計
```bash
# 設計 MCP 使用流程
1. 資料收集 (search, github)
2. 資料處理 (database, filesystem)
3. 結果分享 (slack, email)
```

### 3. 監控和維護
```bash
# 定期檢查
- 每週檢查 MCP 連接狀態
- 每月更新 MCP servers
- 每季度檢視使用統計
```

---

**最後更新**：2025年1月
**版本**：v1.0
**維護者**：Claude Code 課程團隊

---

## 🔗 相關速查表

- [Agent使用速查](./Agent使用速查.md) - Agent 專家系統
- [輸出風格速查](./輸出風格速查.md) - 格式控制
- [常用組合模式](./常用組合模式.md) - 工作流程範本
- [問題排查速查](./問題排查速查.md) - 故障診斷