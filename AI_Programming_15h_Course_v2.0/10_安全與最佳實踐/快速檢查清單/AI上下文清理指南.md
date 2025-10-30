# 🧹 AI 上下文清理指南

> **使用時機**: 每次與 AI 工具 (ChatGPT, Claude, Copilot) 共享代碼或資料前
>
> **耗時**: 1-3 分鐘
>
> **目標**: 防止敏感資訊洩漏給 AI 模型

---

## 🎯 核心原則

```
假設你分享給 AI 的所有內容都會:
1. 被記錄在 AI 的上下文中
2. 可能用於改進模型 (公開 AI)
3. 可能被其他用戶看到 (如有漏洞)
```

---

## 🔴 Level 1: 絕對禁止分享

### 憑證與金鑰

**一旦洩漏,立即構成安全威脅**

- [ ] ❌ **密碼**: 任何形式的密碼字串
- [ ] ❌ **API Keys**: OpenAI, AWS, Stripe, etc.
- [ ] ❌ **Tokens**: JWT tokens, OAuth tokens, session tokens
- [ ] ❌ **私鑰**: SSH keys, SSL certificates, GPG keys
- [ ] ❌ **數據庫憑證**: 連接字串包含密碼

**正確做法**:
```python
# ❌ 不要這樣做
api_key = "sk-proj-abc123..."

# ✅ 改為這樣
api_key = os.getenv('OPENAI_API_KEY')
```

---

### 客戶個人資料 (PII)

**法律風險,可能違反 GDPR/CCPA**

- [ ] ❌ **姓名**: 真實的客戶或員工姓名
- [ ] ❌ **聯絡資訊**: Email, 電話, 地址
- [ ] ❌ **身分證件**: 身分證號, 護照號, 駕照號
- [ ] ❌ **金融資訊**: 信用卡號, 銀行帳號
- [ ] ❌ **醫療記錄**: 任何健康相關資料

**正確做法**:
```python
# ❌ 不要這樣做
user_email = "john.doe@gmail.com"
phone = "+1-234-567-8900"

# ✅ 改為使用假名化數據
user_email = "user_12345@example.com"
phone = "+1-555-0100"  # 保留格式但使用測試號碼
```

---

## 🟡 Level 2: 高度機密

### 商業機密

**競爭風險,影響商業價值**

- [ ] ⚠️ **專有演算法**: 核心競爭力的演算法實作
- [ ] ⚠️ **產品規格**: 未發布產品的詳細功能
- [ ] ⚠️ **定價策略**: 價格計算邏輯
- [ ] ⚠️ **客戶名單**: 重要客戶資訊
- [ ] ⚠️ **財務數據**: 營收、成本、利潤數據

**正確做法**:
```python
# ❌ 不要分享完整商業邏輯
def calculate_dynamic_pricing(customer_tier, purchase_history, competitor_prices):
    # [詳細的定價演算法]
    pass

# ✅ 泛化問題描述
"""
我需要設計一個動態定價系統,考慮以下因素:
- 客戶分級 (bronze/silver/gold)
- 購買歷史
- 市場競爭

如何設計一個可擴展的定價引擎?
"""
```

---

### 內部系統資訊

**安全風險,為攻擊者提供情報**

- [ ] ⚠️ **網路架構**: 內部 IP, VPN 配置
- [ ] ⚠️ **伺服器資訊**: 主機名, 部署拓撲
- [ ] ⚠️ **專案路徑**: `/home/user/company-internal/`
- [ ] ⚠️ **員工資訊**: 內部郵箱, 組織架構
- [ ] ⚠️ **安全配置**: 防火牆規則, 存取控制

**正確做法**:
```python
# ❌ 不要洩漏內部架構
# File: /var/www/company-internal/backend/auth/login.py
# Server: prod-db-01.internal.company.com:5432

# ✅ 泛化路徑和主機名
# File: auth/login.py
# Server: database_host (from environment variable)
```

