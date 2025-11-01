# E02：微服務架構 CI/CD 🔥

## 📋 情境資訊

**難度等級**：⭐⭐⭐ 複雜級
**預估時間**：3-5 小時
**核心技能**：微服務協調、服務網格、分散式追蹤、API Gateway、Event-Driven Architecture
**前置知識**：所有基礎級 + 組合級 C04, C05, C10

---

## 🎯 情境背景

你是一家電商獨角獸公司的平台架構師。公司的單體應用已經成為業務增長的瓶頸,CTO 決定進行微服務改造。

**公司規模**：
- **GMV**：$500M/年（快速增長）
- **訂單量**：100萬單/天（高峰期 10萬單/小時）
- **用戶**：5M+ 註冊用戶
- **團隊**：60 個後端工程師（分成 8 個小組）

**系統架構**（目標）：
```
外部流量
   ↓
┌─────────────────────────┐
│   CDN (CloudFlare)      │
└─────────────────────────┘
   ↓
┌─────────────────────────┐
│   WAF + DDoS Protection │
└─────────────────────────┘
   ↓
┌─────────────────────────┐
│   API Gateway (Kong)    │
│   - Rate Limiting        │
│   - Authentication       │
│   - Request Routing      │
└─────────────────────────┘
   ↓
┌─────────────────────────────────────┐
│   Service Mesh (Istio)              │
│   - Traffic Management               │
│   - Security (mTLS)                  │
│   - Observability                    │
└─────────────────────────────────────┘
   ↓
┌─────────────────────────────────────┐
│   Microservices (10 services)       │
│                                      │
│   1. User Service (Auth/Profile)    │
│   2. Product Service (Catalog)      │
│   3. Inventory Service (Stock)      │
│   4. Cart Service (Shopping Cart)   │
│   5. Order Service (Order Mgmt)     │
│   6. Payment Service (Payments)     │
│   7. Shipping Service (Logistics)   │
│   8. Notification Service (Email/SMS│
│   9. Search Service (Elasticsearch) │
│   10. Analytics Service (Events)    │
│                                      │
└─────────────────────────────────────┘
   ↓
┌─────────────────────────────────────┐
│   Data Layer                         │
│   - PostgreSQL (主資料庫)           │
│   - Redis (快取)                     │
│   - Kafka (事件流)                   │
│   - Elasticsearch (搜尋)            │
│   - S3 (物件儲存)                   │
└─────────────────────────────────────┘
```

**服務依賴圖**：
```
User Service → (基礎服務,無依賴)
Product Service → User Service
Inventory Service → Product Service
Cart Service → User Service, Product Service
Order Service → User Service, Cart Service, Inventory Service, Payment Service
Payment Service → User Service, Order Service
Shipping Service → Order Service, User Service
Notification Service → (訂閱所有服務事件)
Search Service → Product Service, Order Service
Analytics Service → (訂閱所有服務事件)
```

**當前挑戰**：

```bash
挑戰 1：服務間依賴複雜
─────────────────────────
問題：
- Order Service 依賴 5 個其他服務
- 更新順序錯誤導致 API 不相容
- 級聯失敗（一個服務掛掉影響多個）
- 循環依賴風險

實例（上週事故）：
1. Payment Service v2.0 更新 API 格式
2. Order Service 尚未更新（還在使用舊格式）
3. 所有下單失敗
4. 損失：$50,000（2 小時停機）

挑戰 2：測試複雜度爆炸
─────────────────────────
- 單元測試：還可以
- 整合測試：需要啟動 10 個服務
- E2E 測試：環境搭建 30 分鐘
- Contract 測試：未實施

當前測試時間：
- 單元測試：5 分鐘
- 整合測試：25 分鐘
- E2E 測試：45 分鐘
- 總計：75 分鐘（太慢！）

挑戰 3：部署協調困難
─────────────────────────
問題：
- 10 個服務需要按正確順序部署
- 手動協調容易出錯
- 沒有自動化的相容性檢查
- 回退複雜（10 個服務都要回退？）

實例：
需求：添加「優惠券」功能
影響服務：Cart, Order, Payment, Notification, Analytics
部署順序：必須先部署 Cart → Order → Payment → 其他
風險：順序錯誤導致資料不一致

挑戰 4：資料一致性
─────────────────────────
- 分散式事務（Saga pattern）
- 最終一致性
- 事件驅動架構
- 補償機制

實例（數據不一致）：
1. Order Service 建立訂單成功
2. Payment Service 扣款失敗
3. Inventory Service 已扣庫存
4. 結果：庫存錯誤,訂單未支付

挑戰 5：監控與除錯困難
─────────────────────────
- 分散式追蹤（一個請求經過 6 個服務）
- 日誌聚合（10 個服務的日誌）
- 效能瓶頸定位
- 故障定位困難
```

