# B05：TDD 實作購物車

## 📋 情境描述

你正在開發電商平台的購物車功能。這個購物車需要處理複雜的業務邏輯，包括商品管理、價格計算、折扣套用等功能。

**需求**：
購物車需要支援：
- 新增/移除商品
- 更新商品數量
- 價格計算（小計、稅金、總計）
- 折扣碼套用
- 免運費門檻
- 庫存檢查

**任務**：
用 TDD 方式實作這個購物車系統，重點關注複雜的業務邏輯。

**時間估計**：45-60 分鐘

---

## 🎯 學習目標

- [ ] 掌握複雜業務邏輯的 TDD 實作
- [ ] 學習價格計算和折扣邏輯的測試
- [ ] 練習商品數量管理的狀態測試
- [ ] 體驗電商業務邏輯的完整開發

---

## 🛠️ 技術要求

**語言**：Python 3.11+
**測試框架**：pytest
**檔案結構**：
```
shopping_cart/
├── shopping_cart.py       # 購物車實作
├── product.py            # 商品模型
├── cart_item.py          # 購物車項目
└── test_shopping_cart.py # 測試檔案
```

---

## 📝 實作步驟

### 準備工作

**建立專案目錄**：
```bash
mkdir -p shopping_cart
cd shopping_cart

# 建立虛擬環境
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安裝 pytest
pip install pytest
```

**建立檔案**：
```bash
touch shopping_cart.py
touch product.py
touch cart_item.py
touch test_shopping_cart.py
```

---

### 循環 1：商品模型設計

#### 🔴 RED：測試商品建立

**test_shopping_cart.py**：
```python
import pytest
from decimal import Decimal
from product import Product
from cart_item import CartItem
from shopping_cart import ShoppingCart

def test_create_product():
    """測試建立商品"""
    product = Product("iPhone 15", Decimal("30000"), "3C", stock=10)

    assert product.name == "iPhone 15"
    assert product.price == Decimal("30000")
    assert product.category == "3C"
    assert product.stock == 10

def test_product_in_stock():
    """測試商品庫存檢查"""
    product = Product("MacBook", Decimal("50000"), stock=5)

    assert product.is_in_stock(3) is True
    assert product.is_in_stock(5) is True
    assert product.is_in_stock(6) is False

def test_reduce_stock():
    """測試減少庫存"""
    product = Product("iPad", Decimal("20000"), stock=10)

    product.reduce_stock(3)

    assert product.stock == 7
```

**執行測試**：
```bash
$ pytest test_shopping_cart.py -v

FAILED - ModuleNotFoundError: No module named 'product'
```

#### 🟢 GREEN：實作商品模型

**product.py**：
```python
from decimal import Decimal

class Product:
    """商品模型"""

    def __init__(self, name: str, price: Decimal, category: str = "", stock: int = 0):
        self.name = name
        self.price = price
        self.category = category
        self.stock = stock

    def is_in_stock(self, quantity: int) -> bool:
        """檢查庫存是否足夠"""
        return self.stock >= quantity

    def reduce_stock(self, quantity: int):
        """減少庫存"""
        if not self.is_in_stock(quantity):
            raise ValueError(f"{self.name} 庫存不足")
        self.stock -= quantity

    def __eq__(self, other):
        if not isinstance(other, Product):
            return False
        return self.name == other.name and self.price == other.price

    def __str__(self):
        return f"{self.name} - ${self.price}"

    def __repr__(self):
        return f"Product('{self.name}', {self.price})"
```

**執行測試**：
```bash
$ pytest test_shopping_cart.py -v

PASSED ✓✓✓
```

---

### 循環 2：購物車項目

#### 🔴 RED：測試購物車項目

