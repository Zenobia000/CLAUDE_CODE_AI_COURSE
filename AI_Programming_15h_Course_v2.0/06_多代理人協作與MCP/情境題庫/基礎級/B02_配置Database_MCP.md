# B02: 配置 Database MCP - 讓 AI 直接查詢資料庫

## 📋 情境描述

### 你遇到的問題

你是一個資料分析師，每天需要從資料庫查詢數據做報表：

**傳統流程的痛苦**：
1. 打開 SQL 客戶端（MySQL Workbench / pgAdmin）
2. 手動寫 SQL 查詢
3. 執行 → 複製結果
4. 貼到 Excel / Google Sheets
5. 整理格式 → 計算統計
6. 生成報告

**每個報表耗時 30-60 分鐘**，而你每週要做 10+ 個報表。

### 你想要的解決方案

> "如果我能直接問 Claude：'查詢最近 7 天的用戶註冊數'，它自動寫 SQL、執行、分析、給出洞察..."

這就是 **Database MCP** 的威力！

---

## 🎯 學習目標

完成本情境後，你將能夠：

- [ ] 配置 PostgreSQL/MySQL MCP
- [ ] 創建安全的唯讀資料庫帳號
- [ ] 理解資料庫權限管理最佳實踐
- [ ] 讓 Claude 自主寫 SQL 並查詢
- [ ] 建立資料庫安全存取的良好習慣

**時間預估**：45 分鐘
- 準備資料庫帳號：10 分鐘
- 配置 MCP：10 分鐘
- 測試查詢：15 分鐘
- 安全加固：10 分鐘

---

## 第一部分：準備工作（10 分鐘）

### 選擇你的資料庫

本教學支援：
- ✅ PostgreSQL（推薦）
- ✅ MySQL / MariaDB
- ✅ SQLite（檔案型資料庫）

**沒有資料庫？** 使用測試環境：

```bash
# 使用 Docker 快速啟動 PostgreSQL
docker run -d \
  --name postgres-test \
  -e POSTGRES_PASSWORD=testpassword \
  -e POSTGRES_DB=testdb \
  -p 5432:5432 \
  postgres:15
```

---

### Step 1：創建唯讀帳號（Critical）

**為什麼需要唯讀帳號？**

❌ **絕對不要**用 root / admin 帳號：
```sql
-- 危險！Claude 可以刪除所有資料
DROP TABLE users;  -- 所有用戶資料不見了
```

✅ **創建專門的唯讀帳號**：

#### PostgreSQL：

```sql
-- 1. 創建唯讀用戶
CREATE USER claude_readonly WITH PASSWORD 'secure_password_here';

-- 2. 授予連線權限
GRANT CONNECT ON DATABASE your_database TO claude_readonly;

-- 3. 授予 schema 使用權限
GRANT USAGE ON SCHEMA public TO claude_readonly;

-- 4. 授予所有 table 的 SELECT 權限
GRANT SELECT ON ALL TABLES IN SCHEMA public TO claude_readonly;

-- 5. 確保未來新建的 table 也有 SELECT 權限
ALTER DEFAULT PRIVILEGES IN SCHEMA public
GRANT SELECT ON TABLES TO claude_readonly;

-- 6. 驗證權限
\du claude_readonly
```

#### MySQL：

```sql
-- 1. 創建唯讀用戶
CREATE USER 'claude_readonly'@'localhost'
IDENTIFIED BY 'secure_password_here';

-- 2. 授予 SELECT 權限
GRANT SELECT ON your_database.* TO 'claude_readonly'@'localhost';

-- 3. 刷新權限
FLUSH PRIVILEGES;

-- 4. 驗證權限
SHOW GRANTS FOR 'claude_readonly'@'localhost';
```

**驗證唯讀**：
```sql
-- 測試：應該成功
SELECT * FROM users LIMIT 1;

-- 測試：應該失敗
INSERT INTO users (name) VALUES ('test');
-- ERROR: permission denied
```

---

### Step 2：準備連線字串

