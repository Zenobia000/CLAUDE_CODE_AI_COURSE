# 記憶卡庫 - 安全與最佳實踐

本目錄包含 10 張情境式 Anki 閃卡,聚焦於 AI 輔助開發的安全風險識別與應對。

---

## 📋 閃卡設計原則

### ❌ 錯誤的閃卡設計 (定義式)

```
Q: 什麼是 SQL 注入?
A: SQL 注入是一種代碼注入技術...
```

**問題**: 背定義無助於實戰識別問題

---

### ✅ 正確的閃卡設計 (情境式)

```
Q: 【情境】Claude Code 建議這段代碼:
   cursor.execute(f"SELECT * FROM users WHERE id = {user_id}")
   你的反應?

A: 【紅旗】SQL 注入風險!
   【正確做法】cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
   【記憶點】看到 f-string 或 + 拼接 SQL → 立即改用參數化查詢
```

---

## 🎴 閃卡列表 (10 張)

### 憑證安全 (3 張)

**C01: 硬編碼 API Key 識別**
- 情境: AI 生成包含 `api_key = "sk-..."` 的代碼
- 考點: 快速識別並知道正確做法

**C02: Git 憑證洩漏應急**
- 情境: 發現 API key 已 commit 但未 push
- 考點: 15 分鐘內完整應急流程

**C03: 環境變數最佳實踐**
- 情境: 如何正確使用 `.env` 檔案
- 考點: .env vs .env.example vs .gitignore

---

### 代碼安全 (4 張)

**C04: SQL 注入識別**
- 情境: 各種 SQL 注入模式
- 考點: f-string, +, .format() 都不安全

**C05: 路徑遍歷風險**
- 情境: 檔案上傳/下載功能
- 考點: 用戶輸入直接拼接路徑的風險

**C06: 弱密碼雜湊**
- 情境: AI 建議用 MD5 雜湊密碼
- 考點: 為何 MD5 不安全,應該用什麼

**C07: Pickle 反序列化**
- 情境: AI 用 pickle 存儲 session
- 考點: pickle.loads() 的風險與替代方案

---

### 隱私與合規 (3 張)

**C08: AI 上下文清理**
- 情境: 想請 AI 審查包含客戶資料的代碼
- 考點: 4 級資訊分類與清理步驟

**C09: GDPR 合規基礎**
- 情境: 使用 AI 處理 EU 用戶資料
- 考點: 什麼可以分享,什麼絕對不可以

**C10: 安全事件優先級**
- 情境: 發現多個安全問題,如何排優先級
- 考點: CRITICAL vs HIGH vs MEDIUM 的判斷

---

## 📖 完整閃卡內容

### C01: 硬編碼 API Key 識別

**正面 (問題)**:
```
【情境】Claude Code 生成這段代碼:

import openai

openai.api_key = "sk-proj-abc123def456..."

def query_ai(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return response

你的第一反應?
```

**背面 (答案)**:
```
【紅旗】🚨 硬編碼 API Key!

【立即行動】
1. 絕不 commit 這段代碼
2. 立即改為環境變數

【正確做法】
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')
if not openai.api_key:
    raise ValueError("OPENAI_API_KEY not set")

【額外步驟】
- 建立 .env 檔案存放 key
- 確保 .env 在 .gitignore 中
- 建立 .env.example 範本 (不含真實值)

【記憶點】
看到 "sk-", "AKIA", "ghp_" 等前綴 → 立即紅旗
任何 = "xxx..." 的憑證字串 → 必須用 os.getenv()
```

---

### C02: Git 憑證洩漏應急

**正面**:
```
【緊急情境】09:45

你剛 commit 了包含真實 AWS access key 的代碼
- Commit hash: abc1234
- 狀態: 還沒 push
- 後續: 又做了 2 個新 commits
- 時限: 10:00 會自動 push 到遠端

你有 15 分鐘,怎麼辦?
```

