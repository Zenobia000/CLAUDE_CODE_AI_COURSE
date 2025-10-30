# C03：緊急Bug修復（組合級）

## 情境資訊

**編號**：C03
**難度**：⭐⭐⭐⭐☆（組合級）
**預計時間**：1 小時
**學習目標**：
- 掌握在時間壓力下快速定位問題的方法
- 熟練使用 /grep 搜尋可疑代碼模式
- 學會使用 /read 快速理解複雜異步邏輯
- 理解如何在上下文受限時高效工作
- 建立緊急修復的標準流程

**適用對象**：
- 完成模組 2 基礎理論
- 有異步編程經驗
- 需要處理生產環境問題的開發者

---

## 情境描述

### 背景

**時間**：週五晚上 8:30 PM
**地點**：你剛到家準備晚餐

你的手機響了，是公司的 on-call 通知：

```
🚨 CRITICAL ALERT 🚨
Service: Payment Processing
Severity: P0 (Critical)
Issue: Data corruption in order processing
Impact: ~500 customers affected in last 30 minutes
Status: ACTIVE

Symptoms:
- Orders showing incorrect total amounts
- Same order processed multiple times
- Payment charged but order not created
- Logs show race condition errors

You are the on-call engineer. Please investigate ASAP.

Estimated customer impact: $50,000+
SLA: Fix within 1 hour or escalate to VP Engineering
```

你打開筆電，心跳加速。這是一個你不太熟悉的模組，但你必須在 1 小時內找到問題並修復。

### 已知資訊

**錯誤日誌範例**：
```
[ERROR] 2025-01-15 20:15:23 - Race condition detected in order creation
[ERROR] 2025-01-15 20:15:23 - Order ORD-12345 total mismatch: expected $99.99, got $199.98
[ERROR] 2025-01-15 20:16:45 - Duplicate order creation: ORD-12346
[ERROR] 2025-01-15 20:18:12 - Payment charged but order not found in database
[ERROR] 2025-01-15 20:19:34 - ConcurrentModificationException in OrderService.calculateTotal()
```

**最近的程式碼變更**：
```bash
git log --since="24 hours ago" --oneline

a3f2d9e (HEAD -> main) feat: optimize order processing performance
b7e4c1a refactor: extract payment processing to separate service
c9d2f3b fix: handle edge case in cart calculation
```

**系統架構簡圖**：
```
User Request
    ↓
OrderController.createOrder()
    ↓
OrderService.processOrder()
    ├─→ CartService.calculateTotal()
    ├─→ InventoryService.reserveItems()
    ├─→ PaymentService.charge()
    └─→ OrderRepository.save()
```

### 專案結構

```bash
payment-service/
├── src/
│   ├── controllers/
│   │   └── OrderController.js
│   ├── services/
│   │   ├── OrderService.js       # 訂單處理邏輯
│   │   ├── CartService.js        # 購物車計算
│   │   ├── PaymentService.js     # 支付處理
│   │   └── InventoryService.js   # 庫存管理
│   ├── repositories/
│   │   └── OrderRepository.js
│   └── utils/
│       ├── locks.js              # 分散式鎖工具
│       └── logger.js
├── tests/
└── logs/
    └── error.log

總計：
- 15 個 JavaScript 檔案
- ~3,000 行程式碼
- 你從未看過這個專案
- 時間限制：60 分鐘
```

### 你的任務

1. **快速定位**：找出導致 race condition 的程式碼位置（15 分鐘）
2. **理解邏輯**：理解異步流程和數據流（15 分鐘）
3. **識別問題**：找出具體的 bug（15 分鐘）
4. **緊急修復**：實作最小化修復方案（10 分鐘）
5. **驗證測試**：確保修復有效（5 分鐘）

### 限制條件

- **時間壓力**：1 小時內必須修復
- **不熟悉的程式碼**：第一次看這個專案
- **生產環境**：不能隨便實驗，必須確保修復正確
- **影響範圍大**：錯誤修復可能造成更大問題
- **上下文有限**：不能花時間閱讀所有程式碼

---

## 學習重點

1. **緊急情境下的優先級管理**
   - 什麼該先看？什麼可以跳過？
   - 如何快速建立程式碼的心智模型？

