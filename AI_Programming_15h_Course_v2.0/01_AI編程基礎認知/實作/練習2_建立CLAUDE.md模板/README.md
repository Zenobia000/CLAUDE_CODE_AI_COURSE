# 練習 2：建立 CLAUDE.md 模板

## 📋 練習目標

通過為真實專案建立 CLAUDE.md，實踐上下文工程：
- ✅ 理解專案記憶檔案的結構和重要性
- ✅ 學會提取專案的關鍵資訊
- ✅ 設計完整的 CLAUDE.md 模板
- ✅ 驗證 CLAUDE.md 的實際效果

**預計時間**：60 分鐘

---

## 🎯 練習情境

你剛加入一個新團隊，負責一個電商專案的維護與開發。
專案已經運行一年，但沒有任何專案記憶檔案。

團隊成員每次使用 AI 工具時，都要重新解釋專案背景，效率很低。

你的任務：
1. 分析專案程式碼和文檔
2. 提取關鍵資訊
3. 建立完整的 CLAUDE.md
4. 驗證其實際效果

---

## 📂 檔案說明

```
練習2_建立CLAUDE.md模板/
├── README.md（本文件）
├── 專案資訊.md（專案背景和資料）
├── sample_project/
│   ├── src/
│   │   ├── api/
│   │   ├── domain/
│   │   ├── infrastructure/
│   │   └── config/
│   ├── tests/
│   ├── docs/
│   └── README.md
├── 評量標準.md
└── 參考解答/
    └── CLAUDE.md
```

---

## 🚀 開始練習

### 步驟 1：理解專案

閱讀以下文件，了解專案：
1. `專案資訊.md` - 專案背景和技術資訊
2. `sample_project/README.md` - 專案概述
3. `sample_project/docs/` - 現有文檔
4. `sample_project/src/` - 程式碼結構

**目標**：回答以下問題
```
- 專案的核心功能是什麼？
- 使用了哪些技術棧？
- 架構設計遵循什麼原則？
- 有哪些團隊慣例和編碼規範？
- 最常遇到的問題有哪些？
```

---

### 步驟 2：設計 CLAUDE.md 結構

基於 1.3 章節學到的知識，設計 CLAUDE.md 結構。

**必須包含的章節**：

```markdown
# 專案名稱 - 專案記憶

## 概述
[2-3 句話描述專案]

## 技術棧
- 語言：
- 框架：
- 資料庫：
- ...

## 架構原則
[核心設計原則，2-3 個]

## 編碼規範
### 命名規範
### 類型提示
### 文檔字串
### 測試規範

## API 契約
[至少 3 個核心 API 端點]

## 常見問題
[至少 2 個真實問題及解決方案]

## 部署資訊
[環境、URL、監控]

## 開發工作流程
[Git workflow、CI/CD]
```

---

### 步驟 3：撰寫 CLAUDE.md

創建 `CLAUDE.md` 檔案，填入完整內容。

**撰寫要求**：

1. **準確性**
   - 所有技術資訊必須正確
   - API 契約必須與實際程式碼一致
   - 常見問題必須是真實存在的

2. **完整性**
   - 涵蓋所有核心章節
   - 每個章節有具體內容（不能只有標題）
   - 包含實際的程式碼範例

3. **實用性**
   - 資訊對 AI 協作有實際幫助
   - 能夠指導新人快速理解專案
   - 能夠避免常見錯誤

4. **簡潔性**
   - 總長度 < 1000 行
   - 避免冗餘資訊
   - 重點突出

---

### 步驟 4：驗證 CLAUDE.md

使用你建立的 CLAUDE.md 進行實際測試：

**測試 1：生成程式碼**

```bash
# 將 CLAUDE.md 放在專案根目錄
$ claude --add-dir ./sample_project

提示詞：
幫我寫一個創建訂單的函數

檢查：
- AI 是否使用了正確的技術棧？
- 是否遵循了編碼規範？
- 是否包含了完整的錯誤處理？
- 是否符合架構原則？
```

**測試 2：問題解答**

```bash
提示詞：
我遇到了 Redis 連線超時問題，應該如何解決？

檢查：
- AI 是否提供了你在 CLAUDE.md 中記錄的解決方案？
- 是否給出了具體的程式碼範例？
```

**測試 3：新人 Onboarding**

```bash
提示詞：
我是新加入的工程師，請幫我理解這個專案

檢查：
- AI 是否能準確描述專案？
- 是否提到了關鍵的架構設計？
- 是否給出了學習路徑？
```

---

### 步驟 5：迭代優化

根據測試結果，優化 CLAUDE.md：

**發現問題時**：
- AI 生成的程式碼不符合規範 → 補充更詳細的規範
- AI 不知道常見問題 → 添加更多常見問題
- AI 理解錯誤 → 修正或補充專案描述

**優化循環**：
```
撰寫 CLAUDE.md → 測試 → 發現問題 → 優化 → 再測試
```

---

## 💡 撰寫提示

### 如何提取關鍵資訊

**從程式碼中提取**：

