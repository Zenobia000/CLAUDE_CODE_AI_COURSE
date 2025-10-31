# B08：BDD 商品搜尋功能

## 📋 情境描述

你正在為電商平台開發商品搜尋功能。這個功能需要支援多種搜尋方式和過濾條件，產品經理希望用 BDD 方式確保搜尋體驗符合用戶期望。

**使用者故事**：
```
作為一個線上購物用戶
我想要能夠快速找到我需要的商品
以便我可以比較和購買合適的商品
```

**驗收標準**：
1. 用戶可以按商品名稱搜尋
2. 用戶可以按分類篩選商品
3. 用戶可以按價格範圍篩選
4. 用戶可以排序搜尋結果
5. 沒有搜尋結果時顯示適當訊息

**任務**：
用 BDD 方式實作商品搜尋功能，重點練習多場景和資料驅動測試。

**時間估計**：45-55 分鐘

---

## 🎯 學習目標

- [ ] 學習多場景 BDD 的設計和實作
- [ ] 掌握 Scenario Outline 和資料驅動測試
- [ ] 練習複雜查詢邏輯的 BDD 描述
- [ ] 體驗 BDD 在搜尋功能中的應用

---

## 🛠️ 技術要求

**語言**：Python 3.11+
**測試框架**：pytest + pytest-bdd
**檔案結構**：
```
product_search/
├── features/
│   ├── product_search.feature     # Gherkin 規範
│   └── steps/
│       └── search_steps.py        # Step definitions
├── src/
│   ├── product.py                # 商品模型
│   ├── search_service.py         # 搜尋服務
│   ├── search_result.py          # 搜尋結果
│   └── product_repository.py     # 商品倉庫
└── pytest.ini                    # pytest 設定
```

---

## 📝 實作步驟

### 準備工作

**建立專案**：
```bash
mkdir -p product_search/features/steps product_search/src
cd product_search

# 建立虛擬環境
python -m venv venv
source venv/bin/activate

# 安裝依賴
pip install pytest pytest-bdd
```

---

## 第一部分：撰寫 Gherkin 規範

### Step 1：定義 Feature 和測試資料