#### PostgreSQL 連線字串格式：

```
postgresql://用戶名:密碼@主機:埠號/資料庫名

範例：
postgresql://claude_readonly:secure_password@localhost:5432/myapp_production
```

**欄位說明**：
- `claude_readonly`：唯讀帳號名稱
- `secure_password`：密碼（待會會放在環境變數）
- `localhost`：資料庫主機（本機）
- `5432`：PostgreSQL 預設埠號
- `myapp_production`：資料庫名稱

#### MySQL 連線字串格式：

```
mysql://用戶名:密碼@主機:埠號/資料庫名

範例：
mysql://claude_readonly:secure_password@localhost:3306/myapp_production
```

---

## 第二部分：配置 Database MCP（10 分鐘）

### Step 1：更新 mcp-config.json

**PostgreSQL 範例**：

```json
{
  "mcpServers": {
    "github": {
      // 你之前配置的 GitHub MCP
    },
    "postgres": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-postgres"
      ],
      "env": {
        "POSTGRES_CONNECTION_STRING": "postgresql://claude_readonly:YOUR_PASSWORD@localhost:5432/your_database"
      }
    }
  }
}
```

**MySQL 範例**：

```json
{
  "mcpServers": {
    "mysql": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-mysql"
      ],
      "env": {
        "MYSQL_CONNECTION_STRING": "mysql://claude_readonly:YOUR_PASSWORD@localhost:3306/your_database"
      }
    }
  }
}
```

### Step 2：使用環境變數（更安全）

**為什麼？** 避免密碼寫在配置檔裡。

**設定環境變數**：

```bash
# 方法 1：寫入 .env 檔案
echo 'DATABASE_URL="postgresql://claude_readonly:YOUR_PASSWORD@localhost:5432/your_database"' >> .env

# 確保 .env 在 .gitignore
echo ".env" >> .gitignore
```

**更新 mcp-config.json**：

```json
{
  "mcpServers": {
    "postgres": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-postgres"],
      "env": {
        "POSTGRES_CONNECTION_STRING": "${DATABASE_URL}"
      }
    }
  }
}
```

**啟動時載入環境變數**：

```bash
# Linux/Mac
source .env && claude

# Windows
# 手動設定環境變數或使用 dotenv
```

### Step 3：重啟 Claude Code

```bash
# 重新啟動以載入新配置
claude
```

---

## 第三部分：測試查詢（15 分鐘）

### 測試 1：查看資料庫結構

**指令**：
```
查看資料庫有哪些 tables
```

**預期結果**：
```
資料庫結構：

Tables (10):
1. users
2. posts
3. comments
4. orders
5. products
...

想查看某個 table 的結構嗎？
```

**自然學到的**：
- ✅ Claude 自動調用 Database MCP
- ✅ Claude 執行了 `\dt` (PostgreSQL) 或 `SHOW TABLES` (MySQL)

---

### 測試 2：查看 Table Schema

**指令**：
```
查看 users table 的結構
```

**預期結果**：
```
users table 結構：

欄位：
- id: integer (primary key)
- email: varchar(255) (unique, not null)
- name: varchar(100)
- created_at: timestamp
- updated_at: timestamp
- is_active: boolean (default: true)

索引：
- PRIMARY KEY on id
- UNIQUE INDEX on email
- INDEX on created_at

總筆數：約 10,000 筆
```

**自然學到的**：
- ✅ Claude 執行了 `\d users` (PostgreSQL) 或 `DESCRIBE users` (MySQL)
- ✅ Claude 還查詢了 `SELECT COUNT(*) FROM users`

---

### 測試 3：簡單查詢

**指令**：
```
查詢最近 7 天註冊的用戶數
```

**預期結果**：
```
SQL 查詢：
SELECT DATE(created_at) as date, COUNT(*) as count
FROM users
WHERE created_at >= NOW() - INTERVAL '7 days'
GROUP BY DATE(created_at)
ORDER BY date DESC;

結果：
2025-10-30: 145 人
2025-10-29: 132 人
2025-10-28: 128 人
2025-10-27: 98 人
2025-10-26: 112 人
2025-10-25: 156 人
2025-10-24: 134 人

總計：905 人
平均每天：129 人

趨勢：最近 3 天有上升趨勢（+15%）
```

