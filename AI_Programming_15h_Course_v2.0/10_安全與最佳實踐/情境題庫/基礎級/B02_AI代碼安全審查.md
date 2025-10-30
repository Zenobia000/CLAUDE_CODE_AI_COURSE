# B02: AI 代碼安全審查

> **難度**: ⭐⭐ 基礎級
>
> **預計耗時**: 30-45 分鐘
>
> **核心技能**: 識別 AI 生成代碼的安全漏洞、使用自動化掃描工具

---

## 📖 情境描述

你的同事 Alex 使用 GitHub Copilot 快速開發了一個用戶認證系統。他興奮地說:「Copilot 太強了!10 分鐘就寫好了整個登入系統!」

作為 Code Reviewer,你需要審查以下 AI 生成的代碼:

```python
# auth.py
import sqlite3
import hashlib

DATABASE = 'users.db'

def init_db():
    """Initialize database"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT UNIQUE,
            password TEXT,
            email TEXT,
            role TEXT DEFAULT 'user'
        )
    """)
    conn.commit()
    conn.close()

def register_user(username, password, email):
    """Register a new user"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # Hash password
    password_hash = hashlib.md5(password.encode()).hexdigest()

    # Insert user
    query = f"INSERT INTO users (username, password, email) VALUES ('{username}', '{password_hash}', '{email}')"
    cursor.execute(query)

    conn.commit()
    conn.close()
    return True

def login(username, password):
    """Login user"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    password_hash = hashlib.md5(password.encode()).hexdigest()
    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password_hash}'"

    cursor.execute(query)
    user = cursor.fetchone()

    conn.close()

    if user:
        return {"id": user[0], "username": user[1], "role": user[4]}
    return None

def get_user_data(user_id):
    """Get user data by ID"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    query = f"SELECT * FROM users WHERE id = {user_id}"
    cursor.execute(query)
    user = cursor.fetchone()

    conn.close()
    return user

def update_user_role(username, new_role):
    """Update user role (admin function)"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    query = f"UPDATE users SET role = '{new_role}' WHERE username = '{username}'"
    cursor.execute(query)

    conn.commit()
    conn.close()

# Test usage
if __name__ == "__main__":
    init_db()

    # Register test user
    register_user("admin", "admin123", "admin@example.com")

    # Login
    user = login("admin", "admin123")
    if user:
        print(f"Login successful: {user}")
```

Alex 說:「代碼都能跑,而且 Copilot 還自動生成了測試案例!我準備部署到生產環境了。」

**你的任務**: 在他部署前,找出所有安全漏洞並提供修復方案。

---

## 🎯 任務目標

### 任務 1: 安全漏洞識別 (15 分鐘)
- [ ] 通讀代碼,標記所有可疑的地方
- [ ] 分類漏洞類型 (SQL 注入、弱加密等)
- [ ] 評估每個漏洞的嚴重程度

### 任務 2: 自動化掃描 (10 分鐘)
- [ ] 使用 `bandit` 掃描 Python 代碼
- [ ] 使用 `semgrep` 檢測安全模式
- [ ] 比較手動發現和工具發現的差異

### 任務 3: 修復方案 (15 分鐘)
- [ ] 重寫代碼,修復所有安全漏洞
- [ ] 使用參數化查詢
- [ ] 使用安全的密碼雜湊
- [ ] 添加輸入驗證

### 任務 4: Code Review 報告 (5 分鐘)
- [ ] 撰寫 Code Review 評論
- [ ] 說明每個問題的風險
- [ ] 提供清晰的修復建議

---

## 🔍 考察重點

1. **安全漏洞識別能力**: 能否快速找出 Top 5 常見漏洞
2. **工具使用**: 熟悉自動化安全掃描工具
3. **安全編碼**: 知道正確的安全實踐
4. **溝通能力**: 能清楚解釋安全風險給非專家

---

## 💡 提示

<details>
<summary>提示 1: 應該找到至少 5 個嚴重問題</summary>

1. SQL 注入 (CRITICAL)
2. 弱密碼雜湊 (HIGH)
3. 硬編碼測試憑證 (MEDIUM)
4. 缺少輸入驗證 (MEDIUM)
5. 連接未關閉 (LOW)

</details>

<details>
<summary>提示 2: 使用掃描工具</summary>

```bash
# Bandit (Python 安全掃描)
pip install bandit
bandit -r auth.py

# Semgrep (通用安全掃描)
pip install semgrep
semgrep --config "p/python" auth.py
```

</details>

---

## ✅ 參考解答

### 發現的安全漏洞

#### 1. SQL 注入 (CRITICAL) - 3 處

**問題代碼**:
```python
query = f"INSERT INTO users (username, password, email) VALUES ('{username}', '{password_hash}', '{email}')"
query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password_hash}'"
query = f"UPDATE users SET role = '{new_role}' WHERE username = '{username}'"
```

