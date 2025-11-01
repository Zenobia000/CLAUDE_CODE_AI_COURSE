"""
訂單系統 - 領域模型（Domain Model）

這是一個完整的 DDD 領域模型實現範例，展示如何將領域概念轉換為可執行的程式碼。

核心概念實現：
- Value Objects (值對象): Money, Address, OrderId
- Entity (實體): OrderItem
- Aggregate Root (聚合根): Order
- Domain Events (領域事件): OrderCreated, OrderPaid, etc.
- Business Rules (業務規則): 狀態機、不變式

技術棧: Python 3.11+, dataclasses, typing
"""

from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import List, Optional
from uuid import uuid4, UUID


# ============================================================================
# Domain Events (領域事件)
# ============================================================================

@dataclass(frozen=True)
class DomainEvent:
    """Base class for all domain events"""
    event_id: UUID = field(default_factory=uuid4)
    occurred_at: datetime = field(default_factory=datetime.now)


@dataclass(frozen=True)
class OrderCreated(DomainEvent):
    """訂單已創建事件"""
    order_id: str
    customer_id: str
    total_amount: Decimal
    items_count: int


@dataclass(frozen=True)
class OrderPaid(DomainEvent):
    """訂單已支付事件"""
    order_id: str
    payment_id: str
    paid_amount: Decimal


@dataclass(frozen=True)
class OrderCancelled(DomainEvent):
    """訂單已取消事件"""
    order_id: str
    cancellation_reason: str
    cancelled_by: str


@dataclass(frozen=True)
class OrderShipped(DomainEvent):
    """訂單已發貨事件"""
    order_id: str
    tracking_number: str
    carrier: str


@dataclass(frozen=True)
class OrderCompleted(DomainEvent):
    """訂單已完成事件"""
    order_id: str


# ============================================================================
# Enums (枚舉)
# ============================================================================

class OrderStatus(str, Enum):
    """訂單狀態"""
    PENDING = "PENDING"        # 待支付
    PAID = "PAID"              # 已支付
    SHIPPED = "SHIPPED"        # 已發貨
    DELIVERED = "DELIVERED"    # 已送達
    COMPLETED = "COMPLETED"    # 已完成
    CANCELLED = "CANCELLED"    # 已取消
    REFUNDED = "REFUNDED"      # 已退款


class Currency(str, Enum):
    """幣種"""
    USD = "USD"
    TWD = "TWD"
    CNY = "CNY"
    EUR = "EUR"


# ============================================================================
# Value Objects (值對象)
# ============================================================================

@dataclass(frozen=True)
class Money:
    """
    金額值對象

    不變性原則：
    - 值對象是不可變的（使用 frozen=True）
    - 所有操作返回新對象，而非修改當前對象
    - 兩個屬性完全相同的 Money 是可互換的
    """
    amount: Decimal
    currency: Currency = Currency.TWD

    def __post_init__(self):
        """驗證業務規則"""
        if self.amount < 0:
            raise ValueError("金額不能為負數")

        # Ensure amount has at most 2 decimal places
        quantized = self.amount.quantize(Decimal('0.01'))
        object.__setattr__(self, 'amount', quantized)

    def add(self, other: 'Money') -> 'Money':
        """加法運算 - 返回新對象"""
        if self.currency != other.currency:
            raise ValueError(f"不同幣種無法相加: {self.currency} vs {other.currency}")
        return Money(self.amount + other.amount, self.currency)

    def subtract(self, other: 'Money') -> 'Money':
        """減法運算 - 返回新對象"""
        if self.currency != other.currency:
            raise ValueError(f"不同幣種無法相減: {self.currency} vs {other.currency}")
        result = self.amount - other.amount
        if result < 0:
            raise ValueError("結果金額不能為負數")
        return Money(result, self.currency)

    def multiply(self, multiplier: Decimal) -> 'Money':
        """乘法運算 - 返回新對象"""
        return Money(self.amount * multiplier, self.currency)

    def __str__(self) -> str:
        return f"{self.currency.value} {self.amount:.2f}"


@dataclass(frozen=True)
class Address:
    """
    地址值對象

    為什麼是值對象：
    - 兩個完全相同的地址沒有區別
    - 地址是不可變的（修改地址 = 創建新地址）
    - 沒有唯一標識的概念
    """
    country: str
    province: str
    city: str
    district: str
    street: str
    postal_code: str
    recipient_name: str
    recipient_phone: str

    def __post_init__(self):
        """驗證業務規則"""
        if not all([self.country, self.province, self.city,
                   self.street, self.recipient_name, self.recipient_phone]):
            raise ValueError("地址所有字段都必填")

        # Basic phone validation (simplified)
        if not self.recipient_phone.replace('-', '').replace(' ', '').isdigit():
            raise ValueError("電話號碼格式不正確")

    def __str__(self) -> str:
        return (f"{self.country} {self.province}{self.city}{self.district}{self.street}\n"
                f"收件人: {self.recipient_name} ({self.recipient_phone})")


