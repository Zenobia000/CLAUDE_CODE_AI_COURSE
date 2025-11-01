# B03: 配置 Slack MCP - AI 自動發送通知

## 📋 情境描述

### 你遇到的問題

團隊用 Slack 溝通，你需要發送各種通知：
- 建置完成通知
- 部署狀態更新
- 錯誤警報
- 每日報表

**手動發送的痛苦**：
1. 打開 Slack
2. 找到對應的 channel
3. 複製貼上訊息
4. 格式化（加粗、程式碼區塊、emoji）
5. 重複 10+ 次/天

**如果能自動化多好...**

---

## 🎯 學習目標

- [ ] 創建 Slack App 並取得 Bot Token
- [ ] 配置 Slack MCP
- [ ] 讓 Claude 自動發送訊息
- [ ] 掌握 Slack 訊息格式化
- [ ] 建立通知自動化流程

**時間**：30 分鐘

---

## 第一部分：創建 Slack App（10 分鐘）

### Step 1：前往 Slack API

1. 打開 https://api.slack.com/apps
2. 點擊 "Create New App"
3. 選擇 "From scratch"
4. App Name: `Claude Assistant`
5. Workspace: 選擇你的 workspace

### Step 2：配置 Bot 權限

1. 左側選單 → "OAuth & Permissions"
2. 向下滾動到 "Scopes"
3. 在 "Bot Token Scopes" 加入：

**基本權限**：
```
✅ chat:write         - 發送訊息
✅ chat:write.public  - 發送到公開 channel
✅ channels:read      - 讀取 channel 列表
✅ files:write        - 上傳檔案（可選）
```

**進階權限**（可選）：
```
⚠️ chat:write.customize  - 自訂 bot 名稱和頭像
⚠️ channels:history      - 讀取訊息歷史
⚠️ channels:join         - 自動加入 channel
```

**原則**：最小化權限，需要什麼加什麼。

### Step 3：安裝 App 到 Workspace

1. 向上滾動到 "OAuth Tokens"
2. 點擊 "Install to Workspace"
3. 授權
4. 複製 "Bot User OAuth Token"
   ```
   格式：xoxb-xxxxxxxxxxxx-xxxxxxxxxxxx-xxxxxxxxxxxxxxxxxxxxxxxx
   ```

### Step 4：邀請 Bot 到 Channel

```
在 Slack 中：
1. 前往你想發送訊息的 channel
2. 輸入：/invite @Claude Assistant
3. Bot 加入成功！
```

---

## 第二部分：配置 Slack MCP（5 分鐘）

### 更新 mcp-config.json

```json
{
  "mcpServers": {
    "github": { /* ... */ },
    "postgres": { /* ... */ },
    "slack": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-slack"
      ],
      "env": {
        "SLACK_BOT_TOKEN": "xoxb-your-token-here",
        "SLACK_TEAM_ID": "T01234567"
      }
    }
  }
}
```

**如何找 Team ID**：
```
Slack → 右上角 workspace 名稱 → About this workspace
→ 查看 "Workspace ID"（格式：T01234567）
```

**使用環境變數（推薦）**：

```bash
# .env
SLACK_BOT_TOKEN="xoxb-your-token-here"
SLACK_TEAM_ID="T01234567"
```

```json
{
  "mcpServers": {
    "slack": {
      "env": {
        "SLACK_BOT_TOKEN": "${SLACK_BOT_TOKEN}",
        "SLACK_TEAM_ID": "${SLACK_TEAM_ID}"
      }
    }
  }
}
```

**重啟 Claude Code**

---

## 第三部分：測試發送訊息（15 分鐘）

### 測試 1：簡單訊息

```
You: "發送訊息到 #general：'Hello from Claude! 🤖'"
```

**預期結果**：
```
✅ 訊息已發送到 #general

訊息內容：
Hello from Claude! 🤖

訊息連結：
https://workspace.slack.com/archives/C123456/p1234567890
```

**檢查 Slack**：
- 應該看到訊息
- 發送者是 "Claude Assistant" bot

---

### 測試 2：格式化訊息

```
You: "發送到 #engineering：

建置完成 ✅

專案：awesome-project
分支：main
提交：abc1234
狀態：成功
時間：2 分鐘

用程式碼區塊格式化提交雜湊"
```