---

## 🔵 Level 3: 內部使用

### 可分享,但需清理

- [ ] 📝 **代碼片段**: 移除業務邏輯細節
- [ ] 📝 **錯誤訊息**: 清除路徑和主機資訊
- [ ] 📝 **配置檔案**: 移除真實值,保留結構
- [ ] 📝 **測試數據**: 使用合成數據

---

## ✅ 清理步驟 (3-Step Process)

### Step 1: 識別敏感資訊 (30 秒)

快速掃描代碼,標記以下模式:

```python
# 搜尋這些關鍵字
password, pwd, passwd
api_key, apikey, api-key
token, auth, secret
email, phone, ssn
private, confidential
```

---

### Step 2: 替換或移除 (1-2 分鐘)

#### 替換憑證

```python
# 原始代碼
DATABASE_URL = "postgresql://admin:P@ssw0rd@10.0.1.50:5432/prod_db"

# 清理後
DATABASE_URL = os.getenv('DATABASE_URL')
# 或
DATABASE_URL = "postgresql://user:password@host:5432/database"  # 泛化
```

#### 假名化 PII

```python
# 原始數據
users = [
    {"name": "John Doe", "email": "john@gmail.com", "age": 35},
    {"name": "Jane Smith", "email": "jane@yahoo.com", "age": 28}
]

# 清理後
users = [
    {"name": "User_001", "email": "user1@example.com", "age": 35},
    {"name": "User_002", "email": "user2@example.com", "age": 28}
]
```

#### 泛化路徑

```python
# 原始路徑
/home/johndoe/company-internal/backend/src/auth/

# 清理後
src/auth/
```

---

### Step 3: 驗證清理結果 (30 秒)

**最終檢查清單**:

- [ ] 沒有任何密碼或 API keys?
- [ ] 沒有真實客戶資料?
- [ ] 沒有內部 IP 或主機名?
- [ ] 專案路徑已泛化?
- [ ] 業務邏輯已簡化?

---

## 🛠️ 實用工具與技巧

### 正則表達式快速替換

```bash
# 移除所有 email 地址
sed 's/[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}/<EMAIL>/g'

# 移除 IP 地址
sed 's/\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b/<IP_ADDRESS>/g'

# 移除 API keys (sk- 開頭)
sed 's/sk-[a-zA-Z0-9]\{20,\}/<API_KEY>/g'
```

---

### VS Code 快捷清理

1. 搜尋替換 (Cmd/Ctrl + H)
2. 啟用正則表達式模式
3. 批量替換敏感模式

---

### Python 自動清理腳本

```python
import re

def sanitize_code(code):
    """清理代碼中的敏感資訊"""
    # 替換 email
    code = re.sub(r'\b[\w.-]+@[\w.-]+\.\w+\b', '<EMAIL>', code)

    # 替換 IP
    code = re.sub(r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b', '<IP>', code)

    # 替換可能的密碼
    code = re.sub(r'(password|pwd|passwd)\s*=\s*["\'][^"\']+["\']',
                  r'\1="<REDACTED>"', code)

    # 替換 API keys
    code = re.sub(r'(api[_-]?key)\s*=\s*["\'][^"\']+["\']',
                  r'\1="<REDACTED>"', code)

    return code

# 使用範例
original = """
password = "MySecret123"
api_key = "sk-proj-abc123..."
email = "john@company.com"
"""

cleaned = sanitize_code(original)
print(cleaned)
```

---

## 📋 不同情境的清理模板

### 情境 1: 請求代碼審查

```markdown
# ❌ 錯誤方式
"幫我審查這段代碼 [貼上 500 行包含業務邏輯的代碼]"

# ✅ 正確方式
"""
我想審查這段認證邏輯的安全性:

```python
def authenticate(username, password):
    # 使用環境變數的憑證連接資料庫
    user = db.query(User).filter(User.username == username).first()

    if user and check_password(password, user.password_hash):
        return generate_token(user)
    return None
