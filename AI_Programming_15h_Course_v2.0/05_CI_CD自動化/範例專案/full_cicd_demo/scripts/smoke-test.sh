#!/bin/bash
#
# 煙霧測試腳本
#
# 用途：執行部署後的快速驗證測試
# 使用：./smoke-test.sh [URL]

set -e

# 配置
API_URL="${1:-http://localhost:8000}"
TIMEOUT=30

echo "🧪 Running smoke tests against: $API_URL"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Test 1: 根路由
echo ""
echo "Test 1: Root endpoint"
response=$(curl -s -o /dev/null -w "%{http_code}" --max-time $TIMEOUT "$API_URL/")
if [ "$response" = "200" ]; then
    echo "✅ Root endpoint OK (HTTP $response)"
else
    echo "❌ Root endpoint FAILED (HTTP $response)"
    exit 1
fi

# Test 2: 健康檢查
echo ""
echo "Test 2: Health check endpoint"
response=$(curl -s -o /dev/null -w "%{http_code}" --max-time $TIMEOUT "$API_URL/health")
if [ "$response" = "200" ]; then
    echo "✅ Health check OK (HTTP $response)"
else
    echo "❌ Health check FAILED (HTTP $response)"
    exit 1
fi

# Test 3: API 端點
echo ""
echo "Test 3: API endpoints"
response=$(curl -s "$API_URL/api/items")
if echo "$response" | jq -e '.[0].id' > /dev/null 2>&1; then
    echo "✅ API endpoint returns valid data"
else
    echo "❌ API endpoint FAILED - invalid response"
    exit 1
fi

# Test 4: 回應時間
echo ""
echo "Test 4: Response time"
time_total=$(curl -o /dev/null -s -w '%{time_total}\n' "$API_URL/")
if (( $(echo "$time_total < 2.0" | bc -l) )); then
    echo "✅ Response time OK: ${time_total}s (< 2s)"
else
    echo "⚠️  Response time SLOW: ${time_total}s (> 2s)"
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🎉 All smoke tests passed!"
