# 實作練習 2：安全掃描自動化

## 📋 練習概述

**練習目標**：為包含已知漏洞的專案建立多層次安全掃描管線，並用 AI 輔助修復漏洞

**預估時間**：1.5-2 小時

**難度等級**：⭐⭐⭐ 進階

**前置知識**：
- 完成練習 1（基礎 CI 工作流程）
- 理解常見的 Web 安全漏洞（SQL 注入、XSS、CSRF）
- 熟悉 GitHub Actions 基本操作

---

## 🎯 學習目標

完成本練習後，你將能夠：

1. ✅ 識別代碼中的常見安全漏洞
2. ✅ 配置多層次安全掃描（靜態分析 + 依賴掃描）
3. ✅ 理解不同安全工具的優勢和局限
4. ✅ 用 Claude Code 和 GitHub Copilot Autofix 修復漏洞
5. ✅ 建立「無掃描，不合併」的安全防護網

---

## 🚨 為什麼這個練習重要？

### 現實數據

> **40% 的 AI 生成代碼包含安全問題**
> 來源：課程設計文件，基於 GitHub 2024 安全報告

### 常見漏洞類型

本練習的範例專案包含以下典型漏洞：

1. **SQL 注入**（SQL Injection）
2. **跨站腳本攻擊**（XSS）
3. **不安全的依賴**（Known Vulnerabilities in Dependencies）
4. **硬編碼密鑰**（Hardcoded Secrets）
5. **不安全的反序列化**（Insecure Deserialization）

---

## 📂 專案結構

```
練習2_安全掃描管線/
├── README.md（本文件）
├── vulnerable_app/           # 有漏洞的範例應用（待你掃描和修復）
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py          # 包含 SQL 注入、XSS 漏洞
│   │   ├── database.py      # 不安全的資料庫操作
│   │   └── auth.py          # 包含硬編碼密鑰
│   ├── requirements.txt     # 包含有漏洞的依賴版本
│   └── Dockerfile
├── .github/
│   └── workflows/
│       └── security.yml     # 安全掃描 workflow（待你完成）
├── 參考解答/
│   ├── vulnerable_app/      # 修復後的安全代碼
│   ├── .github/workflows/security.yml  # 完整的安全掃描 workflow
│   └── 漏洞修復報告.md      # 詳細的修復說明
└── 評量標準.md
```

---

## 🚀 練習步驟

### 第 1 步：理解現有漏洞（30 分鐘）

#### 1.1 檢視有漏洞的代碼

首先，閱讀 `vulnerable_app/app/main.py`，嘗試找出以下漏洞：

**提示詞（給 Claude Code）**：

```
請幫我分析 vulnerable_app/app/main.py 中的安全漏洞。

請檢查：
1. SQL 注入風險
2. XSS（跨站腳本）風險
3. 不安全的輸入驗證
4. 硬編碼的敏感資訊

對每個漏洞，請說明：
- 漏洞位置（行號）
- 風險等級（高/中/低）
- 可能的攻擊場景
- 修復建議
```

#### 1.2 手動測試漏洞

**SQL 注入測試**：

```bash
# 啟動應用
cd vulnerable_app
pip install -r requirements.txt
uvicorn app.main:app --reload

# 測試 SQL 注入
curl "http://localhost:8000/user?id=1 OR 1=1--"
```

**檢查點**：
- [ ] 找到至少 3 個安全漏洞
- [ ] 理解每個漏洞的危害
- [ ] 能夠手動觸發 SQL 注入

---

### 第 2 步：建立多層次安全掃描（45 分鐘）

#### 2.1 Layer 1：靜態代碼分析（CodeQL）

**提示詞（給 Claude Code）**：

```
請幫我建立 .github/workflows/security.yml，加入 CodeQL 靜態分析：

需求：
1. 觸發條件：
   - push 到 main 分支
   - 所有 pull requests
   - 每週一凌晨定時掃描（schedule）

2. CodeQL 配置：
   - 語言：Python
   - 查詢套件：security-and-quality
   - 上傳結果到 GitHub Security tab

3. 失敗條件：
   - 發現任何 critical 或 high 級別漏洞時失敗
```

**提交並查看結果**：

```bash
git add .github/workflows/security.yml
git commit -m "ci: add CodeQL security scanning"
git push

# 前往 GitHub Security > Code scanning alerts 查看結果
```

#### 2.2 Layer 2：依賴漏洞掃描（Snyk）

**提示詞（給 Claude Code）**：

