# B01：TDD 構建用戶註冊功能

## 📋 情境描述

你正在開發一個線上服務的用戶註冊功能。產品經理給你以下需求：

**需求**：
用戶應該能夠註冊帳號，需要提供：
- Email（必須是有效的 email 格式）
- 密碼（至少 8 個字元）
- 用戶名（3-20 個字元，只能包含字母、數字、底線）

**任務**：
用完整的 TDD 方式實作這個功能。

**時間估計**：30-40 分鐘

---

## 🎯 學習目標

- [ ] 體驗完整的紅-綠-重構循環
- [ ] 理解「測試先行」的威力
- [ ] 掌握小步迭代的節奏
- [ ] 建立對 TDD 的信心

---

## 🛠️ 技術要求

**語言**：Python 3.11+
**測試框架**：pytest
**檔案結構**：
```
registration/
├── user_registration.py    # 實作檔案
└── test_user_registration.py  # 測試檔案
```

---

## 📝 實作步驟

### 準備工作

**建立專案目錄**：
```bash
mkdir -p registration
cd registration

# 建立虛擬環境
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安裝 pytest
pip install pytest
```

**建立檔案**：
```bash
touch user_registration.py
touch test_user_registration.py
```

---

### 循環 1：驗證 Email 格式

#### 🔴 RED：寫第一個測試

**test_user_registration.py**：
```python
import pytest
from user_registration import UserRegistration

def test_valid_email_is_accepted():
    """測試有效的 email 應該被接受"""
    registration = UserRegistration()

    result = registration.validate_email("test@example.com")

    assert result is True
```

**執行測試**：
```bash
$ pytest test_user_registration.py -v

# 預期結果：失敗
FAILED - ModuleNotFoundError: No module named 'user_registration'
```

✓ 測試失敗（預期的）

#### 🟢 GREEN：最簡實作

**user_registration.py**：
```python
class UserRegistration:
    def validate_email(self, email):
        return True  # 最簡單的實作：直接返回 True
```

**執行測試**：
```bash
$ pytest test_user_registration.py -v

PASSED ✓
```

✓ 測試通過！

#### 🔵 REFACTOR：重構（暫不需要）

目前程式碼很簡單，不需要重構。

---

### 循環 2：拒絕無效的 Email

#### 🔴 RED：新增測試

**test_user_registration.py**（新增）：
```python
def test_invalid_email_is_rejected():
    """測試無效的 email 應該被拒絕"""
    registration = UserRegistration()

    result = registration.validate_email("invalid-email")

    assert result is False
```

**執行測試**：
```bash
$ pytest test_user_registration.py -v

# 預期結果：新測試失敗
PASSED test_valid_email_is_accepted ✓
FAILED test_invalid_email_is_rejected ✗
  AssertionError: assert True is False
```

✓ 新測試失敗（預期的）

#### 🟢 GREEN：實作 Email 驗證

**user_registration.py**：
```python
import re

class UserRegistration:
    def validate_email(self, email):
        # 簡單的 email 正則表達式
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))
```

**執行測試**：
```bash
$ pytest test_user_registration.py -v

PASSED test_valid_email_is_accepted ✓
PASSED test_invalid_email_is_rejected ✓
```

✓ 兩個測試都通過！

#### 🔵 REFACTOR：提取常數

**user_registration.py**：
```python
import re

class UserRegistration:
    EMAIL_PATTERN = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

    def validate_email(self, email):
        return bool(re.match(self.EMAIL_PATTERN, email))
```

**執行測試**：
```bash
$ pytest test_user_registration.py -v

PASSED ✓✓  # 測試依然通過
```

---

### 循環 3：驗證密碼長度

#### 🔴 RED：新增測試

**test_user_registration.py**（新增）：
```python
def test_valid_password_is_accepted():
    """測試有效的密碼應該被接受"""
    registration = UserRegistration()

    result = registration.validate_password("password123")

    assert result is True

def test_short_password_is_rejected():
    """測試過短的密碼應該被拒絕"""
    registration = UserRegistration()

    result = registration.validate_password("short")

    assert result is False
```

**執行測試**：
```bash
$ pytest test_user_registration.py -v

PASSED ✓✓
FAILED test_valid_password_is_accepted ✗
  AttributeError: 'UserRegistration' object has no attribute 'validate_password'
```

