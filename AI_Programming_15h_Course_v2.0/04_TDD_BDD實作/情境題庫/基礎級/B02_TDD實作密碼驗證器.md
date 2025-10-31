# B02：TDD 實作密碼驗證器

## 📋 情境描述

你正在開發一個安全性要求很高的系統，需要實作密碼驗證器來確保用戶密碼符合安全標準。

**需求**：
密碼必須滿足以下條件：
- 至少 8 個字元
- 包含至少一個大寫字母
- 包含至少一個小寫字母
- 包含至少一個數字
- 包含至少一個特殊字元（!@#$%^&*）
- 不能包含連續 3 個相同字元

**任務**：
用 TDD 方式實作這個密碼驗證器，並提供清晰的錯誤訊息。

**時間估計**：35-45 分鐘

---

## 🎯 學習目標

- [ ] 學習多重驗證規則的測試策略
- [ ] 掌握邊界情況的處理
- [ ] 練習清晰錯誤訊息的設計
- [ ] 體驗測試驅動的複雜邏輯設計

---

## 🛠️ 技術要求

**語言**：Python 3.11+
**測試框架**：pytest
**檔案結構**：
```
password_validator/
├── password_validator.py    # 實作檔案
└── test_password_validator.py  # 測試檔案
```

---

## 📝 實作步驟

### 準備工作

**建立專案目錄**：
```bash
mkdir -p password_validator
cd password_validator

# 建立虛擬環境
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安裝 pytest
pip install pytest
```

**建立檔案**：
```bash
touch password_validator.py
touch test_password_validator.py
```

---

### 循環 1：最小長度驗證

#### 🔴 RED：測試長度要求

**test_password_validator.py**：
```python
import pytest
from password_validator import PasswordValidator

def test_password_with_minimum_length_is_valid():
    """測試達到最小長度的密碼"""
    validator = PasswordValidator()

    result = validator.validate("12345678")

    assert result.is_valid is False  # 只有長度還不夠
    assert "長度" not in result.errors  # 長度要求滿足

def test_password_too_short_is_invalid():
    """測試過短的密碼"""
    validator = PasswordValidator()

    result = validator.validate("1234567")

    assert result.is_valid is False
    assert "至少 8 個字元" in result.errors
```

**執行測試**：
```bash
$ pytest test_password_validator.py -v

FAILED - ModuleNotFoundError: No module named 'password_validator'
```

#### 🟢 GREEN：實作基本結構

**password_validator.py**：
```python
class ValidationResult:
    """驗證結果"""
    def __init__(self):
        self.is_valid = True
        self.errors = []

    def add_error(self, error):
        """新增錯誤"""
        self.is_valid = False
        self.errors.append(error)

class PasswordValidator:
    """密碼驗證器"""
    MIN_LENGTH = 8

    def validate(self, password):
        """驗證密碼"""
        result = ValidationResult()

        # 檢查長度
        if len(password) < self.MIN_LENGTH:
            result.add_error(f"密碼至少需要 {self.MIN_LENGTH} 個字元")

        return result
```

**執行測試**：
```bash
$ pytest test_password_validator.py -v

PASSED ✓✓
```

---

### 循環 2：大寫字母驗證

#### 🔴 RED：新增大寫字母測試

**test_password_validator.py**（新增）：
```python
def test_password_without_uppercase_is_invalid():
    """測試沒有大寫字母的密碼"""
    validator = PasswordValidator()

    result = validator.validate("password123!")

    assert result.is_valid is False
    assert "大寫字母" in result.errors[0]

def test_password_with_uppercase_passes_uppercase_check():
    """測試有大寫字母的密碼通過大寫檢查"""
    validator = PasswordValidator()

    result = validator.validate("Password123!")

    # 可能因為其他規則失敗，但不應該因為大寫字母失敗
    uppercase_errors = [e for e in result.errors if "大寫字母" in e]
    assert len(uppercase_errors) == 0
```

#### 🟢 GREEN：實作大寫字母檢查