**test_shopping_cart.py**（新增）：
```python
def test_create_cart_item():
    """測試建立購物車項目"""
    product = Product("iPhone", Decimal("30000"))
    item = CartItem(product, 2)

    assert item.product == product
    assert item.quantity == 2
    assert item.subtotal == Decimal("60000")

def test_update_cart_item_quantity():
    """測試更新項目數量"""
    product = Product("iPad", Decimal("20000"))
    item = CartItem(product, 1)

    item.update_quantity(3)

    assert item.quantity == 3
    assert item.subtotal == Decimal("60000")

def test_cart_item_invalid_quantity():
    """測試無效數量"""
    product = Product("MacBook", Decimal("50000"))

    with pytest.raises(ValueError, match="數量必須大於 0"):
        CartItem(product, 0)

    with pytest.raises(ValueError, match="數量必須大於 0"):
        CartItem(product, -1)
```

#### 🟢 GREEN：實作購物車項目

**cart_item.py**：
```python
from decimal import Decimal
from product import Product

class CartItem:
    """購物車項目"""

    def __init__(self, product: Product, quantity: int):
        if quantity <= 0:
            raise ValueError("數量必須大於 0")

        self.product = product
        self.quantity = quantity

    @property
    def subtotal(self) -> Decimal:
        """計算小計"""
        return self.product.price * self.quantity

    def update_quantity(self, new_quantity: int):
        """更新數量"""
        if new_quantity <= 0:
            raise ValueError("數量必須大於 0")
        self.quantity = new_quantity

    def __eq__(self, other):
        if not isinstance(other, CartItem):
            return False
        return self.product == other.product

    def __str__(self):
        return f"{self.product.name} x {self.quantity} = ${self.subtotal}"
```

**執行測試**：
```bash
$ pytest test_shopping_cart.py -v

PASSED ✓✓✓✓✓✓
```

---

### 循環 3：購物車基本功能

#### 🔴 RED：測試購物車基本操作

**test_shopping_cart.py**（新增）：
```python
def test_create_empty_cart():
    """測試建立空購物車"""
    cart = ShoppingCart()

    assert len(cart.items) == 0
    assert cart.get_total() == Decimal("0")

def test_add_item_to_cart():
    """測試新增商品到購物車"""
    cart = ShoppingCart()
    product = Product("iPhone", Decimal("30000"))

    cart.add_item(product, 1)

    assert len(cart.items) == 1
    assert cart.items[0].product == product
    assert cart.items[0].quantity == 1

def test_add_same_product_increases_quantity():
    """測試重複新增相同商品會增加數量"""
    cart = ShoppingCart()
    product = Product("iPhone", Decimal("30000"))

    cart.add_item(product, 1)
    cart.add_item(product, 2)

    assert len(cart.items) == 1
    assert cart.items[0].quantity == 3

def test_remove_item_from_cart():
    """測試從購物車移除商品"""
    cart = ShoppingCart()
    product1 = Product("iPhone", Decimal("30000"))
    product2 = Product("iPad", Decimal("20000"))

    cart.add_item(product1, 1)
    cart.add_item(product2, 1)

    removed = cart.remove_item(product1)

    assert removed is True
    assert len(cart.items) == 1
    assert cart.items[0].product == product2
```

#### 🟢 GREEN：實作購物車基本功能

**shopping_cart.py**：
```python
from decimal import Decimal
from typing import List, Optional
from product import Product
from cart_item import CartItem

class ShoppingCart:
    """購物車"""

    def __init__(self):
        self.items: List[CartItem] = []

    def add_item(self, product: Product, quantity: int):
        """新增商品到購物車"""
        # 檢查是否已存在相同商品
        existing_item = self._find_item(product)
        if existing_item:
            existing_item.update_quantity(existing_item.quantity + quantity)
        else:
            self.items.append(CartItem(product, quantity))

    def remove_item(self, product: Product) -> bool:
        """從購物車移除商品"""
        for i, item in enumerate(self.items):
            if item.product == product:
                self.items.pop(i)
                return True
        return False

    def get_total(self) -> Decimal:
        """計算總價"""
        return sum(item.subtotal for item in self.items)

    def _find_item(self, product: Product) -> Optional[CartItem]:
        """尋找購物車中的商品"""
        for item in self.items:
            if item.product == product:
                return item
        return None
```

**執行測試**：
```bash
$ pytest test_shopping_cart.py -v

PASSED ✓✓✓✓✓✓✓✓✓✓
```

---

### 循環 4：價格計算和稅金

