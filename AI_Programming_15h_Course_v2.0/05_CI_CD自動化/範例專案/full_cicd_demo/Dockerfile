# 多階段構建 Dockerfile

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Stage 1: 構建階段
#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
FROM python:3.11-slim as builder

WORKDIR /build

# 安裝構建依賴
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# 複製依賴文件
COPY requirements.txt .

# 安裝 Python 依賴
RUN pip install --user --no-cache-dir -r requirements.txt

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Stage 2: 運行階段
#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
FROM python:3.11-slim

WORKDIR /app

# 創建非 root 用戶
RUN groupadd -r appuser && \
    useradd -r -g appuser appuser

# 從構建階段複製依賴
COPY --from=builder /root/.local /root/.local

# 確保 scripts 在 PATH 中
ENV PATH=/root/.local/bin:$PATH

# 複製應用代碼
COPY --chown=appuser:appuser ./app ./app
COPY --chown=appuser:appuser ./tests ./tests

# 切換到非 root 用戶
USER appuser

# 健康檢查
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')"

# 暴露端口
EXPOSE 8000

# 啟動命令
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
