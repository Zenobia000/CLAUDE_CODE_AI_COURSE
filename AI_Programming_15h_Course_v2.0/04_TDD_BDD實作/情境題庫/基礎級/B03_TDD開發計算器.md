# B03：TDD 開發計算器

## 📋 情境描述

你要為一個學習應用開發一個簡單但可靠的計算器類別。這個計算器會被其他模組使用，所以必須確保各種情況下都能正確運作。

**需求**：
計算器需要支援：
- 基本四則運算（+、-、×、÷）
- 記憶功能（儲存/清除/回憶數值）
- 錯誤處理（除以零、無效操作）
- 運算歷史記錄

**任務**：
用 TDD 方式實作這個計算器，確保每個功能都有完善的測試。

**時間估計**：30-40 分鐘

---

## 🎯 學習目標

- [ ] 學習基本 TDD 實踐的完整流程
- [ ] 掌握錯誤處理的測試方式
- [ ] 練習狀態管理的測試策略
- [ ] 體驗測試驅動的 API 設計

---

## 🛠️ 技術要求

**語言**：Python 3.11+
**測試框架**：pytest
**檔案結構**：
```
calculator/
├── calculator.py           # 實作檔案
└── test_calculator.py      # 測試檔案
```

---

## 📝 實作步驟

### 準備工作

**建立專案目錄**：
```bash
mkdir -p calculator
cd calculator

# 建立虛擬環境
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安裝 pytest
pip install pytest
```

**建立檔案**：
```bash
touch calculator.py
touch test_calculator.py
```

---

### 循環 1：基本加法運算

#### 🔴 RED：測試加法

**test_calculator.py**：
```python
import pytest
from calculator import Calculator

def test_add_two_positive_numbers():
    """測試兩個正數相加"""
    calc = Calculator()

    result = calc.add(2, 3)

    assert result == 5

def test_add_positive_and_negative():
    """測試正數和負數相加"""
    calc = Calculator()

    result = calc.add(5, -3)

    assert result == 2

def test_add_zeros():
    """測試加零"""
    calc = Calculator()

    result = calc.add(0, 0)

    assert result == 0
```

**執行測試**：
```bash
$ pytest test_calculator.py -v

FAILED - ModuleNotFoundError: No module named 'calculator'
```

#### 🟢 GREEN：實作加法

**calculator.py**：
```python
class Calculator:
    """簡單計算器"""

    def add(self, a, b):
        """加法運算"""
        return a + b
```

**執行測試**：
```bash
$ pytest test_calculator.py -v

PASSED ✓✓✓
```

---

### 循環 2：減法運算

#### 🔴 RED：測試減法

**test_calculator.py**（新增）：
```python
def test_subtract_positive_numbers():
    """測試正數減法"""
    calc = Calculator()

    result = calc.subtract(5, 3)

    assert result == 2

def test_subtract_negative_result():
    """測試減法得到負數"""
    calc = Calculator()

    result = calc.subtract(3, 5)

    assert result == -2
```

#### 🟢 GREEN：實作減法

**calculator.py**（更新）：
```python
class Calculator:
    """簡單計算器"""

    def add(self, a, b):
        """加法運算"""
        return a + b

    def subtract(self, a, b):
        """減法運算"""
        return a - b
```

**執行測試**：
```bash
$ pytest test_calculator.py -v

PASSED ✓✓✓✓✓
```

---

### 循環 3：乘法和除法

#### 🔴 RED：測試乘除法

**test_calculator.py**（新增）：
```python
def test_multiply_positive_numbers():
    """測試正數乘法"""
    calc = Calculator()

    result = calc.multiply(3, 4)

    assert result == 12

def test_multiply_by_zero():
    """測試乘以零"""
    calc = Calculator()

    result = calc.multiply(5, 0)

    assert result == 0

def test_divide_positive_numbers():
    """測試正數除法"""
    calc = Calculator()

    result = calc.divide(10, 2)

    assert result == 5

def test_divide_with_decimal_result():
    """測試除法得到小數"""
    calc = Calculator()

    result = calc.divide(7, 2)

    assert result == 3.5
```

#### 🟢 GREEN：實作乘除法

