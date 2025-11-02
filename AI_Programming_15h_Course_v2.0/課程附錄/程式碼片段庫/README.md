# 程式碼片段庫

> 常用代碼片段收集與個人知識管理

---

## 📖 目錄用途

此目錄用於存放**常用的程式碼片段 (Code Snippets)**，幫助學員建立個人的代碼片段庫，提升開發效率。

---

## 🎯 為什麼需要程式碼片段庫？

### 提升效率
- **避免重複造輪子**: 常用的代碼片段可直接複用
- **加速開發**: 減少手動輸入重複性代碼的時間
- **標準化**: 確保團隊使用一致的代碼模式

### 知識管理
- **學習記錄**: 記錄學到的有用技巧和模式
- **快速查找**: 需要時快速找到曾經用過的解決方案
- **持續優化**: 隨著經驗累積，不斷改進片段品質

---

## 📁 推薦的組織結構

```
程式碼片段庫/
├── Python/
│   ├── FastAPI/
│   │   ├── auth_middleware.py
│   │   ├── cors_config.py
│   │   └── db_session.py
│   ├── Django/
│   ├── Data_Processing/
│   └── Testing/
├── JavaScript/
│   ├── React/
│   ├── Node/
│   └── Utils/
├── SQL/
│   ├── PostgreSQL/
│   └── Queries/
├── Docker/
│   ├── Dockerfiles/
│   └── docker-compose/
├── CI_CD/
│   └── GitHub_Actions/
└── Prompts/
    ├── Code_Review/
    └── Debugging/
```

---

## ✨ 片段類型建議

### 1️⃣ 配置片段

**範例: FastAPI CORS 配置**

```python
# fastapi_cors_config.py
"""
FastAPI CORS middleware configuration
Usage: Copy to main.py and customize allowed origins
"""
from fastapi.middleware.cors import CORSMiddleware

def setup_cors(app):
    origins = [
        "http://localhost:3000",
        "http://localhost:5173",
        # Add your frontend URLs here
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
```

### 2️⃣ 工具函數片段

**範例: Python 日期處理**

```python
# date_utils.py
"""
Common date/time utility functions
"""
from datetime import datetime, timezone

def utc_now():
    """Get current UTC datetime"""
    return datetime.now(timezone.utc)

def format_iso(dt):
    """Format datetime to ISO 8601 string"""
    return dt.isoformat()

def parse_iso(dt_str):
    """Parse ISO 8601 string to datetime"""
    return datetime.fromisoformat(dt_str)
```

### 3️⃣ 測試片段

**範例: Pytest fixture**

```python
# pytest_fixtures.py
"""
Common pytest fixtures
"""
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

@pytest.fixture
def db_session():
    """Create test database session"""
    engine = create_engine("sqlite:///:memory:")
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()
```

### 4️⃣ Docker 片段

**範例: Python Dockerfile**

```dockerfile
# Dockerfile.python
# Multi-stage build for Python application

# Build stage
FROM python:3.11-slim as builder
WORKDIR /app
RUN pip install poetry
COPY pyproject.toml poetry.lock ./
RUN poetry export -f requirements.txt --output requirements.txt

# Runtime stage
FROM python:3.11-slim
WORKDIR /app
COPY --from=builder /app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 5️⃣ AI 提示詞片段

**範例: 代碼審查提示詞**

```markdown
# code_review_prompt.md

請審查以下代碼，關注：

1. **安全性問題**
   - SQL 注入
   - XSS 漏洞
   - 敏感資料處理

2. **效能問題**
   - N+1 查詢
   - 記憶體洩漏
   - 不必要的迴圈

3. **可維護性**
   - 代碼重複
   - 函數長度
   - 命名清晰度

4. **最佳實踐**
   - 錯誤處理
   - 日誌記錄
   - 測試覆蓋

請提供具體建議和改進範例。

代碼：
[PASTE CODE HERE]
```

---

## 🛠️ 管理片段的工具

### VS Code Snippets

**建立自訂片段**:

1. `Ctrl+Shift+P` → `Preferences: Configure User Snippets`
2. 選擇語言（如 `python.json`）
3. 添加片段定義

**範例: Python FastAPI route**

```json
{
  "FastAPI Route": {
    "prefix": "faroute",
    "body": [
      "@router.${1|get,post,put,delete|}('/${2:path}')",
      "async def ${3:function_name}(",
      "    ${4:param}: ${5:type},",
      "    db: Session = Depends(get_db)",
      "):",
      "    \"\"\"${6:Description}\"\"\"",
      "    ${0:# Implementation}",
      "    return {}"
    ],
    "description": "FastAPI route template"
  }
}
```

### GitHub Gist

**使用 Gist 同步片段**:

```bash
# 安裝 gist CLI
npm install -g gist-cli