#### 🔴 RED：測試價格計算

**test_shopping_cart.py**（新增）：
```python
def test_calculate_subtotal():
    """測試計算小計"""
    cart = ShoppingCart()
    cart.add_item(Product("iPhone", Decimal("30000")), 2)
    cart.add_item(Product("iPad", Decimal("20000")), 1)

    subtotal = cart.get_subtotal()

    assert subtotal == Decimal("80000")

def test_calculate_tax():
    """測試計算稅金（5%）"""
    cart = ShoppingCart()
    cart.add_item(Product("iPhone", Decimal("1000")), 1)

    tax = cart.get_tax()

    assert tax == Decimal("50")  # 1000 * 0.05

def test_calculate_total_with_tax():
    """測試含稅總價"""
    cart = ShoppingCart()
    cart.add_item(Product("iPhone", Decimal("1000")), 1)

    total = cart.get_total_with_tax()

    assert total == Decimal("1050")  # 1000 + 50

def test_free_shipping_threshold():
    """測試免運費門檻"""
    cart = ShoppingCart()

    # 低於門檻
    cart.add_item(Product("小商品", Decimal("500")), 1)
    assert cart.get_shipping_fee() == Decimal("100")

    # 達到門檻
    cart.clear()
    cart.add_item(Product("大商品", Decimal("2000")), 1)
    assert cart.get_shipping_fee() == Decimal("0")
```

#### 🟢 GREEN：實作價格計算

**shopping_cart.py**（更新）：
```python
class ShoppingCart:
    TAX_RATE = Decimal("0.05")  # 5% 稅率
    FREE_SHIPPING_THRESHOLD = Decimal("1500")  # 免運費門檻
    SHIPPING_FEE = Decimal("100")  # 運費

    def __init__(self):
        self.items: List[CartItem] = []

    # ... 之前的方法保持不變

    def get_subtotal(self) -> Decimal:
        """計算小計（未含稅）"""
        return sum(item.subtotal for item in self.items)

    def get_tax(self) -> Decimal:
        """計算稅金"""
        return self.get_subtotal() * self.TAX_RATE

    def get_total_with_tax(self) -> Decimal:
        """計算含稅總價"""
        return self.get_subtotal() + self.get_tax()

    def get_shipping_fee(self) -> Decimal:
        """計算運費"""
        if self.get_subtotal() >= self.FREE_SHIPPING_THRESHOLD:
            return Decimal("0")
        return self.SHIPPING_FEE

    def get_total(self) -> Decimal:
        """計算最終總價（含稅含運費）"""
        return self.get_total_with_tax() + self.get_shipping_fee()

    def clear(self):
        """清空購物車"""
        self.items = []
```

**執行測試**：
```bash
$ pytest test_shopping_cart.py -v

PASSED ✓✓✓✓✓✓✓✓✓✓✓✓✓✓
```

---

### 循環 5：折扣功能

#### 🔴 RED：測試折扣

**test_shopping_cart.py**（新增）：
```python
def test_apply_percentage_discount():
    """測試套用百分比折扣"""
    cart = ShoppingCart()
    cart.add_item(Product("iPhone", Decimal("1000")), 1)

    cart.apply_discount(Decimal("0.1"))  # 10% 折扣

    assert cart.discount_amount == Decimal("100")
    assert cart.get_subtotal_after_discount() == Decimal("900")

def test_apply_fixed_amount_discount():
    """測試套用固定金額折扣"""
    cart = ShoppingCart()
    cart.add_item(Product("iPhone", Decimal("1000")), 1)

    cart.apply_fixed_discount(Decimal("200"))

    assert cart.discount_amount == Decimal("200")
    assert cart.get_subtotal_after_discount() == Decimal("800")

def test_discount_cannot_exceed_subtotal():
    """測試折扣不能超過小計"""
    cart = ShoppingCart()
    cart.add_item(Product("iPhone", Decimal("500")), 1)

    cart.apply_fixed_discount(Decimal("1000"))

    assert cart.discount_amount == Decimal("500")  # 最多折到 0
    assert cart.get_subtotal_after_discount() == Decimal("0")

def test_clear_discount():
    """測試清除折扣"""
    cart = ShoppingCart()
    cart.add_item(Product("iPhone", Decimal("1000")), 1)
    cart.apply_discount(Decimal("0.1"))

    cart.clear_discount()

    assert cart.discount_amount == Decimal("0")
    assert cart.get_subtotal_after_discount() == Decimal("1000")
```

