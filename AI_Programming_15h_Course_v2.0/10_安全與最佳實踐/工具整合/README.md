# 安全工具整合指南

本指南提供 3 個關鍵安全工具的快速設置流程,總耗時約 30 分鐘。

---

## 🛠️ 工具列表

### 1. git-secrets (5-10 分鐘)
**用途**: 防止憑證被 commit 到 Git
**檢測**: AWS keys, API keys, passwords

### 2. pre-commit hooks (10-15 分鐘)
**用途**: Commit 前自動執行安全檢查
**檢測**: 憑證、大檔案、私鑰、代碼格式

### 3. Semgrep (10-15 分鐘)
**用途**: 靜態代碼分析,檢測安全模式
**檢測**: SQL 注入、XSS、不安全反序列化

---

## 🚀 快速開始 (30 分鐘完整設置)

### Step 1: git-secrets (5 分鐘)

```bash
# macOS 安裝
brew install git-secrets

# Linux 安裝
git clone https://github.com/awslabs/git-secrets.git
cd git-secrets
sudo make install

# Windows (WSL)
git clone https://github.com/awslabs/git-secrets.git
cd git-secrets
sudo make install

# 在你的專案中啟用
cd /path/to/your/project
git secrets --install

# 註冊 AWS 憑證檢測
git secrets --register-aws

# 添加自訂規則
git secrets --add 'password\s*=\s*["\'][^"\']+["\']'
git secrets --add 'api[_-]?key\s*=\s*["\'][^"\']+["\']'
git secrets --add 'sk-[a-zA-Z0-9]{20,}'  # OpenAI keys
git secrets --add '[0-9]{16}'            # Credit card numbers

# 測試
echo "password = 'test123'" > test.txt
git add test.txt
git commit -m "test"  # 應該被阻止
rm test.txt

# 掃描現有檔案
git secrets --scan

# 掃描整個 Git 歷史
git secrets --scan-history
```

**常見問題**:
- Q: commit 被誤報阻止怎麼辦?
- A: 使用 `git secrets --add --allowed 'pattern'` 添加例外

---

### Step 2: pre-commit hooks (10 分鐘)

```bash
# 安裝 pre-commit
pip install pre-commit

# 建立配置檔案
cat > .pre-commit-config.yaml << 'EOF'
repos:
  # 憑證檢測
  - repo: https://github.com/Yelp/detect-secrets
    rev: v1.4.0
    hooks:
      - id: detect-secrets
        args: ['--baseline', '.secrets.baseline']
        exclude: package-lock.json

  # 基本檢查
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files
        args: ['--maxkb=500']
      - id: detect-private-key
      - id: check-merge-conflict

  # Python 安全掃描
  - repo: https://github.com/PyCQA/bandit
    rev: 1.7.5
    hooks:
      - id: bandit
        args: ['-c', 'pyproject.toml']
        additional_dependencies: ['bandit[toml]']

  # SQL 檢查
  - repo: https://github.com/sqlfluff/sqlfluff
    rev: 2.3.5
    hooks:
      - id: sqlfluff-lint
        args: [--dialect, postgres]
EOF

# 安裝 hooks
pre-commit install

# 建立 secrets baseline
detect-secrets scan > .secrets.baseline

# 測試所有檔案
pre-commit run --all-files

# 更新 .gitignore
cat >> .gitignore << EOF
.secrets.baseline
EOF

# Commit 配置
git add .pre-commit-config.yaml .secrets.baseline .gitignore
git commit -m "chore: add pre-commit security hooks"
```

**每日使用**:
- Commit 時自動執行,無需手動操作
- 若檢查失敗,修復問題後重新 commit
- 定期更新: `pre-commit autoupdate`

---

### Step 3: Semgrep (10 分鐘)

```bash
# 安裝
pip install semgrep

# 快速掃描 (使用官方規則集)
semgrep --config "p/security-audit" .
semgrep --config "p/owasp-top-ten" .
semgrep --config "p/python" .

# 建立自訂規則
mkdir .semgrep
cat > .semgrep/security.yml << 'EOF'
rules:
  # 檢測硬編碼憑證
  - id: hardcoded-password
    pattern-either:
      - pattern: password = "..."
      - pattern: api_key = "..."
      - pattern: secret = "..."
    message: "Hardcoded credential detected"
    severity: ERROR
    languages: [python, javascript]

  # 檢測 SQL 注入
  - id: sql-injection-format
    pattern: cursor.execute(f"... {$VAR} ...")
    message: "Potential SQL injection via f-string"
    severity: ERROR
    languages: [python]

  # 檢測 pickle 使用
  - id: dangerous-pickle
    pattern: pickle.loads($INPUT)
    message: "Dangerous use of pickle with untrusted data"
    severity: WARNING
    languages: [python]

  # 檢測 eval 使用
  - id: dangerous-eval
    pattern-either:
      - pattern: eval($INPUT)
      - pattern: exec($INPUT)
    message: "Dangerous use of eval/exec"
    severity: ERROR
    languages: [python]
EOF

# 使用自訂規則掃描
semgrep --config .semgrep/ .

# 整合到 CI/CD (GitHub Actions)
mkdir -p .github/workflows
cat > .github/workflows/semgrep.yml << 'EOF'
name: Semgrep Security Scan

on:
  pull_request: {}
  push:
    branches: [main, master, develop]

jobs:
  semgrep:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: returntocorp/semgrep-action@v1
        with:
          config: >-
            p/security-audit
            p/owasp-top-ten
EOF

git add .semgrep/ .github/workflows/semgrep.yml
git commit -m "chore: add Semgrep security scanning"
```

