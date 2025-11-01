# B04: 配置 Notion MCP - AI 自動管理知識庫

## 📋 情境描述

### 你遇到的問題

團隊用 Notion 管理知識、會議記錄、專案文檔：

**手動維護的痛苦**：
1. 會議後手動整理筆記到 Notion
2. 專案文檔需要手動更新
3. 知識分散，難以整理
4. 格式不統一
5. 忘記更新 → 資訊過時

**如果知識庫能自動維護...**

---

## 🎯 學習目標

- [ ] 創建 Notion Integration 並取得 API Key
- [ ] 配置 Notion MCP
- [ ] 讓 Claude 自動創建和更新 Pages
- [ ] 掌握 Notion Database 操作
- [ ] 建立知識管理自動化

**時間**：40 分鐘

---

## 第一部分：創建 Notion Integration（15 分鐘）

### Step 1：前往 Notion Integrations

1. 打開 https://www.notion.so/my-integrations
2. 點擊 "+ New integration"
3. 設定：
   - Name: `Claude Assistant`
   - Associated workspace: 選擇你的 workspace
   - Type: Internal Integration

### Step 2：設定 Capabilities

**Content Capabilities**（內容權限）：
```
✅ Read content       - 讀取 pages
✅ Update content     - 更新 pages
✅ Insert content     - 創建 pages
```

**Comment Capabilities**（評論權限，可選）：
```
⚠️ Read comments     - 讀取評論
⚠️ Insert comments   - 新增評論
```

**User Capabilities**（用戶資訊，可選）：
```
⚠️ Read user information  - 讀取用戶資訊（用於 @mention）
```

點擊 "Submit" 創建。

### Step 3：複製 API Key

```
格式：secret_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

**重要**：
- 這是敏感資訊，妥善保管
- 不要分享給任何人
- 不要上傳到 Git

### Step 4：授權 Pages 存取權限

**Critical**：Integration 預設無法存取任何 page。

**授權方式**：

1. 打開你想讓 Claude 存取的 Notion page
2. 點擊右上角 "•••" → "Add connections"
3. 搜尋並選擇 "Claude Assistant"
4. 授權

**建議結構**：

```
📁 Workspace
  └─ 📁 Claude Workspace (授權這個)
      ├─ 📄 會議記錄
      ├─ 📄 專案文檔
      ├─ 📊 知識庫 (Database)
      └─ 📊 週報 (Database)
```

---

## 第二部分：配置 Notion MCP（5 分鐘）

### 更新 mcp-config.json

```json
{
  "mcpServers": {
    "github": { /* ... */ },
    "postgres": { /* ... */ },
    "slack": { /* ... */ },
    "notion": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-notion"
      ],
      "env": {
        "NOTION_API_KEY": "secret_your_api_key_here"
      }
    }
  }
}
```

**使用環境變數**：

```bash
# .env
NOTION_API_KEY="secret_your_api_key_here"
```

```json
{
  "mcpServers": {
    "notion": {
      "env": {
        "NOTION_API_KEY": "${NOTION_API_KEY}"
      }
    }
  }
}
```

**重啟 Claude Code**

---

## 第三部分：測試基本操作（20 分鐘）

### 測試 1：列出可存取的 Pages

```
You: "列出我在 Notion 中可以存取的 pages"
```

**預期結果**：
```
可存取的 Notion pages：

📁 Claude Workspace
├─ 📄 會議記錄
├─ 📄 專案文檔
├─ 📊 知識庫
└─ 📊 週報

總計：4 個 pages/databases
```

**如果看不到任何 page**：
→ 檢查是否有授權 integration 存取權限

---

### 測試 2：創建新 Page

```
You: "在 Claude Workspace 下創建新頁面：

標題：2025-10-30 每日站會記錄

內容：
## 參與者
- Alice
- Bob
- Charlie

## 今日進度
- Alice: 完成登入功能
- Bob: 修復 3 個 bugs
- Charlie: 撰寫 API 文檔

## 待辦事項
- [ ] 測試登入功能
- [ ] 部署到 staging
- [ ] 準備 demo

## 阻礙
無"
```

**預期結果**：
```
✅ 頁面已創建！

標題：2025-10-30 每日站會記錄
位置：Claude Workspace
連結：https://notion.so/...

內容已填入，包含：
- 參與者列表
- 今日進度
- 待辦事項（checkbox）
- 阻礙欄位
```

**檢查 Notion**：
- 應該看到新頁面
- 格式正確
- Checkbox 可以勾選

---

### 測試 3：更新現有 Page

```
You: "更新剛才的站會記錄，
在待辦事項下新增：
- [ ] 審查 PR #123"
```

**預期結果**：
```
✅ 頁面已更新！

新增待辦事項：
- [ ] 審查 PR #123

頁面連結：https://notion.so/...
```

---

### 測試 4：創建 Database Entry

假設你已經有一個「知識庫」Database，欄位包含：
- 標題 (Title)
- 分類 (Select): 技術 / 理論 / 實戰
- 標籤 (Multi-select)
- 日期 (Date)
- 內容 (Rich text)

```
You: "在知識庫 Database 新增一筆：

