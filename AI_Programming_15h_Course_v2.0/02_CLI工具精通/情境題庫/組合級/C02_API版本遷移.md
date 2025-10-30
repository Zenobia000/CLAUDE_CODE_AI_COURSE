# C02：API版本遷移（組合級）

## 情境資訊

**編號**：C02
**難度**：⭐⭐⭐⭐☆（組合級）
**預計時間**：2 小時
**學習目標**：
- 掌握大規模程式碼變更的系統化方法
- 熟練使用 /grep 搜尋所有需要修改的位置
- 學會使用 --add-dir 管理大量檔案的上下文
- 理解如何使用 /compact 在上下文滿載時優化
- 建立安全的遷移與驗證流程

**適用對象**：
- 完成模組 2 基礎理論
- 有 API 開發經驗
- 需要處理大規模程式碼重構的開發者

---

## 情境描述

### 背景

你是一家電商公司的後端工程師。公司的產品 API 已經運作 2 年，隨著業務成長，原本的 v1 API 設計已經無法滿足需求。技術團隊決定推出 v2 API，並計劃在 3 個月後淘汰 v1。

你的任務是將公司的內部管理系統（Admin Dashboard）從 v1 API 遷移到 v2 API。

### API 變更摘要

```javascript
// ===== v1 API（舊版，即將淘汰）=====

// 1. 取得產品列表
GET /products
Response: { products: [...], total: 100 }

// 2. 取得單一產品
GET /product/:id
Response: { product: {...} }

// 3. 建立訂單
POST /order
Body: { userId, productId, quantity }
Response: { orderId: "123", status: "pending" }

// 4. 取得用戶資訊
GET /user/:id
Response: { user: {...} }

// ===== v2 API（新版，需遷移到這個）=====

// 1. 取得產品列表（新增分頁參數）
GET /v2/products?page=1&limit=20
Response: {
  data: [...],
  pagination: { page: 1, limit: 20, total: 100, totalPages: 5 }
}

// 2. 取得單一產品（路徑改變）
GET /v2/products/:id
Response: { data: {...} }

// 3. 建立訂單（欄位名稱改變）
POST /v2/orders
Body: { user_id, product_id, quantity }  // 改用 snake_case
Response: { data: { id: "123", status: "pending" } }

// 4. 取得用戶資訊（路徑改變）
GET /v2/users/:id
Response: { data: {...} }

// 關鍵變更：
// ✓ 路徑添加 /v2 前綴
// ✓ 單數改複數（product → products, order → orders, user → users）
// ✓ 回應格式統一包在 data 欄位
// ✓ 分頁改用 pagination 物件
// ✓ 請求參數改用 snake_case
```

### 專案現狀

```bash
admin-dashboard/
├── src/
│   ├── api/
│   │   ├── products.js        # 產品 API 呼叫
│   │   ├── orders.js          # 訂單 API 呼叫
│   │   ├── users.js           # 用戶 API 呼叫
│   │   ├── client.js          # HTTP 客戶端
│   │   └── index.js
│   ├── components/
│   │   ├── ProductList.jsx    # 使用產品 API
│   │   ├── ProductDetail.jsx
│   │   ├── OrderForm.jsx      # 使用訂單 API
│   │   ├── OrderHistory.jsx
│   │   ├── UserProfile.jsx    # 使用用戶 API
│   │   └── ...（50+ 組件）
│   ├── hooks/
│   │   ├── useProducts.js
│   │   ├── useOrders.js
│   │   └── useUsers.js
│   ├── utils/
│   │   ├── apiHelpers.js
│   │   └── formatters.js
│   └── tests/
├── package.json
└── .env

統計：
- 23 個檔案使用 v1 API
- 87 處 API 呼叫
- 跨越 API 層、Hook 層、組件層
```

### 你的任務

1. **搜尋階段**：找出所有使用 v1 API 的地方
2. **分析階段**：理解每個呼叫的上下文和用途
3. **遷移階段**：系統化地將所有呼叫升級到 v2
4. **測試階段**：確保所有功能正常運作
5. **向後兼容**：添加 feature flag 支援逐步切換

### 限制條件

- 不能一次性切換（需支援逐步遷移）
- 必須保持向後兼容（v1 和 v2 暫時共存）
- 上下文有限（不能一次載入所有檔案）
- 不能破壞現有功能
- 必須通過所有測試

---

## 學習重點

1. **系統化搜尋與識別**
   - 如何確保找到所有需要修改的地方？
   - 如何避免遺漏？