**CTO 的要求**：
> 「我們需要一套完整的微服務 CI/CD 管線,能夠處理服務間的複雜依賴關係,自動化測試,智能部署順序,並確保資料一致性。目標是讓每個團隊能夠**獨立部署**他們的服務,同時不影響其他服務。」

**你的任務**：
設計並實施完整的微服務 CI/CD 管線,包括：
- 服務依賴管理
- Contract 測試
- 智能部署編排
- 分散式追蹤
- 事件驅動架構 CI/CD
- 服務網格整合

---

## 🎬 情境展開

### 階段 1：服務依賴管理（1 小時）

#### 1.1 依賴圖建模

建立服務依賴圖（`tools/dependency-graph.json`）：
```json
{
  "services": {
    "user-service": {
      "dependencies": [],
      "consumers": ["product-service", "cart-service", "order-service"]
    },
    "product-service": {
      "dependencies": ["user-service"],
      "consumers": ["inventory-service", "cart-service", "search-service"]
    },
    "order-service": {
      "dependencies": [
        "user-service",
        "cart-service",
        "inventory-service",
        "payment-service"
      ],
      "consumers": ["shipping-service", "notification-service"]
    }
  }
}
```

#### 1.2 部署順序計算

建立拓撲排序腳本（`scripts/calculate-deploy-order.py`）：
```python
#!/usr/bin/env python3
import json
from collections import defaultdict, deque

def calculate_deployment_order(dependency_graph):
    """使用拓撲排序計算部署順序"""
    in_degree = defaultdict(int)
    graph = defaultdict(list)
    
    # 構建圖
    for service, info in dependency_graph['services'].items():
        for dep in info['dependencies']:
            graph[dep].append(service)
            in_degree[service] += 1
    
    # Kahn's algorithm
    queue = deque([s for s in dependency_graph['services'] 
                   if in_degree[s] == 0])
    order = []
    
    while queue:
        current = queue.popleft()
        order.append(current)
        
        for neighbor in graph[current]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)
    
    if len(order) != len(dependency_graph['services']):
        raise Exception("Circular dependency detected!")
    
    return order

# 使用範例
with open('tools/dependency-graph.json') as f:
    graph = json.load(f)

order = calculate_deployment_order(graph)
print("Deployment Order:")
for i, service in enumerate(order, 1):
    print(f"{i}. {service}")
```

#### 1.3 智能部署 Workflow

`.github/workflows/deploy-microservices.yml`：
```yaml
name: Deploy Microservices

on:
  workflow_dispatch:
    inputs:
      environment:
        required: true
        type: choice
        options: [staging, production]

jobs:
  # Job 1: 計算部署順序
  calculate-order:
    runs-on: ubuntu-latest
    outputs:
      deployment_order: ${{ steps.order.outputs.deployment_order }}
      affected_services: ${{ steps.affected.outputs.affected_services }}

    steps:
      - uses: actions/checkout@v4

      - name: Detect affected services
        id: affected
        run: |
          # 檢測變更的服務
          AFFECTED=$(python scripts/detect-affected-services.py)
          echo "affected_services=$AFFECTED" >> $GITHUB_OUTPUT

      - name: Calculate deployment order
        id: order
        run: |
          ORDER=$(python scripts/calculate-deploy-order.py --affected "$AFFECTED")
          echo "deployment_order=$ORDER" >> $GITHUB_OUTPUT

  # Job 2: 依序部署服務
  deploy-services:
    needs: calculate-order
    runs-on: ubuntu-latest

    strategy:
      matrix:
        service: ${{ fromJson(needs.calculate-order.outputs.deployment_order) }}
      max-parallel: 1  # 按順序部署

    steps:
      - uses: actions/checkout@v4

      - name: Deploy ${{ matrix.service }}
        run: |
          echo "Deploying ${{ matrix.service }}..."
          kubectl set image deployment/${{ matrix.service }} \
            ${{ matrix.service }}=ghcr.io/company/${{ matrix.service }}:${{ github.sha }}

      - name: Wait for rollout
        run: |
          kubectl rollout status deployment/${{ matrix.service }} --timeout=5m

      - name: Health check
        run: |
          # 等待服務健康
          for i in {1..30}; do
            if kubectl exec -n default deploy/${{ matrix.service }} -- \
               wget -q -O- http://localhost:8080/health; then
              echo "✅ ${{ matrix.service }} is healthy"
              break
            fi
            sleep 10
          done

      - name: Smoke test
        run: |
          pytest tests/smoke/${{ matrix.service }}/ \
            --base-url=https://${{ inputs.environment }}.company.com
```