#### 🟢 GREEN：實作密碼驗證

**user_registration.py**（新增）：
```python
class UserRegistration:
    EMAIL_PATTERN = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    MIN_PASSWORD_LENGTH = 8

    def validate_email(self, email):
        return bool(re.match(self.EMAIL_PATTERN, email))

    def validate_password(self, password):
        return len(password) >= self.MIN_PASSWORD_LENGTH
```

**執行測試**：
```bash
$ pytest test_user_registration.py -v

PASSED ✓✓✓✓  # 所有測試通過
```

---

### 循環 4：驗證用戶名

#### 🔴 RED：新增測試

**test_user_registration.py**（新增）：
```python
def test_valid_username_is_accepted():
    """測試有效的用戶名應該被接受"""
    registration = UserRegistration()

    result = registration.validate_username("john_doe")

    assert result is True

def test_short_username_is_rejected():
    """測試過短的用戶名應該被拒絕"""
    registration = UserRegistration()

    result = registration.validate_username("ab")

    assert result is False

def test_long_username_is_rejected():
    """測試過長的用戶名應該被拒絕"""
    registration = UserRegistration()

    result = registration.validate_username("a" * 21)

    assert result is False

def test_invalid_characters_in_username_are_rejected():
    """測試包含無效字元的用戶名應該被拒絕"""
    registration = UserRegistration()

    result = registration.validate_username("john-doe")  # 不允許連字號

    assert result is False
```

**執行測試**：
```bash
$ pytest test_user_registration.py -v

# 前 4 個通過，新的 4 個失敗
```

#### 🟢 GREEN：實作用戶名驗證

**user_registration.py**（新增）：
```python
class UserRegistration:
    EMAIL_PATTERN = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    USERNAME_PATTERN = r'^[a-zA-Z0-9_]{3,20}$'
    MIN_PASSWORD_LENGTH = 8

    def validate_email(self, email):
        return bool(re.match(self.EMAIL_PATTERN, email))

    def validate_password(self, password):
        return len(password) >= self.MIN_PASSWORD_LENGTH

    def validate_username(self, username):
        return bool(re.match(self.USERNAME_PATTERN, username))
```

**執行測試**：
```bash
$ pytest test_user_registration.py -v

PASSED ✓✓✓✓✓✓✓✓  # 所有 8 個測試通過
```

#### 🔵 REFACTOR：提取 fixture

**test_user_registration.py**（重構）：
```python
import pytest
from user_registration import UserRegistration

@pytest.fixture
def registration():
    """建立 UserRegistration 實例"""
    return UserRegistration()

def test_valid_email_is_accepted(registration):
    result = registration.validate_email("test@example.com")
    assert result is True

def test_invalid_email_is_rejected(registration):
    result = registration.validate_email("invalid-email")
    assert result is False

# ... 其他測試也改用 fixture
```

**執行測試**：
```bash
$ pytest test_user_registration.py -v

PASSED ✓✓✓✓✓✓✓✓  # 重構後依然通過
```

---

### 循環 5：完整的註冊功能

#### 🔴 RED：測試註冊流程

**test_user_registration.py**（新增）：
```python
def test_register_user_with_valid_data(registration):
    """測試使用有效資料註冊用戶"""
    user = registration.register(
        email="john@example.com",
        password="password123",
        username="john_doe"
    )

    assert user is not None
    assert user['email'] == "john@example.com"
    assert user['username'] == "john_doe"
    assert 'password' not in user  # 不應該返回密碼

def test_register_user_with_invalid_email(registration):
    """測試使用無效 email 註冊應該失敗"""
    with pytest.raises(ValueError, match="Invalid email"):
        registration.register(
            email="invalid",
            password="password123",
            username="john_doe"
        )

def test_register_user_with_invalid_password(registration):
    """測試使用無效密碼註冊應該失敗"""
    with pytest.raises(ValueError, match="Invalid password"):
        registration.register(
            email="john@example.com",
            password="short",
            username="john_doe"
        )

def test_register_user_with_invalid_username(registration):
    """測試使用無效用戶名註冊應該失敗"""
    with pytest.raises(ValueError, match="Invalid username"):
        registration.register(
            email="john@example.com",
            password="password123",
            username="a"
        )
```