@dataclass(frozen=True)
class OrderId:
    """
    訂單編號值對象

    格式: ORD-YYYYMMDD-RANDOM
    例如: ORD-20251101-A3F7B2
    """
    value: str

    @classmethod
    def generate(cls) -> 'OrderId':
        """生成新訂單編號"""
        import random
        import string
        date_part = datetime.now().strftime('%Y%m%d')
        random_part = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        return cls(f"ORD-{date_part}-{random_part}")

    def __str__(self) -> str:
        return self.value


# ============================================================================
# Entity (實體)
# ============================================================================

@dataclass
class OrderItem:
    """
    訂單項實體

    為什麼是實體而非值對象：
    - 有唯一標識（item_id）
    - 可以單獨修改（如修改數量）
    - 即使兩個訂單項的商品、數量、單價都相同，它們仍是不同的訂單項
    """
    item_id: UUID
    product_id: str
    product_name: str  # 快照，避免跨上下文查詢
    quantity: int
    unit_price: Money

    def __post_init__(self):
        """驗證業務規則"""
        if self.quantity <= 0:
            raise ValueError("數量必須大於 0")
        if self.unit_price.amount <= 0:
            raise ValueError("單價必須大於 0")

    @property
    def subtotal(self) -> Money:
        """計算小計：數量 × 單價"""
        return self.unit_price.multiply(Decimal(self.quantity))

    def update_quantity(self, new_quantity: int) -> None:
        """更新數量（實體可變）"""
        if new_quantity <= 0:
            raise ValueError("數量必須大於 0")
        self.quantity = new_quantity

    def __eq__(self, other: object) -> bool:
        """實體相等性：基於 ID"""
        if not isinstance(other, OrderItem):
            return False
        return self.item_id == other.item_id

    def __hash__(self) -> int:
        """基於 ID 的哈希"""
        return hash(self.item_id)


# ============================================================================
# Aggregate Root (聚合根)
# ============================================================================