**檢查點 1**：
- [ ] 依賴圖正確建立
- [ ] 部署順序自動計算
- [ ] 按順序部署成功
- [ ] 每個服務部署後驗證

---

### 階段 2：Contract 測試（1 小時）

#### 2.1 Pact Contract 測試

**Provider Contract（Order Service）**：
```javascript
// services/order-service/tests/contract/order.pact.spec.js
const { Verifier } = require('@pact-foundation/pact');
const path = require('path');

describe('Order Service Contract', () => {
  it('validates the expectations of Payment Service', () => {
    return new Verifier({
      providerBaseUrl: 'http://localhost:3000',
      pactUrls: [
        path.resolve(__dirname, '../../../payment-service/pacts/payment-order.json')
      ],
      stateHandlers: {
        'order 12345 exists': async () => {
          // 設置測試資料
          await db.orders.create({ id: 12345, status: 'pending' });
        },
        'order 12345 does not exist': async () => {
          await db.orders.destroy({ where: { id: 12345 } });
        }
      }
    }).verifyProvider();
  });
});
```

**Consumer Contract（Payment Service）**：
```javascript
// services/payment-service/tests/contract/order-api.pact.spec.js
const { PactV3 } = require('@pact-foundation/pact');
const { OrderAPIClient } = require('../../src/clients/order-api');

const provider = new PactV3({
  consumer: 'payment-service',
  provider: 'order-service'
});

describe('Payment Service -> Order Service', () => {
  it('can get order details', async () => {
    await provider
      .given('order 12345 exists')
      .uponReceiving('a request for order 12345')
      .withRequest({
        method: 'GET',
        path: '/api/orders/12345',
        headers: { Accept: 'application/json' }
      })
      .willRespondWith({
        status: 200,
        headers: { 'Content-Type': 'application/json' },
        body: {
          id: 12345,
          userId: 100,
          total: 99.99,
          status: 'pending'
        }
      });

    await provider.executeTest(async (mockServer) => {
      const client = new OrderAPIClient(mockServer.url);
      const order = await client.getOrder(12345);
      
      expect(order.id).toBe(12345);
      expect(order.status).toBe('pending');
    });
  });
});
```

#### 2.2 Contract Testing CI

`.github/workflows/contract-test.yml`：
```yaml
name: Contract Testing

on:
  pull_request:
    branches: [main]

jobs:
  # Job 1: Consumer 測試（生成 contract）
  consumer-tests:
    runs-on: ubuntu-latest

    strategy:
      matrix:
        service:
          - payment-service
          - shipping-service
          - cart-service

    steps:
      - uses: actions/checkout@v4

      - name: Run consumer tests
        working-directory: services/${{ matrix.service }}
        run: npm run test:contract

      - name: Publish contracts to Pact Broker
        run: |
          npm install -g @pact-foundation/pact-node
          pact-broker publish \
            services/${{ matrix.service }}/pacts \
            --consumer-app-version=${{ github.sha }} \
            --broker-base-url=${{ secrets.PACT_BROKER_URL }} \
            --broker-token=${{ secrets.PACT_BROKER_TOKEN }}

  # Job 2: Provider 驗證
  provider-verification:
    needs: consumer-tests
    runs-on: ubuntu-latest

    strategy:
      matrix:
        service:
          - order-service
          - product-service
          - user-service

    steps:
      - uses: actions/checkout@v4

      - name: Start provider service
        working-directory: services/${{ matrix.service }}
        run: |
          npm install
          npm run start &
          sleep 10

      - name: Verify contracts
        working-directory: services/${{ matrix.service }}
        run: npm run test:contract:verify

      - name: Can I deploy?
        run: |
          pact-broker can-i-deploy \
            --pacticipant=${{ matrix.service }} \
            --version=${{ github.sha }} \
            --to-environment=staging \
            --broker-base-url=${{ secrets.PACT_BROKER_URL }} \
            --broker-token=${{ secrets.PACT_BROKER_TOKEN }}
```