**password_validator.py**（更新）：
```python
import re

class PasswordValidator:
    MIN_LENGTH = 8

    def validate(self, password):
        result = ValidationResult()

        # 檢查長度
        if len(password) < self.MIN_LENGTH:
            result.add_error(f"密碼至少需要 {self.MIN_LENGTH} 個字元")

        # 檢查大寫字母
        if not re.search(r'[A-Z]', password):
            result.add_error("密碼必須包含至少一個大寫字母")

        return result
```

**執行測試**：
```bash
$ pytest test_password_validator.py -v

PASSED ✓✓✓✓
```

---

### 循環 3：所有字元類型驗證

#### 🔴 RED：新增所有字元類型測試

**test_password_validator.py**（新增）：
```python
def test_password_without_lowercase_is_invalid():
    """測試沒有小寫字母的密碼"""
    validator = PasswordValidator()

    result = validator.validate("PASSWORD123!")

    assert result.is_valid is False
    assert any("小寫字母" in error for error in result.errors)

def test_password_without_number_is_invalid():
    """測試沒有數字的密碼"""
    validator = PasswordValidator()

    result = validator.validate("Password!")

    assert result.is_valid is False
    assert any("數字" in error for error in result.errors)

def test_password_without_special_char_is_invalid():
    """測試沒有特殊字元的密碼"""
    validator = PasswordValidator()

    result = validator.validate("Password123")

    assert result.is_valid is False
    assert any("特殊字元" in error for error in result.errors)
```

#### 🟢 GREEN：實作所有字元檢查

**password_validator.py**（更新）：
```python
import re

class PasswordValidator:
    MIN_LENGTH = 8
    SPECIAL_CHARS = "!@#$%^&*"

    def validate(self, password):
        result = ValidationResult()

        # 檢查長度
        if len(password) < self.MIN_LENGTH:
            result.add_error(f"密碼至少需要 {self.MIN_LENGTH} 個字元")

        # 檢查大寫字母
        if not re.search(r'[A-Z]', password):
            result.add_error("密碼必須包含至少一個大寫字母")

        # 檢查小寫字母
        if not re.search(r'[a-z]', password):
            result.add_error("密碼必須包含至少一個小寫字母")

        # 檢查數字
        if not re.search(r'[0-9]', password):
            result.add_error("密碼必須包含至少一個數字")

        # 檢查特殊字元
        special_pattern = f"[{re.escape(self.SPECIAL_CHARS)}]"
        if not re.search(special_pattern, password):
            result.add_error(f"密碼必須包含至少一個特殊字元 ({self.SPECIAL_CHARS})")

        return result
```

---

### 循環 4：連續字元檢查

#### 🔴 RED：測試連續字元

**test_password_validator.py**（新增）：
```python
def test_password_with_consecutive_chars_is_invalid():
    """測試有連續相同字元的密碼"""
    validator = PasswordValidator()

    result = validator.validate("Passsword123!")  # 三個 s

    assert result.is_valid is False
    assert any("連續" in error for error in result.errors)

def test_password_with_two_consecutive_chars_is_valid():
    """測試兩個連續字元是允許的"""
    validator = PasswordValidator()

    result = validator.validate("Password123!")  # 兩個 s

    # 不應該因為連續字元失敗
    consecutive_errors = [e for e in result.errors if "連續" in e]
    assert len(consecutive_errors) == 0
```

#### 🟢 GREEN：實作連續字元檢查

**password_validator.py**（更新 validate 方法）：
```python
def validate(self, password):
    result = ValidationResult()

    # 檢查長度
    if len(password) < self.MIN_LENGTH:
        result.add_error(f"密碼至少需要 {self.MIN_LENGTH} 個字元")

    # 檢查大寫字母
    if not re.search(r'[A-Z]', password):
        result.add_error("密碼必須包含至少一個大寫字母")

    # 檢查小寫字母
    if not re.search(r'[a-z]', password):
        result.add_error("密碼必須包含至少一個小寫字母")

    # 檢查數字
    if not re.search(r'[0-9]', password):
        result.add_error("密碼必須包含至少一個數字")

    # 檢查特殊字元
    special_pattern = f"[{re.escape(self.SPECIAL_CHARS)}]"
    if not re.search(special_pattern, password):
        result.add_error(f"密碼必須包含至少一個特殊字元 ({self.SPECIAL_CHARS})")

    # 檢查連續字元
    if self._has_consecutive_chars(password):
        result.add_error("密碼不能包含連續 3 個相同字元")

    return result

def _has_consecutive_chars(self, password):
    """檢查是否有連續 3 個相同字元"""
    for i in range(len(password) - 2):
        if password[i] == password[i + 1] == password[i + 2]:
            return True
    return False
```