#### 🟢 GREEN：實作折扣功能

**shopping_cart.py**（更新）：
```python
class ShoppingCart:
    TAX_RATE = Decimal("0.05")
    FREE_SHIPPING_THRESHOLD = Decimal("1500")
    SHIPPING_FEE = Decimal("100")

    def __init__(self):
        self.items: List[CartItem] = []
        self.discount_amount = Decimal("0")

    # ... 之前的方法保持不變

    def apply_discount(self, rate: Decimal):
        """套用百分比折扣"""
        subtotal = self.get_subtotal()
        self.discount_amount = subtotal * rate
        self._validate_discount()

    def apply_fixed_discount(self, amount: Decimal):
        """套用固定金額折扣"""
        self.discount_amount = amount
        self._validate_discount()

    def clear_discount(self):
        """清除折扣"""
        self.discount_amount = Decimal("0")

    def get_subtotal_after_discount(self) -> Decimal:
        """取得折扣後小計"""
        return self.get_subtotal() - self.discount_amount

    def _validate_discount(self):
        """驗證折扣金額不超過小計"""
        subtotal = self.get_subtotal()
        if self.discount_amount > subtotal:
            self.discount_amount = subtotal

    def get_total_with_tax(self) -> Decimal:
        """計算含稅總價（折扣後）"""
        return self.get_subtotal_after_discount() + self.get_tax_after_discount()

    def get_tax_after_discount(self) -> Decimal:
        """計算折扣後的稅金"""
        return self.get_subtotal_after_discount() * self.TAX_RATE

    def get_shipping_fee(self) -> Decimal:
        """計算運費（基於折扣後金額）"""
        if self.get_subtotal_after_discount() >= self.FREE_SHIPPING_THRESHOLD:
            return Decimal("0")
        return self.SHIPPING_FEE
```

---

### 循環 6：庫存檢查和更新數量

#### 🔴 RED：測試庫存和數量管理

**test_shopping_cart.py**（新增）：
```python
def test_update_item_quantity():
    """測試更新商品數量"""
    cart = ShoppingCart()
    product = Product("iPhone", Decimal("30000"), stock=10)
    cart.add_item(product, 2)

    cart.update_item_quantity(product, 5)

    item = cart._find_item(product)
    assert item.quantity == 5

def test_check_stock_availability():
    """測試檢查庫存可用性"""
    cart = ShoppingCart()
    product = Product("iPhone", Decimal("30000"), stock=3)
    cart.add_item(product, 2)

    # 庫存足夠
    assert cart.check_stock_availability() == []

    # 庫存不足
    cart.update_item_quantity(product, 5)
    out_of_stock = cart.check_stock_availability()
    assert len(out_of_stock) == 1
    assert out_of_stock[0] == product

def test_get_cart_summary():
    """測試取得購物車摘要"""
    cart = ShoppingCart()
    cart.add_item(Product("iPhone", Decimal("30000")), 1)
    cart.add_item(Product("iPad", Decimal("20000")), 2)
    cart.apply_discount(Decimal("0.1"))

    summary = cart.get_summary()

    assert summary["item_count"] == 2
    assert summary["total_quantity"] == 3
    assert summary["subtotal"] == Decimal("70000")
    assert summary["discount"] == Decimal("7000")
    assert summary["total"] > Decimal("0")
```

#### 🟢 GREEN：實作庫存檢查和摘要