**背面**:
```
【應急流程】⏱️ 每一秒都很關鍵!

【0-3 分鐘】撤銷憑證
1. 立即登入 AWS Console
2. IAM → Access Keys → Deactivate/Delete
3. 記錄撤銷時間

【3-8 分鐘】清理 Git 歷史
# 方法: Interactive Rebase
git rebase -i HEAD~3
# 將包含 key 的 commit 改為 "edit"
# 修復檔案,使用環境變數
git add .
git commit --amend --no-edit
git rebase --continue

【8-12 分鐘】修復代碼
- 改為 os.getenv('AWS_ACCESS_KEY')
- 建立 .env (新 key)
- 更新 .gitignore

【12-15 分鐘】建立防護
git secrets --install
git secrets --register-aws

【驗證】
git log -p | grep "AKIA"  # 應無輸出

【記憶點】
撤銷憑證 > 清理歷史 > 修復代碼 > 建立防護
時間壓力下保持冷靜,系統化處理!
```

---

### C04: SQL 注入識別

**正面**:
```
【情境】AI 生成以下 4 段代碼,哪些有 SQL 注入風險?

A: cursor.execute(f"SELECT * FROM users WHERE id = {user_id}")
B: cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
C: cursor.execute("SELECT * FROM users WHERE name = '{}'".format(name))
D: User.objects.filter(id=user_id)  # Django ORM

你的判斷?
```

**背面**:
```
【答案】
❌ A: SQL 注入 (f-string 拼接)
✅ B: 安全 (參數化查詢)
❌ C: SQL 注入 (.format() 拼接)
✅ D: 安全 (ORM)

【危險模式識別】
🚨 f"... {variable} ..."
🚨 "... " + variable + " ..."
🚨 "... {}".format(variable)
🚨 "... %s" % variable

【唯一安全模式】
✅ cursor.execute("... ?", (param,))     # SQLite
✅ cursor.execute("... %s", (param,))    # PostgreSQL/MySQL
✅ ORM 查詢 (Django/SQLAlchemy)

【攻擊範例】
user_id = "1 OR 1=1"
# f"SELECT * WHERE id = {user_id}"
# → SELECT * WHERE id = 1 OR 1=1
# 結果: 返回所有用戶!

【記憶點】
看到字串拼接 SQL → 立即紅旗
唯一安全: ? 佔位符 或 ORM
```

---

### C06: 弱密碼雜湊

**正面**:
```
【情境】AI Copilot 建議用這個雜湊密碼:

import hashlib

def hash_password(password):
    return hashlib.md5(password.encode()).hexdigest()

def verify_password(password, hash):
    return hash_password(password) == hash

這樣安全嗎?如果不安全,為什麼?應該用什麼?
```

**背面**:
```
【判斷】❌ 極度不安全!

【問題 1】MD5 已被破解
- 彩虹表攻擊可在秒級破解
- GPU 可每秒嘗試數十億次
- 真實案例: LinkedIn 2012 洩漏,數百萬 MD5 密碼幾天內被破解

【問題 2】沒有 Salt
- 相同密碼 → 相同 hash
- 攻擊者可用預計算表

【問題 3】太快
- MD5 設計為快速,但密碼雜湊應該"慢"
- 慢速可防暴力破解

【正確做法】
import bcrypt

def hash_password(password):
    return bcrypt.hashpw(
        password.encode('utf-8'),
        bcrypt.gensalt()  # 自動生成 salt
    )

def verify_password(password, hashed):
    return bcrypt.checkpw(
        password.encode('utf-8'),
        hashed
    )

【為何 bcrypt 安全】
✅ 設計為慢 (可調節工作因子)
✅ 自動處理 salt
✅ 業界標準

【其他安全選項】
- Argon2 (最新推薦)
- scrypt
- PBKDF2

【記憶點】
看到 MD5/SHA1 用於密碼 → 立即紅旗
密碼雜湊必須: 慢 + Salt + 抗破解演算法
```

---

### C08: AI 上下文清理

**正面**:
```
【情境】你想請 Claude 審查這段代碼:

def send_invoice(customer):
    email_body = f"""
    Dear {customer.name},

    Invoice for {customer.email}
    Amount: ${customer.total}

    Card: {customer.card_number}
    """
    smtp.send(email_body)

# Database config
DB_URL = "postgresql://admin:P@ssw0rd@10.0.1.50/production"

可以直接貼給 AI 嗎?需要清理什麼?
```