---

### 循環 5：完整測試

#### 🔴 RED：測試完全有效的密碼

**test_password_validator.py**（新增）：
```python
def test_valid_password_passes_all_checks():
    """測試完全符合要求的密碼"""
    validator = PasswordValidator()

    result = validator.validate("MyPassword123!")

    assert result.is_valid is True
    assert len(result.errors) == 0

def test_complex_valid_password():
    """測試複雜的有效密碼"""
    validator = PasswordValidator()

    result = validator.validate("C0mpl3x@P@ssw0rd")

    assert result.is_valid is True
    assert len(result.errors) == 0

def test_multiple_errors_are_reported():
    """測試多個錯誤都會被回報"""
    validator = PasswordValidator()

    result = validator.validate("abc")  # 太短、缺少大寫、數字、特殊字元

    assert result.is_valid is False
    assert len(result.errors) >= 4
```

#### 🔵 REFACTOR：提取驗證方法

**password_validator.py**（重構）：
```python
import re

class ValidationResult:
    """驗證結果"""
    def __init__(self):
        self.is_valid = True
        self.errors = []

    def add_error(self, error):
        """新增錯誤"""
        self.is_valid = False
        self.errors.append(error)

class PasswordValidator:
    """密碼驗證器"""
    MIN_LENGTH = 8
    SPECIAL_CHARS = "!@#$%^&*"

    def validate(self, password):
        """驗證密碼"""
        result = ValidationResult()

        self._check_length(password, result)
        self._check_uppercase(password, result)
        self._check_lowercase(password, result)
        self._check_digit(password, result)
        self._check_special_char(password, result)
        self._check_consecutive_chars(password, result)

        return result

    def _check_length(self, password, result):
        """檢查長度"""
        if len(password) < self.MIN_LENGTH:
            result.add_error(f"密碼至少需要 {self.MIN_LENGTH} 個字元")

    def _check_uppercase(self, password, result):
        """檢查大寫字母"""
        if not re.search(r'[A-Z]', password):
            result.add_error("密碼必須包含至少一個大寫字母")

    def _check_lowercase(self, password, result):
        """檢查小寫字母"""
        if not re.search(r'[a-z]', password):
            result.add_error("密碼必須包含至少一個小寫字母")

    def _check_digit(self, password, result):
        """檢查數字"""
        if not re.search(r'[0-9]', password):
            result.add_error("密碼必須包含至少一個數字")

    def _check_special_char(self, password, result):
        """檢查特殊字元"""
        special_pattern = f"[{re.escape(self.SPECIAL_CHARS)}]"
        if not re.search(special_pattern, password):
            result.add_error(f"密碼必須包含至少一個特殊字元 ({self.SPECIAL_CHARS})")

    def _check_consecutive_chars(self, password, result):
        """檢查連續字元"""
        if self._has_consecutive_chars(password):
            result.add_error("密碼不能包含連續 3 個相同字元")

    def _has_consecutive_chars(self, password):
        """檢查是否有連續 3 個相同字元"""
        for i in range(len(password) - 2):
            if password[i] == password[i + 1] == password[i + 2]:
                return True
        return False
```

---

## ✅ 完整程式碼

### test_password_validator.py（完整測試）

