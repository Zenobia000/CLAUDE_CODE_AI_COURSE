# 練習 2：BDD 電商結帳流程實作

## 🎯 練習目標

透過完整的 BDD 實作練習，學會從用戶故事出發設計可執行的測試，體驗行為驅動開發的完整流程。

## 📊 練習概覽

- **練習類型**：BDD 綜合實作
- **預計時間**：3-4 小時
- **難度等級**：中級到進階
- **前置要求**：完成理論 4.2 和基礎情境 B07-B08

## 🎮 核心任務

### 主任務：電商結帳流程

你將使用 BDD 方法，從用戶故事開始，建立完整的電商結帳流程，包含：

1. **購物車管理**（添加、移除、修改數量）
2. **價格計算**（商品價格、折扣、運費、稅金）
3. **庫存檢查**（商品可用性驗證）
4. **付款處理**（信用卡驗證、付款確認）
5. **訂單生成**（訂單建立、狀態追蹤）

### BDD 流程要求

```
每個功能都必須遵循：
1. 📝 用戶故事撰寫（Given-When-Then）
2. 🧪 可執行測試創建（Gherkin 語法）
3. 💻 功能實作（滿足行為規範）
4. 📋 活文檔維護（測試即文檔）
```

## 📁 練習結構

```
練習2_BDD電商結帳/
├── README.md                      # 本練習說明
├── 用戶故事/
│   ├── 購物車管理.feature         # 購物車相關用戶故事
│   ├── 價格計算.feature           # 價格相關用戶故事
│   ├── 庫存管理.feature           # 庫存相關用戶故事
│   ├── 付款流程.feature           # 付款相關用戶故事
│   └── 訂單處理.feature           # 訂單相關用戶故事
├── 起始專案/
│   ├── package.json              # 專案配置（包含 Cucumber.js）
│   ├── cucumber.js               # Cucumber 設定檔
│   ├── features/                 # 空的 feature 檔案夾
│   ├── step_definitions/         # 步驟定義檔案夾
│   ├── src/                      # 業務邏輯實作
│   │   ├── ShoppingCart.js       # 購物車類別骨架
│   │   ├── PriceCalculator.js    # 價格計算器骨架
│   │   ├── InventoryManager.js   # 庫存管理器骨架
│   │   ├── PaymentProcessor.js   # 付款處理器骨架
│   │   └── OrderManager.js       # 訂單管理器骨架
│   └── tests/                    # 單元測試檔案夾
├── 參考解答/
│   ├── 完整專案/                 # 完成版本
│   ├── 階段實作/                 # 每個階段的程式碼
│   ├── BDD實踐記錄.md            # BDD 流程記錄
│   └── 設計思考過程.md           # 設計決策記錄
└── 評量標準/
    ├── BDD實踐檢查清單.md        # BDD 品質檢查
    ├── Gherkin語法標準.md        # 語法品質標準
    └── 活文檔品質標準.md         # 文檔品質評估
```

## 🚀 練習步驟

### 第一階段：需求分析與故事設計（45分鐘）

#### 步驟 1：環境設置
```bash
cd 練習2_BDD電商結帳/起始專案
npm install
```

#### 步驟 2：分析業務需求
閱讀電商結帳的典型用戶旅程：
- 瀏覽商品 → 加入購物車 → 確認商品 → 輸入資訊 → 付款 → 確認訂單

#### 步驟 3：撰寫用戶故事
使用 Gherkin 語法撰寫第一個用戶故事：

```gherkin
# features/shopping_cart.feature

Feature: 購物車管理
  作為電商網站的顧客
  我想要管理我的購物車
  好讓我可以控制要購買的商品

  Background:
    Given 我是已登入的顧客
    And 商品目錄中有以下商品：
      | 商品名稱 | 價格  | 庫存 |
      | iPhone  | 30000 | 10   |
      | AirPods | 5000  | 15   |

  Scenario: 將商品加入購物車
    Given 我的購物車是空的
    When 我將 "iPhone" 加入購物車
    Then 購物車應該包含 1 個商品
    And 購物車總價應該是 30000 元

  Scenario: 修改商品數量
    Given 我的購物車包含 1 個 "iPhone"
    When 我將 "iPhone" 的數量改為 2
    Then 購物車應該包含 2 個 "iPhone"
    And 購物車總價應該是 60000 元
```

### 第二階段：步驟定義實作（90分鐘）

#### 步驟 4：創建步驟定義
```javascript
// step_definitions/shopping_cart_steps.js
const { Given, When, Then } = require('@cucumber/cucumber');
const ShoppingCart = require('../src/ShoppingCart');

Given('我是已登入的顧客', function () {
  this.user = { id: 1, name: 'Test User' };
});

Given('我的購物車是空的', function () {
  this.cart = new ShoppingCart(this.user.id);
});

When('我將 {string} 加入購物車', function (productName) {
  const product = this.products.find(p => p.name === productName);
  this.cart.addItem(product, 1);
});

Then('購物車應該包含 {int} 個商品', function (expectedCount) {
  expect(this.cart.getTotalItems()).toBe(expectedCount);
});
```

