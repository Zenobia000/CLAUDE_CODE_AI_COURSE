# 練習 1：分析 AI 生成程式碼

## 📋 練習目標

通過分析真實的 AI 生成程式碼，培養：
- ✅ 批判性思維，不盲目信任 AI
- ✅ 識別「看似正確」程式碼中的問題
- ✅ 提出具體的修改建議
- ✅ 建立程式碼審查能力

**預計時間**：60 分鐘

---

## 🎯 練習情境

你是團隊的資深開發者，負責審查 AI 生成的程式碼。
初級工程師們使用 AI 工具快速開發功能，但需要你審查程式碼品質。

你的任務：
1. 審查 10 段 AI 生成的程式碼
2. 找出每段程式碼的問題（至少 3 個）
3. 提出具體的修改建議
4. 重寫成正確的版本

---

## 📂 檔案說明

```
練習1_分析AI生成程式碼/
├── README.md（本文件）
├── 情境描述.md（詳細的情境背景）
├── starter_code/
│   ├── example_01_user_auth.py
│   ├── example_02_file_upload.py
│   ├── example_03_api_call.py
│   ├── example_04_data_validation.py
│   ├── example_05_cache_implementation.py
│   ├── example_06_database_query.py
│   ├── example_07_password_reset.py
│   ├── example_08_webhook_handler.py
│   ├── example_09_csv_processor.py
│   └── example_10_email_sender.py
├── 評量標準.md（評分規則）
└── 參考解答/
    ├── analysis_example_01.md
    ├── fixed_example_01.py
    └── ...
```

---

## 🚀 開始練習

### 步驟 1：閱讀情境

閱讀 `情境描述.md`，了解專案背景和要求。

### 步驟 2：審查程式碼

對每個範例程式碼：

1. **第一次閱讀**：程式碼「看起來」做什麼？
2. **安全性檢查**：有沒有安全漏洞？（SQL 注入、XSS、路徑遍歷等）
3. **錯誤處理檢查**：有沒有考慮錯誤情況？
4. **程式碼品質檢查**：命名、類型提示、複雜度如何？
5. **效能檢查**：有沒有效能問題？

### 步驟 3：記錄問題

使用以下格式記錄你的分析：

```markdown
## 程式碼範例 X 分析

### 發現的問題

#### 問題 1：[問題類型]
**嚴重程度**：🔴 嚴重 / 🟡 中等 / 🟢 輕微
**位置**：第 X 行
**描述**：[具體描述問題]
**影響**：[可能造成什麼後果]

#### 問題 2：[問題類型]
...

### 修改建議

1. [具體建議 1]
2. [具體建議 2]
3. [具體建議 3]

### 改進後的程式碼

```python
# 你的改進版本
...
```
```

### 步驟 4：自我檢查

完成後，使用 `評量標準.md` 檢查你的分析：
- [ ] 找出了所有嚴重問題
- [ ] 提出了具體的修改建議
- [ ] 改進後的程式碼解決了所有問題
- [ ] 改進後的程式碼遵循最佳實踐

### 步驟 5：參考解答

最後查看 `參考解答/` 目錄：
- 對比你的分析和參考分析
- 學習你遺漏的問題
- 理解不同的解決方案

---

## 💡 審查提示

### 安全性檢查清單

- [ ] **SQL 注入**：是否使用參數化查詢？
- [ ] **XSS 攻擊**：是否淨化用戶輸入？
- [ ] **路徑遍歷**：是否驗證檔案路徑？
- [ ] **CSRF 攻擊**：是否有 CSRF 保護？
- [ ] **敏感資料**：是否有硬編碼密鑰？
- [ ] **認證授權**：是否檢查權限？

### 錯誤處理檢查清單

- [ ] 是否有 try-except？
- [ ] 是否處理 None 值？
- [ ] 是否處理空列表/字典？
- [ ] 是否處理網路錯誤？
- [ ] 是否處理檔案不存在？
- [ ] 錯誤訊息是否有意義？

### 程式碼品質檢查清單