2. **高效搜尋與定位**
   - 如何用關鍵字快速定位可疑代碼？
   - 如何從錯誤訊息反推代碼位置？

3. **異步代碼的快速理解**
   - 如何快速理解複雜的異步流程？
   - 如何識別 race condition？

4. **最小化修復策略**
   - 什麼是「夠好」的修復？
   - 如何平衡速度與完美？

---

## 建議解決流程

### 階段一：錯誤定位與初步分析（15 分鐘）

**目標**：從錯誤訊息快速定位到問題代碼

**計時開始：00:00**

**步驟**：

1. **分析錯誤訊息找關鍵字**
```bash
# 從錯誤日誌提取關鍵資訊
關鍵字：
- "Race condition"
- "ConcurrentModificationException"
- "OrderService.calculateTotal()"
- "Duplicate order creation"
- "Order total mismatch"

初步判斷：
- 問題在 OrderService
- 與 calculateTotal() 有關
- 涉及並發修改
```

2. **搜尋最可能的問題代碼**
```bash
# 搜尋 calculateTotal 函數
/grep "calculateTotal" --type js

# 預期找到：
# src/services/OrderService.js:45
# src/services/CartService.js:23
```

3. **搜尋 race condition 相關的模式**
```bash
# 搜尋可能有並發問題的模式
/grep "async.*calculateTotal" --type js
/grep "Promise.all\|Promise.race" src/services/ --type js
/grep "await.*forEach\|map.*await" src/services/ --type js
```

**可能發現**：
```javascript
// 找到可疑的代碼模式
src/services/OrderService.js:78
  items.forEach(async (item) => {  // ❌ 危險！forEach + async
    await updatePrice(item);
  });
```

4. **查看最近的變更**
```bash
# 查看最近的 commit，特別是 "optimize" 那個
git show a3f2d9e --stat

# 看哪些檔案被修改了
# 重點關注 OrderService.js
```

**自然學到的技巧**：
- 為什麼從錯誤訊息開始？因為錯誤訊息直接指向問題代碼
- 為什麼搜尋反模式？因為常見的並發問題有已知模式
- 為什麼查看最近變更？因為 bug 通常來自新程式碼

**檢查點（5 分鐘內）**：
- [ ] 找到錯誤訊息中提到的函數
- [ ] 識別可疑的異步模式
- [ ] 知道最近哪些檔案被修改

**計時：00:05**

---

### 階段二：深入閱讀問題代碼（15 分鐘）

**目標**：理解訂單處理流程和 bug 成因

**步驟**：

1. **閱讀核心服務**
```bash
/read src/services/OrderService.js
```

**發現的程式碼（簡化版）**：
```javascript
// src/services/OrderService.js

class OrderService {
  async processOrder(userId, cartId) {
    // 1. 取得購物車
    const cart = await CartService.getCart(cartId);

    // 2. 計算總金額（問題可能在這裡）
    const total = await this.calculateTotal(cart);

    // 3. 預留庫存
    await InventoryService.reserveItems(cart.items);

    // 4. 收取款項
    const payment = await PaymentService.charge(userId, total);

    // 5. 建立訂單
    const order = await OrderRepository.create({
      userId,
      items: cart.items,
      total,
      paymentId: payment.id
    });

    return order;
  }

  async calculateTotal(cart) {
    let total = 0;

    // 🚨 最近的「優化」
    // 之前：用 for...of 循序處理
    // 現在：改用 forEach 並行處理（錯誤！）

    cart.items.forEach(async (item) => {
      const latestPrice = await this.getLatestPrice(item.productId);
      item.price = latestPrice; // ❌ 並發修改 cart 物件
      total += latestPrice * item.quantity; // ❌ 並發修改 total
    });

    // ❌ 這裡會立即返回 0，因為 forEach 不等待 async 函數
    return total;
  }

  async getLatestPrice(productId) {
    // 模擬 API 呼叫，有延遲
    return await PriceService.fetchPrice(productId);
  }
}
```

