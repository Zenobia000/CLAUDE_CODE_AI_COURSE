# 參考解答：練習 1 - FastAPI 專案 CI/CD 管線

## 📋 說明

這是練習 1 的參考解答，提供完整的專案結構和 CI/CD workflow 配置。

**重要提示**：
- ⚠️ 請先自己嘗試完成練習，遇到困難時再參考本解答
- ⚠️ 不要直接複製貼上，理解每一行代碼的作用
- ⚠️ 參考解答只是一種實現方式，你的方案可能更好

---

## 📂 專案結構

```
參考解答/
├── README.md（本文件）
├── fastapi_project/           # FastAPI 專案代碼
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
└── .github/
    └── workflows/
        └── ci.yml            # CI/CD workflow
```

---

## 🚀 快速開始

### 1. 複製專案代碼

```bash
# 複製整個 fastapi_project 目錄到你的工作目錄
cp -r fastapi_project/ /你的工作目錄/
```

### 2. 本地測試

```bash
cd fastapi_project

# 建立虛擬環境（推薦）
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安裝依賴
pip install -r requirements.txt

# 運行應用
uvicorn app.main:app --reload

# 執行測試
pytest

# 執行 linting
black --check app tests
flake8 app tests
isort --check app tests
```

### 3. 複製 Workflow

```bash
# 複製 workflow 到你的專案
mkdir -p .github/workflows
cp .github/workflows/ci.yml /你的工作目錄/.github/workflows/
```

### 4. 設定 GitHub Secrets（如果需要推送 Docker 映像）

前往 GitHub 專案設定：
```
Settings > Secrets and variables > Actions > New repository secret
```

需要的 secrets（如果推送到 GitHub Container Registry）：
- `GITHUB_TOKEN`：自動提供，無需手動設定

---

## 📖 解答說明

### 關鍵設計決策

#### 1. FastAPI 專案結構

**為什麼這樣設計**：
- `app/` 目錄：包含所有應用代碼
- `tests/` 目錄：與 app 平行，便於管理
- 使用 `__init__.py`：標準 Python 套件結構

#### 2. CI Workflow 設計

**並行執行策略**：
```yaml
jobs:
  lint:    # 獨立執行
  test:    # 獨立執行
  security:  # 獨立執行
  build:   # 依賴前三者
    needs: [lint, test, security]
```

**為什麼**：
- lint、test、security 互不依賴，可並行執行
- build 需要確保前面都通過，使用 `needs`

**快取策略**：
```yaml
- uses: actions/setup-python@v4
  with:
    python-version: '3.11'
    cache: 'pip'  # 自動快取 pip 依賴
```

**為什麼**：
- 使用 `actions/setup-python` 內建 cache 功能
- 比手動配置 `actions/cache` 更簡單
- Cache key 自動基於 requirements.txt hash

---

## 🔍 關鍵檔案解析

### 1. `.github/workflows/ci.yml`

#### 觸發條件

```yaml
on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]
```

**解釋**：
- push 到 main：每次推送都執行完整 CI
- PR 到 main：每個 PR 都必須通過 CI

#### Lint Job

```yaml
jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
          cache: 'pip'

      - name: Install linting tools
        run: |
          pip install black flake8 isort

      - name: Run black
        run: black --check app tests

      - name: Run flake8
        run: flake8 app tests --max-line-length=100

      - name: Run isort
        run: isort --check app tests
```

**關鍵點**：
- 三個工具分別執行，任一失敗都會導致 job 失敗
- `--check` 模式：只檢查不修改
- flake8 設定 `--max-line-length=100`：與 black 一致

#### Test Job

```yaml
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
          cache: 'pip'

      - name: Install dependencies
        run: |
          pip install -r requirements.txt

      - name: Run pytest with coverage
        run: |
          pytest --cov=app --cov-report=xml --cov-report=term

      - name: Upload coverage to Codecov
        uses: codecov/codecov-action@v3
        with:
          file: ./coverage.xml
          fail_ci_if_error: false
```

**關鍵點**：
- 使用 `pytest-cov` 產生覆蓋率報告
- 上傳到 Codecov（可選）
- `fail_ci_if_error: false`：Codecov 失敗不影響 CI

#### Security Job

```yaml
  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install safety
        run: pip install safety

      - name: Run safety check
        run: safety check --file requirements.txt
```

**關鍵點**：
- 使用 `safety` 檢查依賴漏洞
- 發現漏洞時會失敗
- 輕量級，執行快速

#### Build Job