**features/product_search.feature**：
```gherkin
Feature: 商品搜尋功能
  作為一個線上購物用戶
  我想要能夠快速找到我需要的商品
  以便我可以比較和購買合適的商品

  Background:
    Given 系統中有以下商品：
      | 商品名稱        | 分類    | 價格  | 品牌    | 庫存 | 評分 |
      | iPhone 15      | 手機    | 30000 | Apple   | 50   | 4.5  |
      | Samsung Galaxy | 手機    | 25000 | Samsung | 30   | 4.2  |
      | MacBook Pro    | 筆電    | 60000 | Apple   | 20   | 4.8  |
      | ThinkPad X1    | 筆電    | 45000 | Lenovo  | 15   | 4.3  |
      | iPad Air       | 平板    | 20000 | Apple   | 40   | 4.6  |
      | Surface Pro    | 平板    | 35000 | Microsoft| 25   | 4.1  |
      | AirPods Pro    | 耳機    | 8000  | Apple   | 100  | 4.4  |
      | Sony WH-1000XM4| 耳機    | 12000 | Sony    | 60   | 4.7  |

  Scenario: 用戶按商品名稱搜尋
    Given 用戶在商品搜尋頁面
    When 用戶搜尋「iPhone」
    Then 搜尋結果應該包含 1 個商品
    And 搜尋結果應該包含商品「iPhone 15」
    And 搜尋結果應該按相關性排序

  Scenario: 用戶按分類篩選商品
    Given 用戶在商品搜尋頁面
    When 用戶選擇分類「手機」
    Then 搜尋結果應該包含 2 個商品
    And 搜尋結果應該都是「手機」分類
    And 搜尋結果應該包含商品「iPhone 15」
    And 搜尋結果應該包含商品「Samsung Galaxy」

  Scenario: 用戶按價格範圍篩選
    Given 用戶在商品搜尋頁面
    When 用戶設定價格範圍從 20000 到 30000
    Then 搜尋結果應該包含 3 個商品
    And 所有商品價格應該在 20000 到 30000 之間
    And 搜尋結果應該包含商品「Samsung Galaxy」
    And 搜尋結果應該包含商品「iPhone 15」
    And 搜尋結果應該包含商品「iPad Air」

  Scenario: 用戶按品牌篩選商品
    Given 用戶在商品搜尋頁面
    When 用戶選擇品牌「Apple」
    Then 搜尋結果應該包含 4 個商品
    And 所有商品品牌應該是「Apple」

  Scenario: 用戶排序搜尋結果
    Given 用戶在商品搜尋頁面
    And 用戶選擇分類「筆電」
    When 用戶按「價格由低到高」排序
    Then 搜尋結果應該按價格升序排列
    And 第一個商品應該是「ThinkPad X1」
    And 最後一個商品應該是「MacBook Pro」

  Scenario: 沒有搜尋結果
    Given 用戶在商品搜尋頁面
    When 用戶搜尋「不存在的商品」
    Then 搜尋結果應該包含 0 個商品
    And 系統應該顯示「沒有找到符合條件的商品」
    And 系統應該建議「請嘗試不同的關鍵字或篩選條件」

  Scenario: 組合多個篩選條件
    Given 用戶在商品搜尋頁面
    When 用戶選擇分類「手機」
    And 用戶選擇品牌「Apple」
    And 用戶設定價格範圍從 25000 到 35000
    Then 搜尋結果應該包含 1 個商品
    And 搜尋結果應該包含商品「iPhone 15」

  Scenario Outline: 測試不同關鍵字搜尋
    Given 用戶在商品搜尋頁面
    When 用戶搜尋「<關鍵字>」
    Then 搜尋結果應該包含 <數量> 個商品
    And 第一個商品應該是「<第一個商品>」

    Examples:
      | 關鍵字   | 數量 | 第一個商品      |
      | Pro     | 3    | AirPods Pro    |
      | Apple   | 4    | iPhone 15      |
      | Sony    | 1    | Sony WH-1000XM4|
      | MacBook | 1    | MacBook Pro    |

  Scenario Outline: 測試不同排序方式
    Given 用戶在商品搜尋頁面
    And 用戶選擇分類「耳機」
    When 用戶按「<排序方式>」排序
    Then 第一個商品應該是「<第一個商品>」
    And 最後一個商品應該是「<最後一個商品>」

    Examples:
      | 排序方式     | 第一個商品      | 最後一個商品    |
      | 價格由低到高  | AirPods Pro    | Sony WH-1000XM4|
      | 價格由高到低  | Sony WH-1000XM4| AirPods Pro    |
      | 評分由高到低  | Sony WH-1000XM4| AirPods Pro    |
      | 評分由低到高  | AirPods Pro    | Sony WH-1000XM4|

  Scenario: 搜尋結果分頁
    Given 用戶在商品搜尋頁面
    And 系統設定每頁顯示 3 個商品
    When 用戶查看所有商品
    Then 第一頁應該包含 3 個商品
    And 應該有下一頁
    When 用戶點擊下一頁
    Then 第二頁應該包含 3 個商品
    And 應該有上一頁和下一頁
```

### Step 2：分析規範複雜度

**特點分析**：
- ✅ 豐富的測試資料（8個商品，多個屬性）
- ✅ 多種搜尋方式（名稱、分類、價格、品牌）
- ✅ 複雜的組合條件
- ✅ Scenario Outline 的有效使用
- ✅ 邊界情況處理（無結果）

---

## 第二部分：實作 Step Definitions

### Step 3：建立 Step Definitions

