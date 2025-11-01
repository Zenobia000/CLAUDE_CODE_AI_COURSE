# B05: 基礎 Agent 切換 - 讓專家處理專業問題

## 📋 情境描述

### 你遇到的問題

你用 Claude 審查程式碼，但總覺得建議太「通用」：

**預設 Agent 的回應**：
```
You: "審查這段程式碼的安全性"

Claude (code-expert):
"這段程式碼看起來不錯，但可能有一些潛在問題：
- 輸入驗證可以加強
- 錯誤處理可以更詳細
- 建議加上註解"
```

**太籠統了！你想要**：
- 具體的安全漏洞指出
- CVE 編號和修復方案
- OWASP Top 10 檢查
- 滲透測試建議

**這就是 Agent 切換的威力！**

---

## 🎯 學習目標

- [ ] 理解不同 Agent 的角色定位
- [ ] 掌握 `/agents` 指令
- [ ] 學會何時切換 Agent
- [ ] 體驗專業 Agent 的威力
- [ ] 理解 Agent 上下文保持

**時間**：30 分鐘

---

## 第一部分：認識 Agent 角色（10 分鐘）

### Claude Code 的 Agent 團隊

**通用 Agents**：
```
🧑‍💻 code-expert（預設）
   - 全方位程式碼專家
   - 適合一般開發任務
   - 樣樣會一點，但不夠專精

🏗️ architect
   - 系統架構師
   - 專注於系統設計
   - 考慮可擴展性和維護性

👨‍⚖️ reviewer
   - 程式碼審查員
   - 專注於程式碼品質
   - 找出 code smell 和改進點

🐛 debugger
   - 除錯專家
   - 專注於問題診斷
   - 擅長根因分析
```

**專業 Agents**：
```
🔒 security-auditor
   - 安全審計員
   - 專注於安全漏洞
   - OWASP、CVE、滲透測試

⚡ performance-optimizer
   - 效能優化師
   - 專注於效能瓶頸
   - Big-O、記憶體、快取

🧪 test-engineer
   - 測試工程師
   - 專注於測試策略
   - TDD、BDD、覆蓋率

📊 data-analyst
   - 資料分析師
   - 專注於資料洞察
   - SQL、統計、視覺化

📝 tech-writer
   - 技術文檔寫手
   - 專注於文檔品質
   - API 文檔、用戶手冊

🚀 devops-engineer
   - DevOps 工程師
   - 專注於部署和 CI/CD
   - Docker、K8s、自動化
```

---

## 第二部分：Agent 切換實戰（20 分鐘）

### 測試 1：安全審計對比

#### 使用預設 Agent

```
You: "審查這段程式碼的安全性：

async function login(username, password) {
    const query = `SELECT * FROM users
                   WHERE username = '${username}'
                   AND password = '${password}'`;
    const result = await db.query(query);
    return result.rows[0];
}
"
```

**預設 Agent 回應**：
```
這段程式碼有一些安全問題：
1. SQL injection 風險
2. 密碼未加密
3. 建議使用 prepared statements
```

**評價**：正確但不夠深入

---

#### 切換到 security-auditor

```
You: "/agents:security-auditor

用安全審計員的角度重新審查剛才的程式碼"
```

**security-auditor 回應**：
```
🔴 Critical Security Issues Detected

【SQL Injection - CWE-89】
Severity: Critical (CVSS 9.8)

Location: Line 2-3
Vulnerable Code:
```sql
const query = `SELECT * FROM users WHERE username = '${username}'`;
```

Attack Vector:
```javascript
// Attacker input:
username = "admin' --"
// Resulting query:
SELECT * FROM users WHERE username = 'admin' --' AND password = '...'
// → Bypasses password check
```

Fix:
```javascript
const query = 'SELECT * FROM users WHERE username = $1 AND password = $2';
const result = await db.query(query, [username, password]);
```

【Plain Text Password Storage - CWE-256】
Severity: High (CVSS 7.5)

Issue: Passwords stored/compared in plain text

Fix:
```javascript
// Hash on registration
const hashedPassword = await bcrypt.hash(password, 10);

// Compare on login
const isValid = await bcrypt.compare(password, user.password_hash);
```

【Missing Input Validation - CWE-20】
Severity: Medium

Recommendations:
1. Validate username format (alphanumeric, length limits)
2. Rate limiting to prevent brute force
3. Account lockout after failed attempts
4. Log security events

【Additional Security Measures】
- Use HTTPS only
- Implement CSRF protection
- Add MFA (Multi-Factor Authentication)
- Session management (expiration, regeneration)
- Security headers (CSP, HSTS)

【OWASP Top 10 Compliance】
❌ A03:2021 – Injection (SQL Injection)
❌ A02:2021 – Cryptographic Failures (Plain text passwords)
⚠️  A07:2021 – Identification and Authentication Failures

Recommended Actions:
1. Fix SQL injection immediately
2. Implement password hashing
3. Add input validation
4. Security audit entire codebase
5. Penetration testing
```