# 建立新 gist
gist create my_snippet.py

# 更新 gist
gist update GIST_ID my_snippet.py

# 下載 gist
gist get GIST_ID
```

### SnippetsLab (macOS)

- 商業軟體，優秀的片段管理工具
- 支援多種語言語法高亮
- iCloud 同步

### massCode (跨平台)

- 開源免費
- 支援資料夾組織
- Markdown 預覽
- [GitHub](https://github.com/massCodeIO/massCode)

---

## 📝 片段編寫最佳實踐

### 1. 添加清晰的註解

```python
# ✅ 好的片段
"""
JWT token validation middleware for FastAPI

Prerequisites:
- pip install pyjwt
- Set JWT_SECRET_KEY in environment

Usage:
    app = FastAPI()
    app.add_middleware(JWTAuthMiddleware)
"""
```

### 2. 包含使用範例

```python
# Example usage:
# from auth_middleware import require_auth
#
# @app.get("/protected")
# @require_auth
# async def protected_route(user: User = Depends(get_current_user)):
#     return {"message": f"Hello {user.username}"}
```

### 3. 提供變數說明

```python
def send_email(
    to: str,          # Recipient email address
    subject: str,     # Email subject line
    body: str,        # Email body (HTML supported)
    from_email: str = None  # Optional sender (uses default if None)
):
    pass
```

### 4. 標註版本與日期

```python
"""
Created: 2024-01-15
Last updated: 2024-02-20
Tested with: Python 3.11, FastAPI 0.104
Author: [Your Name]
"""
```

---

## 🎯 建議收集的片段類型

### 後端開發
- [ ] 數據庫連線設定
- [ ] JWT 認證中間件
- [ ] CORS 配置
- [ ] 錯誤處理裝飾器
- [ ] 日誌配置
- [ ] 分頁查詢工具

### 前端開發
- [ ] API 請求封裝
- [ ] 表單驗證邏輯
- [ ] 通用 Hooks
- [ ] 狀態管理模板
- [ ] 路由守衛

### DevOps
- [ ] Dockerfile 模板
- [ ] docker-compose 配置
- [ ] CI/CD workflow
- [ ] Nginx 配置
- [ ] 環境變數模板

### 測試
- [ ] Pytest fixtures
- [ ] Mock 資料生成
- [ ] 測試資料庫設定
- [ ] API 測試模板

### AI 協作
- [ ] 代碼審查提示詞
- [ ] 測試生成提示詞
- [ ] 重構建議提示詞
- [ ] 文檔生成提示詞

---

## 💡 使用技巧

### 技巧 1: 情境式命名

```
❌ 不好的命名: utils.py, helper.py
✅ 好的命名: jwt_token_validator.py, user_password_hasher.py
```

### 技巧 2: 版本控制片段庫

```bash
# 初始化 git
cd 程式碼片段庫/
git init
git remote add origin <your-repo-url>

# 定期提交更新
git add .
git commit -m "Add FastAPI middleware snippets"
git push
```

### 技巧 3: 建立 README 索引

在每個分類目錄下建立 `README.md`：

```markdown
# FastAPI Snippets

## Authentication
- `jwt_middleware.py` - JWT token validation
- `api_key_auth.py` - API key authentication

## Database
- `db_session.py` - SQLAlchemy session management
- `pagination.py` - Query pagination helper
```

### 技巧 4: 使用標籤系統

在檔案開頭添加標籤註解：

```python
"""
Tags: #authentication #security #fastapi
Dependencies: pyjwt, passlib
Complexity: Medium
Last tested: 2024-02-20
"""
```

---

## 🔗 參考資源

### 公開片段庫
- [30 seconds of code](https://www.30secondsofcode.org/)
- [Python Code Snippets](https://github.com/topics/python-snippets)
- [FastAPI Best Practices](https://github.com/zhanymkanov/fastapi-best-practices)

### 片段管理工具
- [VS Code Snippets](https://code.visualstudio.com/docs/editor/userdefinedsnippets)
- [massCode](https://masscode.io/)
- [SnippetsLab](https://www.renfei.org/snippets-lab/)
- [GitHub Gist](https://gist.github.com/)

---

## 🚀 開始建立你的片段庫

1. **本週目標**: 收集 10 個常用片段
2. **每日習慣**: 將用過 2 次以上的代碼片段記錄下來
3. **定期整理**: 每月審查並優化片段
4. **持續學習**: 從優秀開源專案中學習新模式

---

**建立屬於你自己的程式碼片段庫，讓開發更高效！** 🎯
