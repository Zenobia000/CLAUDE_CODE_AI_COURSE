# 訂單系統領域模型

## 📋 模型概述

這是一個電商訂單系統的完整 DDD 領域模型，展示了如何用 AI 輔助建立領域模型。

**業務場景**：電商訂單管理
**核心聚合**：Order（訂單聚合）
**程式碼規模**：~800 行（包含測試）

---

## 📂 檔案結構

```
訂單系統/
├── README.md（本文件）
├── ubiquitous-language.md    # 通用語言詞彙表
├── event-storming.mmd        # 事件風暴圖
├── context-map.md            # 上下文地圖
├── domain-model.mmd          # 領域模型類圖
└── domain-model.py           # Python 程式碼實現（含測試）
```

---

## 🎯 學習重點

### 1. 聚合根設計
**Order 聚合**包含：
- Order（聚合根）
- OrderItem（內部實體）

**設計原則**：
- 聚合根是唯一入口
- 保護資料一致性（total_amount 自動計算）
- 封裝業務規則（取消邏輯、狀態流轉）

### 2. 值對象設計
本模型包含 3 個值對象：
- **OrderId**：訂單 ID（不可變、可生成）
- **Money**：金額（不可變、支援運算）
- **OrderStatus**：訂單狀態（枚舉）

**設計特點**：
- 使用 `@dataclass(frozen=True)` 保證不可變性
- 封裝領域邏輯（如 Money 的幣種檢查）

### 3. 領域事件
本模型包含 3 個領域事件：
- OrderSubmittedEvent：訂單已提交
- OrderPaidEvent：訂單已支付
- OrderCancelledEvent：訂單已取消

**設計特點**：
- 事件攜帶必要資訊
- 用於解耦系統（訂單不直接調用支付、庫存）

### 4. 狀態流轉管理
訂單有 7 個狀態，狀態流轉規則清晰：
```
DRAFT → PENDING_PAYMENT → PAID → SHIPPED → COMPLETED
                ↓           ↓
            CLOSED      CANCELLED
```

**設計特點**：
- 每個狀態轉換都有業務方法（submit, mark_as_paid）
- 狀態轉換前檢查合法性（如只有待支付才能支付）

---

## 🚀 快速開始

### 閱讀順序

1. **通用語言**：`ubiquitous-language.md`
   - 理解核心概念
   - 理解業務規則

2. **事件風暴**：`event-storming.mmd`
   - 理解業務流程
   - 理解事件流動

3. **領域模型**：`domain-model.mmd`
   - 理解聚合結構
   - 理解實體與值對象關係

4. **程式碼實現**：`domain-model.py`
   - 理解實現方式
   - 執行測試驗證

### 執行測試

```python
# 讀取程式碼
python3 domain-model.py

# 程式碼中已包含測試用例，直接執行即可看到輸出
```

---

## 📝 核心程式碼片段

### 聚合根：Order

```python
class Order:
    """訂單聚合根"""

    def submit(self):
        """提交訂單（業務方法）"""
        # 1. 狀態檢查
        if self.status != OrderStatus.DRAFT:
            raise InvalidOrderStateError("只有草稿狀態才能提交")

        # 2. 業務規則檢查
        if not self.items:
            raise ValueError("訂單必須包含至少一個商品")

        # 3. 狀態變更
        self.status = OrderStatus.PENDING_PAYMENT
        self.payment_deadline = datetime.now() + timedelta(minutes=30)

        # 4. 發布領域事件
        self._events.append(OrderSubmittedEvent(...))

    @property
    def total_amount(self) -> Money:
        """計算總金額（自動保持一致性）"""
        if not self.items:
            return Money(Decimal(0))
        return sum((item.subtotal for item in self.items), Money(Decimal(0)))
```

### 值對象：Money

```python
@dataclass(frozen=True)
class Money:
    """金額值對象"""
    amount: Decimal
    currency: str = "USD"

    def __add__(self, other: 'Money') -> 'Money':
        """金額相加（檢查幣種一致性）"""
        if self.currency != other.currency:
            raise ValueError("幣種不一致")
        return Money(self.amount + other.amount, self.currency)
```

---

## 🤔 設計決策

### Q1：為什麼 OrderItem 在 Order 聚合內？

**答**：因為訂單項與訂單必須保持一致性：
- 修改訂單項數量 → 訂單總金額必須同步更新
- 刪除訂單項 → 訂單總金額必須同步更新
- 如果分離，無法保證一致性

### Q2：為什麼 Payment 不在 Order 聚合內？

**答**：因為支付與訂單可以最終一致性：
- 訂單只需要知道「已支付」這個事實
- 不需要知道支付的詳細資訊（支付方式、支付流水號）
- 分離後，支付系統可以獨立演化

### Q3：為什麼使用領域事件而不是直接調用？

**答**：解耦的需要：
- Order 不需要知道誰關心「訂單已支付」事件
- 新增功能（如積分系統）不需要修改 Order
- 某個訂閱者失敗不影響其他訂閱者

---

## 📊 模型統計

- **聚合數量**：1 個（Order）
- **實體數量**：2 個（Order, OrderItem）
- **值對象數量**：3 個（OrderId, Money, OrderStatus）
- **領域事件數量**：3 個
- **業務方法數量**：8 個
- **程式碼行數**：~500 行（不含測試）
- **測試用例數量**：12 個

---

## 🔗 相關資源

- **情境題**：[B01 訂單系統 DDD 建模](../../情境題庫/基礎級/B01_訂單系統DDD建模.md)
- **理論基礎**：[7.1 DDD 核心概念速覽](../../理論/7.1_DDD核心概念速覽.md)

---

**模型版本**：v1.0
**最後更新**：2025-10-30
**業務場景**：電商訂單管理