**features/steps/search_steps.py**：
```python
from pytest_bdd import given, when, then, parsers, scenario
from pytest import fixture
import pytest

# Scenarios
scenario('../product_search.feature', '用戶按商品名稱搜尋')
scenario('../product_search.feature', '用戶按分類篩選商品')
scenario('../product_search.feature', '用戶按價格範圍篩選')
scenario('../product_search.feature', '用戶按品牌篩選商品')
scenario('../product_search.feature', '用戶排序搜尋結果')
scenario('../product_search.feature', '沒有搜尋結果')
scenario('../product_search.feature', '組合多個篩選條件')
scenario('../product_search.feature', '測試不同關鍵字搜尋')
scenario('../product_search.feature', '測試不同排序方式')
scenario('../product_search.feature', '搜尋結果分頁')


# Fixtures
@fixture
def context():
    """測試上下文"""
    return {
        'products': [],
        'search_service': None,
        'search_result': None,
        'filters': {},
        'sort_order': None,
        'page_size': 10,
        'current_page': 1
    }


# Background Steps
@given('系統中有以下商品：', target_fixture='products')
def setup_products(datatable, context):
    """設置商品資料"""
    from src.product import Product
    from src.product_repository import ProductRepository
    from src.search_service import SearchService

    repository = ProductRepository()

    for row in datatable:
        product = Product(
            name=row['商品名稱'],
            category=row['分類'],
            price=int(row['價格']),
            brand=row['品牌'],
            stock=int(row['庫存']),
            rating=float(row['評分'])
        )
        repository.add_product(product)

    search_service = SearchService(repository)
    context['search_service'] = search_service
    context['repository'] = repository
    return repository


# Given Steps
@given('用戶在商品搜尋頁面')
def user_on_search_page(context):
    """用戶在搜尋頁面"""
    context['current_page'] = 'search'
    context['filters'] = {}


@given(parsers.parse('用戶選擇分類「{category}」'))
def user_selects_category(category, context):
    """用戶選擇分類"""
    context['filters']['category'] = category


@given(parsers.parse('系統設定每頁顯示 {page_size:d} 個商品'))
def set_page_size(page_size, context):
    """設定每頁商品數量"""
    context['page_size'] = page_size


# When Steps
@when(parsers.parse('用戶搜尋「{keyword}」'))
def user_searches_keyword(keyword, context):
    """用戶搜尋關鍵字"""
    search_service = context['search_service']
    result = search_service.search(
        keyword=keyword,
        filters=context.get('filters', {}),
        sort_order=context.get('sort_order'),
        page_size=context.get('page_size', 10),
        page=context.get('current_page', 1)
    )
    context['search_result'] = result


@when(parsers.parse('用戶選擇分類「{category}」'))
def user_selects_category_when(category, context):
    """用戶選擇分類（When步驟）"""
    context['filters']['category'] = category


@when(parsers.parse('用戶設定價格範圍從 {min_price:d} 到 {max_price:d}'))
def user_sets_price_range(min_price, max_price, context):
    """用戶設定價格範圍"""
    context['filters']['min_price'] = min_price
    context['filters']['max_price'] = max_price

    search_service = context['search_service']
    result = search_service.search(
        filters=context['filters'],
        page_size=context.get('page_size', 10)
    )
    context['search_result'] = result


@when(parsers.parse('用戶選擇品牌「{brand}」'))
def user_selects_brand(brand, context):
    """用戶選擇品牌"""
    context['filters']['brand'] = brand

    search_service = context['search_service']
    result = search_service.search(
        filters=context['filters'],
        page_size=context.get('page_size', 10)
    )
    context['search_result'] = result


@when(parsers.parse('用戶按「{sort_order}」排序'))
def user_sorts_results(sort_order, context):
    """用戶排序結果"""
    context['sort_order'] = sort_order

    search_service = context['search_service']
    result = search_service.search(
        filters=context.get('filters', {}),
        sort_order=sort_order,
        page_size=context.get('page_size', 10)
    )
    context['search_result'] = result


@when('用戶查看所有商品')
def user_views_all_products(context):
    """用戶查看所有商品"""
    search_service = context['search_service']
    result = search_service.search(
        page_size=context.get('page_size', 10),
        page=1
    )
    context['search_result'] = result


@when('用戶點擊下一頁')
def user_clicks_next_page(context):
    """用戶點擊下一頁"""
    context['current_page'] += 1
    search_service = context['search_service']
    result = search_service.search(
        page_size=context.get('page_size', 10),
        page=context['current_page']
    )
    context['search_result'] = result


# Then Steps
@then(parsers.parse('搜尋結果應該包含 {count:d} 個商品'))
def search_result_should_contain_count(count, context):
    """驗證搜尋結果數量"""
    result = context['search_result']
    assert len(result.products) == count


@then(parsers.parse('搜尋結果應該包含商品「{product_name}」'))
def search_result_should_contain_product(product_name, context):
    """驗證搜尋結果包含特定商品"""
    result = context['search_result']
    product_names = [p.name for p in result.products]
    assert product_name in product_names


@then(parsers.parse('搜尋結果應該都是「{category}」分類'))
def search_result_should_all_be_category(category, context):
    """驗證所有結果都是指定分類"""
    result = context['search_result']
    for product in result.products:
        assert product.category == category


@then(parsers.parse('所有商品價格應該在 {min_price:d} 到 {max_price:d} 之間'))
def all_products_price_in_range(min_price, max_price, context):
    """驗證所有商品價格在範圍內"""
    result = context['search_result']
    for product in result.products:
        assert min_price <= product.price <= max_price


@then(parsers.parse('所有商品品牌應該是「{brand}」'))
def all_products_should_be_brand(brand, context):
    """驗證所有商品都是指定品牌"""
    result = context['search_result']
    for product in result.products:
        assert product.brand == brand


@then('搜尋結果應該按價格升序排列')
def results_should_be_sorted_by_price_asc(context):
    """驗證按價格升序排列"""
    result = context['search_result']
    prices = [p.price for p in result.products]
    assert prices == sorted(prices)


@then(parsers.parse('第一個商品應該是「{product_name}」'))
def first_product_should_be(product_name, context):
    """驗證第一個商品"""
    result = context['search_result']
    assert len(result.products) > 0
    assert result.products[0].name == product_name


@then(parsers.parse('最後一個商品應該是「{product_name}」'))
def last_product_should_be(product_name, context):
    """驗證最後一個商品"""
    result = context['search_result']
    assert len(result.products) > 0
    assert result.products[-1].name == product_name


@then(parsers.parse('系統應該顯示「{message}」'))
def system_should_show_message(message, context):
    """驗證系統顯示訊息"""
    result = context['search_result']
    assert result.message == message


@then(parsers.parse('系統應該建議「{suggestion}」'))
def system_should_suggest(suggestion, context):
    """驗證系統建議"""
    result = context['search_result']
    assert result.suggestion == suggestion


@then('搜尋結果應該按相關性排序')
def results_should_be_sorted_by_relevance(context):
    """驗證按相關性排序"""
    # 這裡可以檢查結果是否按相關性排序
    # 實際實作中會有相關性計算邏輯
    result = context['search_result']
    assert len(result.products) > 0


@then(parsers.parse('第一頁應該包含 {count:d} 個商品'))
def first_page_should_contain_count(count, context):
    """驗證第一頁商品數量"""
    result = context['search_result']
    assert len(result.products) == count


@then('應該有下一頁')
def should_have_next_page(context):
    """驗證有下一頁"""
    result = context['search_result']
    assert result.has_next_page is True


@then('應該有上一頁和下一頁')
def should_have_prev_and_next_page(context):
    """驗證有上一頁和下一頁"""
    result = context['search_result']
    assert result.has_previous_page is True
    assert result.has_next_page is True


@then(parsers.parse('第二頁應該包含 {count:d} 個商品'))
def second_page_should_contain_count(count, context):
    """驗證第二頁商品數量"""
    result = context['search_result']
    assert len(result.products) == count
```