---

## 🔄 完整工作流程整合

### Makefile 整合

```makefile
.PHONY: security-check security-install security-scan

# 一次性設置所有工具
security-install:
	@echo "Installing security tools..."
	pip install pre-commit semgrep bandit safety
	brew install git-secrets || (git clone https://github.com/awslabs/git-secrets.git && cd git-secrets && sudo make install)
	@echo "✅ Security tools installed"

# 執行所有安全檢查
security-check:
	@echo "Running security checks..."
	@echo "\n🔍 1. git-secrets scan..."
	git secrets --scan || true
	@echo "\n🔍 2. pre-commit checks..."
	pre-commit run --all-files || true
	@echo "\n🔍 3. Bandit scan..."
	bandit -r . -f json -o bandit-report.json || true
	@echo "\n🔍 4. Safety check..."
	safety check || true
	@echo "\n🔍 5. Semgrep scan..."
	semgrep --config "p/security-audit" . || true
	@echo "\n✅ Security checks complete. Review reports above."

# 快速掃描 (只掃描變更的檔案)
security-scan:
	pre-commit run
```

使用:
```bash
# 初次設置
make security-install

# 每次開發後
make security-check

# Commit 前快速檢查
make security-scan
```

---

## 📊 CI/CD 整合

### GitHub Actions 完整配置

```yaml
# .github/workflows/security.yml
name: Security Checks

on:
  pull_request:
  push:
    branches: [main, develop]

jobs:
  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
        with:
          fetch-depth: 0  # 完整歷史 (for secret scanning)

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          pip install bandit safety semgrep

      - name: Run Bandit
        run: bandit -r . -f json -o bandit-report.json
        continue-on-error: true

      - name: Run Safety
        run: safety check --json
        continue-on-error: true

      - name: Run Semgrep
        run: semgrep --config "p/security-audit" --json --output semgrep-report.json .
        continue-on-error: true

      - name: Upload reports
        uses: actions/upload-artifact@v3
        with:
          name: security-reports
          path: |
            bandit-report.json
            semgrep-report.json

      - name: Check for critical issues
        run: |
          CRITICAL=$(jq '[.results[] | select(.issue_severity == "CRITICAL")] | length' bandit-report.json)
          if [ "$CRITICAL" -gt 0 ]; then
            echo "❌ Found $CRITICAL critical security issues"
            exit 1
          fi
          echo "✅ No critical issues found"
```

---

## 🎯 每日工作流程

### 開發者日常檢查清單

```markdown
## 每天開始工作時
- [ ] `git pull` (同步最新的安全配置)
- [ ] `pre-commit autoupdate` (每週一次)

## 開發過程中
- [ ] 寫代碼時參考安全檢查清單
- [ ] 避免硬編碼憑證
- [ ] 使用參數化 SQL 查詢

## Commit 前
- [ ] pre-commit hooks 自動執行 (無需手動)
- [ ] 如果被阻止,修復問題後重試
- [ ] 絕不使用 `--no-verify` 跳過檢查

## Pull Request 前
- [ ] `make security-check` 完整掃描
- [ ] 檢查 CI/CD 安全報告
- [ ] 確保無 CRITICAL/HIGH 問題
```

---

## 🔧 工具比較

| 工具 | 檢測類型 | 速度 | 誤報率 | 適用場景 |
|------|----------|------|--------|----------|
| **git-secrets** | 憑證洩漏 | ⚡⚡⚡ 極快 | 低 | Commit 前快速檢查 |
| **pre-commit** | 多種 (集成) | ⚡⚡ 快 | 低-中 | Commit hook 自動化 |
| **Bandit** | Python 安全 | ⚡⚡ 快 | 中 | Python 專案深度掃描 |
| **Semgrep** | 通用安全模式 | ⚡⚡ 快 | 低 | 跨語言安全掃描 |
| **Safety** | 依賴漏洞 | ⚡⚡⚡ 極快 | 極低 | 第三方套件檢查 |
| **TruffleHog** | 歷史憑證 | ⚡ 慢 | 中-高 | Git 歷史深度掃描 |

---

## ✅ 驗證設置成功

```bash
# 測試 git-secrets
echo 'password = "test123"' > test.py
git add test.py
git commit -m "test"  # 應該被阻止
git reset HEAD test.py && rm test.py

# 測試 pre-commit
echo 'eval(user_input)' > test.py
git add test.py
git commit -m "test"  # Bandit 應該報錯
rm test.py

# 測試 Semgrep
semgrep --config "p/security-audit" . | grep -i "error\|warning"
```

**所有測試通過** = 設置成功! ✅

---

## 📚 延伸學習

- [git-secrets 官方文檔](https://github.com/awslabs/git-secrets)
- [pre-commit 官方網站](https://pre-commit.com/)
- [Semgrep 規則庫](https://semgrep.dev/explore)
- [Bandit 文檔](https://bandit.readthedocs.io/)

---

**下一步**: 將這些工具應用到你的實際專案中,並加入團隊的開發規範!