2. **分析問題**
```bash
# 請 Claude 幫忙分析
我找到以下可疑的程式碼：
[貼上 calculateTotal 函數]

這個函數有什麼問題？為什麼會導致：
1. Order total mismatch
2. Race condition
3. Duplicate order creation

請詳細解釋 bug 成因。
```

**Claude 的分析**：
```markdown
# Bug 分析報告

## 🔴 Critical Bug：forEach + async 反模式

### 問題 1：total 永遠是 0
```javascript
cart.items.forEach(async (item) => {
  const latestPrice = await this.getLatestPrice(item.productId);
  total += latestPrice * item.quantity;
});

return total; // ❌ 立即返回，此時所有 async 函數還在執行中
```

**原因**：
- `forEach` 不等待 async 函數完成
- `return total` 在任何 `await` 完成前就執行了
- 結果：total = 0

**影響**：
- 訂單金額錯誤
- 可能免費送貨（total = 0）

### 問題 2：並發修改 cart 物件
```javascript
item.price = latestPrice; // 多個 async 函數同時修改 cart
```

**原因**：
- forEach 會同時啟動多個 async 函數
- 它們並發修改同一個 cart 物件
- JavaScript 物件不是 thread-safe

**影響**：
- cart.items 的 price 可能被覆蓋
- 導致 total mismatch

### 問題 3：後續流程使用錯誤的 total
```javascript
const payment = await PaymentService.charge(userId, total); // total = 0
const order = await OrderRepository.create({ total }); // total = 0
```

**影響**：
- 付款金額錯誤（可能是 0 或隨機值）
- 資料庫中的訂單金額錯誤
- 客服需要手動處理大量退款

### 問題 4：Race Condition 導致重複訂單

因為 `calculateTotal` 返回錯誤值，有些請求會 retry，導致：
1. 第一次請求：total = 0，付款失敗
2. 用戶重試
3. 第二次請求：total = 0（又失敗）或正確值（成功）
4. 如果兩次都成功 → 重複訂單

## 📊 時間線重建

```
Time 0ms:   forEach 啟動 3 個 async 函數（3 個商品）
Time 0ms:   return total (= 0)
Time 50ms:  第 1 個 getLatestPrice 完成，total += 29.99
Time 100ms: 第 2 個 getLatestPrice 完成，total += 49.99
Time 150ms: 第 3 個 getLatestPrice 完成，total += 19.99

但是 total 已經被返回了（值是 0）！
後續的計算完全沒用。
```

## ✅ 正確的做法

```javascript
async calculateTotal(cart) {
  let total = 0;

  // 使用 for...of（會等待每個 await）
  for (const item of cart.items) {
    const latestPrice = await this.getLatestPrice(item.productId);
    item.price = latestPrice;
    total += latestPrice * item.quantity;
  }

  return total; // ✓ 所有價格都已取得
}

// 或者使用 Promise.all（平行但安全）
async calculateTotal(cart) {
  const pricePromises = cart.items.map(item =>
    this.getLatestPrice(item.productId)
  );

  const prices = await Promise.all(pricePromises);

  let total = 0;
  cart.items.forEach((item, index) => {
    item.price = prices[index];
    total += prices[index] * item.quantity;
  });

  return total;
}
```
```

**自然學到的知識**：
- forEach + async 是經典反模式
- JavaScript 的異步陷阱
- 為什麼需要 for...of 或 Promise.all

**記憶沉澱**：
```bash
/memory save

主題：JavaScript forEach + async 反模式

❌ 錯誤模式：
array.forEach(async (item) => {
  await doSomething(item);
});
// forEach 不等待 async 函數，全部並發執行

✅ 正確做法：

1. 循序處理（保證順序）
for (const item of array) {
  await doSomething(item);
}

2. 並行處理（更快，但要注意並發修改）
const results = await Promise.all(
  array.map(item => doSomething(item))
);

常見症狀：
- 函數立即返回預設值（如 0, null）
- Race condition
- 數據不一致

檢測方法：
/grep "forEach.*async" --type js
```

**檢查點（15 分鐘內）**：
- [ ] 理解 bug 的根本原因
- [ ] 知道為什麼 total 是 0
- [ ] 理解 race condition 如何發生
- [ ] 使用 /memory 記錄反模式

**計時：00:15**

---

