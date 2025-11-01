#!/bin/bash
#
# 健康檢查腳本
#
# 用途：檢查應用程式是否正常運行
# 使用：./health-check.sh [URL]

set -e

# 配置
URL="${1:-http://localhost:8000}"
HEALTH_ENDPOINT="/health"
TIMEOUT=30
MAX_RETRIES=10
RETRY_DELAY=5

echo "🏥 Running health check against: $URL$HEALTH_ENDPOINT"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# 帶重試的健康檢查
for i in $(seq 1 $MAX_RETRIES); do
    echo "Attempt $i/$MAX_RETRIES..."

    response_code=$(curl -s -o /dev/null -w "%{http_code}" \
        --max-time $TIMEOUT \
        "$URL$HEALTH_ENDPOINT" || echo "000")

    if [ "$response_code" = "200" ]; then
        echo "✅ Health check passed (HTTP $response_code)"

        # 獲取詳細資訊
        response=$(curl -s "$URL$HEALTH_ENDPOINT")
        echo ""
        echo "Response:"
        echo "$response" | jq '.' 2>/dev/null || echo "$response"

        exit 0
    fi

    echo "⏳ Health check failed (HTTP $response_code), retrying in ${RETRY_DELAY}s..."
    sleep $RETRY_DELAY
done

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "❌ Health check failed after $MAX_RETRIES attempts"
exit 1
