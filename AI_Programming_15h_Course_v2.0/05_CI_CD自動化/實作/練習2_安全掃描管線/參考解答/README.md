# 參考解答：練習 2 - 安全掃描自動化

## 📋 說明

這是練習 2 的參考解答，展示如何建立多層次安全掃描管線並修復常見漏洞。

**重要提示**：
- ⚠️ 務必先自己分析和修復漏洞，再參考本解答
- ⚠️ 理解每個漏洞的原理和修復方法，不要盲目複製
- ⚠️ 安全問題沒有「萬能解法」，需要根據情境調整

---

## 📂 專案結構

```
參考解答/
├── README.md（本文件）
├── vulnerable_app/           # 有漏洞的原始代碼
│   └── app/
│       ├── main.py          # 包含 SQL 注入、XSS
│       ├── database.py      # 不安全的資料庫操作
│       └── auth.py          # 硬編碼密鑰
├── fixed_app/               # 修復後的安全代碼
│   └── app/
│       ├── main.py          # 修復後
│       ├── database.py      # 修復後
│       └── auth.py          # 修復後
├── .github/workflows/
│   └── security.yml         # 完整安全掃描 workflow
└── 漏洞修復報告.md           # 詳細修復說明
```

---

## 🚨 發現的漏洞總覽

### Layer 1: 靜態代碼分析（CodeQL）

| 漏洞類型 | 位置 | 嚴重性 | 狀態 |
|---------|------|--------|------|
| SQL 注入 | database.py:15 | Critical | ✅ 已修復 |
| SQL 注入 | database.py:28 | Critical | ✅ 已修復 |
| XSS | main.py:45 | High | ✅ 已修復 |
| 不安全反序列化 | main.py:67 | High | ✅ 已修復 |

### Layer 2: 依賴漏洞掃描（Snyk）

| 依賴套件 | 版本 | CVE | 嚴重性 | 修復版本 |
|---------|------|-----|--------|---------|
| requests | 2.25.0 | CVE-2021-33503 | High | 2.31.0 |
| pillow | 8.0.0 | CVE-2021-23437 | Critical | 10.0.0 |
| urllib3 | 1.26.4 | CVE-2021-33503 | Medium | 1.26.18 |

### Layer 3: 密鑰掃描（Gitleaks）

| 密鑰類型 | 位置 | 狀態 |
|---------|------|------|
| API Key | auth.py:10 | ✅ 已移除並改用環境變數 |
| Database Password | database.py:5 | ✅ 已移除並改用環境變數 |

---

## 🔧 漏洞修復詳解

### 1. SQL 注入修復

#### ❌ 漏洞代碼（database.py:15）

```python
def get_user_by_id(user_id):
    """不安全：使用字串拼接構建 SQL 查詢"""
    query = f"SELECT * FROM users WHERE id = {user_id}"
    result = db.execute(query)
    return result
```

**問題**：
- 使用 f-string 直接拼接使用者輸入
- 攻擊者可以注入惡意 SQL：`1 OR 1=1--`
- 可能導致資料外洩、刪除、修改

**攻擊範例**：
```python
# 正常使用
get_user_by_id(1)  # SELECT * FROM users WHERE id = 1

# 攻擊
get_user_by_id("1 OR 1=1--")
# 執行: SELECT * FROM users WHERE id = 1 OR 1=1--
# 結果: 返回所有用戶資料！
```

#### ✅ 修復方案

**方法 1：使用參數化查詢（推薦）**

```python
def get_user_by_id(user_id):
    """安全：使用參數化查詢"""
    query = "SELECT * FROM users WHERE id = ?"
    result = db.execute(query, (user_id,))
    return result
```

**方法 2：使用 ORM（最佳）**

```python
from sqlalchemy.orm import Session
from .models import User

def get_user_by_id(db: Session, user_id: int):
    """使用 SQLAlchemy ORM（最安全）"""
    return db.query(User).filter(User.id == user_id).first()
```