### 階段三：確認問題範圍與影響（10 分鐘）

**目標**：確保理解完整問題，避免修了 A 壞了 B

**步驟**：

1. **搜尋其他可能有相同問題的地方**
```bash
# 搜尋整個專案中的 forEach + async
/grep "forEach.*async\|forEach.*=>" src/ --type js -A 2

# 可能發現其他地方也有相同問題
```

2. **檢查測試是否涵蓋此情況**
```bash
/read tests/OrderService.test.js

# 查看是否有測試 calculateTotal 的異步行為
```

**可能發現**：
```javascript
// tests/OrderService.test.js

describe('OrderService', () => {
  // ❌ 測試不夠嚴謹
  it('calculates order total', async () => {
    const cart = { items: [{ productId: 1, quantity: 2 }] };
    const total = await orderService.calculateTotal(cart);

    // 這個測試可能會通過（如果 API 夠快）
    // 或失敗（如果 API 慢）
    // → flaky test
    expect(total).toBeGreaterThan(0);
  });
});
```

3. **確認修復策略**
```bash
# 請 Claude 確認修復方案
我計劃這樣修復：

1. 將 forEach 改為 for...of
2. 添加測試確保異步行為正確
3. 檢查是否有其他地方有相同問題

這樣的修復是否足夠？是否有遺漏？
```

**自然學到的習慣**：
- 為什麼要搜尋類似問題？因為同樣的錯誤可能出現多次
- 為什麼要檢查測試？因為測試可以防止未來再犯

**檢查點（25 分鐘內）**：
- [ ] 確認問題的完整範圍
- [ ] 知道是否有其他地方需要修
- [ ] 確定修復策略

**計時：00:25**

---

### 階段四：實作最小化修復（15 分鐘）

**目標**：實作最安全、最快的修復方案

**步驟**：

1. **修復核心問題**
```bash
/read src/services/OrderService.js

# 請求修改
請將 calculateTotal 函數中的 forEach 改為 for...of，
確保正確等待所有異步操作完成。
```

**修復後的程式碼**：
```javascript
// src/services/OrderService.js（修復後）

async calculateTotal(cart) {
  let total = 0;

  // ✅ 修復：使用 for...of 確保循序執行
  for (const item of cart.items) {
    const latestPrice = await this.getLatestPrice(item.productId);
    item.price = latestPrice;
    total += latestPrice * item.quantity;
  }

  return total; // ✓ 現在 total 是正確的了
}
```

2. **添加防護性檢查**
```bash
# 請求添加驗證
請在 calculateTotal 返回前添加驗證，確保 total > 0，
如果 total <= 0，拋出錯誤。
```

**增強後的程式碼**：
```javascript
async calculateTotal(cart) {
  if (!cart || !cart.items || cart.items.length === 0) {
    throw new Error('Invalid cart: no items');
  }

  let total = 0;

  for (const item of cart.items) {
    const latestPrice = await this.getLatestPrice(item.productId);

    if (latestPrice <= 0) {
      throw new Error(`Invalid price for product ${item.productId}`);
    }

    item.price = latestPrice;
    total += latestPrice * item.quantity;
  }

  // 防護性檢查
  if (total <= 0) {
    throw new Error(`Invalid total calculated: ${total}`);
  }

  return total;
}
```

3. **添加日誌**
```bash
# 請求添加日誌
請在關鍵步驟添加日誌，方便未來除錯。
```

**最終版本**：
```javascript
async calculateTotal(cart) {
  logger.info(`Calculating total for cart ${cart.id} with ${cart.items.length} items`);

  if (!cart || !cart.items || cart.items.length === 0) {
    throw new Error('Invalid cart: no items');
  }

  let total = 0;

  for (const item of cart.items) {
    const latestPrice = await this.getLatestPrice(item.productId);

    if (latestPrice <= 0) {
      logger.error(`Invalid price ${latestPrice} for product ${item.productId}`);
      throw new Error(`Invalid price for product ${item.productId}`);
    }

    item.price = latestPrice;
    total += latestPrice * item.quantity;

    logger.debug(`Item ${item.productId}: ${latestPrice} × ${item.quantity}`);
  }

  if (total <= 0) {
    logger.error(`Invalid total calculated: ${total}`);
    throw new Error(`Invalid total calculated: ${total}`);
  }

  logger.info(`Total calculated: ${total}`);
  return total;
}
```

