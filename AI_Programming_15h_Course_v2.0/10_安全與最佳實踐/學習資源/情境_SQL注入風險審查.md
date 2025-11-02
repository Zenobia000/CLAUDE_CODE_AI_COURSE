# 情境：SQL 注入風險審查

> **學習目標**: 透過真實場景學習識別並修復 AI 生成代碼中的 SQL 注入漏洞

---

## 情境背景

你正在開發用戶搜尋功能，向 Claude 詢問：

**你的提問**:
> "幫我寫一個 Python 函數，根據用戶名搜尋資料庫中的用戶資料"

**Claude 回覆的代碼**:
```python
import sqlite3

def search_users(keyword):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    # 搜尋用戶
    query = f"SELECT * FROM users WHERE name LIKE '%{keyword}%'"
    cursor.execute(query)

    results = cursor.fetchall()
    conn.close()
    return results
```

這段代碼看起來能正常運作，你測試後確實能搜尋到用戶...

---

## 🚨 問題識別

### 危險信號

```python
query = f"SELECT * FROM users WHERE name LIKE '%{keyword}%'"  # ⚠️ SQL 注入風險！
```

**為什麼危險？**
- 用戶輸入 (`keyword`) 直接插入 SQL 語句
- 攻擊者可以構造惡意輸入改變 SQL 結構
- 可能導致數據洩漏、刪除或篡改

### 攻擊範例

```python
# 正常使用
search_users("張三")  # → SELECT * FROM users WHERE name LIKE '%張三%'

# 惡意輸入 #1: 洩漏所有數據
search_users("' OR '1'='1")
# → SELECT * FROM users WHERE name LIKE '%' OR '1'='1%'
# 結果: 返回所有用戶資料！

# 惡意輸入 #2: 刪除數據
search_users("'; DROP TABLE users--")
# → SELECT * FROM users WHERE name LIKE '%'; DROP TABLE users--%'
# 結果: 刪除整個 users 表！
```

---

## 🔧 修復方案

### 方案 #1: 參數化查詢 (推薦)

```python
# ✅ 安全做法
import sqlite3

def search_users(keyword):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    # 使用參數化查詢（佔位符 ?）
    query = "SELECT * FROM users WHERE name LIKE ?"
    cursor.execute(query, (f'%{keyword}%',))  # 參數作為 tuple 傳遞

    results = cursor.fetchall()
    conn.close()
    return results
```

**為什麼安全？**
- SQL 語句與數據分離
- 資料庫驅動會自動轉義特殊字元
- 攻擊者無法改變 SQL 結構

### 方案 #2: 使用 ORM (SQLAlchemy)

```python
# ✅ 使用 ORM 更安全
from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)

engine = create_engine('sqlite:///users.db')
Session = sessionmaker(bind=engine)

def search_users(keyword):
    session = Session()
    # ORM 自動處理參數化
    results = session.query(User).filter(
        User.name.like(f'%{keyword}%')
    ).all()
    session.close()
    return results
```

---

## 🛡️ 預防措施

### 防線 #1: 使用 Semgrep 掃描

```bash
# 安裝 Semgrep
pip install semgrep

# 掃描 SQL 注入風險
semgrep --config "p/sql-injection" .
```

**Semgrep 規則** (`.semgrep.yml`):
```yaml
rules:
  - id: sql-injection-f-string
    pattern: cursor.execute(f"... {$VAR} ...")
    message: "SQL injection risk using f-string"
    severity: ERROR
    languages: [python]

  - id: sql-injection-concat
    pattern: cursor.execute("..." + $VAR + "...")
    message: "SQL injection risk using string concatenation"
    severity: ERROR
    languages: [python]
```

---

### 防線 #2: 代碼審查檢查清單

```
SQL 注入風險檢查:

[ ] 是否使用 f-string 構造 SQL 查詢？
    f"SELECT ... {variable}"  → ❌ 危險

[ ] 是否使用字串拼接構造 SQL？
    "SELECT ... " + variable  → ❌ 危險

[ ] 是否使用 .format() 構造 SQL？
    "SELECT ... {}".format(variable)  → ❌ 危險

[ ] 是否使用參數化查詢？
    cursor.execute("SELECT ... ?", (variable,))  → ✅ 安全

[ ] 是否使用 ORM？
    query(User).filter(User.name == variable)  → ✅ 安全
```

---

## 📚 自然學到的指令與工具

### 安全檢測工具

```bash
# Semgrep - 靜態代碼分析
semgrep --config "p/sql-injection" .
semgrep --config auto .

# Bandit - Python 安全掃描
bandit -r . -f json

# SQLMap - SQL 注入測試工具 (滲透測試用)
sqlmap -u "http://example.com/search?q=test"
```

### Python 參數化查詢

```python
# SQLite3
cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))

# PostgreSQL (psycopg2)
cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))

# MySQL (mysql-connector-python)
cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))

# SQLAlchemy ORM
session.query(User).filter(User.id == user_id).first()
```

---

## 🎯 情境延伸

### 挑戰: 檢查現有專案

```bash
# 快速掃描所有 Python 文件中的 SQL 注入風險
grep -rn "execute(f\"" --include="*.py" .
grep -rn "execute(\".*\" \+" --include="*.py" .
grep -rn "\.format(" --include="*.py" | grep -i "select\|insert\|update\|delete"

# 使用 Semgrep 自動化掃描
semgrep --config "p/sql-injection" . --json > sql_injection_report.json
```

---

## ✅ 學習驗證

完成此情境後，你應該能夠：

- [ ] 識別 f-string、字串拼接、.format() 構造的 SQL 查詢
- [ ] 使用參數化查詢重構代碼
- [ ] 理解 SQL 注入的攻擊原理
- [ ] 使用 Semgrep 掃描 SQL 注入風險

---

## 🔗 延伸學習

- **理論**: `理論/10.1_AI生成代碼安全風險.md` - 深入了解 SQL 注入
- **實作**: `情境題庫/基礎級/B02_AI代碼安全審查.md` - 完整安全審查流程
- **工具**: [OWASP SQL Injection Guide](https://owasp.org/www-community/attacks/SQL_Injection)

---

**記住**：

> **「永遠不要相信用戶輸入 — 包括你自己的輸入」**

使用參數化查詢是防止 SQL 注入的黃金法則。
