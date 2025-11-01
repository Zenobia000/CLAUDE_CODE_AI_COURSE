# 實作練習 1：FastAPI 專案 CI/CD 管線建立

## 📋 練習概述

**練習目標**：為 FastAPI 專案建立完整的 CI/CD 管線

**預估時間**：2-3 小時

**難度等級**：⭐⭐ 中級

**前置知識**：
- 熟悉 Python 和 FastAPI 基礎
- 理解 GitHub Actions 基本概念（已學習 `理論/5.1_GitHub_Actions整合.md`）
- 了解測試的基本概念

---

## 🎯 學習目標

完成本練習後，你將能夠：

1. ✅ 為 FastAPI 專案建立自動化測試管線
2. ✅ 配置程式碼品質檢查（linting、formatting）
3. ✅ 整合安全掃描工具
4. ✅ 實現 Docker 映像自動構建
5. ✅ 用 Claude Code 輔助生成和優化 workflow

---

## 📂 專案結構

```
練習1_基礎CI工作流程/
├── README.md（本文件）
├── fastapi_project/           # FastAPI 專案代碼（待你完成）
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py           # FastAPI 應用主程式
│   │   └── models.py         # 資料模型
│   ├── tests/
│   │   ├── __init__.py
│   │   └── test_main.py      # 測試代碼
│   ├── requirements.txt       # Python 依賴
│   ├── Dockerfile            # Docker 映像配置
│   └── .gitignore
├── .github/
│   └── workflows/
│       └── ci.yml            # CI/CD workflow（待你完成）
├── 參考解答/
│   ├── fastapi_project/      # 完整專案代碼
│   └── .github/workflows/ci.yml  # 參考 workflow
└── 評量標準.md
```

---

## 🚀 練習步驟

### 第 1 步：建立 FastAPI 專案（30 分鐘）

#### 1.1 創建專案結構

在 `fastapi_project/` 目錄下建立基本的 FastAPI 應用。

**提示詞（給 Claude Code）**：

```
請幫我在 fastapi_project/ 目錄下建立一個簡單的 FastAPI 專案：

需求：
1. 建立 app/main.py，包含：
   - 基礎的 FastAPI 應用
   - GET / 路由（返回 "Hello World"）
   - GET /health 路由（健康檢查）
   - GET /items/{item_id} 路由（查詢項目）

2. 建立 app/models.py，定義 Item 資料模型（id, name, description）

3. 建立 tests/test_main.py，包含：
   - 測試 GET / 路由
   - 測試 GET /health 路由
   - 測試 GET /items/{item_id} 路由

4. 建立 requirements.txt，包含：
   - fastapi
   - uvicorn
   - pytest
   - httpx（測試用）

5. 建立 Dockerfile，用於構建 FastAPI 應用映像
```

#### 1.2 本地測試

確保專案可以在本地運行：

```bash
cd fastapi_project

# 安裝依賴（建議使用虛擬環境）
pip install -r requirements.txt

# 運行應用
uvicorn app.main:app --reload

# 執行測試
pytest
```

**檢查點**：
- [ ] FastAPI 應用可以成功啟動
- [ ] 訪問 http://localhost:8000 能看到 "Hello World"
- [ ] pytest 測試全部通過

---

### 第 2 步：建立基礎測試管線（45 分鐘）

#### 2.1 創建 workflow 檔案

在 `.github/workflows/ci.yml` 建立 GitHub Actions workflow。

**提示詞（給 Claude Code）**：

```
請幫我建立 .github/workflows/ci.yml，實現以下功能：

需求：
1. 觸發條件：
   - 所有 push 到 main 分支
   - 所有 pull request

2. 測試工作流程（test job）：
   - 使用 Python 3.11
   - 安裝依賴（requirements.txt）
   - 執行 pytest
   - 產生測試覆蓋率報告

3. 環境：
   - 使用 ubuntu-latest
   - 快取 pip 依賴以加速執行
```

#### 2.2 測試 workflow

```bash
# 提交代碼觸發 workflow
git add .
git commit -m "ci: add basic test workflow"
git push

# 前往 GitHub Actions 頁面查看執行結果
```

**檢查點**：
- [ ] Workflow 成功執行
- [ ] 測試步驟全部通過
- [ ] 可以在 GitHub Actions 看到測試結果

---

### 第 3 步：加入程式碼品質檢查（30 分鐘）

#### 3.1 添加 linting 工具

更新 `requirements.txt`，加入：

```
black
flake8
isort
```

#### 3.2 更新 workflow

**提示詞（給 Claude Code）**：

```
請幫我更新 .github/workflows/ci.yml，加入程式碼品質檢查：

需求：
1. 新增 lint job（在 test job 之前執行）：
   - 使用 black 檢查代碼格式
   - 使用 flake8 檢查代碼風格
   - 使用 isort 檢查 import 排序

2. 確保：
   - lint 失敗時，整個 workflow 失敗
   - test job 依賴 lint job 通過
```

**檢查點**：
- [ ] Lint job 成功執行
- [ ] 代碼格式符合 black 標準
- [ ] 代碼風格符合 flake8 規則

---

### 第 4 步：整合安全掃描（30 分鐘）

#### 4.1 添加依賴掃描

**提示詞（給 Claude Code）**：

```
請幫我在 .github/workflows/ci.yml 加入安全掃描：

需求：
1. 新增 security job：
   - 使用 Snyk 掃描 Python 依賴漏洞
   - 使用 Safety 檢查已知的不安全套件

2. 配置：
   - 發現高危漏洞時失敗
   - 產生安全報告
```

#### 4.2 處理掃描結果