**自然學到的原則**：
- 為什麼加驗證？因為可以早期發現異常
- 為什麼加日誌？因為方便未來除錯
- 為什麼選擇 for...of 而非 Promise.all？因為更保守、更安全（緊急修復優先穩定性）

**檢查點（40 分鐘內）**：
- [ ] 核心問題已修復
- [ ] 添加防護性檢查
- [ ] 添加日誌
- [ ] 程式碼可讀性良好

**計時：00:40**

---

### 階段五：快速驗證與部署（15 分鐘）

**目標**：確保修復有效且沒有破壞其他功能

**步驟**：

1. **執行單元測試**
```bash
npm test -- OrderService

# 預期結果
✓ calculates order total correctly
✓ handles empty cart
✓ throws error for invalid price
```

2. **本地手動測試**
```bash
# 啟動服務
npm run dev

# 測試訂單建立
curl -X POST http://localhost:3000/orders \
  -H "Content-Type: application/json" \
  -d '{
    "userId": "user123",
    "cartId": "cart456"
  }'

# 檢查回應
{
  "orderId": "ORD-78910",
  "total": 129.97,  // ✓ 不再是 0
  "status": "completed"
}
```

3. **檢查日誌**
```bash
tail -f logs/app.log

# 應該看到
[INFO] Calculating total for cart cart456 with 3 items
[DEBUG] Item PROD-1: 29.99 × 1
[DEBUG] Item PROD-2: 49.99 × 2
[DEBUG] Item PROD-3: 19.99 × 1
[INFO] Total calculated: 129.97
```

4. **建立緊急修復 commit**
```bash
git add src/services/OrderService.js
git commit -m "fix(orders): resolve race condition in calculateTotal

Critical bug fix for P0 incident.

Problem:
- forEach + async causing race condition
- calculateTotal returning 0 immediately
- Payment charged with incorrect amounts

Solution:
- Changed forEach to for...of loop
- Added validation for total > 0
- Added defensive checks for prices
- Added logging for debugging

Incident: INC-2025-01-15-001
Affected customers: ~500
Estimated impact: $50,000+

Tested:
- Unit tests passing
- Manual testing verified
- Logs showing correct behavior"

git push origin main
```

5. **部署並監控**
```bash
# 部署到生產環境（假設有 CI/CD）
# 或通知 DevOps 團隊

# 監控錯誤率
watch -n 5 'tail -100 logs/error.log | grep "Race condition"'

# 應該看到錯誤停止出現
```

6. **更新事件報告**
```bash
# 在事件管理系統中更新狀態

🟢 INCIDENT RESOLVED

Root Cause:
- forEach + async anti-pattern in OrderService.calculateTotal()
- Introduced in commit a3f2d9e (performance optimization)

Fix:
- Changed to for...of loop
- Added defensive validation
- Added logging

Deployed: 2025-01-15 21:25 UTC
Time to Resolution: 55 minutes
```

**最終記憶沉澱**：
```bash
/memory save

主題：緊急 Bug 修復完整流程

時間壓力下的 5 階段流程：

階段1️⃣：快速定位（15 min）
- 從錯誤訊息提取關鍵字
- /grep 搜尋可疑模式
- 查看最近變更（git log）
- 重點：速度優先，找到大致範圍即可

階段2️⃣：深入理解（15 min）
- /read 閱讀核心程式碼
- 請 Claude 分析 bug 成因
- 理解異步流程
- 用 /memory 記錄反模式

階段3️⃣：確認範圍（10 min）
- /grep 搜尋類似問題
- 檢查測試覆蓋
- 確認修復策略
- 避免修了 A 壞了 B

階段4️⃣：最小化修復（15 min）
- 修復核心問題
- 添加防護性檢查
- 添加日誌
- 重點：穩定性 > 完美

階段5️⃣：驗證部署（15 min）
- 單元測試
- 手動測試
- 檢查日誌
- 部署監控

關鍵原則：
- 時間壓力下優先找到問題，而非理解全部
- 善用 /grep 和 /read，避免盲目閱讀
- 最小化修復：夠用就好，不要過度優化
- 防護性編程：添加驗證和日誌
- 記錄過程：方便事後回顧

常見反模式：
- forEach + async（本次）
- Promise 未處理
- 並發修改共享狀態
- 缺少錯誤處理

總時間：55 分鐘（在 SLA 內）
```