**calculator.py**（更新）：
```python
class Calculator:
    """簡單計算器"""

    def add(self, a, b):
        """加法運算"""
        return a + b

    def subtract(self, a, b):
        """減法運算"""
        return a - b

    def multiply(self, a, b):
        """乘法運算"""
        return a * b

    def divide(self, a, b):
        """除法運算"""
        return a / b
```

**執行測試**：
```bash
$ pytest test_calculator.py -v

PASSED ✓✓✓✓✓✓✓✓✓
```

---

### 循環 4：除以零錯誤處理

#### 🔴 RED：測試除以零

**test_calculator.py**（新增）：
```python
def test_divide_by_zero_raises_error():
    """測試除以零應該拋出錯誤"""
    calc = Calculator()

    with pytest.raises(ValueError, match="不能除以零"):
        calc.divide(5, 0)

def test_divide_zero_by_number():
    """測試零除以其他數"""
    calc = Calculator()

    result = calc.divide(0, 5)

    assert result == 0
```

#### 🟢 GREEN：實作錯誤處理

**calculator.py**（更新 divide 方法）：
```python
def divide(self, a, b):
    """除法運算"""
    if b == 0:
        raise ValueError("不能除以零")
    return a / b
```

**執行測試**：
```bash
$ pytest test_calculator.py -v

PASSED ✓✓✓✓✓✓✓✓✓✓✓
```

---

### 循環 5：記憶功能

#### 🔴 RED：測試記憶功能

**test_calculator.py**（新增）：
```python
def test_store_and_recall_memory():
    """測試儲存和回憶記憶"""
    calc = Calculator()

    calc.store_memory(42)
    result = calc.recall_memory()

    assert result == 42

def test_clear_memory():
    """測試清除記憶"""
    calc = Calculator()

    calc.store_memory(100)
    calc.clear_memory()
    result = calc.recall_memory()

    assert result == 0

def test_memory_initially_zero():
    """測試記憶初始值為零"""
    calc = Calculator()

    result = calc.recall_memory()

    assert result == 0

def test_add_to_memory():
    """測試將值加到記憶中"""
    calc = Calculator()

    calc.store_memory(10)
    calc.add_to_memory(5)
    result = calc.recall_memory()

    assert result == 15
```

#### 🟢 GREEN：實作記憶功能

**calculator.py**（更新）：
```python
class Calculator:
    """簡單計算器"""

    def __init__(self):
        """初始化計算器"""
        self.memory = 0

    def add(self, a, b):
        """加法運算"""
        return a + b

    def subtract(self, a, b):
        """減法運算"""
        return a - b

    def multiply(self, a, b):
        """乘法運算"""
        return a * b

    def divide(self, a, b):
        """除法運算"""
        if b == 0:
            raise ValueError("不能除以零")
        return a / b

    def store_memory(self, value):
        """儲存值到記憶中"""
        self.memory = value

    def recall_memory(self):
        """回憶記憶中的值"""
        return self.memory

    def clear_memory(self):
        """清除記憶"""
        self.memory = 0

    def add_to_memory(self, value):
        """將值加到記憶中"""
        self.memory += value
```

**執行測試**：
```bash
$ pytest test_calculator.py -v

PASSED ✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓
```

---

### 循環 6：運算歷史

#### 🔴 RED：測試歷史記錄

**test_calculator.py**（新增）：
```python
def test_history_records_operations():
    """測試歷史記錄運算"""
    calc = Calculator()

    calc.add(2, 3)
    calc.multiply(4, 5)
    history = calc.get_history()

    assert len(history) == 2
    assert "2 + 3 = 5" in history
    assert "4 × 5 = 20" in history

def test_clear_history():
    """測試清除歷史"""
    calc = Calculator()

    calc.add(1, 1)
    calc.clear_history()
    history = calc.get_history()

    assert len(history) == 0

def test_history_initially_empty():
    """測試歷史初始為空"""
    calc = Calculator()

    history = calc.get_history()

    assert len(history) == 0
```

#### 🟢 GREEN：實作歷史記錄

