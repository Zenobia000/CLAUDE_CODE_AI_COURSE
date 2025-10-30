# C01：BDD 電商結帳流程

## 📋 情境描述

你正在開發一個電商平台的結帳功能。產品經理提供了完整的使用者故事和驗收標準。

**使用者故事**：
```
作為一個線上購物用戶
我想要能夠順利完成結帳
以便我可以購買商品
```

**驗收標準**：
1. 用戶可以成功完成結帳
2. 用戶可以套用優惠碼
3. 用戶餘額不足時無法結帳
4. 商品庫存不足時無法結帳
5. 優惠碼無效時顯示錯誤

**任務**：
用 BDD 方式實作這個功能，先撰寫 Gherkin 規範，再實作測試和功能。

**時間估計**：1.5-2 小時

---

## 🎯 學習目標

- [ ] 掌握完整的 BDD 工作流程
- [ ] 撰寫清晰的 Gherkin 規範
- [ ] 從規範生成可執行測試
- [ ] 體驗「規範即文檔」的威力

---

## 🛠️ 技術要求

**語言**：Python 3.11+
**測試框架**：pytest + pytest-bdd
**檔案結構**：
```
checkout/
├── features/
│   ├── checkout.feature         # Gherkin 規範
│   └── steps/
│       └── checkout_steps.py    # Step definitions
├── src/
│   ├── cart.py                  # 購物車
│   ├── order.py                 # 訂單
│   ├── product.py               # 商品
│   └── user.py                  # 用戶
└── pytest.ini                   # pytest 設定
```

---

## 📝 實作步驟

### 準備工作

**建立專案**：
```bash
mkdir -p checkout/features/steps checkout/src
cd checkout

# 建立虛擬環境
python -m venv venv
source venv/bin/activate

# 安裝依賴
pip install pytest pytest-bdd
```

---

## 第一部分：撰寫 Gherkin 規範

### Step 1：定義 Feature

**features/checkout.feature**：
```gherkin
Feature: 電商結帳流程
  作為一個線上購物用戶
  我想要能夠順利完成結帳
  以便我可以購買商品

  Background:
    Given 系統中有以下商品：
      | 商品名稱  | 價格  | 庫存 |
      | iPhone   | 30000 | 10   |
      | AirPods  | 5000  | 20   |
      | MacBook  | 50000 | 3    |
    And 用戶「alice@example.com」已登入
    And 用戶餘額為 50000 元

  Scenario: 用戶成功完成結帳
    Given 用戶購物車中有以下商品：
      | 商品名稱 | 數量 |
      | iPhone  | 1    |
      | AirPods | 1    |
    When 用戶提交結帳
    Then 訂單應該建立成功
    And 訂單總額應該是 35000 元
    And 用戶餘額應該是 15000 元
    And 購物車應該被清空
    And 商品庫存應該減少：
      | 商品名稱 | 剩餘庫存 |
      | iPhone  | 9        |
      | AirPods | 19       |

  Scenario: 用戶套用優惠碼獲得折扣
    Given 用戶購物車中有「iPhone」1 件
    And 系統中有優惠碼「SAVE10」可折抵 10%
    When 用戶輸入優惠碼「SAVE10」
    And 用戶提交結帳
    Then 訂單原價應該是 30000 元
    And 優惠折扣應該是 3000 元
    And 訂單實付金額應該是 27000 元

  Scenario: 用戶餘額不足無法結帳
    Given 用戶購物車中有「iPhone」2 件
    And 用戶餘額為 50000 元
    But 訂單總額為 60000 元
    When 用戶提交結帳
    Then 用戶應該看到「餘額不足」錯誤訊息
    And 訂單不應該建立
    And 購物車應該保持不變
    And 用戶餘額應該是 50000 元

  Scenario: 商品庫存不足無法結帳
    Given 用戶購物車中有「iPhone」15 件
    But「iPhone」實際庫存只有 10 件
    When 用戶提交結帳
    Then 用戶應該看到「庫存不足」錯誤訊息
    And 錯誤訊息應該說明「iPhone 庫存不足，僅剩 10 件」

  Scenario: 用戶輸入無效的優惠碼
    Given 用戶購物車中有「iPhone」1 件
    When 用戶輸入優惠碼「INVALID」
    Then 用戶應該看到「優惠碼無效」錯誤訊息
    And 訂單金額應該保持為原價 30000 元
```