**背面**:
```
【判斷】❌ 絕對不可直接分享!

【需要清理的內容】

🔴 Level 1: 絕對禁止
- ❌ `customer.card_number` (金融資訊)
- ❌ `P@ssw0rd` (資料庫密碼)

🟡 Level 2: 高度機密
- ⚠️ `10.0.1.50` (內部 IP)
- ⚠️ `admin` (資料庫用戶名)

🟠 Level 3: 個人資料
- ⚠️ `customer.name` (可能是真實姓名)
- ⚠️ `customer.email` (可能是真實郵箱)

【清理後版本】
def send_invoice(customer):
    """
    問題: 這個郵件發送函數需要改進:
    1. 如何添加錯誤處理?
    2. 模板應該分離到單獨檔案嗎?
    """
    email_body = generate_invoice_email(customer)
    smtp.send(email_body)

# 配置使用環境變數
DB_URL = os.getenv('DATABASE_URL')

【清理步驟】
1. 移除所有憑證 → os.getenv()
2. 移除真實 PII → 用假名或移除
3. 移除內部資訊 → 泛化描述
4. 聚焦問題 → 只分享必要上下文

【記憶點】
假設分享給 AI = 公開發布
3 秒檢查清單: 憑證?PII?內部資訊?
```

---

### C10: 安全事件優先級

**正面**:
```
【情境】安全掃描發現以下問題,如何排優先級?

A. SQL 注入 (login 函數)
B. 使用 MD5 雜湊密碼
C. .env 檔案不在 .gitignore
D. 缺少 rate limiting
E. 硬編碼 JWT secret
F. 日誌包含用戶 email
G. 依賴套件有 CVE (critical)

你的修復順序?
```

**背面**:
```
【優先級排序】

🔴 P0 - CRITICAL (立即修復,< 24 小時)
1. A - SQL 注入 (可直接竊取資料庫)
2. E - 硬編碼 JWT secret (可偽造任意用戶)
3. G - 依賴漏洞 CVE (可能被遠端攻擊)

🟠 P1 - HIGH (本週內)
4. C - .env 不在 .gitignore (隨時可能洩漏)
5. B - 弱密碼雜湊 (可被破解,但需已洩漏)

🟡 P2 - MEDIUM (2 週內)
6. F - 日誌洩漏 PII (合規問題)
7. D - 缺少 rate limiting (暴力破解風險)

【判斷標準】

CRITICAL:
- 可直接導致資料洩漏/系統控制
- 不需其他條件即可利用
- 影響所有用戶

HIGH:
- 需要一定條件才能利用
- 或影響範圍較小
- 但仍有嚴重後果

MEDIUM:
- 需要多個條件配合
- 或主要是合規/最佳實踐問題
- 後果相對可控

【記憶點】
能直接拿 shell 或竊取資料 → CRITICAL
需要先有其他漏洞配合 → HIGH
主要是合規或防禦深度 → MEDIUM

優先修復能被直接利用的漏洞!
```

---

## 📊 使用建議

### 學習節奏
- **第 1 週**: 每天 2 張,聚焦憑證與代碼安全
- **第 2 週**: 每天 2 張,覆蓋隱私與合規
- **第 3 週**: 複習所有卡片,測試反應速度

### 目標
- 看到問題代碼能在 **5 秒內** 反應
- 知道 **為什麼** 不安全
- 知道 **怎麼修復**
- 形成肌肉記憶

---

## 🎯 Anki 設置

### 匯入這些卡片

1. 下載 [Anki](https://apps.ankiweb.net/)
2. 建立新 Deck: "AI 輔助開發安全"
3. 每張卡片手動輸入或使用提供的 CSV
4. 每天複習 (Anki 會自動排程)

### 最佳實踐
- 早上複習,保持警覺性
- 答錯時實際寫一遍正確代碼
- 定期更新卡片 (新的安全模式)

---

**完成所有閃卡後,安全意識將成為你的本能反應!**