**檢查點（60 分鐘內）**：
- [ ] 測試通過
- [ ] 手動驗證正常
- [ ] 已部署到生產環境
- [ ] 錯誤停止出現
- [ ] 事件報告已更新
- [ ] 使用 /memory 記錄流程

**計時：00:55 ✅ 任務完成**

---

## 驗證標準

### 必須達成 ✅

- [ ] 在 60 分鐘內完成修復
- [ ] 正確識別問題根源（forEach + async）
- [ ] 使用 /grep 快速定位可疑代碼
- [ ] 使用 /read 理解核心邏輯
- [ ] 實作正確的修復（for...of）
- [ ] 添加防護性檢查
- [ ] 所有測試通過
- [ ] 手動驗證功能正常
- [ ] 錯誤停止出現
- [ ] 使用 /memory 記錄反模式和流程

### 額外成就 🌟

- [ ] 在 45 分鐘內完成
- [ ] 發現並修復其他潛在問題
- [ ] 添加新的測試案例
- [ ] 建立事後分析報告
- [ ] 提出長期改進建議（如添加 ESLint 規則）
- [ ] 優化為 Promise.all 版本（效能更好）

---

## 學習反思

### 反思問題

1. **時間管理**：
   - 你如何分配 60 分鐘？
   - 哪個階段花最多時間？為什麼？
   - 如何判斷「已經足夠理解」可以開始修了？

2. **搜尋策略**：
   - 你用什麼關鍵字搜尋？為什麼選這些？
   - /grep 和 /read 的使用時機差異？
   - 如何避免在不相關的代碼上浪費時間？

3. **修復策略**：
   - 為什麼選擇 for...of 而非 Promise.all？
   - 最小化修復 vs. 完美解決方案的權衡？
   - 如何確保修復不會引入新問題？

4. **壓力管理**：
   - 時間壓力如何影響你的決策？
   - 如何在緊急情況下保持冷靜？
   - 何時應該升級而非自己解決？

### 延伸練習

1. **優化修復**：
   - 將 for...of 改為 Promise.all 版本
   - 添加快取避免重複呼叫 API
   - 添加重試機制

2. **預防機制**：
   - 建立 ESLint 規則檢測 forEach + async
   - 添加 pre-commit hook
   - 建立更完整的測試

3. **事後分析**：
   - 撰寫完整的事件報告
   - 分析為什麼這個 bug 會進入生產環境
   - 提出流程改進建議

4. **知識分享**：
   - 整理成團隊培訓材料
   - 建立「常見異步陷阱」文檔
   - 分享到團隊知識庫

---

## 相關資源

### 下一步學習

- **C04：功能模組提取** - 學習重構複雜耦合代碼
- **C05：安全漏洞修復** - 學習系統化發現安全問題
- **模組 8：效能優化實戰** - 學習優化異步性能

### 工具參考

- **ESLint** - 靜態代碼分析
- **node-clinic** - Node.js 效能分析
- **Sentry** - 錯誤監控與追蹤
- **Datadog** - 應用監控

### 相關概念

- **Event Loop** - JavaScript 異步機制
- **Promise.all vs. for...of** - 並行 vs. 循序
- **Race Condition** - 並發問題
- **Defensive Programming** - 防護性編程

### JavaScript 異步模式

- **Anti-patterns**:
  - forEach + async
  - 未處理的 Promise rejection
  - async 函數中的同步 return

- **Best Practices**:
  - for...of（循序）
  - Promise.all（並行）
  - try-catch 包裹 await
  - Promise rejection 處理

---

**建議完成時間**：1 小時（嚴格限制）
**難度評估**：4/5（時間壓力高）
**重要度**：5/5（生產環境問題處理是必備技能）
**可複用性**：5/5（緊急修復流程可應用到任何 bug）