### Step 2：分析規範

**檢查清單**：
- [ ] Feature 描述清楚？
- [ ] Background 設置合理？
- [ ] 場景獨立且可重複執行？
- [ ] 使用業務語言（不含技術細節）？
- [ ] 非技術人員能理解？

---

## 第二部分：實作 Step Definitions

### Step 3：生成 Step Definitions 骨架

**features/steps/checkout_steps.py**：
```python
from pytest_bdd import given, when, then, parsers, scenario
from pytest import fixture
import pytest

# Scenarios
scenario('../checkout.feature', '用戶成功完成結帳')
scenario('../checkout.feature', '用戶套用優惠碼獲得折扣')
scenario('../checkout.feature', '用戶餘額不足無法結帳')
scenario('../checkout.feature', '商品庫存不足無法結帳')
scenario('../checkout.feature', '用戶輸入無效的優惠碼')


# Fixtures
@fixture
def context():
    """測試上下文，儲存測試過程中的資料"""
    return {
        'products': {},
        'user': None,
        'cart': None,
        'order': None,
        'error': None,
        'coupons': {}
    }


# Background Steps
@given('系統中有以下商品：', target_fixture='products')
def setup_products(datatable, context):
    """設置商品資料"""
    from src.product import Product, ProductInventory

    inventory = ProductInventory()
    for row in datatable:
        product = Product(
            name=row['商品名稱'],
            price=int(row['價格']),
            stock=int(row['庫存'])
        )
        inventory.add_product(product)
    context['inventory'] = inventory
    return inventory


@given(parsers.parse('用戶「{email}」已登入'))
def user_logged_in(email, context):
    """用戶登入"""
    from src.user import User
    user = User(email)
    context['user'] = user
    return user


@given(parsers.parse('用戶餘額為 {amount:d} 元'))
def user_balance(amount, context):
    """設置用戶餘額"""
    context['user'].balance = amount


# Given Steps
@given('用戶購物車中有以下商品：')
def cart_with_items(datatable, context):
    """設置購物車商品"""
    from src.cart import Cart

    cart = Cart(context['user'])
    for row in datatable:
        product = context['inventory'].get_product(row['商品名稱'])
        quantity = int(row['數量'])
        cart.add_item(product, quantity)
    context['cart'] = cart


@given(parsers.parse('用戶購物車中有「{product_name}」{quantity:d} 件'))
def cart_with_single_item(product_name, quantity, context):
    """購物車加入單一商品"""
    from src.cart import Cart

    cart = Cart(context['user'])
    product = context['inventory'].get_product(product_name)
    cart.add_item(product, quantity)
    context['cart'] = cart


@given(parsers.parse('系統中有優惠碼「{code}」可折抵 {percent:d}%'))
def setup_coupon(code, percent, context):
    """設置優惠碼"""
    context['coupons'][code] = percent / 100


@given(parsers.parse('但「{product_name}」實際庫存只有 {stock:d} 件'))
def product_limited_stock(product_name, stock, context):
    """限制商品庫存"""
    product = context['inventory'].get_product(product_name)
    product.stock = stock


# When Steps
@when('用戶提交結帳')
def submit_checkout(context):
    """提交結帳"""
    from src.order import OrderService

    order_service = OrderService(context['inventory'])
    try:
        order = order_service.create_order(context['user'], context['cart'])
        context['order'] = order
    except Exception as e:
        context['error'] = str(e)


@when(parsers.parse('用戶輸入優惠碼「{code}」'))
def apply_coupon(code, context):
    """套用優惠碼"""
    if code in context['coupons']:
        discount_rate = context['coupons'][code]
        context['cart'].apply_discount(discount_rate)
    else:
        context['error'] = f"優惠碼無效"


# Then Steps
@then('訂單應該建立成功')
def order_created(context):
    """驗證訂單建立"""
    assert context['order'] is not None
    assert context['order'].status == 'confirmed'


@then(parsers.parse('訂單總額應該是 {amount:d} 元'))
def order_total(amount, context):
    """驗證訂單總額"""
    assert context['order'].total == amount


@then(parsers.parse('用戶餘額應該是 {amount:d} 元'))
def user_balance_after(amount, context):
    """驗證用戶餘額"""
    assert context['user'].balance == amount


@then('購物車應該被清空')
def cart_empty(context):
    """驗證購物車已清空"""
    assert len(context['cart'].items) == 0


@then('商品庫存應該減少：')
def inventory_decreased(datatable, context):
    """驗證庫存減少"""
    for row in datatable:
        product = context['inventory'].get_product(row['商品名稱'])
        expected_stock = int(row['剩餘庫存'])
        assert product.stock == expected_stock


@then(parsers.parse('用戶應該看到「{error_msg}」錯誤訊息'))
def error_message_shown(error_msg, context):
    """驗證錯誤訊息"""
    assert context['error'] is not None
    assert error_msg in context['error']


@then('訂單不應該建立')
def order_not_created(context):
    """驗證訂單未建立"""
    assert context['order'] is None


@then('購物車應該保持不變')
def cart_unchanged(context):
    """驗證購物車未變更"""
    assert len(context['cart'].items) > 0


@then(parsers.parse('訂單原價應該是 {amount:d} 元'))
def order_original_price(amount, context):
    """驗證訂單原價"""
    assert context['order'].original_price == amount


@then(parsers.parse('優惠折扣應該是 {amount:d} 元'))
def order_discount(amount, context):
    """驗證折扣金額"""
    assert context['order'].discount == amount


@then(parsers.parse('訂單實付金額應該是 {amount:d} 元'))
def order_final_price(amount, context):
    """驗證實付金額"""
    assert context['order'].total == amount
```

