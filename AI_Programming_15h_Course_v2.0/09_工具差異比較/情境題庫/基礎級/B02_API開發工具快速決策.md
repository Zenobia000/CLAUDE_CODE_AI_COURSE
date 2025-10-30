# B02: API 開發工具快速決策

**難度**：★☆☆
**預估時間**：思考 3 分鐘 + 閱讀解答 5 分鐘
**考察重點**：識別簡單任務與工具的匹配

---

## 情境描述

今天是星期一早上，你有 8 個 API endpoints 要實作，全都是標準 CRUD 操作。

### 任務清單

```
今日待辦（預計 4 小時完成）：

1. GET /products - 列出所有商品
2. GET /products/:id - 取得單一商品
3. POST /products - 新增商品
4. PUT /products/:id - 更新商品
5. DELETE /products/:id - 刪除商品

6. GET /categories - 列出所有分類
7. POST /categories - 新增分類
8. DELETE /categories/:id - 刪除分類

技術棧：
- Node.js + Express
- MongoDB + Mongoose
- 標準 RESTful 設計

要求：
- 輸入驗證（express-validator）
- 錯誤處理（統一格式）
- 簡單的單元測試
```

### 你的思考

```
內心 OS：
"這些都是重複性工作...
第一個寫完，後面 7 個應該很類似...
我應該用什麼工具最快？"
```

---

## 任務

### Part 1: 快速決策（30 秒內）

選擇你的工具：

- [ ] Claude Code
- [ ] GitHub Copilot
- [ ] Cursor

理由（一句話）：
```
_______________________________________
```

### Part 2: 效率預估

估算每個工具完成 8 個 endpoints 的時間：

```
Claude Code：_______ 小時
Copilot：_______ 小時
Cursor：_______ 小時
手動編寫：_______ 小時
```

---

## 參考解答

### 工具選擇：[Copilot]

#### 決策邏輯（閃電思考）

```
問題核心判斷：
✓ 高度重複（CRUD 模式）
✓ 規模小（每個 endpoint 30-50 行）
✓ 時間緊迫（4 小時完成 8 個）
✓ 不需深度思考（模式已知）

決策：Copilot（速度為王）
```

#### 實際工作流程

```javascript
// Step 1: 手動寫第一個 endpoint（建立模板）
// routes/products.js

const express = require('express');
const router = express.Router();
const { body, validationResult } = require('express-validator');
const Product = require('../models/Product');

// GET /products
router.get('/', async (req, res) => {
  try {
    const products = await Product.find();
    res.json({ success: true, data: products });
  } catch (error) {
    res.status(500).json({ success: false, error: error.message });
  }
});

// POST /products
router.post('/',
  [
    body('name').notEmpty(),
    body('price').isNumeric(),
  ],
  async (req, res) => {
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
      return res.status(400).json({ errors: errors.array() });
    }

    try {
      const product = await Product.create(req.body);
      res.status(201).json({ success: true, data: product });
    } catch (error) {
      res.status(500).json({ success: false, error: error.message });
    }
  }
);

// Step 2: Copilot 學習模式，自動補全其餘
// 你打：// PUT /products/:id
// Copilot 立即建議完整代碼（<1 秒）

// Step 3: Categories 更快
// 切換到 routes/categories.js
// 你打：const express =
// Copilot 建議整個檔案（因為學會了 products 的模式）

總時間：
- 第一個模組（Products）：45 分鐘
- 第二個模組（Categories）：15 分鐘
- 測試：30 分鐘
- 總計：90 分鐘 ✅（比預計快 2.5x）
```

#### 效率對比

```
工具對比：

Copilot（90 分鐘）：
✓ 最快
✓ 流暢不打斷
✓ 學習你的模式

Cursor（2 小時）：
- 速度中等（2-5 秒生成）
- 可以一次生成多檔案
- 但對這種簡單任務是 overkill

Claude Code（3-4 小時）：
- 每次生成 20-30 秒
- 會深度分析（不必要）
- API 成本累積
- 殺雞用牛刀

手動（4-5 小時）：
- 最慢
- 容易出錯
- 沒有理由不用 AI

結論：Copilot 勝出
```

---

## 學習重點

### 關鍵洞察

```
簡單任務的黃金法則：
"重複性高 + 模式已知 → 選最快的工具"

Copilot 的最佳場景：
✓ CRUD 開發
✓ 測試撰寫
✓ Boilerplate 代碼
✓ 日常編碼

不要用 Claude Code 的場景：
✗ 簡單重複任務（浪費時間和金錢）
✗ 高頻操作（累積延遲）
✗ 模式已知的編碼（不需深度思考）
```

### 常見錯誤

```
錯誤 1：習慣性使用 Claude Code
"我習慣用 Claude Code，所有任務都用它"
→ 結果：簡單任務浪費 2-3x 時間

錯誤 2：低估 Copilot 的能力
"Copilot 只是自動補全，不夠智能"
→ 結果：手動寫重複代碼，浪費時間

正確心態：
"讓合適的工具做合適的事"
```

---

**最後更新**：2025-10-30
