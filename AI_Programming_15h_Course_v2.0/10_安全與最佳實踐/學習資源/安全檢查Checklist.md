# 安全檢查 Checklist

> **使用場景**: 每次接受 AI 生成的代碼前、每次 commit 前、每次 code review 時使用

---

## 📋 代碼審查前必問的 5 個問題

### 1️⃣ 是否有硬編碼的憑證？

```python
# ❌ 危險信號
password = "admin123"
api_key = "sk-proj-..."
db_url = "postgresql://user:pass@localhost"
SECRET_KEY = "my-secret-key"

# ✅ 安全做法
password = os.getenv('DB_PASSWORD')
api_key = os.getenv('API_KEY')
db_url = os.getenv('DATABASE_URL')
SECRET_KEY = os.getenv('SECRET_KEY')
```

**快速檢查**:
```bash
grep -rn "password\s*=\s*[\"']" --include="*.py" .
grep -rn "api_key\s*=\s*[\"']" --include="*.py" .
grep -rn "secret\s*=\s*[\"']" --include="*.py" .
```

---

### 2️⃣ 是否有 SQL 注入風險？

```python
# ❌ 危險信號
query = f"SELECT * FROM users WHERE name = '{user_input}'"
query = "SELECT * FROM users WHERE id = " + str(user_id)
query = "SELECT * FROM users WHERE email = {}".format(email)

# ✅ 安全做法
query = "SELECT * FROM users WHERE name = ?"
cursor.execute(query, (user_input,))
```

**快速檢查**:
```bash
grep -rn "execute(f\"" --include="*.py" .
grep -rn "execute(\".*\" \+" --include="*.py" .
```

---

### 3️⃣ 是否有路徑遍歷風險？

```python
# ❌ 危險信號
file_path = f"/uploads/{user_filename}"
with open(user_input, 'r') as f:
    content = f.read()

# ✅ 安全做法
from pathlib import Path
UPLOAD_DIR = Path("/uploads").resolve()
file_path = (UPLOAD_DIR / user_filename).resolve()
file_path.relative_to(UPLOAD_DIR)  # 驗證在允許範圍內
```

**快速檢查**:
```bash
grep -rn "open(.*request\." --include="*.py" .
grep -rn "send_file(f\"" --include="*.py" .
```

---

### 4️⃣ 是否使用不安全的反序列化？

```python
# ❌ 危險信號
import pickle
data = pickle.loads(user_input)

import yaml
config = yaml.load(user_input)  # 沒有使用 safe_load

# ✅ 安全做法
import json
data = json.loads(user_input)

import yaml
config = yaml.safe_load(user_input)
```

**快速檢查**:
```bash
grep -rn "pickle.loads" --include="*.py" .
grep -rn "yaml.load" --include="*.py" | grep -v "safe_load"
grep -rn "eval(" --include="*.py" .
grep -rn "exec(" --include="*.py" .
```

---

### 5️⃣ 是否有過度權限？

```bash
# ❌ 危險信號
chmod 777 config.json
sudo python app.py
docker run --privileged myapp

# ✅ 安全做法
chmod 600 config.json  # 只有擁有者可讀寫
python app.py  # 不使用 sudo
docker run --user 1000:1000 --cap-drop=ALL myapp
```

**快速檢查**:
```bash
grep -rn "chmod 777" --include="*.sh" --include="Dockerfile" .
grep -rn "sudo " --include="*.sh" .
grep -rn "--privileged" --include="Dockerfile" --include="docker-compose.yml" .
```

---

## ⚡ Commit 前安全自檢流程 (30 秒)

```bash
# 1. 搜尋憑證 (5 秒)
git diff | grep -E "(password|api_key|secret|token)" --color

# 2. 自動掃描 (10 秒)
git secrets --scan  # 或使用 detect-secrets

# 3. 靜態分析 (15 秒)
semgrep --config auto --diff
# 或
bandit -r . -ll  # 只顯示中高風險
```

**整合到 Git Workflow**:
```bash
# 設置 pre-commit hook
cat > .git/hooks/pre-commit <<'EOF'
#!/bin/bash
# 安全檢查
git secrets --scan || exit 1
detect-secrets-hook --baseline .secrets.baseline || exit 1
EOF

chmod +x .git/hooks/pre-commit
```

---

## 🔍 常見漏洞模式速查表

| 漏洞類型 | 危險模式 | 安全替代 | 檢測工具 |
|----------|----------|----------|----------|
| **硬編碼憑證** | `password = "..."` | `os.getenv('PASSWORD')` | git-secrets |
| **SQL 注入** | `f"SELECT ... {var}"` | `execute("SELECT ... ?", (var,))` | Semgrep |
| **路徑遍歷** | `open(user_input)` | `Path(ALLOWED_DIR / user_input).resolve()` | Semgrep |
| **XSS** | `render_template_string(user_input)` | `escape(user_input)` | Bandit |
| **命令注入** | `os.system(user_input)` | `subprocess.run([cmd, arg])` | Bandit |
| **不安全反序列化** | `pickle.loads(data)` | `json.loads(data)` | Bandit |
| **弱加密** | `md5(password)` | `bcrypt.hashpw(password)` | Bandit |
| **過度權限** | `chmod 777` | `chmod 600` | Manual |