2. **上下文管理策略**
   - 檔案很多時如何管理 Claude 的上下文？
   - 何時使用 /compact？
   - 如何分批處理？

3. **安全遷移模式**
   - 如何確保不破壞現有功能？
   - 如何支援逐步切換？
   - 如何回滾？

4. **驗證與測試**
   - 如何確保所有地方都已遷移？
   - 如何測試遷移的正確性？

---

## 建議解決流程

### 階段一：全面搜尋與盤點（25 分鐘）

**目標**：找出所有使用 v1 API 的程式碼位置

**步驟**：

1. **搜尋所有 API 端點**
```bash
# 搜尋所有產品 API 呼叫
/grep "'/product" -i

# 搜尋所有訂單 API 呼叫
/grep "'/order" -i

# 搜尋所有用戶 API 呼叫
/grep "'/user'" -i
```

**預期輸出**：
```
Found in 23 files:
src/api/products.js:15:  return axios.get('/products')
src/api/products.js:23:  return axios.get(`/product/${id}`)
src/components/ProductList.jsx:45:  fetch('/products')
src/hooks/useProducts.js:12:  const url = '/products'
...
```

2. **分類整理發現的呼叫**
```bash
請幫我將搜尋結果分類整理成以下格式：

1. API 層（src/api/*.js）
   - products.js: 3 個呼叫
   - orders.js: 2 個呼叫
   - users.js: 1 個呼叫

2. Hook 層（src/hooks/*.js）
   - useProducts.js: 2 個呼叫
   - useOrders.js: 1 個呼叫

3. 組件層（src/components/*.jsx）
   - ProductList.jsx: 1 個直接呼叫（需重構）
   - OrderForm.jsx: 1 個直接呼叫（需重構）
   ...

4. 工具層（src/utils/*.js）
   - apiHelpers.js: 可能影響所有呼叫

請標註哪些是高優先級（核心 API 層）、哪些是低優先級（個別組件）
```

**Claude 產生的分類**：
```markdown
# API v1 → v2 遷移清單

## 🔴 高優先級（核心層，影響範圍大）

### API 層（先改這裡，影響最大）
- [ ] src/api/products.js (3 處)
  - getProducts(): '/products' → '/v2/products'
  - getProduct(id): '/product/:id' → '/v2/products/:id'
  - updateProduct(id): '/product/:id' → '/v2/products/:id'

- [ ] src/api/orders.js (2 處)
  - createOrder(): '/order' → '/v2/orders'
  - getOrders(): '/orders' → '/v2/orders'（已經是複數）

- [ ] src/api/users.js (1 處)
  - getUser(id): '/user/:id' → '/v2/users/:id'

### 工具層（可能影響所有呼叫）
- [ ] src/utils/apiHelpers.js
  - buildUrl() 函數需要檢查

## 🟡 中優先級（Hook 層，間接影響）

- [ ] src/hooks/useProducts.js (2 處)
  - 需更新回應格式處理（data 欄位）

- [ ] src/hooks/useOrders.js (1 處)
  - 需更新請求參數（camelCase → snake_case）

- [ ] src/hooks/useUsers.js (1 處)
  - 需更新回應格式處理

## 🟢 低優先級（個別組件，直接呼叫 API，需重構）

- [ ] src/components/ProductList.jsx (直接呼叫，應改用 Hook)
- [ ] src/components/OrderForm.jsx (直接呼叫，應改用 Hook)

## 📊 統計

- 總共 23 個檔案
- 87 處 API 呼叫
- 核心改動：6 個檔案（API 層 + 工具層）
- 間接影響：3 個 Hook
- 需重構：2 個組件（直接呼叫改為使用 Hook）
```

3. **建立遷移計劃**
```bash
/memory save

主題：API v1 → v2 遷移計劃

遷移策略：
1. 先改核心（API 層）
2. 再改中間層（Hooks）
3. 最後改應用層（組件）
4. 使用 feature flag 控制切換

需要處理的變更：
- URL 路徑：添加 /v2 前綴
- 單複數：product → products, order → orders, user → users
- 回應格式：包裹在 data 欄位
- 分頁格式：改用 pagination 物件
- 參數命名：camelCase → snake_case

高風險點：
- 直接在組件中呼叫 API（需重構）
- apiHelpers.js 可能影響所有呼叫（需仔細檢查）

驗證方式：
- 單元測試必須通過
- 手動測試每個功能
- 檢查 Network 面板確認呼叫 v2 API
```