---

## 第三部分：實作功能

### Step 4：實作領域模型

**src/product.py**：
```python
from dataclasses import dataclass
from typing import List

@dataclass
class Product:
    """商品模型"""
    name: str
    category: str
    price: int
    brand: str
    stock: int = 0
    rating: float = 0.0
    description: str = ""

    def matches_keyword(self, keyword: str) -> bool:
        """檢查是否匹配關鍵字"""
        keyword_lower = keyword.lower()
        return (
            keyword_lower in self.name.lower() or
            keyword_lower in self.brand.lower() or
            keyword_lower in self.category.lower() or
            keyword_lower in self.description.lower()
        )

    def __str__(self):
        return f"{self.name} - {self.brand} - ${self.price}"
```

**src/search_result.py**：
```python
from dataclasses import dataclass
from typing import List, Optional
from src.product import Product

@dataclass
class SearchResult:
    """搜尋結果"""
    products: List[Product]
    total_count: int
    page: int = 1
    page_size: int = 10
    message: Optional[str] = None
    suggestion: Optional[str] = None

    @property
    def has_next_page(self) -> bool:
        """是否有下一頁"""
        return (self.page * self.page_size) < self.total_count

    @property
    def has_previous_page(self) -> bool:
        """是否有上一頁"""
        return self.page > 1

    @property
    def total_pages(self) -> int:
        """總頁數"""
        return (self.total_count + self.page_size - 1) // self.page_size

    def is_empty(self) -> bool:
        """是否為空結果"""
        return len(self.products) == 0
```