如果發現漏洞：

```
提示詞給 Claude Code：
我的專案掃描出以下安全漏洞：
[貼上掃描結果]

請幫我分析並提供修復建議。
```

**檢查點**：
- [ ] 安全掃描成功執行
- [ ] 沒有高危漏洞（或已修復）
- [ ] 理解每個漏洞的風險

---

### 第 5 步：加入 Docker 構建（45 分鐘）

#### 5.1 更新 workflow

**提示詞（給 Claude Code）**：

```
請幫我在 .github/workflows/ci.yml 加入 Docker 構建：

需求：
1. 新增 docker job（依賴 test 和 security 通過）：
   - 使用 docker/build-push-action
   - 構建 Docker 映像
   - 標記為 fastapi-app:latest
   - 測試映像可以成功啟動

2. 優化：
   - 使用 Docker layer caching 加速構建
   - 只在 main 分支 push 時構建
```

#### 5.2 測試 Docker 映像

本地測試 Docker 映像：

```bash
# 構建映像
docker build -t fastapi-app:latest ./fastapi_project

# 運行容器
docker run -p 8000:8000 fastapi-app:latest

# 測試 API
curl http://localhost:8000/health
```

**檢查點**：
- [ ] Docker 映像成功構建
- [ ] 容器可以成功啟動
- [ ] API 在容器中正常運作

---

## 🎯 完成標準

完成本練習後，你的 CI/CD 管線應該包含：

### ✅ 必要功能（80 分）

- [ ] **自動化測試**：每次 push/PR 自動執行 pytest
- [ ] **程式碼品質**：black、flake8、isort 檢查
- [ ] **安全掃描**：依賴漏洞掃描
- [ ] **Docker 構建**：自動構建容器映像
- [ ] **快取優化**：使用 pip cache 和 Docker layer cache

### ✅ 進階功能（100 分）

- [ ] **測試覆蓋率**：產生並顯示覆蓋率報告
- [ ] **並行執行**：lint、test、security 並行執行
- [ ] **條件執行**：Docker 構建僅在 main 分支執行
- [ ] **錯誤處理**：清晰的錯誤訊息和失敗通知
- [ ] **文檔完整**：workflow 中有清晰的註解

---

## 🔍 自我檢查清單

### 功能性檢查

- [ ] Workflow 在 push 到 main 時自動執行
- [ ] Workflow 在 PR 時自動執行
- [ ] 所有測試通過
- [ ] Lint 檢查通過
- [ ] 安全掃描通過（無高危漏洞）
- [ ] Docker 映像成功構建

### 效能檢查

- [ ] Workflow 執行時間 < 5 分鐘
- [ ] 使用了適當的快取機制
- [ ] 並行執行提升了效率

### 品質檢查

- [ ] Workflow 配置清晰易讀
- [ ] 包含適當的註解
- [ ] 錯誤訊息清晰明確
- [ ] 符合最佳實踐

---

## 💡 學習重點

### 關鍵概念

1. **CI/CD 管線結構**
   - Jobs 的依賴關係（depends-on）
   - 並行 vs 串行執行
   - 條件執行（if 條件）

2. **快取策略**
   - Pip 依賴快取
   - Docker layer caching
   - 快取鍵（cache key）設計

3. **安全掃描整合**
   - 依賴漏洞掃描的重要性
   - 如何處理掃描結果
   - 風險等級評估

### 常見問題

**Q1: Workflow 執行太慢怎麼辦？**

A: 優化策略：
- 使用快取（actions/cache）
- 並行執行獨立的 jobs
- 只在必要時執行（條件執行）

**Q2: 依賴安裝失敗？**

A: 檢查：
- requirements.txt 格式是否正確
- Python 版本是否匹配
- 是否需要系統級依賴（apt install）

**Q3: Docker 構建失敗？**

A: 常見原因：
- Dockerfile 路徑錯誤
- 上下文（context）設置不正確
- 基礎映像不可用

---

## 📚 延伸學習

完成基礎練習後，可以嘗試：

1. **加入更多測試類型**
   - 整合測試（integration tests）
   - API 端點測試
   - 負載測試

2. **優化 Docker 映像**
   - 使用多階段構建（multi-stage build）
   - 減小映像大小
   - 使用 Alpine Linux

3. **加入通知機制**
   - Slack 通知
   - Email 通知
   - GitHub Status 徽章

4. **實現自動部署**
   - 部署到測試環境
   - 藍綠部署
   - 金絲雀部署

---

## 🆘 需要協助？

### 參考資源

- **參考解答**：查看 `參考解答/` 目錄
- **理論文檔**：複習 `理論/5.1_GitHub_Actions整合.md`
- **情境題庫**：參考 `情境題庫/基礎級/B01_建立基礎測試管線.md`

### 提示詞範例

**當你遇到困難時，可以這樣問 Claude Code**：

```
我的 GitHub Actions workflow 執行失敗，錯誤訊息是：
[貼上錯誤訊息]

請幫我分析問題原因並提供解決方案。
```

```
我想優化我的 workflow 執行速度，目前需要 10 分鐘。
請檢查我的配置並提供優化建議：
[貼上 workflow 配置]
```

---

## ✅ 完成後的下一步

完成本練習後：

1. **提交作業**：將完成的 workflow 提交到 GitHub
2. **進入練習 2**：學習安全掃描自動化
3. **應用到實際專案**：為你的專案建立類似的 CI/CD 管線

---

**預祝學習順利！** 🚀

記住：CI/CD 的目標是「快速失敗，快速修復」。不要害怕錯誤，從錯誤中學習是最快的進步方式。