**自然學到的概念**：
- 為什麼要全面搜尋？因為遺漏一個就可能導致功能失效
- 為什麼要分類？因為可以規劃優先級和依賴關係
- 為什麼從核心層開始改？因為可以減少重複修改

**檢查點**：
- [ ] 找到所有 API 呼叫（使用 /grep）
- [ ] 分類整理成清單
- [ ] 識別高風險點
- [ ] 制定遷移順序
- [ ] 使用 /memory 保存計劃

---

### 階段二：建立 API 版本抽象層（30 分鐘）

**目標**：建立支援 v1/v2 切換的機制

**步驟**：

1. **建立 feature flag 機制**
```bash
/read .env

# 請求建立
請幫我建立環境變數支援 API 版本切換：

1. 添加 VITE_API_VERSION 變數（預設 'v1'）
2. 建立 src/config/api.js 讀取此設定
3. 建立函數根據版本返回正確的 base URL
```

**產生的程式碼**：
```javascript
// .env
VITE_API_VERSION=v1  # 改為 v2 即可切換

// src/config/api.js
export const API_CONFIG = {
  version: import.meta.env.VITE_API_VERSION || 'v1',
  baseURL: import.meta.env.VITE_API_BASE_URL || 'https://api.example.com'
};

export const getAPIPath = (endpoint) => {
  const { version } = API_CONFIG;

  if (version === 'v2') {
    return `/v2${endpoint}`;
  }

  return endpoint; // v1 沒有前綴
};

export const getEndpoint = (resource, id = null) => {
  const { version } = API_CONFIG;

  // v2 使用複數形式
  const pluralMap = {
    product: 'products',
    order: 'orders',
    user: 'users'
  };

  const resourceName = version === 'v2' ? pluralMap[resource] || resource : resource;
  const basePath = version === 'v2' ? `/v2/${resourceName}` : `/${resourceName}`;

  return id ? `${basePath}/${id}` : basePath;
};
```

2. **建立回應格式轉換器**
```bash
# 請求建立
請建立 src/utils/apiAdapters.js，用於統一 v1 和 v2 的回應格式：

1. normalizeResponse(response, version) - 統一回應格式
2. normalizePagination(response, version) - 統一分頁格式
3. normalizeRequest(data, version) - 統一請求參數（camelCase ↔ snake_case）
```

**產生的轉換器**：
```javascript
// src/utils/apiAdapters.js

/**
 * 將 API 回應格式統一為 v2 格式
 */
export const normalizeResponse = (response, version = 'v1') => {
  if (version === 'v2') {
    return response.data; // v2 已經包在 data 中
  }

  // v1 各種格式統一處理
  if (response.product) return response.product;
  if (response.products) return response.products;
  if (response.order) return response.order;
  if (response.orders) return response.orders;
  if (response.user) return response.user;

  return response;
};

/**
 * 統一分頁格式
 */
export const normalizePagination = (response, version = 'v1') => {
  if (version === 'v2') {
    return response.pagination;
  }

  // v1 格式轉換
  return {
    page: 1,
    limit: response.total || 0,
    total: response.total || 0,
    totalPages: 1
  };
};

/**
 * 將請求參數轉換為對應版本格式
 */
export const normalizeRequest = (data, version = 'v1') => {
  if (version === 'v1') {
    return data; // v1 使用 camelCase，保持原樣
  }

  // v2 需要轉換為 snake_case
  return Object.keys(data).reduce((acc, key) => {
    const snakeKey = key.replace(/([A-Z])/g, '_$1').toLowerCase();
    acc[snakeKey] = data[key];
    return acc;
  }, {});
};
```

**自然學到的模式**：
- 為什麼需要抽象層？因為可以在不修改業務邏輯的情況下切換版本
- 為什麼需要轉換器？因為可以讓上層代碼不感知版本差異

**檢查點**：
- [ ] 建立 feature flag 機制
- [ ] 建立路徑生成函數
- [ ] 建立回應格式轉換器
- [ ] 建立請求參數轉換器

---

### 階段三：遷移 API 層（30 分鐘）

**目標**：修改核心 API 呼叫，使用新的抽象層

**步驟**：

1. **讀取並修改 products API**
```bash
/read src/api/products.js

# 請求修改
請使用我們剛建立的 getEndpoint 和 normalizeResponse 重構此檔案。
確保同時支援 v1 和 v2。
```