```

問題:
1. 密碼驗證邏輯是否安全?
2. 是否需要添加 rate limiting?
3. token 生成方式是否合適?
"""
```

---

### 情境 2: Debug 協助

```markdown
# ❌ 錯誤方式
"這是完整的錯誤日誌 [包含路徑、主機名、token 的完整 stack trace]"

# ✅ 正確方式
"""
我的資料庫查詢失敗,錯誤訊息:

```
psycopg2.OperationalError: could not connect to server
FATAL: password authentication failed for user "app_user"
```

相關代碼:
```python
conn = psycopg2.connect(
    host=os.getenv('DB_HOST'),
    database=os.getenv('DB_NAME'),
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PASSWORD')
)
```

問題: 環境變數都已設置,但連接仍失敗,可能是什麼原因?
"""
```

---

### 情境 3: 數據分析

```markdown
# ❌ 錯誤方式
"分析這個 CSV [包含真實客戶資料]"

# ✅ 正確方式
"""
我需要分析用戶購買模式,數據結構如下:

user_id (匿名),purchase_amount,category,timestamp
U001,299.99,electronics,2024-01-01
U002,89.99,books,2024-01-01
U003,1499.00,electronics,2024-01-02

問題: 如何識別高價值用戶並預測流失?

[使用合成數據或聚合統計,不包含 PII]
"""
```

---

## 🚨 常見錯誤

### 錯誤 1: 註解中的憑證

```python
# ❌ 以為註解掉就安全
# Old API key: sk-proj-old123...
# Production password: P@ssw0rd!2024

# ✅ 完全移除
# Credentials moved to environment variables
```

---

### 錯誤 2: 測試代碼中的真實資料

```python
# ❌ 測試使用真實客戶資料
def test_email_sending():
    send_email("real.customer@gmail.com", "Test subject")

# ✅ 使用測試數據
def test_email_sending():
    send_email("test@example.com", "Test subject")
```

---

### 錯誤 3: Git diff 包含敏感資訊

```bash
# ❌ 直接貼上 git diff
git diff  # 可能包含剛刪除的憑證

# ✅ 描述變更,不貼完整 diff
"""
我修改了認證邏輯:
- 從硬編碼改為環境變數
- 添加了錯誤處理
- 增強了日誌記錄 (不含敏感資訊)

問題: 這樣的修改是否安全?
"""
```

---

## 📚 學習資源

### 自動化工具

- **detect-secrets**: Python 專案憑證掃描
- **git-secrets**: Git commit 憑證防護
- **TruffleHog**: Git 歷史憑證掃描

### 數據假名化工具

- **Faker** (Python): 生成假數據
- **Anonymizer**: 自動假名化工具

---

## 💡 最佳實踐

### 養成習慣

1. **複製前暫停 3 秒**: 快速心理檢查
2. **使用清理腳本**: 自動化常見替換
3. **聚焦問題**: 只分享解決問題所需的最少資訊
4. **使用範例數據**: 準備一組安全的測試數據集

---

### 團隊協作

- **建立共享模板**: 團隊統一的清理模板
- **Code Review**: 互相檢查 AI 互動內容
- **定期培訓**: 每季度更新安全意識

---

## ✅ 快速自檢

**分享給 AI 前,問自己三個問題**:

1. **如果這段內容被公開,會有問題嗎?**
   - 如果答案是「是」,繼續清理

2. **我是否分享了完成任務所需的最少資訊?**
   - 如果答案是「否」,刪減內容

3. **我能在公開論壇發布這段內容嗎?**
   - 如果答案是「否」,不要分享給 AI

---

**記住**:

> **「與 AI 分享上下文 = 在公開論壇發問」**
>
> **「清理上下文多花 2 分鐘,總好過洩漏後補救 2 天」**

---

**版本**: v1.0
**最後更新**: 2024-01-15
**適用範圍**: 所有 AI 輔助開發工具