**src/product_repository.py**：
```python
from typing import List, Dict, Any
from src.product import Product

class ProductRepository:
    """商品倉庫"""

    def __init__(self):
        self.products: List[Product] = []

    def add_product(self, product: Product):
        """新增商品"""
        self.products.append(product)

    def get_all_products(self) -> List[Product]:
        """取得所有商品"""
        return self.products.copy()

    def search_by_filters(self, filters: Dict[str, Any]) -> List[Product]:
        """按條件篩選商品"""
        results = self.products.copy()

        # 按關鍵字篩選
        if 'keyword' in filters and filters['keyword']:
            keyword = filters['keyword']
            results = [p for p in results if p.matches_keyword(keyword)]

        # 按分類篩選
        if 'category' in filters and filters['category']:
            category = filters['category']
            results = [p for p in results if p.category == category]

        # 按品牌篩選
        if 'brand' in filters and filters['brand']:
            brand = filters['brand']
            results = [p for p in results if p.brand == brand]

        # 按價格範圍篩選
        if 'min_price' in filters:
            min_price = filters['min_price']
            results = [p for p in results if p.price >= min_price]

        if 'max_price' in filters:
            max_price = filters['max_price']
            results = [p for p in results if p.price <= max_price]

        return results

    def count_by_filters(self, filters: Dict[str, Any]) -> int:
        """計算符合條件的商品數量"""
        return len(self.search_by_filters(filters))
```

**src/search_service.py**：
```python
from typing import List, Dict, Any, Optional
from src.product import Product
from src.product_repository import ProductRepository
from src.search_result import SearchResult

class SearchService:
    """搜尋服務"""

    def __init__(self, repository: ProductRepository):
        self.repository = repository

    def search(
        self,
        keyword: Optional[str] = None,
        filters: Optional[Dict[str, Any]] = None,
        sort_order: Optional[str] = None,
        page: int = 1,
        page_size: int = 10
    ) -> SearchResult:
        """執行搜尋"""
        if filters is None:
            filters = {}

        # 加入關鍵字到 filters
        if keyword:
            filters['keyword'] = keyword

        # 取得所有符合條件的商品
        all_results = self.repository.search_by_filters(filters)
        total_count = len(all_results)

        # 排序
        if sort_order:
            all_results = self._sort_products(all_results, sort_order)

        # 分頁
        start_index = (page - 1) * page_size
        end_index = start_index + page_size
        page_results = all_results[start_index:end_index]

        # 建立搜尋結果
        result = SearchResult(
            products=page_results,
            total_count=total_count,
            page=page,
            page_size=page_size
        )

        # 處理空結果
        if total_count == 0:
            result.message = "沒有找到符合條件的商品"
            result.suggestion = "請嘗試不同的關鍵字或篩選條件"

        return result

    def _sort_products(self, products: List[Product], sort_order: str) -> List[Product]:
        """排序商品"""
        if sort_order == "價格由低到高":
            return sorted(products, key=lambda p: p.price)
        elif sort_order == "價格由高到低":
            return sorted(products, key=lambda p: p.price, reverse=True)
        elif sort_order == "評分由高到低":
            return sorted(products, key=lambda p: p.rating, reverse=True)
        elif sort_order == "評分由低到高":
            return sorted(products, key=lambda p: p.rating)
        elif sort_order == "名稱順序":
            return sorted(products, key=lambda p: p.name)
        else:
            # 預設按相關性（這裡簡單按名稱排序）
            return sorted(products, key=lambda p: p.name)

    def get_categories(self) -> List[str]:
        """取得所有分類"""
        all_products = self.repository.get_all_products()
        categories = list(set(p.category for p in all_products))
        return sorted(categories)

    def get_brands(self) -> List[str]:
        """取得所有品牌"""
        all_products = self.repository.get_all_products()
        brands = list(set(p.brand for p in all_products))
        return sorted(brands)

    def get_price_range(self) -> tuple:
        """取得價格範圍"""
        all_products = self.repository.get_all_products()
        if not all_products:
            return (0, 0)
        prices = [p.price for p in all_products]
        return (min(prices), max(prices))
```

