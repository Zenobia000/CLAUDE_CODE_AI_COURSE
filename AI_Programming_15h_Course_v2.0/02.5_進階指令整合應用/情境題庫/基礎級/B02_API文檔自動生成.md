# B02：API 文檔自動生成 - 輸出風格的威力

## 🎯 學習目標

**知識目標**：
- [ ] 理解 `/output-style` 指令的作用
- [ ] 掌握 `documentation-writer` agent 的特點
- [ ] 了解 API 文檔的標準格式

**技能目標**：
- [ ] 能使用輸出風格控制 AI 產出格式
- [ ] 能生成專業的 API 文檔
- [ ] 能組合 agent + 輸出風格

**時間估計**：25-30 分鐘

---

## 📋 情境描述

### 背景故事
你正在開發一個電商 API，已經完成了幾個核心端點的實作。現在需要為這些 API 生成標準的文檔，供前端團隊和第三方開發者使用。手動寫文檔很耗時，而且容易出錯，你想嘗試自動生成。

### 問題陳述
你有以下 Flask API 程式碼，需要生成完整的 API 文檔：

```python
# ecommerce_api.py
from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

@app.route('/api/products', methods=['GET'])
def get_products():
    """獲取產品列表"""
    category = request.args.get('category')
    limit = request.args.get('limit', 10, type=int)

    # 模擬數據
    products = [
        {"id": 1, "name": "筆記型電腦", "price": 25000, "category": "electronics"},
        {"id": 2, "name": "手機", "price": 15000, "category": "electronics"},
        {"id": 3, "name": "書籍", "price": 300, "category": "books"}
    ]

    if category:
        products = [p for p in products if p['category'] == category]

    return jsonify({
        'products': products[:limit],
        'total': len(products),
        'page': 1
    })

@app.route('/api/products', methods=['POST'])
def create_product():
    """創建新產品"""
    data = request.get_json()

    if not data or 'name' not in data or 'price' not in data:
        return jsonify({'error': 'Missing required fields'}), 400

    product = {
        'id': 999,  # 模擬生成的 ID
        'name': data['name'],
        'price': data['price'],
        'category': data.get('category', 'general'),
        'created_at': datetime.now().isoformat()
    }

    return jsonify(product), 201

@app.route('/api/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    """獲取單一產品詳情"""
    # 模擬數據查詢
    if product_id == 1:
        return jsonify({
            "id": 1,
            "name": "筆記型電腦",
            "price": 25000,
            "category": "electronics",
            "description": "高效能筆記型電腦",
            "in_stock": True,
            "stock_count": 50
        })
    else:
        return jsonify({'error': 'Product not found'}), 404
```

### 任務要求
1. 生成標準格式的 API 文檔
2. 包含每個端點的完整說明
3. 提供請求/回應範例
4. 確保文檔的一致性和專業性

---

## 🛠️ 實作步驟

### 步驟 1：準備 API 程式碼
```bash
# 1. 創建工作目錄
mkdir api_documentation
cd api_documentation

# 2. 保存 API 程式碼
# 將上述程式碼保存為 ecommerce_api.py
```

### 步驟 2：使用一般模式嘗試（對比實驗）
```bash
claude --add-file ecommerce_api.py
```

**提示詞**：
```
請為這個 Flask API 生成文檔。
```

**觀察重點**：
- 產出格式是否一致？
- 結構是否標準？
- 細節是否完整？

### 步驟 3：使用專業方式（Agent + 輸出風格）
```bash
# 切換到文檔撰寫專家
/agents:documentation-writer

# 設定專業的 API 文檔輸出格式
/output-style:api-documentation
```

**提示詞**：
```
請為這個電商 API 生成完整的 API 文檔，包含：

1. API 概述
2. 認證說明（假設使用 API Key）
3. 所有端點的詳細文檔
4. 錯誤處理說明
5. 使用範例

請確保文檔專業、完整且易於理解。
```

### 步驟 4：對比與分析

**預期的改進**：

**🎯 一般模式 vs 專業模式對比**：

| 面向 | 一般模式 | Agent + 輸出風格 |
|------|---------|-----------------|
| 格式一致性 | 隨意 | 標準化 |
| 內容完整性 | 基本 | 詳細 |
| 專業術語 | 一般 | 專業 |
| 範例品質 | 簡單 | 實用 |
| 結構組織 | 鬆散 | 系統化 |

**🔍 專業文檔應包含**：
- OpenAPI/Swagger 風格的結構
- 完整的請求/回應範例
- 錯誤碼說明
- 使用限制說明
- 測試方法