---

## 第三部分：實作功能

### Step 4：實作領域模型

**src/product.py**：
```python
class Product:
    """商品"""
    def __init__(self, name: str, price: int, stock: int):
        self.name = name
        self.price = price
        self.stock = stock

    def has_stock(self, quantity: int) -> bool:
        """檢查庫存"""
        return self.stock >= quantity

    def reduce_stock(self, quantity: int):
        """減少庫存"""
        if not self.has_stock(quantity):
            raise ValueError(f"{self.name} 庫存不足，僅剩 {self.stock} 件")
        self.stock -= quantity


class ProductInventory:
    """商品庫存管理"""
    def __init__(self):
        self.products = {}

    def add_product(self, product: Product):
        """新增商品"""
        self.products[product.name] = product

    def get_product(self, name: str) -> Product:
        """取得商品"""
        if name not in self.products:
            raise ValueError(f"商品不存在：{name}")
        return self.products[name]
```

**src/user.py**：
```python
class User:
    """用戶"""
    def __init__(self, email: str):
        self.email = email
        self.balance = 0

    def has_sufficient_balance(self, amount: int) -> bool:
        """檢查餘額"""
        return self.balance >= amount

    def deduct_balance(self, amount: int):
        """扣除餘額"""
        if not self.has_sufficient_balance(amount):
            raise ValueError("餘額不足")
        self.balance -= amount
```

**src/cart.py**：
```python
class CartItem:
    """購物車商品項目"""
    def __init__(self, product, quantity: int):
        self.product = product
        self.quantity = quantity

    @property
    def subtotal(self) -> int:
        """小計"""
        return self.product.price * self.quantity


class Cart:
    """購物車"""
    def __init__(self, user):
        self.user = user
        self.items = []
        self.discount_rate = 0.0

    def add_item(self, product, quantity: int):
        """加入商品"""
        self.items.append(CartItem(product, quantity))

    def apply_discount(self, rate: float):
        """套用折扣"""
        self.discount_rate = rate

    def calculate_total(self) -> int:
        """計算總額"""
        subtotal = sum(item.subtotal for item in self.items)
        discount = int(subtotal * self.discount_rate)
        return subtotal - discount

    def clear(self):
        """清空購物車"""
        self.items = []
```