```
請幫我在 .github/workflows/security.yml 加入 Snyk 依賴掃描：

需求：
1. 新增 dependency-scan job：
   - 使用 snyk/actions/python@master
   - 掃描 requirements.txt
   - 發現高危漏洞時失敗

2. 配置：
   - 需要 SNYK_TOKEN（從 GitHub Secrets 讀取）
   - 產生 SARIF 報告並上傳到 GitHub

注意：請告訴我如何取得和配置 SNYK_TOKEN。
```

#### 2.3 Layer 3：密鑰掃描（Gitleaks）

**提示詞（給 Claude Code）**：

```
請在 .github/workflows/security.yml 加入 Gitleaks 掃描：

需求：
1. 新增 secret-scan job：
   - 使用 gitleaks/gitleaks-action
   - 掃描代碼中的硬編碼密鑰
   - 發現密鑰時失敗並提供詳細報告
```

**檢查點**：
- [ ] CodeQL 掃描成功執行
- [ ] Snyk 掃描成功執行
- [ ] Gitleaks 掃描成功執行
- [ ] 所有掃描都發現了預期的漏洞

---

### 第 3 步：用 AI 輔助修復漏洞（45 分鐘）

#### 3.1 修復 SQL 注入

**提示詞（給 Claude Code）**：

```
我的代碼被 CodeQL 標記為 SQL 注入漏洞：

[貼上 vulnerable_app/app/database.py 的相關代碼]

請幫我：
1. 解釋為什麼這是 SQL 注入漏洞
2. 提供安全的修復方案（使用參數化查詢）
3. 提供修復後的完整代碼
4. 說明如何驗證修復是否有效
```

#### 3.2 修復 XSS 漏洞

**提示詞（給 Claude Code）**：

```
我的代碼被標記為 XSS 漏洞：

[貼上相關代碼]

請幫我：
1. 解釋 XSS 攻擊的原理
2. 提供安全的輸出編碼方案
3. 推薦適合的 Python 函式庫（如 bleach、markupsafe）
```

#### 3.3 修復依賴漏洞

**提示詞（給 Claude Code）**：

```
Snyk 掃描發現以下依賴漏洞：
[貼上掃描結果]

請幫我：
1. 分析每個漏洞的風險等級
2. 提供升級建議（哪些需要立即升級，哪些可以延後）
3. 檢查升級後是否有 breaking changes
4. 生成更新後的 requirements.txt
```

#### 3.4 移除硬編碼密鑰

**提示詞（給 Claude Code）**：

```
我的代碼中有硬編碼的 API 密鑰：

[貼上代碼]

請幫我：
1. 重構代碼，改用環境變數
2. 建立 .env.example 範本檔案
3. 更新 .gitignore 確保 .env 不被提交
4. 提供在 GitHub Actions 中使用 secrets 的配置
```

**檢查點**：
- [ ] SQL 注入漏洞已修復
- [ ] XSS 漏洞已修復
- [ ] 依賴升級到安全版本
- [ ] 沒有硬編碼密鑰

---

### 第 4 步：驗證修復（20 分鐘）

#### 4.1 重新執行安全掃描

```bash
# 提交修復後的代碼
git add .
git commit -m "fix: resolve security vulnerabilities"
git push

# 查看 GitHub Actions 中的掃描結果
```

#### 4.2 手動驗證

**測試 SQL 注入修復**：

```bash
# 嘗試之前的攻擊，應該被阻止
curl "http://localhost:8000/user?id=1 OR 1=1--"

# 應該返回錯誤或空結果，而不是所有用戶資料
```

**檢查點**：
- [ ] 所有安全掃描通過（無高危漏洞）
- [ ] 手動測試確認漏洞已修復
- [ ] 應用功能正常運作（沒有因修復而破壞功能）

---

## 🎯 完成標準

完成本練習後，你的安全掃描管線應該包含：

### ✅ 必要功能（80 分）

- [ ] **靜態分析**：CodeQL 掃描並上傳結果到 GitHub
- [ ] **依賴掃描**：Snyk 檢測有漏洞的依賴
- [ ] **密鑰掃描**：Gitleaks 檢測硬編碼密鑰
- [ ] **自動失敗**：發現高危漏洞時阻止 PR 合併
- [ ] **漏洞修復**：至少修復 3 個主要漏洞

### ✅ 進階功能（100 分）

- [ ] **定時掃描**：每週自動執行安全掃描
- [ ] **漏洞報告**：生成詳細的修復報告
- [ ] **自動化修復**：使用 Dependabot 自動更新依賴
- [ ] **安全徽章**：在 README 中加入安全掃描徽章
- [ ] **文檔完整**：記錄每個漏洞的修復過程

---

## 🔍 自我檢查清單

### 掃描覆蓋度

- [ ] 靜態代碼分析（CodeQL）
- [ ] 依賴漏洞掃描（Snyk）
- [ ] 密鑰洩漏掃描（Gitleaks）
- [ ] 容器映像掃描（選做：Trivy）