**執行測試**：
```bash
$ pytest test_user_registration.py -v

# 前 8 個通過，新的 4 個失敗（預期）
```

#### 🟢 GREEN：實作註冊功能

**user_registration.py**（新增）：
```python
class UserRegistration:
    EMAIL_PATTERN = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    USERNAME_PATTERN = r'^[a-zA-Z0-9_]{3,20}$'
    MIN_PASSWORD_LENGTH = 8

    def validate_email(self, email):
        return bool(re.match(self.EMAIL_PATTERN, email))

    def validate_password(self, password):
        return len(password) >= self.MIN_PASSWORD_LENGTH

    def validate_username(self, username):
        return bool(re.match(self.USERNAME_PATTERN, username))

    def register(self, email, password, username):
        # 驗證所有欄位
        if not self.validate_email(email):
            raise ValueError("Invalid email")
        if not self.validate_password(password):
            raise ValueError("Invalid password")
        if not self.validate_username(username):
            raise ValueError("Invalid username")

        # 建立用戶（實際應該儲存到資料庫）
        user = {
            'email': email,
            'username': username,
            # 實際應該雜湊密碼
        }
        return user
```

**執行測試**：
```bash
$ pytest test_user_registration.py -v

PASSED ✓✓✓✓✓✓✓✓✓✓✓✓  # 所有 12 個測試通過！
```

---

## ✅ 完整程式碼

### user_registration.py（最終版本）

```python
import re

class UserRegistration:
    """處理用戶註冊邏輯"""

    EMAIL_PATTERN = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    USERNAME_PATTERN = r'^[a-zA-Z0-9_]{3,20}$'
    MIN_PASSWORD_LENGTH = 8

    def validate_email(self, email):
        """驗證 email 格式"""
        return bool(re.match(self.EMAIL_PATTERN, email))

    def validate_password(self, password):
        """驗證密碼長度"""
        return len(password) >= self.MIN_PASSWORD_LENGTH

    def validate_username(self, username):
        """驗證用戶名格式和長度"""
        return bool(re.match(self.USERNAME_PATTERN, username))

    def register(self, email, password, username):
        """註冊新用戶"""
        if not self.validate_email(email):
            raise ValueError("Invalid email")
        if not self.validate_password(password):
            raise ValueError("Invalid password")
        if not self.validate_username(username):
            raise ValueError("Invalid username")

        # 在真實應用中，這裡應該：
        # 1. 雜湊密碼
        # 2. 儲存到資料庫
        # 3. 返回用戶 ID

        user = {
            'email': email,
            'username': username,
        }
        return user
```

### test_user_registration.py（最終版本）

```python
import pytest
from user_registration import UserRegistration

@pytest.fixture
def registration():
    return UserRegistration()

# Email 驗證測試
def test_valid_email_is_accepted(registration):
    assert registration.validate_email("test@example.com") is True

def test_invalid_email_is_rejected(registration):
    assert registration.validate_email("invalid-email") is False

# 密碼驗證測試
def test_valid_password_is_accepted(registration):
    assert registration.validate_password("password123") is True

def test_short_password_is_rejected(registration):
    assert registration.validate_password("short") is False

# 用戶名驗證測試
def test_valid_username_is_accepted(registration):
    assert registration.validate_username("john_doe") is True

def test_short_username_is_rejected(registration):
    assert registration.validate_username("ab") is False

def test_long_username_is_rejected(registration):
    assert registration.validate_username("a" * 21) is False

def test_invalid_characters_in_username_are_rejected(registration):
    assert registration.validate_username("john-doe") is False

# 註冊流程測試
def test_register_user_with_valid_data(registration):
    user = registration.register(
        email="john@example.com",
        password="password123",
        username="john_doe"
    )
    assert user is not None
    assert user['email'] == "john@example.com"
    assert user['username'] == "john_doe"
    assert 'password' not in user

def test_register_user_with_invalid_email(registration):
    with pytest.raises(ValueError, match="Invalid email"):
        registration.register(
            email="invalid",
            password="password123",
            username="john_doe"
        )

def test_register_user_with_invalid_password(registration):
    with pytest.raises(ValueError, match="Invalid password"):
        registration.register(
            email="john@example.com",
            password="short",
            username="john_doe"
        )

def test_register_user_with_invalid_username(registration):
    with pytest.raises(ValueError, match="Invalid username"):
        registration.register(
            email="john@example.com",
            password="password123",
            username="a"
        )
```