**shopping_cart.py**（更新）：
```python
def update_item_quantity(self, product: Product, new_quantity: int):
    """更新商品數量"""
    item = self._find_item(product)
    if item:
        item.update_quantity(new_quantity)

def check_stock_availability(self) -> List[Product]:
    """檢查庫存可用性，返回庫存不足的商品"""
    out_of_stock = []
    for item in self.items:
        if not item.product.is_in_stock(item.quantity):
            out_of_stock.append(item.product)
    return out_of_stock

def get_summary(self) -> dict:
    """取得購物車摘要"""
    return {
        "item_count": len(self.items),
        "total_quantity": sum(item.quantity for item in self.items),
        "subtotal": self.get_subtotal(),
        "discount": self.discount_amount,
        "subtotal_after_discount": self.get_subtotal_after_discount(),
        "tax": self.get_tax_after_discount(),
        "shipping_fee": self.get_shipping_fee(),
        "total": self.get_total()
    }

def is_empty(self) -> bool:
    """檢查購物車是否為空"""
    return len(self.items) == 0

def __len__(self):
    """返回商品種類數量"""
    return len(self.items)

def __str__(self):
    """返回購物車的字串表示"""
    if self.is_empty():
        return "購物車是空的"

    lines = ["購物車內容："]
    for item in self.items:
        lines.append(f"  {item}")

    summary = self.get_summary()
    lines.append(f"\n小計：${summary['subtotal']}")
    if summary['discount'] > 0:
        lines.append(f"折扣：-${summary['discount']}")
    lines.append(f"稅金：${summary['tax']}")
    lines.append(f"運費：${summary['shipping_fee']}")
    lines.append(f"總計：${summary['total']}")

    return "\n".join(lines)
```

---

## ✅ 完整程式碼

由於篇幅限制，這裡僅展示測試檔案的完整版本：

### test_shopping_cart.py（完整測試）

```python
import pytest
from decimal import Decimal
from product import Product
from cart_item import CartItem
from shopping_cart import ShoppingCart

@pytest.fixture
def iphone():
    return Product("iPhone 15", Decimal("30000"), "3C", stock=10)

@pytest.fixture
def ipad():
    return Product("iPad Air", Decimal("20000"), "3C", stock=5)

@pytest.fixture
def empty_cart():
    return ShoppingCart()

@pytest.fixture
def cart_with_items(iphone, ipad):
    cart = ShoppingCart()
    cart.add_item(iphone, 1)
    cart.add_item(ipad, 2)
    return cart

# 商品測試
def test_create_product(iphone):
    assert iphone.name == "iPhone 15"
    assert iphone.price == Decimal("30000")
    assert iphone.category == "3C"
    assert iphone.stock == 10

def test_product_stock_check(iphone):
    assert iphone.is_in_stock(5) is True
    assert iphone.is_in_stock(10) is True
    assert iphone.is_in_stock(11) is False

# 購物車項目測試
def test_cart_item_creation(iphone):
    item = CartItem(iphone, 2)
    assert item.quantity == 2
    assert item.subtotal == Decimal("60000")

def test_cart_item_invalid_quantity(iphone):
    with pytest.raises(ValueError):
        CartItem(iphone, 0)

# 購物車基本功能測試
def test_empty_cart(empty_cart):
    assert len(empty_cart) == 0
    assert empty_cart.get_total() == Decimal("0")
    assert empty_cart.is_empty() is True

def test_add_items(empty_cart, iphone):
    empty_cart.add_item(iphone, 2)
    assert len(empty_cart) == 1
    assert empty_cart.items[0].quantity == 2

def test_add_same_product_twice(empty_cart, iphone):
    empty_cart.add_item(iphone, 1)
    empty_cart.add_item(iphone, 2)
    assert len(empty_cart) == 1
    assert empty_cart.items[0].quantity == 3

# 價格計算測試
def test_price_calculation(cart_with_items):
    # iPhone(30000) * 1 + iPad(20000) * 2 = 70000
    assert cart_with_items.get_subtotal() == Decimal("70000")

def test_tax_calculation(cart_with_items):
    # 70000 * 0.05 = 3500
    expected_tax = Decimal("3500")
    assert cart_with_items.get_tax_after_discount() == expected_tax

def test_shipping_fee(empty_cart):
    # 低於免運門檻
    low_value_product = Product("便宜商品", Decimal("500"))
    empty_cart.add_item(low_value_product, 1)
    assert empty_cart.get_shipping_fee() == Decimal("100")

    # 達到免運門檻
    empty_cart.clear()
    high_value_product = Product("昂貴商品", Decimal("2000"))
    empty_cart.add_item(high_value_product, 1)
    assert empty_cart.get_shipping_fee() == Decimal("0")

# 折扣測試
def test_percentage_discount(cart_with_items):
    cart_with_items.apply_discount(Decimal("0.1"))  # 10%
    assert cart_with_items.discount_amount == Decimal("7000")
    assert cart_with_items.get_subtotal_after_discount() == Decimal("63000")

def test_fixed_discount(cart_with_items):
    cart_with_items.apply_fixed_discount(Decimal("5000"))
    assert cart_with_items.discount_amount == Decimal("5000")
    assert cart_with_items.get_subtotal_after_discount() == Decimal("65000")

# 庫存測試
def test_stock_check(empty_cart):
    limited_stock = Product("限量商品", Decimal("1000"), stock=2)
    empty_cart.add_item(limited_stock, 3)  # 超過庫存

    out_of_stock = empty_cart.check_stock_availability()
    assert len(out_of_stock) == 1
    assert out_of_stock[0] == limited_stock

# 購物車摘要測試
def test_cart_summary(cart_with_items):
    cart_with_items.apply_discount(Decimal("0.1"))
    summary = cart_with_items.get_summary()

    assert summary["item_count"] == 2
    assert summary["total_quantity"] == 3
    assert summary["subtotal"] == Decimal("70000")
    assert summary["discount"] == Decimal("7000")
```