**為什麼這樣安全**：
- 參數化查詢將資料與 SQL 分離
- 資料庫驅動會自動轉義特殊字元
- 攻擊字串被當作「資料」而非「SQL 代碼」

---

### 2. XSS 漏洞修復

#### ❌ 漏洞代碼（main.py:45）

```python
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

@app.get("/greet/{name}", response_class=HTMLResponse)
async def greet(name: str):
    """不安全：直接將用戶輸入插入 HTML"""
    return f"<h1>Hello {name}!</h1>"
```

**問題**：
- 使用者輸入直接插入 HTML
- 攻擊者可以注入 JavaScript 代碼

**攻擊範例**：
```bash
# 正常使用
curl http://localhost:8000/greet/Alice
# 返回: <h1>Hello Alice!</h1>

# XSS 攻擊
curl "http://localhost:8000/greet/<script>alert('XSS')</script>"
# 返回: <h1>Hello <script>alert('XSS')</script>!</h1>
# 瀏覽器會執行這段 JavaScript！
```

#### ✅ 修復方案

**方法 1：使用 HTML 轉義**

```python
from html import escape
from fastapi.responses import HTMLResponse

@app.get("/greet/{name}", response_class=HTMLResponse)
async def greet(name: str):
    """安全：轉義用戶輸入"""
    safe_name = escape(name)
    return f"<h1>Hello {safe_name}!</h1>"
```

**方法 2：使用模板引擎（推薦）**

```python
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")

@app.get("/greet/{name}")
async def greet(request: Request, name: str):
    """使用 Jinja2（自動轉義）"""
    return templates.TemplateResponse("greet.html", {
        "request": request,
        "name": name  # Jinja2 會自動轉義
    })
```

**為什麼這樣安全**：
- `escape()` 將 `<` `>` 等轉換為 HTML 實體（`&lt;` `&gt;`）
- Jinja2 預設啟用 auto-escaping
- 攻擊代碼被顯示為文字而非執行

---

### 3. 依賴漏洞修復

#### ❌ 有漏洞的 requirements.txt

```txt
fastapi==0.95.0
uvicorn==0.21.0
requests==2.25.0      # ❌ CVE-2021-33503 (High)
pillow==8.0.0         # ❌ CVE-2021-23437 (Critical)
urllib3==1.26.4       # ❌ CVE-2021-33503 (Medium)
pytest==7.2.0
```

#### ✅ 修復後的 requirements.txt

```txt
fastapi==0.109.0      # ✅ 更新到最新穩定版
uvicorn==0.27.0       # ✅ 更新
requests==2.31.0      # ✅ 修復 CVE-2021-33503
pillow==10.2.0        # ✅ 修復 CVE-2021-23437
urllib3==1.26.18      # ✅ 修復漏洞
pytest==8.0.0         # ✅ 更新
pytest-cov==4.1.0     # ✅ 新增覆蓋率工具
```

**修復步驟**：
1. 查看 Snyk 報告，確認受影響的套件
2. 檢查每個套件的 changelog，確認無 breaking changes
3. 逐一升級並測試
4. 重新執行安全掃描確認

**注意事項**：
- 不要盲目升級到最新版（可能有破壞性變更）
- 優先修復 Critical 和 High 級別漏洞
- Medium 和 Low 可以計劃修復
- 升級後必須執行完整測試

---

### 4. 密鑰移除與環境變數配置

#### ❌ 硬編碼密鑰（auth.py:10）

```python
# ❌ 嚴重安全問題：硬編碼 API 密鑰
API_KEY = "sk_live_EXAMPLE_DO_NOT_USE_REAL_KEY_HERE_xxxxx"
DATABASE_URL = "postgresql://admin:MyP@ssw0rd@localhost/mydb"

def authenticate(request_key):
    return request_key == API_KEY
```

**問題**：
- 密鑰直接寫在代碼中
- 提交到 Git 後永久留存（即使刪除）
- 任何能看到代碼的人都能取得密鑰

#### ✅ 修復方案

**步驟 1：移除硬編碼密鑰**