**差異巨大！**
- ✅ 具體的 CVE 和 CWE 編號
- ✅ CVSS 評分
- ✅ 攻擊向量示範
- ✅ 完整的修復程式碼
- ✅ OWASP Top 10 對照
- ✅ 額外的安全措施建議

---

### 測試 2：效能優化對比

#### 使用預設 Agent

```
You: "優化這個函數：

function findUsers(filters) {
    let users = getAllUsers();  // 10,000 筆

    if (filters.age) {
        users = users.filter(u => u.age === filters.age);
    }
    if (filters.city) {
        users = users.filter(u => u.city === filters.city);
    }
    if (filters.status) {
        users = users.filter(u => u.status === filters.status);
    }

    return users.sort((a, b) => a.name.localeCompare(b.name));
}
"
```

**預設 Agent 回應**：
```
可以優化：
1. 合併 filter 條件
2. 考慮使用資料庫查詢而非載入全部
3. 排序可以在資料庫完成
```

---

#### 切換到 performance-optimizer

```
You: "/agents:performance-optimizer

分析這個函數的效能瓶頸"
```

**performance-optimizer 回應**：
```
⚡ Performance Analysis Report

【Current Performance】
Time Complexity: O(n * m + n log n)
- getAllUsers(): O(n) - 10,000 rows
- 3x filter(): O(n * m) - worst case 30,000 iterations
- sort(): O(n log n)

Estimated execution time: ~200ms (10k records)
Memory usage: ~50MB (loading all users)

【Bottlenecks Identified】
🔴 Critical: Loading entire dataset
🟡 Major: Multiple filter passes
🟡 Major: In-memory sorting

【Optimization Strategy】

**Level 1: Database-Level Optimization (Recommended)**
```javascript
async function findUsers(filters) {
    const conditions = [];
    const params = [];
    let paramCount = 1;

    if (filters.age) {
        conditions.push(`age = $${paramCount++}`);
        params.push(filters.age);
    }
    if (filters.city) {
        conditions.push(`city = $${paramCount++}`);
        params.push(filters.city);
    }
    if (filters.status) {
        conditions.push(`status = $${paramCount++}`);
        params.push(filters.status);
    }

    const whereClause = conditions.length > 0
        ? 'WHERE ' + conditions.join(' AND ')
        : '';

    const query = `
        SELECT * FROM users
        ${whereClause}
        ORDER BY name ASC
    `;

    return await db.query(query, params);
}
```

Performance Gain:
- Time: 200ms → 5ms (40x faster)
- Memory: 50MB → 1MB (50x reduction)
- Scalability: O(n) → O(log n) with indexes

**Level 2: Add Database Indexes**
```sql
CREATE INDEX idx_users_age ON users(age);
CREATE INDEX idx_users_city ON users(city);
CREATE INDEX idx_users_status ON users(status);
CREATE INDEX idx_users_name ON users(name);

-- Composite index for common combinations
CREATE INDEX idx_users_filter ON users(age, city, status);
```

Performance Gain:
- Query time: 5ms → 0.5ms (10x faster)

**Level 3: Caching Strategy**
```javascript
const cache = new LRU({ max: 500, ttl: 5 * 60 * 1000 }); // 5 min

async function findUsers(filters) {
    const cacheKey = JSON.stringify(filters);

    if (cache.has(cacheKey)) {
        return cache.get(cacheKey);
    }

    const users = await queryDatabase(filters);
    cache.set(cacheKey, users);
    return users;
}
```

Performance Gain:
- Repeated queries: 0.5ms → 0.01ms (50x faster)

【Benchmark Results】
```
Original:     200ms | 50MB RAM
Optimized:    0.5ms |  1MB RAM
With Cache:  0.01ms |  1MB RAM + cache

Total improvement: 20,000x faster
```

【Monitoring Recommendations】
- Add query execution time logging
- Set up alerts for queries > 10ms
- Monitor cache hit rate
- Track memory usage trends
```

**又是巨大差異！**
- ✅ Big-O 分析
- ✅ 量化的效能評估
- ✅ 多層次優化方案
- ✅ Benchmark 數據
- ✅ 監控建議

---

### 測試 3：Agent 上下文保持

**關鍵問題**：切換 Agent 後，上下文還在嗎？

**驗證**：