---

## 📊 執行測試

**執行所有測試**：
```bash
$ pytest test_shopping_cart.py -v

================= test session starts =================
# 所有測試都應該通過
================= XX passed in X.XXs =================
```

**測試覆蓋率**：
```bash
$ pytest --cov=. --cov-report=term-missing

Name                Stmts   Miss  Cover
---------------------------------------
cart_item.py           XX      0   100%
product.py             XX      0   100%
shopping_cart.py       XX      0   100%
---------------------------------------
TOTAL                  XX      0   100%
```

---

## 🎓 學習重點

### 複雜業務邏輯的 TDD

1. **領域模型設計**：
   - Product、CartItem、ShoppingCart 清晰的職責分工
   - 每個類別都有明確的邊界
   - 豐富的業務規則實作

2. **計算邏輯的測試**：
   - 價格、稅金、運費的複雜計算
   - 折扣邏輯的各種情況
   - 邊界情況的完整覆蓋

3. **狀態管理**：
   - 商品數量的變更
   - 折扣狀態的管理
   - 庫存狀態的追蹤

### 關鍵收穫

✅ **電商業務邏輯**：
- 購物車的完整生命週期
- 複雜的價格計算規則
- 庫存管理和驗證

✅ **精確的金額計算**：
- 使用 Decimal 避免浮點數誤差
- 稅金和折扣的正確計算
- 四捨五入和精度控制

✅ **測試策略**：
- 使用 fixture 簡化測試設置
- 複雜業務邏輯的分層測試
- 邊界情況的全面覆蓋

---

## 🚀 進階挑戰

### 挑戰 1：優惠券系統
- 多種優惠券類型（滿減、折扣、買一送一）
- 優惠券使用條件和限制
- 多張優惠券的組合使用

### 挑戰 2：會員等級折扣
- 不同會員等級的折扣
- 會員積分計算
- 升級條件判斷

### 挑戰 3：批量定價
- 階梯式定價（買越多越便宜）
- 批發價格計算
- 最小訂購量限制

### 挑戰 4：購物車持久化
- 儲存到資料庫
- 跨裝置同步
- 購物車過期機制

---

## 📈 自我評量

- [ ] 能設計清晰的領域模型
- [ ] 複雜計算邏輯正確實作
- [ ] 折扣和促銷邏輯完整
- [ ] 庫存管理功能可靠
- [ ] 測試覆蓋所有業務場景
- [ ] 程式碼結構良好且可維護

**恭喜完成購物車系統的 TDD 實作！**
**你現在能處理複雜的電商業務邏輯了！**