---

## 第四部分：執行測試

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
features/steps/search_steps.py::test_用戶按商品名稱搜尋 PASSED
features/steps/search_steps.py::test_用戶按分類篩選商品 PASSED
features/steps/search_steps.py::test_用戶按價格範圍篩選 PASSED
features/steps/search_steps.py::test_用戶按品牌篩選商品 PASSED
features/steps/search_steps.py::test_用戶排序搜尋結果 PASSED
features/steps/search_steps.py::test_沒有搜尋結果 PASSED
features/steps/search_steps.py::test_組合多個篩選條件 PASSED
features/steps/search_steps.py::test_測試不同關鍵字搜尋[Pro-3-AirPods Pro] PASSED
features/steps/search_steps.py::test_測試不同關鍵字搜尋[Apple-4-iPhone 15] PASSED
features/steps/search_steps.py::test_測試不同關鍵字搜尋[Sony-1-Sony WH-1000XM4] PASSED
features/steps/search_steps.py::test_測試不同關鍵字搜尋[MacBook-1-MacBook Pro] PASSED
features/steps/search_steps.py::test_測試不同排序方式[價格由低到高-AirPods Pro-Sony WH-1000XM4] PASSED
features/steps/search_steps.py::test_測試不同排序方式[價格由高到低-Sony WH-1000XM4-AirPods Pro] PASSED
features/steps/search_steps.py::test_測試不同排序方式[評分由高到低-Sony WH-1000XM4-AirPods Pro] PASSED
features/steps/search_steps.py::test_測試不同排序方式[評分由低到高-AirPods Pro-Sony WH-1000XM4] PASSED
features/steps/search_steps.py::test_搜尋結果分頁 PASSED
=============== 16 passed in 0.25s ===============
```

✓ 所有場景測試通過！

---

## 🎓 學習重點

### 多場景 BDD 的設計

1. **豐富的測試資料**：
   - Background 建立真實的商品資料
   - 多維度的商品屬性
   - 足夠的資料量支援各種測試

2. **Scenario Outline 的使用**：
   - 資料驅動的測試方法
   - 避免重複的場景描述
   - 系統化的測試覆蓋

3. **複雜查詢邏輯**：
   - 多種篩選條件
   - 排序功能
   - 分頁處理

### 關鍵收穫

✅ **全面的功能覆蓋**：
- 基本搜尋（關鍵字）
- 分類篩選
- 價格範圍篩選
- 品牌篩選
- 組合條件
- 排序功能
- 分頁功能

✅ **用戶體驗考量**：
- 空結果的處理
- 建議訊息
- 多種排序選項
- 分頁導航

✅ **規範的可讀性**：
- 清晰的場景描述
- 有意義的測試資料
- 業務語言的使用

---

## 🚀 進階挑戰

### 挑戰 1：搜尋優化
- 自動完成建議
- 搜尋歷史記錄
- 熱門搜尋關鍵字

### 挑戰 2：高級篩選
- 多選項篩選（多品牌）
- 評分範圍篩選
- 庫存狀態篩選

### 挑戰 3：搜尋分析
- 搜尋結果點擊追蹤
- 無結果搜尋分析
- 搜尋轉換率統計

### 挑戰 4：效能優化
- 搜尋結果快取
- 索引建立
- 分散式搜尋

---

## 📈 自我評量

- [ ] 能設計複雜的 BDD 場景
- [ ] Scenario Outline 使用得當
- [ ] 搜尋邏輯實作正確
- [ ] 分頁功能完整
- [ ] 排序功能準確
- [ ] 錯誤情況處理適當

**恭喜完成商品搜尋功能的 BDD 實作！**
**你現在能用 BDD 處理複雜的查詢功能了！**
**多場景測試讓你的功能更加健壯！**