標題：MCP 協議深入解析
分類：技術
標籤：AI, MCP, 自動化
日期：2025-10-30
內容：MCP（Model Context Protocol）是 AI 與外部系統溝通的標準協議..."
```

**預期結果**：
```
✅ 已新增到知識庫 Database

標題：MCP 協議深入解析
分類：✅ 技術
標籤：#AI #MCP #自動化
日期：2025-10-30

頁面連結：https://notion.so/...
```

---

### 測試 5：查詢 Database

```
You: "查詢知識庫 Database，
列出所有「技術」分類的筆記"
```

**預期結果**：
```
找到 12 筆技術類筆記：

1. MCP 協議深入解析
   標籤：#AI #MCP #自動化
   日期：2025-10-30

2. PostgreSQL 效能優化技巧
   標籤：#Database #PostgreSQL
   日期：2025-10-28

3. Git 分支策略最佳實踐
   標籤：#Git #DevOps
   日期：2025-10-25

...
```

---

## 第四部分：實戰案例

### 案例 1：自動化會議記錄

```
You: "生成今日站會記錄並儲存到 Notion：

參與者：從 Slack #standup channel 最近的訊息提取
進度：從 GitHub 最近的 commits 提取
待辦：從 GitHub open issues 提取

格式使用標準會議記錄模板"
```

**Claude 會**：
1. 調用 Slack MCP 讀取訊息
2. 調用 GitHub MCP 讀取 commits 和 issues
3. 整理成會議記錄格式
4. 調用 Notion MCP 創建 page

**時間**：從 30 分鐘 → 2 分鐘

---

### 案例 2：知識萃取管道

```
You: "建立知識萃取系統：

1. 從 GitHub README 提取關鍵資訊
2. 整理成結構化筆記
3. 自動分類（技術/理論/實戰）
4. 儲存到 Notion 知識庫
5. 建立與相關筆記的連結"
```

**Claude 會**：
1. 調用 GitHub MCP 讀取 README
2. 分析並提取關鍵資訊
3. 自動分類和標籤
4. 調用 Notion MCP 創建 database entry
5. 搜尋相關筆記並建立連結

---

### 案例 3：專案文檔自動更新

```
You: "更新專案文檔：

1. 從 GitHub 獲取最新的 API 端點
2. 從 Database 獲取資料表 schema
3. 更新 Notion 的 API 文檔頁面
4. 標註更新時間和版本"
```

---

### 案例 4：週報自動生成

```
You: "生成本週週報並儲存到 Notion：

資料來源：
- GitHub: commits, PRs, issues
- Database: 用戶數據, 訂單統計
- Slack: 重要討論摘要

儲存到：週報 Database
格式：使用週報模板"
```

**這是 4-MCP 協同的完整示範！**

---

## 第五部分：Notion 進階技巧

### 技巧 1：Page Templates

```
You: "創建會議記錄模板，
儲存為 Notion template，
之後每次只需填入內容"
```

### 技巧 2：Database Views

```
You: "在知識庫 Database 創建不同 views：
- 依分類分組
- 依日期排序
- 只顯示最近一週的筆記"
```

### 技巧 3：Relations & Rollups

```
You: "建立關聯：
會議記錄 ↔ 專案
讓我能從專案頁面看到所有相關會議"
```

### 技巧 4：Backlinks（反向連結）

```
You: "分析知識庫，
為所有提到 'MCP' 的筆記建立反向連結"
```

---

## 第六部分：常見問題

### 問題 1：無法存取 Page

**症狀**：
```
Error: Page not found
```

**原因**：沒有授權 integration

**解決**：
1. 打開該 page
2. •••  → Add connections → Claude Assistant

---

### 問題 2：格式跑掉

**症狀**：Markdown 格式沒有正確轉換

**原因**：Notion 的 block 結構與 Markdown 有差異

**解決**：
```
You: "用 Notion blocks 格式創建 page，
而不是 Markdown"
```

---

### 問題 3：Database 欄位不匹配

**症狀**：
```
Error: Property 'XXX' does not exist
```

**原因**：Database schema 不匹配

**解決**：
```
You: "先查詢這個 Database 的 schema，
然後根據 schema 創建 entry"
```

---

## 🎓 學習檢查點

- [ ] 能創建 Notion Integration 和 API Key
- [ ] 能配置 Notion MCP
- [ ] 能創建和更新 Notion pages
- [ ] 能操作 Notion databases
- [ ] 理解 Notion 權限管理
- [ ] 能結合多個 MCP 自動化知識管理

---

## 📚 下一步

- `B05_基礎Agent切換.md` - 用專業 Agent 提升輸出品質
- `C01_自動化週報生成系統.md` - 完整的 4-MCP 協同實作

---

## 💡 關鍵收穫

**Notion MCP = AI 知識管理員**

1. **自動化文檔維護**
   - 會議記錄自動生成
   - 文檔自動更新
   - 知識自動分類

2. **多 MCP 協同核心**
   - 從各處收集資訊
   - 整理成結構化知識
   - 統一儲存到 Notion

3. **團隊知識庫活化**
   - 不再過時
   - 即時更新
   - 自動連結

**恭喜！你的 AI 現在是專業的知識管理員了！** 🎉