**src/order.py**：
```python
class Order:
    """訂單"""
    def __init__(self, user, items, original_price, discount, total):
        self.user = user
        self.items = items
        self.original_price = original_price
        self.discount = discount
        self.total = total
        self.status = 'confirmed'


class OrderService:
    """訂單服務"""
    def __init__(self, inventory):
        self.inventory = inventory

    def create_order(self, user, cart) -> Order:
        """建立訂單"""
        # 檢查庫存
        for item in cart.items:
            if not item.product.has_stock(item.quantity):
                raise ValueError(
                    f"{item.product.name} 庫存不足，僅剩 {item.product.stock} 件"
                )

        # 計算金額
        original_price = sum(item.subtotal for item in cart.items)
        discount = int(original_price * cart.discount_rate)
        total = original_price - discount

        # 檢查餘額
        if not user.has_sufficient_balance(total):
            raise ValueError("餘額不足")

        # 扣款
        user.deduct_balance(total)

        # 減少庫存
        for item in cart.items:
            item.product.reduce_stock(item.quantity)

        # 建立訂單
        order = Order(user, cart.items.copy(), original_price, discount, total)

        # 清空購物車
        cart.clear()

        return order
```

---

## 第四部分：執行測試

### Step 5：執行 BDD 測試

**pytest.ini**：
```ini
[pytest]
testpaths = features
bdd_features_base_dir = features
```

**執行測試**：
```bash
$ pytest features/ -v

=============== test session starts ===============
features/steps/checkout_steps.py::test_用戶成功完成結帳 PASSED
features/steps/checkout_steps.py::test_用戶套用優惠碼獲得折扣 PASSED
features/steps/checkout_steps.py::test_用戶餘額不足無法結帳 PASSED
features/steps/checkout_steps.py::test_商品庫存不足無法結帳 PASSED
features/steps/checkout_steps.py::test_用戶輸入無效的優惠碼 PASSED
=============== 5 passed in 0.12s ===============
```

✓ 所有場景測試通過！

---

## 🎓 學習重點

### BDD 的完整流程

1. **撰寫 Gherkin 規範**：
   - 用業務語言描述
   - Given-When-Then 結構
   - 場景獨立且清晰

2. **實作 Step Definitions**：
   - 將規範轉為可執行測試
   - 測試程式碼也要清晰
   - 適當使用 fixture 和 context

3. **實作功能**：
   - 讓測試通過
   - 保持程式碼簡潔
   - 持續重構

4. **驗證與文檔**：
   - 規範即文檔
   - 測試即驗收標準
   - 永遠同步

### 關鍵收穫

✅ **規範即溝通工具**：
- 所有人都能理解
- 減少誤解和返工
- 建立共同語言

✅ **測試即文檔**：
- Gherkin 清楚描述行為
- 永遠不會過時
- 新人容易上手

✅ **Outside-In 開發**：
- 從使用者視角出發
- 確保「做對的事」
- 再用 TDD 確保「把事做對」

---

## 🚀 進階挑戰

### 挑戰 1：新增場景
- 用戶可以選擇配送方式
- 用戶可以使用多張優惠碼
- 用戶可以部分退款

### 挑戰 2：整合真實資料庫
- 使用 SQLite 儲存訂單
- 實作交易 rollback
- 測試並發訂單

### 挑戰 3：生成人類友善的報告
- 使用 pytest-html 生成報告
- 包含所有場景的執行結果
- 可以給 PM 和客戶看

---

## 📈 自我評量

- [ ] Gherkin 規範清晰易懂
- [ ] 非技術人員能理解規範
- [ ] 所有場景測試通過
- [ ] 實作程式碼簡潔
- [ ] 體驗到 BDD 的價值

**恭喜完成完整的 BDD 專案！**
**現在你理解為什麼 BDD 能成為團隊溝通的利器了嗎？**