```yaml
  build:
    needs: [lint, test, security]
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write

    steps:
      - uses: actions/checkout@v4

      - name: Log in to GitHub Container Registry
        uses: docker/login-action@v2
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Extract metadata
        id: meta
        uses: docker/metadata-action@v4
        with:
          images: ghcr.io/${{ github.repository }}
          tags: |
            type=sha
            type=ref,event=branch
            type=ref,event=pr

      - name: Build and push
        uses: docker/build-push-action@v4
        with:
          context: ./fastapi_project
          push: ${{ github.event_name != 'pull_request' }}
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
          cache-from: type=gha
          cache-to: type=gha,mode=max
```

**關鍵點**：
- `needs: [lint, test, security]`：確保前面都通過
- 使用 `docker/metadata-action` 自動生成標記
- `push` 條件：只在非 PR 時推送
- 使用 GitHub Actions cache 加速構建

---

## 💡 學習重點

### 1. 並行 vs 串行

**並行執行**（推薦）：
```yaml
jobs:
  lint:    # 同時開始
  test:    # 同時開始
  security:  # 同時開始
```

**串行執行**（不推薦）：
```yaml
jobs:
  lint:
  test:
    needs: lint  # 等待 lint 完成
  security:
    needs: test  # 等待 test 完成
```

**為什麼並行更好**：
- 節省時間（3 個 job 各 2 分鐘，並行 2 分鐘 vs 串行 6 分鐘）
- 更早發現問題
- 更好的資源利用

### 2. 快取策略

**方法 1：使用 actions/setup-python 內建 cache**（推薦）：
```yaml
- uses: actions/setup-python@v4
  with:
    python-version: '3.11'
    cache: 'pip'
```

**方法 2：手動配置 actions/cache**：
```yaml
- uses: actions/cache@v3
  with:
    path: ~/.cache/pip
    key: ${{ runner.os }}-pip-${{ hashFiles('requirements.txt') }}
    restore-keys: |
      ${{ runner.os }}-pip-
```

**為什麼選擇方法 1**：
- 更簡單，無需手動配置
- 自動處理 cache key
- 支援多種套件管理器

### 3. Docker 構建快取

```yaml
- uses: docker/build-push-action@v4
  with:
    cache-from: type=gha
    cache-to: type=gha,mode=max
```

**解釋**：
- `type=gha`：使用 GitHub Actions cache
- `mode=max`：快取所有層（不只是最終層）
- 大幅加速後續構建

---

## 🎯 與你的方案比較

完成練習後，對比一下：

### 功能完整性
- [ ] 你的方案是否實現了所有必要功能？
- [ ] 缺少哪些功能？為什麼？

### 代碼品質
- [ ] 你的 workflow 配置是否清晰易讀？
- [ ] 是否有冗餘或可優化的部分？

### 執行效率
- [ ] 你的 workflow 執行時間是多少？
- [ ] 是否使用了並行執行和快取？

### 最佳實踐
- [ ] 是否遵循 GitHub Actions 最佳實踐？
- [ ] 是否考慮了安全性（secrets 管理）？

---

## 📚 延伸學習

看完參考解答後，可以嘗試：

### 優化方向

1. **加入矩陣測試**
```yaml
test:
  strategy:
    matrix:
      python-version: ['3.10', '3.11', '3.12']
  steps:
    - uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}
```

2. **條件執行**
```yaml
test:
  if: contains(github.event.head_commit.message, 'test') || github.event_name == 'pull_request'
```

3. **自動化 PR 評論**
```yaml
- name: Comment PR with coverage
  uses: py-cov-action/python-coverage-comment-action@v3
  with:
    GITHUB_TOKEN: ${{ github.token }}
```

---

## 🆘 常見問題

### Q1: 為什麼我的 workflow 比參考解答慢？

A: 檢查：
- 是否使用快取？
- 是否並行執行？
- 是否有不必要的步驟？

### Q2: Docker 構建失敗？

A: 檢查：
- Dockerfile 路徑是否正確？
- `context` 設定是否正確？
- 基礎映像是否可用？

### Q3: Safety 檢查失敗怎麼辦？

A: 兩種方案：
1. 升級有漏洞的依賴（推薦）
2. 暫時忽略（不推薦）：`safety check --ignore xxx`

---

## ✅ 記住

參考解答只是一種實現方式，不是唯一正確答案。

重要的是：
1. **理解原理**：為什麼這樣設計？
2. **學習優化**：如何改進你的方案？
3. **應用實踐**：如何應用到實際專案？

**繼續加油！** 🚀