```python
import os
from dotenv import load_dotenv

# 載入環境變數
load_dotenv()

# ✅ 從環境變數讀取
API_KEY = os.getenv("API_KEY")
DATABASE_URL = os.getenv("DATABASE_URL")

# 驗證環境變數存在
if not API_KEY:
    raise ValueError("API_KEY environment variable is not set")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is not set")

def authenticate(request_key):
    return request_key == API_KEY
```

**步驟 2：創建 `.env.example`**

```bash
# .env.example（提交到 Git）
API_KEY=your_api_key_here
DATABASE_URL=postgresql://user:password@localhost/dbname
```

**步驟 3：更新 `.gitignore`**

```bash
# .gitignore
.env
*.env
!.env.example
```

**步驟 4：在 GitHub Actions 中使用 Secrets**

```yaml
# .github/workflows/security.yml
- name: Run tests
  env:
    API_KEY: ${{ secrets.API_KEY }}
    DATABASE_URL: ${{ secrets.DATABASE_URL }}
  run: pytest
```

**重要**：
- 如果密鑰已經提交到 Git，必須撤銷該密鑰並重新生成
- 刪除提交記錄也無法徹底移除（需要 git filter-branch 或重寫歷史）

---

## 🔒 安全掃描 Workflow

查看 `.github/workflows/security.yml` 了解完整的三層安全掃描配置。

### 關鍵特性

1. **三層防護**
   - CodeQL：靜態分析（SQL 注入、XSS 等）
   - Snyk：依賴漏洞掃描
   - Gitleaks：密鑰掃描

2. **定時掃描**
   - 每週一凌晨自動執行
   - 持續監控新漏洞

3. **PR 阻止**
   - 發現 High/Critical 漏洞時阻止合併
   - 配合 Branch Protection Rules

4. **報告整合**
   - 上傳到 GitHub Security tab
   - 集中查看所有 alerts

---

## 📊 修復驗證

### 修復前

```bash
# CodeQL: 4 個高危漏洞
# Snyk: 3 個依賴漏洞（1 Critical, 2 High）
# Gitleaks: 2 個密鑰洩漏
# 總計: 9 個安全問題
```

### 修復後

```bash
# ✅ CodeQL: 0 個漏洞
# ✅ Snyk: 0 個高危漏洞
# ✅ Gitleaks: 0 個密鑰
# ✅ 所有測試通過
# ✅ 功能正常運作
```

---

## 💡 學習重點

### 1. 永遠不要信任用戶輸入

```python
# ❌ 錯誤思維
"用戶不會輸入惡意資料"

# ✅ 正確思維
"所有輸入都可能是惡意的，必須驗證和轉義"
```

### 2. 深度防禦（Defense in Depth）

```
Layer 1: 輸入驗證
Layer 2: 參數化查詢/轉義
Layer 3: 最小權限原則
Layer 4: 監控和告警
```

### 3. 安全是持續過程

- 不是「一次修復，永遠安全」
- 需要持續掃描（新漏洞不斷出現）
- 需要定期更新依賴
- 需要團隊安全意識

### 4. AI 輔助，但要驗證

- 用 AI 分析漏洞：✅ 好的
- 盲目複製 AI 修復代碼：❌ 危險
- 理解修復原理並驗證：✅ 必須

---

## 🎯 自我檢查

完成修復後，確認：

- [ ] 所有 SQL 查詢使用參數化查詢或 ORM
- [ ] 所有用戶輸入都經過適當轉義
- [ ] 依賴升級到安全版本
- [ ] 無硬編碼密鑰
- [ ] 環境變數配置正確
- [ ] 所有測試通過
- [ ] 功能無損
- [ ] 安全掃描全部通過

---

## 📚 延伸閱讀

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [GitHub Security Best Practices](https://docs.github.com/en/code-security)
- [FastAPI Security](https://fastapi.tiangolo.com/tutorial/security/)

---

**記住**：在 AI 時代，40% 的代碼包含安全問題。

自動化安全掃描不是選項，而是必須！🔒