### 漏洞修復驗證

- [ ] SQL 注入已修復並驗證
- [ ] XSS 已修復並驗證
- [ ] 依賴已更新到安全版本
- [ ] 密鑰已移除並改用環境變數
- [ ] 所有功能正常運作

### 流程自動化

- [ ] PR 自動觸發安全掃描
- [ ] 高危漏洞阻止 PR 合併
- [ ] 掃描結果自動上傳到 GitHub Security
- [ ] 定時掃描正常執行

---

## 💡 學習重點

### 三層安全防禦架構

```
Layer 1: 靜態代碼分析（CodeQL）
         → 找出代碼邏輯中的安全問題
         → SQL 注入、XSS、CSRF、路徑遍歷等

Layer 2: 依賴漏洞掃描（Snyk/Dependabot）
         → 找出第三方套件的已知漏洞
         → CVE 漏洞資料庫匹配

Layer 3: 密鑰掃描（Gitleaks）
         → 找出硬編碼的密鑰和敏感資訊
         → API keys、passwords、tokens
```

### 漏洞修復原則

1. **優先級排序**：
   - Critical/High → 立即修復
   - Medium → 計劃修復
   - Low → 評估後決定

2. **回歸測試**：
   - 修復後必須重新測試功能
   - 確保修復沒有引入新問題

3. **文檔記錄**：
   - 記錄漏洞詳情
   - 記錄修復方案
   - 便於未來參考

### 常見問題

**Q1: CodeQL 掃描太慢？**

A: 優化策略：
- 限制掃描範圍（只掃描關鍵目錄）
- 使用 cache 加速後續掃描
- 只在 PR 時做增量掃描

**Q2: Snyk 免費額度不夠？**

A: 替代方案：
- 使用 GitHub Dependabot（完全免費）
- 使用 pip-audit（開源工具）
- 使用 Safety（有免費額度）

**Q3: 修復漏洞後功能壞了？**

A: 這很正常！安全和功能需要平衡：
- 確保有足夠的測試覆蓋
- 在測試環境驗證修復
- 必要時尋求資深開發者協助

---

## 📚 延伸學習

完成基礎練習後，可以嘗試：

1. **加入容器掃描**
   - 使用 Trivy 掃描 Docker 映像
   - 檢測基礎映像的漏洞
   - 優化 Dockerfile 減少攻擊面

2. **建立安全政策**
   - 編寫 SECURITY.md
   - 定義漏洞回報流程
   - 設定安全更新策略

3. **整合更多工具**
   - Bandit（Python 安全檢查）
   - Safety（Python 依賴掃描）
   - Semgrep（自定義規則掃描）

4. **實現自動修復**
   - 使用 Dependabot 自動 PR
   - 使用 GitHub Copilot Autofix
   - 建立自動化修復腳本

---

## 🎓 重要概念回顧

### AI 時代的安全挑戰

> **40% 的 AI 生成代碼包含安全問題**

這意味著：
- ❌ 不能盲目信任 AI 生成的代碼
- ✅ 必須建立自動化安全掃描
- ✅ 採用「信任但驗證」的原則
- ✅ 將安全融入開發流程（DevSecOps）

### 無掃描，不合併

建立這個原則：
```
代碼審查 ✅
測試通過 ✅
安全掃描通過 ✅  ← 必須！
    ↓
才能合併到 main
```

---

## 🆘 需要協助？

### 參考資源

- **參考解答**：查看 `參考解答/` 目錄
- **理論文檔**：複習 `理論/5.2_安全掃描與自動修復.md`
- **情境題庫**：參考 `情境題庫/組合級/C01_安全掃描管線建立.md`

### 常用提示詞

**分析掃描結果**：
```
這是我的安全掃描結果：
[貼上結果]

請幫我：
1. 解釋每個漏洞的風險
2. 排序修復優先級
3. 提供修復建議
```

**驗證修復**：
```
我修復了 SQL 注入漏洞，請幫我檢查修復是否正確：
[貼上修復後的代碼]

請確認：
1. 漏洞是否完全修復
2. 是否引入新問題
3. 是否有更好的方案
```

---

## ✅ 完成後的下一步

完成本練習後：

1. **提交修復報告**：記錄你的修復過程
2. **進入練習 3**：整合完整的 CI/CD 管線
3. **應用到實際專案**：為所有專案加入安全掃描

---

**記住**：安全不是一次性的任務，而是持續的過程。

每次寫代碼前問自己：
- 這段代碼有 SQL 注入風險嗎？
- 用戶輸入有驗證嗎？
- 敏感資訊有保護嗎？

**預祝學習順利！** 🔒