@dataclass
class Order:
    """
    訂單聚合根

    職責：
    - 維護訂單生命週期
    - 保護業務不變式
    - 發布領域事件
    - 控制聚合邊界

    不變式（Invariants）：
    - 訂單至少包含一個訂單項
    - 訂單總金額必須 > 0
    - 訂單狀態變更必須遵循狀態機規則
    """
    order_id: OrderId
    customer_id: str
    items: List[OrderItem]
    shipping_address: Address
    status: OrderStatus
    created_at: datetime
    updated_at: datetime

    # 領域事件列表
    _domain_events: List[DomainEvent] = field(default_factory=list, init=False, repr=False)

    # 可選字段
    payment_id: Optional[str] = None
    tracking_number: Optional[str] = None
    carrier: Optional[str] = None
    paid_at: Optional[datetime] = None
    shipped_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None

    def __post_init__(self):
        """驗證聚合不變式"""
        self._validate_invariants()

    def _validate_invariants(self) -> None:
        """驗證業務不變式"""
        if not self.items:
            raise ValueError("訂單至少需要一個訂單項")

        if self.total_amount.amount <= 0:
            raise ValueError("訂單總金額必須大於 0")

        # Validate all items have same currency
        currencies = {item.unit_price.currency for item in self.items}
        if len(currencies) > 1:
            raise ValueError("訂單內所有商品必須使用相同幣種")

    @classmethod
    def create(cls, customer_id: str, items: List[OrderItem],
               shipping_address: Address) -> 'Order':
        """
        工廠方法：創建新訂單

        這是訂單的唯一創建入口，確保：
        - 生成唯一訂單ID
        - 初始化狀態為 PENDING
        - 發布 OrderCreated 事件
        """
        now = datetime.now()
        order = cls(
            order_id=OrderId.generate(),
            customer_id=customer_id,
            items=items,
            shipping_address=shipping_address,
            status=OrderStatus.PENDING,
            created_at=now,
            updated_at=now
        )

        # Publish domain event
        order._add_domain_event(OrderCreated(
            order_id=str(order.order_id),
            customer_id=customer_id,
            total_amount=order.total_amount.amount,
            items_count=len(items)
        ))

        return order

    @property
    def total_amount(self) -> Money:
        """
        計算訂單總金額

        注意：這裡簡化了計算邏輯，實際應用中可能需要：
        - 應用折扣
        - 計算運費
        - 應用優惠券
        - 這些複雜計算可以委託給 OrderPricingService（領域服務）
        """
        if not self.items:
            return Money(Decimal('0'), Currency.TWD)

        total = self.items[0].unit_price.multiply(Decimal('0'))  # Start with zero
        for item in self.items:
            total = total.add(item.subtotal)

        return total

    # ========================================================================
    # 命令方法（Command Methods）
    # ========================================================================

    def pay(self, payment_id: str) -> None:
        """
        支付訂單

        前置條件：
        - 訂單狀態必須是 PENDING

        後置條件：
        - 訂單狀態變更為 PAID
        - 記錄支付信息
        - 發布 OrderPaid 事件
        """
        # Check preconditions
        if self.status != OrderStatus.PENDING:
            raise ValueError(f"只有待支付訂單可以支付，當前狀態: {self.status.value}")

        # Update state
        self.status = OrderStatus.PAID
        self.payment_id = payment_id
        self.paid_at = datetime.now()
        self.updated_at = datetime.now()

        # Publish event
        self._add_domain_event(OrderPaid(
            order_id=str(self.order_id),
            payment_id=payment_id,
            paid_amount=self.total_amount.amount
        ))

    def cancel(self, reason: str, cancelled_by: str) -> None:
        """
        取消訂單

        前置條件：
        - 訂單狀態必須是 PENDING 或 PAID
        - 如果已支付，必須尚未發貨

        後置條件：
        - 訂單狀態變更為 CANCELLED
        - 發布 OrderCancelled 事件
        """
        # Check preconditions
        if self.status not in [OrderStatus.PENDING, OrderStatus.PAID]:
            raise ValueError(f"訂單狀態 {self.status.value} 無法取消")

        if self.status == OrderStatus.PAID and self.shipped_at is not None:
            raise ValueError("已發貨訂單無法取消，請申請退貨")

        # Update state
        self.status = OrderStatus.CANCELLED
        self.updated_at = datetime.now()

        # Publish event
        self._add_domain_event(OrderCancelled(
            order_id=str(self.order_id),
            cancellation_reason=reason,
            cancelled_by=cancelled_by
        ))

    def ship(self, tracking_number: str, carrier: str) -> None:
        """
        發貨訂單

        前置條件：
        - 訂單狀態必須是 PAID

        後置條件：
        - 訂單狀態變更為 SHIPPED
        - 記錄物流信息
        - 發布 OrderShipped 事件
        """
        # Check preconditions
        if self.status != OrderStatus.PAID:
            raise ValueError(f"只有已支付訂單可以發貨，當前狀態: {self.status.value}")

        # Update state
        self.status = OrderStatus.SHIPPED
        self.tracking_number = tracking_number
        self.carrier = carrier
        self.shipped_at = datetime.now()
        self.updated_at = datetime.now()

        # Publish event
        self._add_domain_event(OrderShipped(
            order_id=str(self.order_id),
            tracking_number=tracking_number,
            carrier=carrier
        ))

    def mark_as_delivered(self) -> None:
        """
        標記為已送達（通常由物流系統回調）

        前置條件：
        - 訂單狀態必須是 SHIPPED

        後置條件：
        - 訂單狀態變更為 DELIVERED
        """
        if self.status != OrderStatus.SHIPPED:
            raise ValueError(f"只有已發貨訂單可以標記送達，當前狀態: {self.status.value}")

        self.status = OrderStatus.DELIVERED
        self.updated_at = datetime.now()

    def complete(self) -> None:
        """
        完成訂單（客戶確認收貨或自動確認）

        前置條件：
        - 訂單狀態必須是 DELIVERED

        後置條件：
        - 訂單狀態變更為 COMPLETED
        - 發布 OrderCompleted 事件
        """
        if self.status != OrderStatus.DELIVERED:
            raise ValueError(f"只有已送達訂單可以完成，當前狀態: {self.status.value}")

        self.status = OrderStatus.COMPLETED
        self.completed_at = datetime.now()
        self.updated_at = datetime.now()

        # Publish event
        self._add_domain_event(OrderCompleted(
            order_id=str(self.order_id)
        ))

    # ========================================================================
    # 查詢方法（Query Methods）
    # ========================================================================

    def can_be_cancelled(self) -> bool:
        """檢查訂單是否可以取消"""
        return self.status in [OrderStatus.PENDING, OrderStatus.PAID] and \
               self.shipped_at is None

    def can_be_paid(self) -> bool:
        """檢查訂單是否可以支付"""
        return self.status == OrderStatus.PENDING

    def is_final_state(self) -> bool:
        """檢查訂單是否處於終態"""
        return self.status in [OrderStatus.COMPLETED, OrderStatus.CANCELLED, OrderStatus.REFUNDED]

    # ========================================================================
    # 領域事件管理
    # ========================================================================

    def _add_domain_event(self, event: DomainEvent) -> None:
        """添加領域事件"""
        self._domain_events.append(event)

    def get_domain_events(self) -> List[DomainEvent]:
        """獲取所有領域事件"""
        return self._domain_events.copy()

    def clear_domain_events(self) -> None:
        """清除領域事件（通常在事件發布後調用）"""
        self._domain_events.clear()