**修改前**：
```javascript
// src/api/products.js（舊版）

import axios from 'axios';

export const getProducts = async () => {
  const response = await axios.get('/products');
  return response.data.products; // v1 格式
};

export const getProduct = async (id) => {
  const response = await axios.get(`/product/${id}`);
  return response.data.product; // v1 格式
};

export const updateProduct = async (id, data) => {
  const response = await axios.put(`/product/${id}`, data);
  return response.data.product;
};
```

**修改後**：
```javascript
// src/api/products.js（新版，支援 v1/v2）

import axios from 'axios';
import { API_CONFIG, getEndpoint } from '@/config/api';
import { normalizeResponse, normalizeRequest } from '@/utils/apiAdapters';

export const getProducts = async (params = {}) => {
  const endpoint = getEndpoint('product'); // 自動處理 product → products (v2)
  const requestParams = normalizeRequest(params, API_CONFIG.version);

  const response = await axios.get(endpoint, { params: requestParams });
  return normalizeResponse(response.data, API_CONFIG.version);
};

export const getProduct = async (id) => {
  const endpoint = getEndpoint('product', id);
  const response = await axios.get(endpoint);
  return normalizeResponse(response.data, API_CONFIG.version);
};

export const updateProduct = async (id, data) => {
  const endpoint = getEndpoint('product', id);
  const requestData = normalizeRequest(data, API_CONFIG.version);

  const response = await axios.put(endpoint, requestData);
  return normalizeResponse(response.data, API_CONFIG.version);
};
```

2. **重複處理其他 API 檔案**
```bash
# 依序處理
/read src/api/orders.js
# 請求：請用相同模式重構 orders.js

/read src/api/users.js
# 請求：請用相同模式重構 users.js
```

3. **使用 /compact 優化上下文**
```bash
# 當上下文過多時
/compact

# Claude 會保留關鍵資訊，移除冗餘內容
```

**自然學到的技巧**：
- 為什麼要建立一致的模式？因為可以快速重複應用
- 何時使用 /compact？當修改很多檔案，上下文開始滿載時

**檢查點**：
- [ ] 所有 API 檔案已重構
- [ ] 使用統一的 getEndpoint 和 normalizeResponse
- [ ] 支援 feature flag 切換
- [ ] 上下文管理得當（使用 /compact）

---

### 階段四：更新 Hooks 層（25 分鐘）

**目標**：更新 Hooks 以處理新的分頁格式

**步驟**：

1. **修改 useProducts Hook**
```bash
/read src/hooks/useProducts.js

# 請求修改
請更新此 Hook：
1. 支援 v2 的分頁參數（page, limit）
2. 處理 v2 的分頁回應格式
3. 使用 normalizePagination 統一格式
```

**修改前**：
```javascript
// src/hooks/useProducts.js（舊版）

import { useState, useEffect } from 'react';
import { getProducts } from '@/api/products';

export const useProducts = () => {
  const [products, setProducts] = useState([]);
  const [total, setTotal] = useState(0);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    const fetchProducts = async () => {
      setLoading(true);
      const data = await getProducts();
      setProducts(data);
      setTotal(data.length);
      setLoading(false);
    };

    fetchProducts();
  }, []);

  return { products, total, loading };
};
```

**修改後**：
```javascript
// src/hooks/useProducts.js（新版）

import { useState, useEffect } from 'react';
import { getProducts } from '@/api/products';
import { API_CONFIG } from '@/config/api';

export const useProducts = (page = 1, limit = 20) => {
  const [products, setProducts] = useState([]);
  const [pagination, setPagination] = useState({
    page: 1,
    limit: 20,
    total: 0,
    totalPages: 0
  });
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    const fetchProducts = async () => {
      setLoading(true);

      try {
        // v2 支援分頁參數
        const params = API_CONFIG.version === 'v2'
          ? { page, limit }
          : {};

        const response = await getProducts(params);

        // v2 回應包含 data 和 pagination
        if (API_CONFIG.version === 'v2') {
          setProducts(response.data);
          setPagination(response.pagination);
        } else {
          // v1 回應直接是陣列
          setProducts(response);
          setPagination({
            page: 1,
            limit: response.length,
            total: response.length,
            totalPages: 1
          });
        }
      } catch (error) {
        console.error('Failed to fetch products:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchProducts();
  }, [page, limit]);

  return { products, pagination, loading };
};
```

2. **更新其他 Hooks**
```bash
/read src/hooks/useOrders.js
# 請求：請用相同模式更新 useOrders

/read src/hooks/useUsers.js
# 請求：請用相同模式更新 useUsers（如需要）
```