**攻擊範例**:
```python
# 攻擊 1: 繞過登入
login("admin' OR '1'='1", "anything")
# 實際 SQL: SELECT * FROM users WHERE username = 'admin' OR '1'='1' AND password = '...'

# 攻擊 2: 提升權限
update_user_role("nonexist' OR '1'='1", "admin")
# 實際 SQL: UPDATE users SET role = 'admin' WHERE username = 'nonexist' OR '1'='1'
# 結果: 所有用戶都變成 admin!

# 攻擊 3: 資料庫破壞
register_user("test'); DROP TABLE users; --", "pass", "email")
```

---

#### 2. 弱密碼雜湊 (HIGH)

**問題代碼**:
```python
password_hash = hashlib.md5(password.encode()).hexdigest()
```

**問題**:
- MD5 已被破解,不安全
- 沒有 salt,容易被彩虹表攻擊
- 可以在秒級時間內暴力破解

**正確做法**: 使用 `bcrypt` 或 `argon2`

---

#### 3. 硬編碼測試憑證 (MEDIUM)

**問題代碼**:
```python
register_user("admin", "admin123", "admin@example.com")
```

**風險**:
- 如果這段代碼部署到生產環境
- 會建立一個已知憑證的 admin 帳號
- 攻擊者可以直接登入

---

#### 4. 缺少輸入驗證 (MEDIUM)

**問題**:
- 沒有驗證 username 格式
- 沒有驗證 email 格式
- 沒有檢查密碼強度
- 沒有限制輸入長度

---

#### 5. 資源洩漏 (LOW)

**問題**: 每個函數都創建新連接但在錯誤情況下可能不關閉

---

### 自動化掃描結果

```bash
# Bandit 掃描
$ bandit -r auth.py

>> Issue: [B608:hardcoded_sql_expressions] Possible SQL injection vector
   Severity: Medium   Confidence: Low
   Location: auth.py:23
   More Info: https://bandit.readthedocs.io/en/latest/plugins/b608_hardcoded_sql_expressions.html

>> Issue: [B303:md5] Use of insecure MD5 hash function
   Severity: Medium   Confidence: High
   Location: auth.py:22

# 總共發現 6 個問題
```

---

### 修復後的安全版本

```python
# auth_secure.py
import sqlite3
from contextlib import contextmanager
import bcrypt
import re
from typing import Optional, Dict

DATABASE = 'users.db'

# Input validation patterns
USERNAME_PATTERN = re.compile(r'^[a-zA-Z0-9_]{3,20}$')
EMAIL_PATTERN = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')

@contextmanager
def get_db_connection():
    """Context manager for database connections"""
    conn = sqlite3.connect(DATABASE)
    try:
        yield conn
    finally:
        conn.close()

def validate_username(username: str) -> bool:
    """Validate username format"""
    return bool(USERNAME_PATTERN.match(username))

def validate_email(email: str) -> bool:
    """Validate email format"""
    return bool(EMAIL_PATTERN.match(email))

def validate_password_strength(password: str) -> bool:
    """Check password strength"""
    if len(password) < 8:
        return False
    if not any(c.isupper() for c in password):
        return False
    if not any(c.islower() for c in password):
        return False
    if not any(c.isdigit() for c in password):
        return False
    return True

def init_db():
    """Initialize database"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                role TEXT DEFAULT 'user' NOT NULL,
                CHECK(role IN ('user', 'admin'))
            )
        """)
        conn.commit()

def register_user(username: str, password: str, email: str) -> Dict:
    """Register a new user"""
    # Input validation
    if not validate_username(username):
        raise ValueError("Invalid username format (3-20 alphanumeric chars)")

    if not validate_email(email):
        raise ValueError("Invalid email format")

    if not validate_password_strength(password):
        raise ValueError(
            "Password must be at least 8 characters with "
            "uppercase, lowercase, and numbers"
        )

    # Hash password with bcrypt (includes salt automatically)
    password_hash = bcrypt.hashpw(
        password.encode('utf-8'),
        bcrypt.gensalt()
    ).decode('utf-8')

    with get_db_connection() as conn:
        cursor = conn.cursor()

        # Parameterized query (prevents SQL injection)
        try:
            cursor.execute(
                "INSERT INTO users (username, password, email) VALUES (?, ?, ?)",
                (username, password_hash, email)
            )
            conn.commit()
            return {"success": True, "message": "User registered successfully"}
        except sqlite3.IntegrityError:
            return {"success": False, "message": "Username or email already exists"}

def login(username: str, password: str) -> Optional[Dict]:
    """Login user"""
    if not username or not password:
        return None

    with get_db_connection() as conn:
        cursor = conn.cursor()

        # Parameterized query
        cursor.execute(
            "SELECT id, username, password, role FROM users WHERE username = ?",
            (username,)
        )
        user = cursor.fetchone()

    if user and bcrypt.checkpw(password.encode('utf-8'), user[2].encode('utf-8')):
        return {
            "id": user[0],
            "username": user[1],
            "role": user[3]
        }

    return None

def get_user_data(user_id: int) -> Optional[tuple]:
    """Get user data by ID"""
    if not isinstance(user_id, int) or user_id <= 0:
        raise ValueError("Invalid user ID")

    with get_db_connection() as conn:
        cursor = conn.cursor()

        # Parameterized query
        cursor.execute(
            "SELECT id, username, email, role FROM users WHERE id = ?",
            (user_id,)
        )
        return cursor.fetchone()

def update_user_role(user_id: int, new_role: str, admin_user_id: int) -> Dict:
    """Update user role (admin function only)"""
    # Validate role
    if new_role not in ('user', 'admin'):
        raise ValueError("Invalid role")

    # Check if requester is admin
    admin = get_user_data(admin_user_id)
    if not admin or admin[3] != 'admin':
        raise PermissionError("Only admins can change user roles")

    with get_db_connection() as conn:
        cursor = conn.cursor()

        # Parameterized query
        cursor.execute(
            "UPDATE users SET role = ? WHERE id = ?",
            (new_role, user_id)
        )
        conn.commit()

    return {"success": True, "message": "Role updated successfully"}

# Test usage (should be in separate test file, not production code)
if __name__ == "__main__":
    import os

    # Use environment variable for test password
    test_password = os.getenv('TEST_PASSWORD', 'TestPass123!')

    init_db()

    # Register test user (use strong password)
    result = register_user("testuser", test_password, "test@example.com")
    print(result)

    # Login
    user = login("testuser", test_password)
    if user:
        print(f"Login successful: {user}")
    else:
        print("Login failed")
```