# ============================================================================
# Domain Services (領域服務)
# ============================================================================

class OrderValidationService:
    """
    訂單驗證領域服務

    為什麼需要領域服務：
    - 驗證邏輯涉及多個聚合或外部上下文
    - 不屬於任何單一聚合的職責
    """

    @staticmethod
    def validate_order_creation(customer_id: str, items: List[OrderItem],
                               address: Address) -> None:
        """
        驗證訂單創建

        實際應用中，這裡會：
        - 調用庫存上下文檢查庫存
        - 調用商品上下文驗證商品狀態
        - 調用用戶上下文驗證用戶資格
        """
        if not customer_id:
            raise ValueError("客戶 ID 不能為空")

        if not items:
            raise ValueError("訂單至少需要一個商品")

        # Simplified validation
        for item in items:
            if item.quantity > 999:
                raise ValueError(f"商品 {item.product_name} 數量超過限制 (最多 999)")


class OrderPricingService:
    """
    訂單定價領域服務

    職責：
    - 計算訂單總金額（含折扣、運費等複雜邏輯）
    - 應用促銷活動
    - 應用優惠券
    """

    @staticmethod
    def calculate_total(items: List[OrderItem],
                       discount_rate: Decimal = Decimal('0')) -> Money:
        """
        計算訂單總金額

        實際應用中，這裡會：
        - 調用促銷上下文獲取折扣
        - 計算運費
        - 應用優惠券
        """
        if not items:
            return Money(Decimal('0'), Currency.TWD)

        # Calculate items total
        total = items[0].unit_price.multiply(Decimal('0'))
        for item in items:
            total = total.add(item.subtotal)

        # Apply discount
        if discount_rate > 0:
            discount_amount = total.multiply(discount_rate)
            total = total.subtract(discount_amount)

        return total


# ============================================================================
# 使用範例（Example Usage）
# ============================================================================

if __name__ == "__main__":
    print("=== 訂單系統領域模型範例 ===\n")

    # 1. 創建訂單項
    print("1. 創建訂單項")
    item1 = OrderItem(
        item_id=uuid4(),
        product_id="PROD-001",
        product_name="iPhone 15 Pro",
        quantity=1,
        unit_price=Money(Decimal('35900'), Currency.TWD)
    )

    item2 = OrderItem(
        item_id=uuid4(),
        product_id="PROD-002",
        product_name="AirPods Pro",
        quantity=2,
        unit_price=Money(Decimal('7490'), Currency.TWD)
    )

    print(f"   - {item1.product_name} x {item1.quantity} = {item1.subtotal}")
    print(f"   - {item2.product_name} x {item2.quantity} = {item2.subtotal}\n")

    # 2. 創建配送地址
    print("2. 創建配送地址")
    address = Address(
        country="台灣",
        province="台北市",
        city="信義區",
        district="",
        street="信義路五段7號",
        postal_code="110",
        recipient_name="張三",
        recipient_phone="0912-345-678"
    )
    print(f"   {address}\n")

    # 3. 創建訂單
    print("3. 創建訂單")
    order = Order.create(
        customer_id="CUST-12345",
        items=[item1, item2],
        shipping_address=address
    )
    print(f"   訂單編號: {order.order_id}")
    print(f"   訂單狀態: {order.status.value}")
    print(f"   訂單總金額: {order.total_amount}")
    print(f"   領域事件: {order.get_domain_events()[0].__class__.__name__}\n")

    # 4. 支付訂單
    print("4. 支付訂單")
    order.pay(payment_id="PAY-67890")
    print(f"   訂單狀態: {order.status.value}")
    print(f"   支付ID: {order.payment_id}")
    print(f"   領域事件: {order.get_domain_events()[-1].__class__.__name__}\n")

    # 5. 發貨訂單
    print("5. 發貨訂單")
    order.ship(tracking_number="SF1234567890", carrier="順豐速運")
    print(f"   訂單狀態: {order.status.value}")
    print(f"   物流追蹤號: {order.tracking_number}")
    print(f"   領域事件: {order.get_domain_events()[-1].__class__.__name__}\n")

    # 6. 標記送達
    print("6. 標記送達")
    order.mark_as_delivered()
    print(f"   訂單狀態: {order.status.value}\n")

    # 7. 完成訂單
    print("7. 完成訂單")
    order.complete()
    print(f"   訂單狀態: {order.status.value}")
    print(f"   領域事件: {order.get_domain_events()[-1].__class__.__name__}\n")

    # 8. 顯示所有領域事件
    print("8. 所有領域事件:")
    for i, event in enumerate(order.get_domain_events(), 1):
        print(f"   {i}. {event.__class__.__name__} at {event.occurred_at}")

    print("\n=== 範例完成 ===")