**自然學到的模式**：
- 為什麼 Hooks 也要感知版本？因為回應格式不同
- 如何保持 Hooks 的向後兼容？使用條件判斷處理不同版本

**檢查點**：
- [ ] 所有 Hooks 已更新
- [ ] 支援 v2 分頁參數
- [ ] 處理 v2 分頁回應
- [ ] 保持向後兼容

---

### 階段五：修正組件層的直接呼叫（20 分鐘）

**目標**：重構直接在組件中呼叫 API 的反模式

**步驟**：

1. **找出直接呼叫 API 的組件**
```bash
/grep "axios.get\|fetch" src/components/ --type jsx
```

2. **重構 ProductList 組件**
```bash
/read src/components/ProductList.jsx

# 請求重構
這個組件直接呼叫 API，請重構為使用 useProducts Hook。
```

**重構前**：
```jsx
// src/components/ProductList.jsx（反模式）

import { useState, useEffect } from 'react';
import axios from 'axios';

const ProductList = () => {
  const [products, setProducts] = useState([]);

  useEffect(() => {
    axios.get('/products').then(res => {
      setProducts(res.data.products); // 直接呼叫，耦合 v1 格式
    });
  }, []);

  return (
    <div>
      {products.map(product => (
        <div key={product.id}>{product.name}</div>
      ))}
    </div>
  );
};
```

**重構後**：
```jsx
// src/components/ProductList.jsx（正確）

import { useProducts } from '@/hooks/useProducts';

const ProductList = () => {
  const { products, loading } = useProducts();

  if (loading) return <div>Loading...</div>;

  return (
    <div>
      {products.map(product => (
        <div key={product.id}>{product.name}</div>
      ))}
    </div>
  );
};
```

**自然學到的原則**：
- 為什麼不應該在組件中直接呼叫 API？因為會與 API 格式緊耦合
- 為什麼使用 Hook？因為可以在一個地方處理版本差異

**檢查點**：
- [ ] 找出所有直接呼叫 API 的組件
- [ ] 重構為使用 Hooks
- [ ] 移除硬編碼的 API 路徑

---

### 階段六：測試與驗證（30 分鐘）

**目標**：確保遷移正確且沒有遺漏

**步驟**：

1. **執行單元測試（v1 模式）**
```bash
# 確保 .env 設定為 v1
VITE_API_VERSION=v1

npm test
```

**預期**：
```
✓ All tests passed (87 tests)
```

2. **切換到 v2 並測試**
```bash
# 修改 .env
VITE_API_VERSION=v2

npm test
```

**如果有失敗**：
```bash
# 請 Claude 幫忙分析
我在 v2 模式下遇到以下測試失敗：
[貼上錯誤]

請幫我分析原因並修正。
```

3. **手動測試各功能**
```bash
npm run dev

# 測試清單：
# [ ] 產品列表顯示正常
# [ ] 產品詳情顯示正常
# [ ] 建立訂單成功
# [ ] 訂單歷史顯示正常
# [ ] 用戶資料顯示正常
# [ ] 分頁功能正常（v2）

# 打開瀏覽器 Network 面板確認：
# [ ] 所有請求都使用 /v2/ 路徑
# [ ] 請求參數使用 snake_case
# [ ] 回應格式包含 data 欄位
```

4. **使用 /grep 確認沒有遺漏**
```bash
# 檢查是否還有硬編碼的 v1 路徑
/grep "'/product'" src/ --type js
/grep "'/order'" src/ --type js
/grep "'/user'" src/ --type js

# 應該只剩註解或測試 mock
```

5. **檢查回應處理**
```bash
# 確認所有地方都使用 normalizeResponse
/grep "response.data.product" src/ --type js
/grep "response.data.order" src/ --type js

# 不應該有任何結果（應該都改用 normalizeResponse 了）
```