---

## 📊 執行測試與覆蓋率

**執行所有測試**：
```bash
$ pytest test_user_registration.py -v

================= test session starts =================
test_user_registration.py::test_valid_email_is_accepted PASSED
test_user_registration.py::test_invalid_email_is_rejected PASSED
test_user_registration.py::test_valid_password_is_accepted PASSED
test_user_registration.py::test_short_password_is_rejected PASSED
test_user_registration.py::test_valid_username_is_accepted PASSED
test_user_registration.py::test_short_username_is_rejected PASSED
test_user_registration.py::test_long_username_is_rejected PASSED
test_user_registration.py::test_invalid_characters_in_username_are_rejected PASSED
test_user_registration.py::test_register_user_with_valid_data PASSED
test_user_registration.py::test_register_user_with_invalid_email PASSED
test_user_registration.py::test_register_user_with_invalid_password PASSED
test_user_registration.py::test_register_user_with_invalid_username PASSED
================= 12 passed in 0.05s =================
```

**測試覆蓋率**：
```bash
$ pytest --cov=user_registration --cov-report=term-missing

Name                    Stmts   Miss  Cover   Missing
-----------------------------------------------------
user_registration.py       15      0   100%
-----------------------------------------------------
TOTAL                      15      0   100%
```

✓ 100% 測試覆蓋率！

---

## 🎓 學習重點

### 你學到了什麼

1. **紅-綠-重構循環**：
   - 先寫失敗的測試
   - 用最簡單的方式讓測試通過
   - 重構改善程式碼品質

2. **小步迭代**：
   - 一次只做一件事
   - 每個循環 5-10 分鐘
   - 累積進度建立信心

3. **測試驅動設計**：
   - 測試迫使你思考介面
   - 測試揭示設計問題
   - 簡潔的 API 設計

4. **即時反饋**：
   - 幾秒內知道是否正確
   - 錯誤時容易定位
   - 避免累積技術債

### 關鍵收穫

✅ **TDD 不會拖慢開發**：
- 雖然一開始感覺慢
- 但幾乎不需要 debug
- 整體速度反而更快

✅ **測試即文檔**：
- 測試清楚描述行為
- 永遠不會過時
- 新人可以通過測試理解程式碼

✅ **重構的保護網**：
- 有測試保護，敢放心重構
- 保持程式碼乾淨
- 持續改善設計

---

## 🚀 進階挑戰

完成基本實作後，嘗試以下挑戰：

### 挑戰 1：新增密碼強度檢查
- 必須包含大寫字母
- 必須包含小寫字母
- 必須包含數字
- 必須包含特殊字元

### 挑戰 2：檢查重複註冊
- Email 不能重複
- 用戶名不能重複
- 需要 mock 資料庫

### 挑戰 3：密碼雜湊
- 使用 bcrypt 雜湊密碼
- 不儲存明文密碼
- 提供密碼驗證方法

### 挑戰 4：完整錯誤訊息
- 返回具體的錯誤原因
- 支援多語言錯誤訊息
- 友善的用戶體驗

---

## 📈 自我評量

完成本情境後，檢查以下項目：

### 流程遵循
- [ ] 每個功能都先寫測試
- [ ] 看到測試失敗後才實作
- [ ] 測試通過後進行重構
- [ ] 重構後測試依然通過

### 程式碼品質
- [ ] 測試清晰且易讀
- [ ] 測試名稱描述性強
- [ ] 實作簡潔不過度設計
- [ ] 使用適當的常數和 fixture

### 測試品質
- [ ] 覆蓋率達 100%
- [ ] 測試獨立且可重複執行
- [ ] 測試執行速度快（< 1 秒）
- [ ] 測試失敗時容易定位問題

---

**恭喜完成第一個 TDD 情境！**
**體驗如何？是否感受到測試先行的威力？**
**繼續練習，TDD 會成為你的自然習慣！**