**關鍵觀察**：
- ✅ Claude **自動寫 SQL**（你不需要寫！）
- ✅ Claude **執行查詢**
- ✅ Claude **分析結果** 並給出洞察

---

### 測試 4：複雜分析

**指令**：
```
分析用戶活躍度，告訴我：
1. 活躍用戶（最近 30 天有登入）的數量
2. 流失用戶（超過 90 天沒登入）的數量
3. 用戶留存率
4. 給我建議如何提升留存率
```

**預期結果**：
```
用戶活躍度分析：

【活躍用戶】
- 總數：3,456 人
- 佔比：34.5%
- 平均登入頻率：每週 4.2 次

【流失用戶】
- 總數：2,234 人
- 佔比：22.3%
- 主要流失在註冊後 30 天內（65%）

【留存率】
- Day 1: 78%
- Day 7: 45%
- Day 30: 28%
- Day 90: 18%

【洞察與建議】
1. 首週流失嚴重（45% → 28%）
   建議：改善 onboarding 流程

2. 長期留存低（18%）
   建議：
   - 增加推播通知
   - 建立會員獎勵機制
   - 分析流失用戶的共同特徵

3. 活躍用戶黏性高（每週 4.2 次）
   建議：研究這群用戶的使用模式，複製到其他用戶
```

**自然學到的**：
- ✅ Claude 執行了多個 SQL 查詢
- ✅ Claude 計算了複雜的統計指標
- ✅ Claude 提供了商業洞察（不只是數據）

---

### 測試 5：多輪探索

**Round 1**：
```
You: "查詢所有訂單"
Claude: [執行 SELECT * FROM orders LIMIT 10]
```

**Round 2**：
```
You: "過去 30 天的訂單金額總計是多少？"
Claude: [執行 SELECT SUM(amount) FROM orders WHERE created_at >= NOW() - INTERVAL '30 days']
結果：NT$ 1,234,567
```

**Round 3**：
```
You: "哪個產品賣最好？"
Claude: [JOIN orders 和 products tables]
最熱賣產品：
1. Product A - 234 筆訂單
2. Product B - 189 筆訂單
3. Product C - 156 筆訂單
```

**Round 4**：
```
You: "Product A 的買家有什麼特徵？"
Claude: [JOIN orders, products, users]
買家特徵分析：
- 年齡：25-35 歲居多（60%）
- 性別：女性為主（70%）
- 地區：台北、台中、高雄（75%）
- 消費習慣：通常一次買 2-3 個產品
```

**這就是 Database MCP 的威力**：
- 持續探索資料
- 動態調整查詢
- 提供商業洞察

---

## 第四部分：安全加固（10 分鐘）

### 安全檢查清單

#### 1. 權限驗證

```
You: "幫我測試一下，嘗試刪除 users table 的一筆資料"

Claude: [執行 DELETE FROM users WHERE id = 1]
ERROR: permission denied for table users

好消息！唯讀帳號無法刪除資料，配置正確。
```

#### 2. 連線字串保護

**檢查**：
- [ ] `.claude/mcp-config.json` 在 `.gitignore`
- [ ] `.env` 在 `.gitignore`
- [ ] Git 歷史中沒有洩漏密碼

```bash
# 驗證
git status  # 不應該看到 mcp-config.json 或 .env
git log -p | grep -i "password"  # 不應該有結果
```

#### 3. 網路隔離（生產環境）

**生產資料庫不應該直接暴露**：

```
推薦架構：

[Claude Code] → [跳板機 / VPN] → [生產資料庫]

或者使用唯讀 replica：

[Claude Code] → [Read Replica] → [不影響主資料庫]
```

#### 4. 查詢限制

**考慮設定查詢超時**：