**最終記憶沉澱**：
```bash
/memory save

主題：大規模 API 遷移完整流程

階段1️⃣：全面搜尋（25 min）
- /grep 找出所有 API 呼叫
- 分類整理（API層、Hook層、組件層）
- 識別高風險點
- 制定優先級

階段2️⃣：建立抽象層（30 min）
- Feature flag 支援版本切換
- getEndpoint() 統一路徑生成
- normalizeResponse() 統一回應格式
- normalizeRequest() 統一請求參數

階段3️⃣：遷移核心層（30 min）
- 先改 API 層（影響最大）
- 使用抽象函數替換硬編碼
- 確保同時支援 v1/v2
- 使用 /compact 管理上下文

階段4️⃣：更新中間層（25 min）
- 更新 Hooks 處理新格式
- 支援分頁參數
- 保持向後兼容

階段5️⃣：修正應用層（20 min）
- 重構直接呼叫 API 的組件
- 改用 Hooks

階段6️⃣：測試驗證（30 min）
- v1 模式測試
- v2 模式測試
- 手動功能測試
- /grep 確認無遺漏

關鍵成功因素：
- 全面搜尋，避免遺漏
- 建立抽象層，支援逐步切換
- 從核心到外圍，減少重複修改
- 頻繁測試，快速發現問題
- 使用 /compact 管理大量檔案

總時間：2 小時
修改檔案：23 個
修改行數：~300 行
```

**檢查點**：
- [ ] v1 模式所有測試通過
- [ ] v2 模式所有測試通過
- [ ] 手動測試所有功能正常
- [ ] Network 面板確認使用 v2 API
- [ ] /grep 確認無硬編碼路徑
- [ ] 使用 /memory 保存流程

---

## 驗證標準

### 必須達成 ✅

- [ ] 使用 /grep 找出所有 API 呼叫位置
- [ ] 建立支援 v1/v2 切換的抽象層
- [ ] 所有 API 層檔案已遷移
- [ ] 所有 Hooks 已更新支援新格式
- [ ] 移除組件中的直接 API 呼叫
- [ ] v1 和 v2 模式測試都通過
- [ ] 手動測試所有功能正常
- [ ] 使用 /compact 有效管理上下文
- [ ] 使用 /memory 記錄遷移流程

### 額外成就 🌟

- [ ] 建立自動化測試同時驗證 v1 和 v2
- [ ] 添加 API 版本切換的 UI 開關
- [ ] 建立遷移文檔供團隊參考
- [ ] 優化抽象層支援更多版本（v3 預備）
- [ ] 建立 API 回應格式的 TypeScript 類型
- [ ] 完成整個遷移不超過 2 小時

---

## 學習反思

### 反思問題

1. **搜尋策略**：
   - 你如何確保找到所有需要修改的地方？
   - 有哪些容易遺漏的地方？
   - 如何驗證沒有遺漏？

2. **架構設計**：
   - 為什麼需要抽象層？直接全部改不行嗎？
   - Feature flag 的價值是什麼？
   - 如何在向後兼容和代碼簡潔之間平衡？

3. **上下文管理**：
   - 何時應該使用 /compact？
   - 如何分批處理大量檔案？
   - --add-dir 和 /read 的使用時機差異？

4. **測試策略**：
   - 如何設計測試確保兩個版本都正常？
   - 如何測試版本切換的正確性？
   - 手動測試和自動化測試的平衡？

### 延伸練習

1. **完善抽象層**：
   - 添加錯誤處理（v1/v2 錯誤格式不同）
   - 添加 retry 機制
   - 添加 API 監控和日誌

2. **自動化測試**：
   - 建立測試同時執行 v1 和 v2 模式
   - 建立 API contract testing
   - 建立視覺化遷移進度報告

3. **流程文檔化**：
   - 整理成「API 遷移 SOP」
   - 建立檢查清單
   - 建立回滾計劃

4. **擴展應用**：
   - 應用相同模式到其他 API 變更
   - 建立 API 版本管理策略
   - 設計 deprecation 警告機制

---

## 相關資源

### 下一步學習

- **C03：緊急Bug修復** - 學習時間壓力下的快速定位
- **C04：功能模組提取** - 學習識別和提取耦合代碼
- **模組 5：TDD/BDD實戰** - 學習測試驅動的遷移策略

### 工具參考

- **Feature Flags** (LaunchDarkly, Unleash) - 生產級別的 feature toggle
- **API Versioning** - RESTful API 版本管理最佳實踐
- **Contract Testing** (Pact) - API 契約測試

### 相關概念

- **Adapter Pattern** - 統一不同介面
- **Strangler Fig Pattern** - 逐步遷移遺留系統
- **Blue-Green Deployment** - 零停機部署
- **Backward Compatibility** - 向後兼容設計

---

**建議完成時間**：2-2.5 小時（含測試與反思）
**難度評估**：4/5
**重要度**：5/5（大規模重構是高級開發者必備技能）
**可複用性**：5/5（此流程可應用到任何 API 或框架遷移）