**calculator.py**（更新）：
```python
class Calculator:
    """簡單計算器"""

    def __init__(self):
        """初始化計算器"""
        self.memory = 0
        self.history = []

    def add(self, a, b):
        """加法運算"""
        result = a + b
        self._record_operation(f"{a} + {b} = {result}")
        return result

    def subtract(self, a, b):
        """減法運算"""
        result = a - b
        self._record_operation(f"{a} - {b} = {result}")
        return result

    def multiply(self, a, b):
        """乘法運算"""
        result = a * b
        self._record_operation(f"{a} × {b} = {result}")
        return result

    def divide(self, a, b):
        """除法運算"""
        if b == 0:
            raise ValueError("不能除以零")
        result = a / b
        self._record_operation(f"{a} ÷ {b} = {result}")
        return result

    def store_memory(self, value):
        """儲存值到記憶中"""
        self.memory = value

    def recall_memory(self):
        """回憶記憶中的值"""
        return self.memory

    def clear_memory(self):
        """清除記憶"""
        self.memory = 0

    def add_to_memory(self, value):
        """將值加到記憶中"""
        self.memory += value

    def get_history(self):
        """取得運算歷史"""
        return self.history.copy()

    def clear_history(self):
        """清除運算歷史"""
        self.history = []

    def _record_operation(self, operation):
        """記錄運算到歷史中"""
        self.history.append(operation)
```

**執行測試**：
```bash
$ pytest test_calculator.py -v

PASSED ✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓
```

---

### 🔵 REFACTOR：提取 fixture 和最佳化

**test_calculator.py**（重構）：
```python
import pytest
from calculator import Calculator

@pytest.fixture
def calc():
    """建立 Calculator 實例"""
    return Calculator()

# 基本運算測試
def test_add_two_positive_numbers(calc):
    assert calc.add(2, 3) == 5

def test_add_positive_and_negative(calc):
    assert calc.add(5, -3) == 2

def test_add_zeros(calc):
    assert calc.add(0, 0) == 0

def test_subtract_positive_numbers(calc):
    assert calc.subtract(5, 3) == 2

def test_subtract_negative_result(calc):
    assert calc.subtract(3, 5) == -2

def test_multiply_positive_numbers(calc):
    assert calc.multiply(3, 4) == 12

def test_multiply_by_zero(calc):
    assert calc.multiply(5, 0) == 0

def test_divide_positive_numbers(calc):
    assert calc.divide(10, 2) == 5

def test_divide_with_decimal_result(calc):
    assert calc.divide(7, 2) == 3.5

# 錯誤處理測試
def test_divide_by_zero_raises_error(calc):
    with pytest.raises(ValueError, match="不能除以零"):
        calc.divide(5, 0)

def test_divide_zero_by_number(calc):
    assert calc.divide(0, 5) == 0

# 記憶功能測試
def test_store_and_recall_memory(calc):
    calc.store_memory(42)
    assert calc.recall_memory() == 42

def test_clear_memory(calc):
    calc.store_memory(100)
    calc.clear_memory()
    assert calc.recall_memory() == 0

def test_memory_initially_zero(calc):
    assert calc.recall_memory() == 0

def test_add_to_memory(calc):
    calc.store_memory(10)
    calc.add_to_memory(5)
    assert calc.recall_memory() == 15

# 歷史記錄測試
def test_history_records_operations(calc):
    calc.add(2, 3)
    calc.multiply(4, 5)
    history = calc.get_history()
    assert len(history) == 2
    assert "2 + 3 = 5" in history
    assert "4 × 5 = 20" in history

def test_clear_history(calc):
    calc.add(1, 1)
    calc.clear_history()
    assert len(calc.get_history()) == 0

def test_history_initially_empty(calc):
    assert len(calc.get_history()) == 0
```

---

## ✅ 完整程式碼

### calculator.py（最終版本）

```python
class Calculator:
    """功能完整的計算器類別"""

    def __init__(self):
        """初始化計算器"""
        self.memory = 0
        self.history = []

    def add(self, a, b):
        """加法運算"""
        result = a + b
        self._record_operation(f"{a} + {b} = {result}")
        return result

    def subtract(self, a, b):
        """減法運算"""
        result = a - b
        self._record_operation(f"{a} - {b} = {result}")
        return result

    def multiply(self, a, b):
        """乘法運算"""
        result = a * b
        self._record_operation(f"{a} × {b} = {result}")
        return result

    def divide(self, a, b):
        """除法運算"""
        if b == 0:
            raise ValueError("不能除以零")
        result = a / b
        self._record_operation(f"{a} ÷ {b} = {result}")
        return result

    def store_memory(self, value):
        """儲存值到記憶中"""
        self.memory = value

    def recall_memory(self):
        """回憶記憶中的值"""
        return self.memory

    def clear_memory(self):
        """清除記憶"""
        self.memory = 0

    def add_to_memory(self, value):
        """將值加到記憶中"""
        self.memory += value

    def get_history(self):
        """取得運算歷史（返回副本以防止外部修改）"""
        return self.history.copy()

    def clear_history(self):
        """清除運算歷史"""
        self.history = []

    def _record_operation(self, operation):
        """記錄運算到歷史中"""
        self.history.append(operation)
```