---

### Code Review 報告範本

```markdown
## Code Review: auth.py

### 🔴 Critical Issues (Must Fix Before Deployment)

#### 1. SQL Injection Vulnerabilities
**Location**: Lines 23, 34, 54, 68
**Risk**: Attacker can bypass authentication, elevate privileges, or destroy database
**Impact**: Complete system compromise

**Current Code**:
```python
query = f"SELECT * FROM users WHERE username = '{username}' AND ..."
```

**Fix**:
```python
cursor.execute("SELECT * FROM users WHERE username = ? AND ...", (username,))
```

**Attack Demo**:
- Input: `admin' OR '1'='1`
- Result: Bypass login as any user

---

#### 2. Weak Password Hashing (MD5)
**Location**: Lines 22, 33
**Risk**: Passwords can be cracked in seconds using rainbow tables
**Impact**: All user accounts compromised

**Current Code**:
```python
password_hash = hashlib.md5(password.encode()).hexdigest()
```

**Fix**:
```python
import bcrypt
password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
```

---

### 🟡 High Priority Issues

#### 3. Hardcoded Test Credentials
**Location**: Line 76
**Risk**: Known admin credentials in production
**Impact**: Unauthorized admin access

**Fix**: Move to separate test file, use environment variables

---

#### 4. Missing Input Validation
**Risk**: Malformed input can cause errors or attacks
**Fix**: Add regex validation for username/email, password strength check

---

### ✅ Recommendations

1. **Immediate Actions**:
   - Stop deployment
   - Fix SQL injection (highest priority)
   - Replace MD5 with bcrypt

2. **Before Next Deploy**:
   - Add input validation
   - Remove test credentials
   - Add proper error handling

3. **Long Term**:
   - Implement rate limiting
   - Add logging for security events
   - Set up automated security scans in CI/CD

---

**Approval Status**: ❌ **NOT APPROVED** for production

**Estimated Fix Time**: 2-3 hours
```

---

## 🤔 延伸思考

### 為什麼 AI 會生成不安全的代碼?

1. **訓練數據偏差**: 很多教學範例使用不安全的簡化寫法
2. **功能優先**: AI 優化為「能運行」而非「安全運行」
3. **上下文限制**: AI 不知道這是生產代碼還是教學範例

### 如何讓 AI 生成更安全的代碼?

**更好的 Prompt**:
```
請幫我寫一個用戶認證系統,要求:
- 使用參數化查詢防止 SQL 注入
- 使用 bcrypt 進行密碼雜湊
- 包含輸入驗證
- 添加適當的錯誤處理
- 遵循 OWASP 安全最佳實踐
```

---

## 📝 檢查清單

完成此情境後,你應該能夠:

- [ ] 在 5 分鐘內識別代碼中的 SQL 注入
- [ ] 知道為什麼 MD5 不安全
- [ ] 會使用 bandit/semgrep 掃描代碼
- [ ] 能撰寫清晰的 Code Review 評論
- [ ] 理解如何引導 AI 生成更安全的代碼

---

**下一步**: 完成組合級情境 C01,學習執行完整的安全審計流程