```python
# 1. 查看 imports 了解技術棧
from fastapi import FastAPI
from sqlalchemy import create_engine
# → 使用 FastAPI 和 SQLAlchemy

# 2. 查看配置檔了解環境
DATABASE_URL = "postgresql://..."
REDIS_URL = "redis://..."
# → 使用 PostgreSQL 和 Redis

# 3. 查看架構了解設計原則
src/
├── domain/    # 領域層
├── application/  # 應用層
└── infrastructure/  # 基礎設施層
# → Clean Architecture

# 4. 查看測試了解規範
def test_create_user_with_valid_data_should_succeed():
# → 測試命名規範
```

**從文檔中提取**：

```markdown
# README.md → 專案概述
# docs/architecture.md → 架構設計
# docs/api.md → API 契約
# docs/troubleshooting.md → 常見問題
```

**從 Git 歷史提取**：

```bash
# 查看最常修改的檔案 → 核心模組
git log --pretty=format: --name-only | sort | uniq -c

# 查看最常修復的問題 → 常見問題
git log --grep="fix"

# 查看最近的架構決策 → 設計原則
git log --grep="refactor\|architecture"
```

---

### 如何寫好「常見問題」章節

**格式**：

```markdown
### 問題 X：[簡短描述]

**現象**：
```
[錯誤訊息或症狀]
```

**原因**：
[根本原因，1-2 句話]

**解決方案**：
```python
# 具體的解決程式碼
...
```

**預防措施**：
- [如何避免再次發生]
```

**真實範例**：

```markdown
### 問題 1：Redis 連線池耗盡

**現象**：
```
redis.exceptions.ConnectionError: Connection pool exhausted
```

**原因**：
高併發時 Redis 連線未正確釋放，連線池耗盡。

**解決方案**：
```python
# 使用 context manager 確保連線釋放
async with redis_client.pipeline() as pipe:
    await pipe.set('key', 'value')
    await pipe.execute()

# 或增加連線池大小
REDIS_POOL_SIZE = 50
```

**預防措施**：
- 所有 Redis 操作使用 context manager
- 定期監控連線池使用率
- 設定連線池最大值和超時
```

---

## 📊 評分標準

### 總分：100 分

#### 結構完整性（20 分）
- 包含所有必要章節（10 分）
- 章節組織清晰合理（10 分）

#### 內容準確性（30 分）
- 技術棧資訊正確（10 分）
- API 契約與程式碼一致（10 分）
- 常見問題真實可驗證（10 分）

#### 實用性（30 分）
- AI 生成程式碼符合規範（10 分）
- 能幫助新人理解專案（10 分）
- 能避免常見錯誤（10 分）

#### 簡潔性（10 分）
- 長度適中（< 1000 行）（5 分）
- 重點突出，無冗餘（5 分）

#### 程式碼範例（10 分）
- 包含實際程式碼範例（5 分）
- 程式碼範例清晰可執行（5 分）

---

## 🎯 完成檢查點

完成本練習後，你應該能夠：

- [ ] 分析專案並提取關鍵資訊
- [ ] 設計完整的 CLAUDE.md 結構
- [ ] 撰寫準確、實用、簡潔的專案記憶
- [ ] 驗證 CLAUDE.md 的實際效果
- [ ] 根據反饋迭代優化

**自我評估**：

使用你的 CLAUDE.md 進行 3 次測試：
1. 生成一個新功能的程式碼
2. 詢問一個常見問題的解決方案
3. 請 AI 解釋專案架構

如果 3 次測試都得到準確的回應，你的 CLAUDE.md 就成功了！

---

## 💬 常見問題

**Q：不知道該寫什麼內容？**

A：從最基本的資訊開始：
1. 專案是做什麼的（一句話）
2. 用了哪些技術（列表）
3. 怎麼運行（命令）
4. 有什麼規範（3-5 條）

然後逐步補充。

**Q：CLAUDE.md 太長了怎麼辦？**

A：分層設計：
- CLAUDE.md：核心資訊（< 1000 行）
- docs/：詳細文檔
- CLAUDE.md 中添加指引，告訴 AI 去哪裡找詳細資訊

**Q：如何知道寫得好不好？**

A：測試！讓 AI 生成程式碼，看是否：
- 使用正確的技術
- 遵循編碼規範
- 包含錯誤處理
- 符合架構原則

**Q：專案沒有文檔怎麼辦？**

A：這正是建立 CLAUDE.md 的好機會！
通過分析程式碼和 Git 歷史提取資訊。

---

## 🔗 參考資源

### 模板

- [CLAUDE.md 基礎模板](./templates/basic_template.md)
- [CLAUDE.md 完整模板](./templates/full_template.md)
- [常見問題範例](./templates/faq_examples.md)

### 工具

- [專案分析腳本](./tools/analyze_project.py)
- [Git 歷史分析](./tools/analyze_git_history.sh)
- [API 契約生成器](./tools/generate_api_spec.py)

---

**準備好了嗎？開始建立你的第一個 CLAUDE.md！**

---

**練習版本**：v1.0
**預計時間**：60 分鐘
**難度**：⭐⭐ 中級