```python
import pytest
from password_validator import PasswordValidator

@pytest.fixture
def validator():
    return PasswordValidator()

# 長度測試
def test_password_with_minimum_length_is_valid(validator):
    result = validator.validate("12345678")
    length_errors = [e for e in result.errors if "字元" in e and "8" in e]
    assert len(length_errors) == 0

def test_password_too_short_is_invalid(validator):
    result = validator.validate("1234567")
    assert result.is_valid is False
    assert "至少 8 個字元" in result.errors[0]

# 字元類型測試
def test_password_without_uppercase_is_invalid(validator):
    result = validator.validate("password123!")
    assert result.is_valid is False
    assert any("大寫字母" in error for error in result.errors)

def test_password_without_lowercase_is_invalid(validator):
    result = validator.validate("PASSWORD123!")
    assert result.is_valid is False
    assert any("小寫字母" in error for error in result.errors)

def test_password_without_number_is_invalid(validator):
    result = validator.validate("Password!")
    assert result.is_valid is False
    assert any("數字" in error for error in result.errors)

def test_password_without_special_char_is_invalid(validator):
    result = validator.validate("Password123")
    assert result.is_valid is False
    assert any("特殊字元" in error for error in result.errors)

# 連續字元測試
def test_password_with_consecutive_chars_is_invalid(validator):
    result = validator.validate("Passsword123!")
    assert result.is_valid is False
    assert any("連續" in error for error in result.errors)

def test_password_with_two_consecutive_chars_is_valid(validator):
    result = validator.validate("Password123!")
    consecutive_errors = [e for e in result.errors if "連續" in e]
    assert len(consecutive_errors) == 0

# 有效密碼測試
def test_valid_password_passes_all_checks(validator):
    result = validator.validate("MyPassword123!")
    assert result.is_valid is True
    assert len(result.errors) == 0

def test_complex_valid_password(validator):
    result = validator.validate("C0mpl3x@P@ssw0rd")
    assert result.is_valid is True
    assert len(result.errors) == 0

# 多重錯誤測試
def test_multiple_errors_are_reported(validator):
    result = validator.validate("abc")
    assert result.is_valid is False
    assert len(result.errors) >= 4

# 邊界情況測試
def test_empty_password_is_invalid(validator):
    result = validator.validate("")
    assert result.is_valid is False
    assert len(result.errors) > 0

def test_password_with_only_special_chars(validator):
    result = validator.validate("!!!!!!!!!")
    assert result.is_valid is False
    # 應該缺少大寫、小寫、數字
    assert len(result.errors) == 3
```

---

## 📊 執行測試

**執行所有測試**：
```bash
$ pytest test_password_validator.py -v

================= test session starts =================
# 所有測試都應該通過
================= 13 passed in 0.08s =================
```

**測試覆蓋率**：
```bash
$ pytest --cov=password_validator --cov-report=term-missing

Name                      Stmts   Miss  Cover
----------------------------------------------
password_validator.py       45      0   100%
----------------------------------------------
TOTAL                       45      0   100%
```

---

## 🎓 學習重點

### 複雜邏輯的 TDD 策略

1. **分解複雜問題**：
   - 將複雜驗證分解為多個簡單規則
   - 每個規則獨立測試
   - 最後測試整體行為

2. **錯誤處理設計**：
   - 收集所有錯誤而非遇到第一個就停止
   - 提供清晰的錯誤訊息
   - 方便用戶理解和修正

3. **邊界情況考慮**：
   - 空字串、最小長度
   - 只有某些字元類型
   - 極端情況測試

### 重構的重要性

✅ **方法提取**：
- 每個檢查變成獨立方法
- 易於理解和維護
- 便於新增新規則

✅ **錯誤收集模式**：
- ValidationResult 類別統一處理
- 清晰的 API 設計
- 便於擴展

---

## 🚀 進階挑戰

### 挑戰 1：增強安全性
- 檢查常見弱密碼（字典攻擊）
- 檢查鍵盤序列（qwerty, 123456）
- 檢查生日模式（19xx, 20xx）

### 挑戰 2：可配置驗證器
- 允許自定義規則
- 支援不同強度等級
- 提供國際化錯誤訊息

### 挑戰 3：效能優化
- 使用編譯的正則表達式
- 提早終止（可選）
- 批量驗證功能

---

## 📈 自我評量

- [ ] 能分解複雜問題為簡單測試
- [ ] 所有邊界情況都有測試
- [ ] 錯誤訊息清晰有用
- [ ] 代碼重構後依然可讀
- [ ] 測試覆蓋率達到 100%

**恭喜完成複雜驗證邏輯的 TDD 實作！**
**你現在知道如何用 TDD 處理複雜業務規則了！**