#### 步驟 5：實作業務邏輯
```javascript
// src/ShoppingCart.js
class ShoppingCart {
  constructor(userId) {
    this.userId = userId;
    this.items = [];
  }

  addItem(product, quantity) {
    const existingItem = this.items.find(item => item.product.id === product.id);

    if (existingItem) {
      existingItem.quantity += quantity;
    } else {
      this.items.push({ product, quantity });
    }
  }

  getTotalItems() {
    return this.items.reduce((total, item) => total + item.quantity, 0);
  }

  getTotalPrice() {
    return this.items.reduce((total, item) =>
      total + (item.product.price * item.quantity), 0);
  }
}
```

#### 步驟 6：執行 BDD 測試
```bash
npx cucumber-js
# 確認所有場景通過
```

### 第三階段：複雜場景實作（90分鐘）

繼續實作其他複雜的用戶故事：

#### 價格計算場景
```gherkin
Feature: 價格計算
  Scenario: 應用折扣碼
    Given 我的購物車包含價值 1000 元的商品
    When 我使用 "SAVE10" 折扣碼
    Then 折扣應該是 100 元
    And 最終價格應該是 900 元
```

#### 付款處理場景
```gherkin
Feature: 付款處理
  Scenario: 信用卡付款成功
    Given 我有一張有效的信用卡
    And 購物車總價是 1500 元
    When 我確認付款
    Then 付款應該成功
    And 應該產生訂單編號
```

## ✅ 成果檢核

### 必備產出
- [ ] **完整的 Feature 檔案**（5個業務領域）
- [ ] **可執行的步驟定義**（所有步驟都有實作）
- [ ] **業務邏輯實作**（滿足所有行為規範）
- [ ] **BDD 流程記錄**（學習過程文檔）
- [ ] **活文檔**（測試即規格文檔）

### 品質標準

#### BDD 實踐品質
- [ ] 用戶故事清晰易懂（非技術人員可理解）
- [ ] Gherkin 語法正確且一致
- [ ] 場景涵蓋正常和異常情況
- [ ] 步驟定義可重複使用
- [ ] 測試作為活文檔使用

#### 程式碼品質
- [ ] 業務邏輯與框架分離
- [ ] 程式碼可測試且模組化
- [ ] 異常處理完整
- [ ] 程式碼品質良好

### 學習驗證

請回答以下問題驗證學習成果：

1. **BDD 價值**：BDD 與 TDD 的差異是什麼？各自適用什麼場景？
2. **Gherkin 語法**：Given-When-Then 分別代表什麼？如何寫好的場景？
3. **活文檔概念**：如何讓測試成為活的文檔？有什麼好處？
4. **協作流程**：BDD 如何促進技術與業務人員的協作？

## 🚀 進階挑戰

### 挑戰 1：國際化支援
為電商系統添加國際化功能：
- 多語言支援
- 多幣別價格計算
- 不同地區的稅務規則

### 挑戰 2：庫存管理
實作完整的庫存管理系統：
- 即時庫存檢查
- 預留庫存機制
- 庫存不足處理

### 挑戰 3：促銷引擎
建立靈活的促銷系統：
- 多種折扣類型
- 促銷規則引擎
- 促銷衝突處理

## 💡 實戰技巧

### BDD 最佳實踐
1. **用戶視角**：始終從用戶的角度撰寫故事
2. **場景獨立**：每個場景都應該獨立可執行
3. **具體範例**：使用具體的數據而非抽象描述
4. **可理解性**：確保非技術人員能理解場景

### Gherkin 語法技巧
1. **Given**：描述前置條件，設定場景
2. **When**：描述用戶行動，觸發行為
3. **Then**：描述預期結果，驗證行為
4. **And/But**：補充額外的條件或結果

## 🔗 相關資源

### 練習內資源
- **用戶故事範例**：完整的 Feature 檔案範例
- **步驟定義指南**：如何實作步驟定義
- **參考解答**：完整的 BDD 實作

### 模組資源
- **理論 4.2**：行為驅動開發與 Gherkin
- **情境 B07-B08**：BDD 基礎實作情境
- **學習資源**：BDD 工作流程和範本

### 工具資源
- **Cucumber.js**：JavaScript BDD 測試框架
- **Gherkin 語法指南**：官方語法文檔
- **BDD 最佳實踐**：社群經驗分享

---

**記住**：BDD 的核心是溝通，不只是測試。通過可執行的規格，讓整個團隊對需求有一致的理解。

**開始你的 BDD 實戰，讓測試成為團隊溝通的橋樑！**