**檢查點 2**：
- [ ] Consumer contract 測試通過
- [ ] Provider contract 驗證通過
- [ ] Contract 發布到 Pact Broker
- [ ] 相容性檢查通過

---

### 階段 3：Event-Driven Architecture CI/CD（1 小時）

#### 3.1 事件 Schema 管理

使用 Avro/Protobuf 定義事件 schema（`schemas/events/order-created.avsc`）：
```json
{
  "type": "record",
  "name": "OrderCreated",
  "namespace": "com.company.events",
  "fields": [
    {"name": "orderId", "type": "string"},
    {"name": "userId", "type": "string"},
    {"name": "items", "type": {"type": "array", "items": "string"}},
    {"name": "total", "type": "double"},
    {"name": "timestamp", "type": "long"},
    {"name": "version", "type": "string", "default": "1.0"}
  ]
}
```

#### 3.2 Schema 驗證

`.github/workflows/schema-validation.yml`：
```yaml
name: Event Schema Validation

on:
  pull_request:
    paths:
      - 'schemas/**'

jobs:
  validate-schemas:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Validate Avro schemas
        run: |
          npm install -g avro-tools
          for schema in schemas/events/*.avsc; do
            echo "Validating $schema..."
            avro-tools validate $schema
          done

      - name: Check backward compatibility
        run: |
          python scripts/check-schema-compatibility.py

      - name: Register schemas
        if: github.event_name == 'push'
        run: |
          # 註冊到 Schema Registry
          for schema in schemas/events/*.avsc; do
            curl -X POST \
              -H "Content-Type: application/vnd.schemaregistry.v1+json" \
              --data @$schema \
              ${{ secrets.SCHEMA_REGISTRY_URL }}/subjects/$(basename $schema .avsc)/versions
          done
```

#### 3.3 事件驅動測試

測試事件發布與消費（`tests/events/test-order-created.js`）：
```javascript
const { Kafka } = require('kafkajs');
const { OrderService } = require('../../services/order-service');

describe('Order Created Event', () => {
  let kafka, producer, consumer;

  beforeAll(async () => {
    kafka = new Kafka({
      clientId: 'test-client',
      brokers: ['localhost:9092']
    });

    producer = kafka.producer();
    consumer = kafka.consumer({ groupId: 'test-group' });

    await producer.connect();
    await consumer.connect();
    await consumer.subscribe({ topic: 'order-created' });
  });

  it('publishes OrderCreated event when order is created', async () => {
    const eventReceived = new Promise((resolve) => {
      consumer.run({
        eachMessage: async ({ message }) => {
          const event = JSON.parse(message.value.toString());
          if (event.orderId === '12345') {
            resolve(event);
          }
        }
      });
    });

    // 建立訂單
    const orderService = new OrderService();
    await orderService.createOrder({
      userId: '100',
      items: ['item1', 'item2'],
      total: 99.99
    });

    // 驗證事件
    const event = await eventReceived;
    expect(event.orderId).toBe('12345');
    expect(event.userId).toBe('100');
  }, 10000);

  afterAll(async () => {
    await producer.disconnect();
    await consumer.disconnect();
  });
});
```

**檢查點 3**：
- [ ] Event schema 定義完整
- [ ] Schema 向後相容
- [ ] Event 發布測試通過
- [ ] Event 消費測試通過

---

### 階段 4：服務網格整合（45 分鐘）

#### 4.1 Istio 流量管理

部署 Canary（`k8s/order-service-canary.yaml`）：
```yaml
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: order-service
spec:
  hosts:
  - order-service
  http:
  - match:
    - headers:
        x-canary:
          exact: "true"
    route:
    - destination:
        host: order-service
        subset: canary
      weight: 100
  - route:
    - destination:
        host: order-service
        subset: stable
      weight: 95
    - destination:
        host: order-service
        subset: canary
      weight: 5
---
apiVersion: networking.istio.io/v1beta1
kind: DestinationRule
metadata:
  name: order-service
spec:
  host: order-service
  subsets:
  - name: stable
    labels:
      version: stable
  - name: canary
    labels:
      version: canary
```

#### 4.2 自動化 Canary 分析