### 步驟 5：生成不同格式的文檔
**提示詞**：
```
請基於剛才的文檔，生成以下三種格式：

1. Markdown 格式（適合 GitHub）
2. OpenAPI 3.0 YAML 格式（適合 Swagger UI）
3. 純文字格式（適合內部文檔）

每種格式都要保持相同的資訊完整性。
```

---

## ✅ 成功檢查點

完成此情境後，你應該能夠：

**理解檢查點**：
- [ ] 我了解為什麼需要輸出風格控制
- [ ] 我明白 `documentation-writer` agent 的專業性
- [ ] 我能區分不同文檔格式的適用場景

**技能檢查點**：
- [ ] 我成功使用了 `/agents:documentation-writer` 指令
- [ ] 我成功使用了 `/output-style:api-documentation` 指令
- [ ] 我能生成多種格式的 API 文檔

**品質檢查點**：
- [ ] 生成的文檔包含所有必要資訊
- [ ] 請求/回應範例是正確的
- [ ] 文檔結構清晰且專業

---

## 🎓 學習收穫

### 核心概念
1. **輸出風格的價值**：確保產出的一致性和專業性
2. **Agent 專業化**：不同 agent 有不同的專業知識和寫作風格
3. **組合使用**：Agent + 輸出風格 = 更專業的結果

### 實用技巧
1. **最佳實踐流程**：
   ```
   claude → /agents:documentation-writer → /output-style:api-documentation → 具體要求
   ```

2. **文檔品質要素**：
   - 完整性：所有端點都有說明
   - 準確性：範例能正常執行
   - 可用性：開發者能快速上手

3. **格式選擇策略**：
   - Markdown：GitHub、內部文檔
   - OpenAPI：Swagger UI、工具整合
   - 純文字：簡單分享、打印

### 延伸思考
- 如何將文檔生成整合到 CI/CD 流程中？
- 如何確保文檔與程式碼同步更新？
- 不同團隊可能需要哪些客製化的輸出風格？

---

## 🚀 進階挑戰

### 挑戰 1：客製化輸出風格
**提示詞**：
```
請為我們公司創建一個客製化的 API 文檔模板，包含：

1. 公司標準格式
2. 安全性說明章節
3. SDK 使用範例
4. 版本控制說明
5. 支援聯絡資訊

將此保存為可重複使用的模板。
```

### 挑戰 2：多語言文檔
**提示詞**：
```
將 API 文檔翻譯成英文和日文版本，並確保：
1. 技術術語的準確性
2. 範例程式碼的本地化（註解）
3. 文化適應性（禮貌用語）
```

### 挑戰 3：互動式文檔
**提示詞**：
```
生成一個 HTML 版本的 API 文檔，包含：
1. 可展開/收合的章節
2. 程式碼語法高亮
3. 複製按鈕
4. 測試功能（curl 命令）
```

---

## 📚 相關資源

**工具推薦**：
- [Swagger UI](https://swagger.io/tools/swagger-ui/) - API 文檔視覺化
- [Postman](https://www.postman.com/) - API 測試與文檔
- [GitBook](https://www.gitbook.com/) - 文檔託管平台

**最佳實踐**：
- [OpenAPI Specification](https://swagger.io/specification/)
- [API 文檔設計指南](https://blog.readme.com/api-documentation-best-practices/)

**後續學習**：
- B04：安全漏洞掃描 - 學習 `security-auditor`
- C03：自動化文檔生成系統 - 更複雜的文檔工作流程

---

## 💭 反思問題

1. **效率提升**：自動生成文檔 vs 手動撰寫，時間節省了多少？
2. **品質對比**：AI 生成的文檔 vs 人工文檔，各有什麼優缺點？
3. **一致性**：使用輸出風格對文檔一致性有什麼幫助？
4. **實際應用**：你會如何將這個方法整合到團隊的開發流程中？

---

## 🔄 與前一情境的連結

**從 B01 到 B02 的進步**：
- B01：學會單一 Agent 使用
- B02：學會 Agent + 輸出風格組合
- 下一步：學會更複雜的指令整合

**技能累積**：
```
B01: /agents:code-reviewer
B02: /agents:documentation-writer + /output-style:api-documentation
B03: 更多組合...
```

---

**完成時間記錄**：___ 分鐘
**難度評分** (1-5)：___
**與 B01 相比的進步**：___
**筆記區域**：
```
記錄你在使用輸出風格時的發現...
```

---

*本情境重點是體驗輸出風格的威力，以及 Agent 的專業化能力。*