---

## 🎯 分級檢查策略

### Level 1: 快速掃描 (30 秒)

適用於日常 commit

```bash
# 只掃描 staged files
git diff --staged | grep -E "(password|api_key|secret|token)"
git secrets --scan
```

---

### Level 2: 標準檢查 (5 分鐘)

適用於 pull request 前

```bash
# 完整掃描
pre-commit run --all-files
semgrep --config "p/owasp-top-ten" .
bandit -r . -ll
```

---

### Level 3: 深度審計 (30 分鐘)

適用於發布前、定期審計

```bash
# 全面掃描
semgrep --config auto .
bandit -r . -f json -o security_report.json
trufflehog git file://. --only-verified
npm audit  # 如果有 Node.js 依賴
pip-audit  # 掃描 Python 套件漏洞

# 檢查依賴套件
safety check  # Python
snyk test  # 多語言
```

---

## 📝 審查紀錄模板

```markdown
## 安全審查記錄

**審查日期**: 2025-11-02
**審查者**: [Your Name]
**範圍**: [具體範圍，如 "新增的 API 模組"]

### 檢查結果

#### 1. 硬編碼憑證檢查
- [ ] 無硬編碼憑證
- [ ] 所有憑證使用環境變數

#### 2. SQL 注入檢查
- [ ] 所有 SQL 查詢使用參數化
- [ ] 或使用 ORM (SQLAlchemy)

#### 3. 路徑遍歷檢查
- [ ] 所有文件操作驗證路徑
- [ ] 使用 pathlib.resolve() + relative_to()

#### 4. 反序列化檢查
- [ ] 無 pickle.loads() 用於不可信數據
- [ ] 使用 JSON 或 Pydantic

#### 5. 權限檢查
- [ ] 配置檔案權限 600
- [ ] 應用不使用 root 運行

### 發現的問題

- [問題描述]
- [嚴重程度: 高/中/低]
- [修復建議]

### 自動化工具結果

- git-secrets: ✅ 通過
- detect-secrets: ✅ 通過
- Semgrep: ⚠️ 發現 2 個警告
- Bandit: ✅ 通過

### 下一步行動

- [ ] 修復發現的中高風險問題
- [ ] 更新 .semgrep.yml 規則
- [ ] 團隊分享審查結果
```

---

## 🛠️ 自動化工具快速設置

### 一鍵設置所有工具

```bash
#!/bin/bash
# setup_security_tools.sh

# 安裝工具
pip install pre-commit detect-secrets semgrep bandit

# 設置 git-secrets (macOS)
brew install git-secrets
git secrets --install
git secrets --register-aws

# 設置 pre-commit
cat > .pre-commit-config.yaml <<'EOF'
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: detect-private-key

  - repo: https://github.com/Yelp/detect-secrets
    rev: v1.4.0
    hooks:
      - id: detect-secrets

  - repo: https://github.com/PyCQA/bandit
    rev: 1.7.6
    hooks:
      - id: bandit
        args: ['-ll']
EOF

pre-commit install
detect-secrets scan > .secrets.baseline

echo "✅ 安全工具設置完成!"
```

---

## 🚨 緊急情況快速參考

### 發現憑證洩漏怎麼辦？

1. **立即撤銷** (< 1 分鐘)
   - OpenAI: https://platform.openai.com/api-keys
   - AWS: https://console.aws.amazon.com/iam/
   - GitHub: https://github.com/settings/tokens

2. **生成新憑證** (< 2 分鐘)

3. **更新環境變數** (< 3 分鐘)
   ```bash
   echo "NEW_API_KEY=..." >> .env
   ```

4. **從 Git 歷史移除** (< 5 分鐘)
   ```bash
   git filter-branch --force --index-filter \
     "git rm --cached --ignore-unmatch path/to/file" \
     --prune-empty --tag-name-filter cat -- --all
   git push origin --force --all
   ```

詳細步驟: 參考「應急處理手冊.md」

---

## 📚 延伸資源

- **理論**: `理論/10.1_AI生成代碼安全風險.md`
- **工具**: `學習資源/工具整合實戰.md`
- **應急**: `學習資源/應急處理手冊.md`
- **OWASP Top 10**: https://owasp.org/www-project-top-ten/

---

**記住**：

> **「安全檢查不是額外負擔，而是保護你的保險」**

將這個 Checklist 加入你的日常開發流程，讓安全成為習慣。