- [ ] 是否有類型提示？
- [ ] 是否有文檔字串？
- [ ] 命名是否清楚？
- [ ] 函數是否太長（>50行）？
- [ ] 是否有重複程式碼？
- [ ] 是否遵循專案規範？

### 效能檢查清單

- [ ] 是否有 N+1 查詢？
- [ ] 是否使用 SELECT *？
- [ ] 是否有不必要的循環？
- [ ] 是否有記憶體洩漏風險？
- [ ] 是否可以使用快取？

---

## 🎓 學習要點

### 常見的 AI 程式碼問題模式

#### 1. 安全漏洞（40% 出現率）

```python
# ❌ AI 常生成的不安全程式碼
query = f"SELECT * FROM users WHERE username = '{username}'"

# ✅ 正確做法
query = "SELECT * FROM users WHERE username = ?"
```

#### 2. 錯誤處理缺失（60% 出現率）

```python
# ❌ AI 常生成的程式碼
def get_user(user_id):
    user = db.query(...)
    return user['name']  # 如果 user 是 None 會崩潰

# ✅ 正確做法
def get_user(user_id: int) -> Optional[str]:
    user = db.query(...)
    return user['name'] if user else None
```

#### 3. 過度工程化（30% 出現率）

```python
# ❌ AI 常生成的複雜程式碼
class UserServiceFactory:
    def create_service(self):
        return UserService(
            db=DatabaseConnection(),
            cache=CacheManager(),
            logger=LoggerFactory().create(),
            validator=ValidatorService()
        )

# ✅ 簡單版本（實際需要的）
def get_user(user_id):
    return db.query("SELECT * FROM users WHERE id = ?", user_id)
```

#### 4. 類型提示缺失（70% 出現率）

```python
# ❌ AI 常生成的程式碼
def process_data(data):
    return data.transform()

# ✅ 正確做法
def process_data(data: List[Dict[str, Any]]) -> List[ProcessedData]:
    return [ProcessedData.from_dict(item) for item in data]
```

---

## 📊 評分標準

### 總分：100 分

#### 發現問題（50 分）
- 找出所有嚴重安全問題（30 分）
- 找出錯誤處理問題（10 分）
- 找出程式碼品質問題（10 分）

#### 修改建議（20 分）
- 建議具體可執行（10 分）
- 建議符合最佳實踐（10 分）

#### 改進程式碼（30 分）
- 解決所有問題（15 分）
- 符合專案規範（10 分）
- 程式碼清晰易讀（5 分）

### 及格標準

- **基本及格**（60 分）：找出所有嚴重問題
- **良好**（75 分）：找出所有問題並提出建議
- **優秀**（85 分）：完整分析並提供高品質改進程式碼
- **卓越**（95+ 分）：超越參考解答，提出創新改進

---

## 🔗 相關資源

### 安全參考

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [SQL Injection Prevention](https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html)

### 程式碼品質

- [PEP 8 Python Style Guide](https://pep8.org/)
- [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html)

### 錯誤處理

- [Error Handling Best Practices](https://docs.python.org/3/tutorial/errors.html)

---

## 💬 常見問題

**Q：找不到問題怎麼辦？**

A：使用檢查清單逐項檢查。每個範例都至少有 3 個問題。

**Q：我的答案和參考解答不同？**

A：這很正常！有多種正確的解決方案。重要的是你的分析邏輯和改進方案是否合理。

**Q：需要重寫整個程式碼嗎？**

A：視問題嚴重程度：
- 小問題：局部修改
- 嚴重問題：可能需要重寫
- 過度工程：簡化重寫

**Q：練習時間不夠？**

A：優先完成前 5 個範例，它們涵蓋最常見的問題類型。

---

## 🎯 完成檢查點

完成本練習後，你應該能夠：

- [ ] 快速識別 SQL 注入等常見安全漏洞
- [ ] 發現錯誤處理缺失的問題
- [ ] 評估程式碼品質（命名、類型提示、複雜度）
- [ ] 提出具體可執行的修改建議
- [ ] 重寫程式碼解決所有問題

---

**練習版本**：v1.0
**預計時間**：60 分鐘
**難度**：⭐⭐ 中級