`.github/workflows/canary-deployment.yml`：
```yaml
name: Canary Deployment

jobs:
  deploy-canary:
    runs-on: ubuntu-latest

    steps:
      - name: Deploy canary (5% traffic)
        run: |
          kubectl apply -f k8s/${{ matrix.service }}-canary.yaml

      - name: Monitor metrics (10 min)
        run: |
          python scripts/monitor-canary.py \
            --service=${{ matrix.service }} \
            --duration=600 \
            --error-threshold=0.01 \
            --latency-threshold=200

      - name: Promote or rollback
        run: |
          if [ -f canary-success ]; then
            echo "✅ Canary successful. Promoting to 100%"
            kubectl patch vs ${{ matrix.service }} --type=json \
              -p='[{"op": "replace", "path": "/spec/http/0/route/0/weight", "value": 0}]'
            kubectl patch vs ${{ matrix.service }} --type=json \
              -p='[{"op": "replace", "path": "/spec/http/0/route/1/weight", "value": 100}]'
          else
            echo "❌ Canary failed. Rolling back"
            kubectl delete -f k8s/${{ matrix.service }}-canary.yaml
          fi
```

**檢查點 4**：
- [ ] Istio 流量管理配置完成
- [ ] Canary 部署成功
- [ ] 自動監控指標
- [ ] 自動 promote/rollback

---

### 階段 5：分散式追蹤與監控（30 分鐘）

#### 5.1 Jaeger 整合

應用層追蹤（`services/order-service/src/tracing.js`）：
```javascript
const { initTracer } = require('jaeger-client');

const config = {
  serviceName: 'order-service',
  sampler: {
    type: 'const',
    param: 1
  },
  reporter: {
    logSpans: true,
    collectorEndpoint: process.env.JAEGER_ENDPOINT
  }
};

const tracer = initTracer(config);

// 使用範例
async function createOrder(req, res) {
  const span = tracer.startSpan('create_order');
  span.setTag('user_id', req.body.userId);

  try {
    // 1. 驗證庫存
    const inventorySpan = tracer.startSpan('check_inventory', {
      childOf: span
    });
    await inventoryService.checkStock(req.body.items);
    inventorySpan.finish();

    // 2. 處理支付
    const paymentSpan = tracer.startSpan('process_payment', {
      childOf: span
    });
    await paymentService.charge(req.body.total);
    paymentSpan.finish();

    span.setTag('http.status_code', 200);
    span.finish();

    res.json({ orderId: '12345' });
  } catch (error) {
    span.setTag('error', true);
    span.log({ event: 'error', message: error.message });
    span.finish();

    res.status(500).json({ error: error.message });
  }
}
```

**檢查點 5**：
- [ ] Jaeger 追蹤整合
- [ ] 完整請求鏈路可視
- [ ] 效能瓶頸可定位
- [ ] 錯誤追蹤完整

---

## 🎯 最終交付物

完成所有階段後:

### 技術交付物
- [ ] 完整微服務 CI/CD 管線
- [ ] 服務依賴管理系統
- [ ] Contract 測試框架
- [ ] Event-driven 測試體系
- [ ] 服務網格整合
- [ ] 分散式追蹤系統

### 效能指標
- [ ] 部署時間 < 15 分鐘（10 個服務）
- [ ] Contract 測試覆蓋率 100%
- [ ] 部署成功率 > 99%
- [ ] MTTR < 10 分鐘
- [ ] 服務間通訊延遲 < 50ms

### 業務成果
- [ ] 支持獨立部署
- [ ] 零停機部署
- [ ] 自動化依賴管理
- [ ] 完整的可觀測性

---

## 💡 延伸挑戰

### 挑戰 1：Chaos Engineering
- 定期故障注入
- 服務韌性測試
- 自動恢復驗證

### 挑戰 2：Multi-Region Deployment
- 跨區域部署
- 流量智能路由
- 資料同步

### 挑戰 3：Service Mesh Security
- mTLS 自動化
- 零信任網路
- 細粒度授權

---

## 📚 參考資源

- [Microservices Patterns](https://microservices.io/patterns/)
- [Pact Documentation](https://docs.pact.io/)
- [Istio Documentation](https://istio.io/docs/)
- [Jaeger Documentation](https://www.jaegertracing.io/docs/)

---

**恭喜！** 完成這個情境後,你已經掌握了微服務架構的完整 CI/CD 能力！