---

## 📊 執行測試

**執行所有測試**：
```bash
$ pytest test_calculator.py -v

================= test session starts =================
test_calculator.py::test_add_two_positive_numbers PASSED
test_calculator.py::test_add_positive_and_negative PASSED
test_calculator.py::test_add_zeros PASSED
test_calculator.py::test_subtract_positive_numbers PASSED
test_calculator.py::test_subtract_negative_result PASSED
test_calculator.py::test_multiply_positive_numbers PASSED
test_calculator.py::test_multiply_by_zero PASSED
test_calculator.py::test_divide_positive_numbers PASSED
test_calculator.py::test_divide_with_decimal_result PASSED
test_calculator.py::test_divide_by_zero_raises_error PASSED
test_calculator.py::test_divide_zero_by_number PASSED
test_calculator.py::test_store_and_recall_memory PASSED
test_calculator.py::test_clear_memory PASSED
test_calculator.py::test_memory_initially_zero PASSED
test_calculator.py::test_add_to_memory PASSED
test_calculator.py::test_history_records_operations PASSED
test_calculator.py::test_clear_history PASSED
test_calculator.py::test_history_initially_empty PASSED
================= 18 passed in 0.05s =================
```

**測試覆蓋率**：
```bash
$ pytest --cov=calculator --cov-report=term-missing

Name            Stmts   Miss  Cover
-----------------------------------
calculator.py      32      0   100%
-----------------------------------
TOTAL              32      0   100%
```

---

## 🎓 學習重點

### TDD 的基本節奏

1. **小步迭代**：
   - 一次只實作一個功能
   - 每個功能從最簡單的測試開始
   - 逐漸增加複雜度

2. **測試驅動設計**：
   - 測試決定了 API 的設計
   - 清晰的方法命名
   - 合理的錯誤處理

3. **重構的時機**：
   - 功能完成後立即重構
   - 提取 fixture 減少重複
   - 保持測試和程式碼都乾淨

### 關鍵收穫

✅ **錯誤處理的測試**：
- 使用 `pytest.raises()` 測試例外
- 驗證錯誤訊息的內容
- 確保錯誤情況被正確處理

✅ **狀態管理的測試**：
- 測試初始狀態
- 測試狀態變更
- 測試狀態重置

✅ **測試命名規範**：
- 描述測試的行為
- 使用 `test_動作_條件_預期結果` 格式
- 清晰易懂的測試意圖

---

## 🚀 進階挑戰

### 挑戰 1：科學計算功能
- 平方根、次方運算
- 三角函數（sin, cos, tan）
- 對數函數

### 挑戰 2：表達式解析
- 支援字串表達式輸入
- 運算子優先權
- 括號支援

### 挑戰 3：不同數字系統
- 二進位、八進位、十六進位
- 進位轉換功能
- 位元運算

### 挑戰 4：精度控制
- 浮點數精度設定
- 四捨五入模式
- 大數運算支援

---

## 📈 自我評量

完成本情境後，檢查以下項目：

### TDD 流程
- [ ] 每個功能都先寫測試
- [ ] 看到測試失敗才開始實作
- [ ] 實作後進行適當重構
- [ ] 重構後測試依然通過

### 測試品質
- [ ] 測試覆蓋所有功能
- [ ] 包含邊界情況和錯誤處理
- [ ] 測試名稱清楚描述意圖
- [ ] 使用適當的測試工具（fixture, pytest.raises）

### 程式碼品質
- [ ] API 設計清晰一致
- [ ] 錯誤處理適當
- [ ] 程式碼簡潔可讀
- [ ] 適當的註解和文檔

---

**恭喜完成計算器的 TDD 實作！**
**你現在掌握了 TDD 的基本節奏和常見模式！**
**繼續練習，讓 TDD 成為你的開發習慣！**