**預期結果（Slack 中）**：
```
建置完成 ✅

專案：awesome-project
分支：main
提交：`abc1234`
狀態：成功
時間：2 分鐘
```

**自然學到的**：
- ✅ Slack 用 `backticks` 表示行內程式碼
- ✅ Claude 自動格式化訊息
- ✅ Emoji 可以直接使用

---

### 測試 3：結構化訊息（Blocks）

```
You: "發送結構化訊息到 #alerts：

⚠️ 系統警報

環境：Production
服務：API Server
錯誤：Database connection timeout
影響：50% 請求失敗
時間：2025-10-30 14:30

使用 Slack Blocks 格式，讓它更醒目"
```

**預期結果（Slack 中）**：
- 使用彩色邊框（紅色）
- 欄位清楚分隔
- 視覺上更專業

---

### 測試 4：多 Channel 廣播

```
You: "同時發送以下訊息到 #engineering, #management, #general：

🎉 新版本發布

版本：v2.0.0
變更：
- 新增深色模式
- 效能優化 30%
- 修復 15 個 bugs

Release Notes：https://github.com/org/repo/releases/v2.0.0"
```

**預期結果**：
```
✅ 已發送到 3 個 channels：
- #engineering
- #management
- #general
```

---

### 測試 5：條件通知

```
You: "如果資料庫的用戶數超過 10,000，
發送通知到 #milestones"
```

**Claude 會**：
1. 調用 Database MCP 查詢用戶數
2. 檢查條件
3. 如果達成，調用 Slack MCP 發送

**這就是多 MCP 協同！**

---

## 第四部分：實戰案例

### 案例 1：建置通知自動化

```
You: "當 GitHub 有新的 PR merge 時，
發送通知到 #engineering，包含：
- PR 標題和編號
- 作者
- 變更的檔案數
- 連結"
```

**實作**：
1. Claude 調用 GitHub MCP 監測 merges
2. 提取 PR 資訊
3. 調用 Slack MCP 發送通知

---

### 案例 2：每日報表自動發送

```
You: "生成每日報表並發送到 #daily-reports：

報表內容：
- GitHub: 今日 closed issues 數
- Database: 今日新用戶數
- Database: 今日訂單總額

格式要專業，用表格"
```

**Claude 會**：
1. 並行調用 GitHub MCP + Database MCP
2. 收集資料
3. 格式化成表格
4. 調用 Slack MCP 發送

---

### 案例 3：錯誤警報

```
You: "監控日誌檔案 /var/log/app.log
如果發現 'ERROR' 關鍵字，
立即發送警報到 #alerts"
```

---

## 第五部分：進階技巧

### 技巧 1：Slack Threads（回覆串）

```
You: "發送訊息到 #general，
如果有人回覆，自動回應說明"
```

### 技巧 2：Interactive Messages

```
You: "發送互動式訊息到 #approvals：

需要批准：部署到 Production

環境：Production
版本：v2.0.0
風險：中

添加兩個按鈕：
[✅ 批准] [❌ 拒絕]"
```

### 技巧 3：排程訊息

```
You: "設定排程：
每週一早上 9:00 發送週報到 #weekly-reports"
```

---

## 🎓 學習檢查點

- [ ] 能創建 Slack App 和 Bot Token
- [ ] 能配置 Slack MCP
- [ ] 能發送簡單和格式化訊息
- [ ] 理解 Slack 權限管理
- [ ] 能結合其他 MCP 實現自動化通知

---

## 📚 下一步

- `B04_配置Notion_MCP.md` - 將訊息儲存到 Notion
- `C01_自動化週報生成系統.md` - Database + Slack + Notion 協同

---

## 💡 關鍵收穫

**Slack MCP = AI 通知中樞**

1. **從手動到自動**
   - 不再手動複製貼上
   - AI 自動格式化
   - 智能條件觸發

2. **與其他 MCP 協同**
   - GitHub events → Slack
   - Database alerts → Slack
   - 任何資料 → Slack

3. **團隊賦能**
   - 即時通知
   - 減少資訊延遲
   - 提升協作效率

**恭喜！你的 AI 現在可以跟團隊溝通了！** 🎉
