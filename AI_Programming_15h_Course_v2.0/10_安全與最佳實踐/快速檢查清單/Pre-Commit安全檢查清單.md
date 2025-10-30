# 🔒 Pre-Commit 安全檢查清單

> **使用時機**: 每次執行 `git commit` 前
>
> **耗時**: 30-60 秒
>
> **目標**: 防止將敏感資訊和安全漏洞提交到版本控制

---

## ⚠️ 第一優先: 憑證與秘密

### 🚫 絕對不可提交的內容

- [ ] **密碼**: `password = "..."`, `pwd = "..."`
- [ ] **API Keys**: `api_key = "..."`, `apiKey = "..."`
- [ ] **Tokens**: `token = "..."`, `auth_token = "..."`
- [ ] **私鑰**: `*.key`, `*.pem`, `id_rsa`
- [ ] **憑證檔案**: `.env`, `credentials.json`, `secrets.yaml`

### ✅ 正確做法檢查

- [ ] 所有憑證都使用 `os.getenv('VAR_NAME')`?
- [ ] `.env` 檔案已加入 `.gitignore`?
- [ ] 配置範例使用 `.env.example` 而非真實值?

---

## 🛡️ 代碼安全檢查

### SQL 注入風險

- [ ] **無字串拼接**: 沒有 `f"SELECT * FROM {table}"`?
- [ ] **使用參數化**: 所有 SQL 使用 `?` 或 `%s` 佔位符?
- [ ] **ORM 優先**: 使用 SQLAlchemy/Django ORM?

### 路徑遍歷風險

- [ ] **路徑驗證**: 檔案路徑使用 `pathlib.Path.resolve().is_relative_to()`?
- [ ] **無直接拼接**: 沒有 `f"/uploads/{user_input}"`?
- [ ] **白名單驗證**: 檔案類型和名稱經過驗證?

### 反序列化風險

- [ ] **避免 pickle**: 沒有 `pickle.loads(user_input)`?
- [ ] **使用 JSON**: 優先使用 `json.loads()`?
- [ ] **輸入驗證**: 使用 Pydantic 等驗證庫?

### 權限問題

- [ ] **無 chmod 777**: 沒有過度開放的檔案權限?
- [ ] **無不必要 sudo**: 腳本不要求 root 權限?
- [ ] **最小權限**: 服務以非 root 用戶運行?

---

## 📊 數據隱私檢查

### 個人資料 (PII)

- [ ] 沒有真實姓名、郵箱、電話?
- [ ] 沒有地址或身分證號?
- [ ] 測試數據使用合成資料?
- [ ] 日誌輸出不包含 PII?

### 內部資訊

- [ ] 沒有內部 IP 位址或主機名?
- [ ] 沒有員工資訊?
- [ ] 沒有專案路徑 (`/home/user/company-project/`)?
- [ ] 錯誤訊息已清理敏感資訊?

---

## 🔍 依賴與配置

### 依賴套件

- [ ] `requirements.txt` / `package.json` 更新?
- [ ] 沒有新增未經審查的依賴?
- [ ] 依賴版本明確指定 (不用 `*` 或 `latest`)?
- [ ] 執行過 `npm audit` / `safety check`?

### 配置檔案

- [ ] 配置檔案不包含憑證?
- [ ] 敏感配置使用環境變數?
- [ ] 範例配置 (`.example`) 已更新?

---

## 📝 代碼品質

### 註解與文檔

- [ ] 註解不包含 TODO with passwords?
- [ ] 沒有註解掉的舊憑證?
- [ ] 不包含內部聯絡資訊?

### Debug 代碼

- [ ] 移除 `console.log()` / `print()` debug 輸出?
- [ ] 移除 `debugger;` 語句?
- [ ] 移除測試用的硬編碼資料?

---

## 🤖 AI 生成代碼特別檢查

### 如果本次 commit 包含 AI 生成的代碼

- [ ] 已通過所有上述檢查?
- [ ] AI 代碼沒有硬編碼憑證?
- [ ] SQL 查詢使用參數化?
- [ ] 檔案操作有路徑驗證?
- [ ] 沒有使用 `eval()` 或 `exec()`?
- [ ] 依賴的 License 已確認相容?

---

## ✅ 最終確認

**在執行 `git commit` 前,確認以下所有項目**:

- [ ] 所有上述檢查項目都已通過
- [ ] 執行過 `git diff --cached` 確認變更內容
- [ ] 本地測試通過
- [ ] 如有自動化工具 (git-secrets, pre-commit),已通過檢查

---

## 🚀 自動化工具

**建議設置以下工具自動執行檢查**:

```bash
# 1. git-secrets (掃描憑證)
git secrets --install
git secrets --register-aws

# 2. pre-commit (多種檢查)
pip install pre-commit
pre-commit install

# 3. 手動掃描 (可選)
semgrep --config "p/security-audit" .
```

---

## 📞 發現問題怎麼辦?

### 如果發現敏感資訊

1. **立即停止 commit**
2. 移除或替換敏感資訊
3. 再次執行此檢查清單
4. 如已 commit,使用 `git commit --amend` 或 `git reset`

### 如果不確定

- **Ask**: 向資深同事或安全團隊確認
- **Don't commit**: 寧可多花 5 分鐘確認,也不要冒險

---

## 💡 記住

> **「每一次 commit 都是永久記錄」**
>
> 即使後來刪除,敏感資訊仍存在於 Git 歷史中

養成習慣,讓安全檢查成為肌肉記憶。

---

**版本**: v1.0
**最後更新**: 2024-01-15
**適用於**: 所有使用版本控制的專案