```
Step 1:
You: "這是我的程式碼：[貼上程式碼]"
Claude (code-expert): [分析程式碼]

Step 2:
You: "/agents:security-auditor
     審查剛才的程式碼"

Claude (security-auditor):
[可以存取剛才的程式碼！]
分析剛才你提供的程式碼...

Step 3:
You: "/agents:performance-optimizer
     優化剛才 security-auditor 指出的修復方案"

Claude (performance-optimizer):
[可以存取之前的所有對話！]
針對剛才 security-auditor 提出的修復方案...
```

**結論**：✅ 上下文完整保留

---

## 第三部分：Agent 切換決策樹

### 何時應該切換 Agent？

```
任務描述
    │
    ├─ 安全相關？
    │   ├─ 是 → security-auditor
    │   │       (漏洞掃描、合規檢查、滲透測試)
    │   └─ 否 ↓
    │
    ├─ 效能問題？
    │   ├─ 是 → performance-optimizer
    │   │       (瓶頸分析、Big-O、記憶體優化)
    │   └─ 否 ↓
    │
    ├─ 測試相關？
    │   ├─ 是 → test-engineer
    │   │       (測試策略、覆蓋率、TDD/BDD)
    │   └─ 否 ↓
    │
    ├─ 系統設計？
    │   ├─ 是 → architect
    │   │       (架構設計、可擴展性、技術選型)
    │   └─ 否 ↓
    │
    ├─ 程式碼審查？
    │   ├─ 是 → reviewer
    │   │       (程式碼品質、code smell、重構)
    │   └─ 否 ↓
    │
    ├─ Bug 診斷？
    │   ├─ 是 → debugger
    │   │       (根因分析、除錯策略、日誌分析)
    │   └─ 否 ↓
    │
    ├─ 資料分析？
    │   ├─ 是 → data-analyst
    │   │       (SQL 優化、統計分析、報表)
    │   └─ 否 ↓
    │
    ├─ 文檔撰寫？
    │   ├─ 是 → tech-writer
    │   │       (API 文檔、README、用戶手冊)
    │   └─ 否 ↓
    │
    ├─ 部署/CI/CD？
    │   ├─ 是 → devops-engineer
    │   │       (Docker、K8s、CI/CD 管道)
    │   └─ 否 ↓
    │
    └─ 一般開發 → code-expert (預設)
```

### 成本 vs 收益分析

**何時不要切換（成本 > 收益）**：
- ✅ 簡單任務（如「寫一個 hello world」）
- ✅ 只需要通用建議
- ✅ 快速驗證想法

**何時應該切換（成本 < 收益）**：
- ✅ 安全審計（Critical）
- ✅ 效能瓶頸診斷
- ✅ 複雜的系統設計
- ✅ 生產問題除錯
- ✅ 企業級程式碼審查

---

## 第四部分：進階技巧

### 技巧 1：Agent 鏈

```
You: "完整審查這個專案：

1. 程式碼品質（reviewer）
2. 安全性（security-auditor）
3. 效能（performance-optimizer）
4. 測試（test-engineer）

依序進行，每個 Agent 完成後換下一個"
```

### 技巧 2：Agent 協商

```
You: "security-auditor 和 performance-optimizer
     針對這個函數給出的建議衝突了
     （安全要加密，效能要避免加密）

     請 architect 協調並給出平衡方案"
```

### 技巧 3：專案角色映射

```
不同階段用不同 Agent：

需求階段 → architect（系統設計）
開發階段 → code-expert（實作）
測試階段 → test-engineer（測試策略）
審查階段 → reviewer + security-auditor（審查）
部署階段 → devops-engineer（CI/CD）
維護階段 → debugger（問題診斷）
```

---

## 🎓 學習檢查點

- [ ] 理解不同 Agent 的專長
- [ ] 能使用 `/agents` 指令切換
- [ ] 知道何時應該切換 Agent
- [ ] 體驗過專業 Agent 的深度
- [ ] 理解 Agent 上下文保持機制

---

## 📚 下一步

**你已經完成所有基礎級情境題！** 🎉

準備進入組合級：
- `C01_自動化週報生成系統.md` - 4-MCP + 多-Agent 協同
- `C02_知識萃取系統.md` - Agent 切換與工作流程編排

---

## 💡 關鍵收穫

**Agent 切換 = 找對專家做對事**

1. **通才 vs 專家**
   - 預設 Agent：樣樣會一點
   - 專業 Agent：術業有專攻

2. **品質提升顯著**
   - 從「還可以」到「專業級」
   - 從「建議」到「具體方案」
   - 從「通用」到「深入」

3. **何時切換**
   - 簡單任務：不切換
   - 專業問題：一定要切換
   - 關鍵任務：多 Agent 協同

**恭喜完成基礎級所有情境題！** 🚀
**準備好進入多 MCP 協同的世界了嗎？**