```sql
-- PostgreSQL：設定查詢超時（防止慢查詢）
ALTER USER claude_readonly SET statement_timeout = '30s';

-- MySQL：
SET GLOBAL max_execution_time = 30000;  -- 30 秒
```

---

## 第五部分：常見問題

### 問題 1：連線失敗

**症狀**：
```
Error: Connection refused
```

**診斷步驟**：

```bash
# 1. 檢查資料庫是否執行
# PostgreSQL
pg_isready -h localhost -p 5432

# MySQL
mysqladmin ping -h localhost

# 2. 檢查連線字串格式
# 確認：用戶名、密碼、主機、埠號、資料庫名都正確

# 3. 測試連線
# PostgreSQL
psql "postgresql://claude_readonly:password@localhost:5432/database"

# MySQL
mysql -u claude_readonly -p -h localhost database
```

### 問題 2：權限不足

**症狀**：
```
ERROR: permission denied for table sensitive_data
```

**原因**：唯讀帳號沒有某個 table 的 SELECT 權限

**解決**：
```sql
-- 授予權限
GRANT SELECT ON sensitive_data TO claude_readonly;
```

### 問題 3：查詢太慢

**症狀**：Claude 回應很慢，超過 30 秒

**原因**：
- 資料量太大
- 沒有索引
- 複雜的 JOIN

**解決**：

```
You: "剛才那個查詢太慢了，能優化嗎？"

Claude: [分析 EXPLAIN 結果]
問題：users table 的 created_at 沒有索引

建議：
CREATE INDEX idx_users_created_at ON users(created_at);

優化後查詢時間：從 15 秒 → 0.2 秒
```

---

## 第六部分：實戰案例

### 案例 1：每日報表自動化

**之前**：
1. 手動寫 SQL
2. 執行 → 複製結果
3. 貼到 Excel → 整理格式
4. 計算統計 → 生成圖表
5. 寫報告 → 發給主管

**時間**：60 分鐘

**現在**：
```
You: "生成今日運營報表，包含：
- 新用戶數
- 訂單數與金額
- 熱賣產品 Top 5
- 用戶活躍度
- 異常指標預警

以 Markdown 格式輸出，我要貼到 Slack"
```

**時間**：2 分鐘

---

### 案例 2：資料清理檢查

```
You: "檢查資料品質，找出：
1. 重複的 email
2. 無效的電話號碼格式
3. 超過 90 天沒更新的記錄
4. 孤兒記錄（references 不存在的外鍵）

給我修復建議"
```

**Claude 會**：
- 執行多個檢查查詢
- 列出所有問題
- 提供修復的 SQL（但不會執行，因為是唯讀）

---

### 案例 3：效能分析

```
You: "分析資料庫效能，找出：
1. 最慢的 10 個 queries
2. 缺少索引的 tables
3. 資料表肥大問題
4. 給我優化建議"
```

---

## 🎓 學習檢查點

- [ ] 能創建唯讀資料庫帳號
- [ ] 能配置 PostgreSQL/MySQL MCP
- [ ] 理解連線字串格式
- [ ] 知道如何保護資料庫密碼
- [ ] 能讓 Claude 自主寫 SQL 查詢
- [ ] 理解資料庫安全存取原則

---

## 📚 下一步

- 進階：`B03_配置Slack_MCP.md` - 將查詢結果自動發送通知
- 組合：`C01_自動化週報生成系統.md` - Database + GitHub + Slack + Notion 協同

---

## 💡 關鍵收穫

**Database MCP = AI 資料分析師**

1. **不需要寫 SQL**
   - Claude 自動寫查詢
   - Claude 自動優化
   - Claude 給出商業洞察

2. **安全永遠第一**
   - 永遠使用唯讀帳號
   - 密碼不進 Git
   - 權限最小化

3. **從重複勞動到策略思考**
   - 把時間省下來
   - 專注在分析與決策
   - AI 處理機械性的查詢工作

**恭喜！你現在可以讓 AI 直接分析資料庫了！** 🎉
