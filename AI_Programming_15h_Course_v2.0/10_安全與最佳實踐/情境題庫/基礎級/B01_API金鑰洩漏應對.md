# B01: API 金鑰洩漏應對

> **難度**: ⭐⭐ 基礎級
>
> **預計耗時**: 30-45 分鐘
>
> **核心技能**: 憑證洩漏緊急處理、Git 歷史清理、預防機制建立

---

## 📖 情境描述

### 背景

你正在使用 Claude Code 開發一個天氣預報應用,需要整合 OpenWeatherMap API。

你向 Claude 詢問:「如何使用 OpenWeatherMap API 獲取天氣資料?」

Claude 生成了以下代碼:

```python
import requests

# OpenWeatherMap API configuration
API_KEY = "your_api_key_here"
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

def get_weather(city):
    """Get current weather for a city"""
    params = {
        'q': city,
        'appid': API_KEY,
        'units': 'metric'
    }

    response = requests.get(BASE_URL, params=params)
    return response.json()

if __name__ == "__main__":
    weather = get_weather("Taipei")
    print(f"Temperature: {weather['main']['temp']}°C")
```

你興奮地複製代碼,將 `"your_api_key_here"` 替換為你的真實 OpenWeatherMap API key: `"a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6"`,然後:

1. 測試代碼 → 成功運行!
2. `git add weather.py`
3. `git commit -m "Add weather API integration"`

**10 分鐘後**,你突然意識到: 「糟糕!我把 API key 硬編碼進去了!」

更糟的是,你檢查發現:
- ❌ 這個 commit **還沒有 push** 到 GitHub
- ⚠️ 但你已經繼續工作,又做了 2 個新 commits
- 😰 現在是時候 09:45,團隊每天 10:00 會自動同步所有分支到遠端

**你只有 15 分鐘來處理這個問題!**

---

## 🎯 任務目標

你需要在 **15 分鐘內** 完成以下所有任務:

### 任務 1: 緊急評估 (2 分鐘)
- [ ] 確認 API key 是否已推送到遠端
- [ ] 確認倉庫是公開還是私有
- [ ] 檢查 API key 的權限範圍
- [ ] 評估如果洩漏的潛在影響

### 任務 2: 撤銷 API Key (3 分鐘)
- [ ] 登入 OpenWeatherMap
- [ ] 撤銷或重新生成 API key
- [ ] 生成新的 API key
- [ ] 記錄舊 key 的撤銷時間

### 任務 3: 清理 Git 歷史 (5 分鐘)
- [ ] 從 Git 歷史中移除包含 API key 的 commit
- [ ] 保留後續的 2 個 commits 的變更
- [ ] 驗證 API key 不再出現在 Git 歷史中

### 任務 4: 修復代碼 (3 分鐘)
- [ ] 使用環境變數替代硬編碼
- [ ] 建立 `.env` 檔案
- [ ] 確保 `.env` 在 `.gitignore` 中
- [ ] 測試修復後的代碼

### 任務 5: 建立防護 (2 分鐘)
- [ ] 設置 git-secrets 或 pre-commit hook
- [ ] 測試防護機制是否有效
- [ ] 記錄經驗教訓

---

## 🔍 考察重點

本情境測試你的能力:

1. **緊急應變**: 在時間壓力下快速決策
2. **Git 操作**: 安全地修改 Git 歷史
3. **安全意識**: 理解硬編碼憑證的風險
4. **預防思維**: 建立自動化防護機制
5. **壓力管理**: 保持冷靜,系統化處理問題

---

## 💡 提示與資源

### 提示 1: 檢查 Git 狀態

```bash
# 檢查是否已推送
git log origin/main..HEAD

# 如果輸出有 commits,表示還沒推送
# 如果輸出為空,表示已經推送 (糟糕!)
```

---

### 提示 2: Git 歷史清理策略

**情境 A**: 問題 commit 是最新的
```bash
# 使用 amend
git commit --amend
```

**情境 B**: 問題 commit 在中間 (本題情況)
```bash
# 方法 1: Interactive rebase
git rebase -i HEAD~3

# 方法 2: Reset 並重新 commit
git reset --soft HEAD~3
# 修復檔案後重新 commit
```

---

### 提示 3: 正確的環境變數使用

```python
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv('OPENWEATHER_API_KEY')
if not API_KEY:
    raise ValueError("OPENWEATHER_API_KEY not found in environment")
```

`.env` 檔案:
```
OPENWEATHER_API_KEY=your_new_api_key_here
```

---

### 提示 4: 驗證清理成功

```bash
# 搜尋所有歷史中的 API key 痕跡
git log -p | grep -i "a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6"

# 應該沒有任何輸出
```

---

## ✅ 參考解答

### Step 1: 緊急評估 (2 分鐘)

```bash
# 1. 檢查是否已推送
git log origin/main..HEAD

# 輸出範例:
# abc1234 Add error handling
# def5678 Update README
# 789abcd Add weather API integration  ← 包含 API key 的 commit

# ✅ 好消息: 還沒推送

# 2. 檢查倉庫可見性
gh repo view --json isPrivate

# 輸出: {"isPrivate": true}
# ✅ 倉庫是私有的

# 3. 評估風險
# - API key 權限: 免費方案,1000 calls/day
# - 潛在損失: 有限,但仍需撤銷
# - 時間壓力: 15 分鐘內處理
```

---

### Step 2: 撤銷 API Key (3 分鐘)

**Web UI 操作** (最快):

1. 前往 https://home.openweathermap.org/api_keys
2. 找到洩漏的 key: `a1b2c3...`
3. 點擊 "Delete" 或 "Regenerate"
4. 複製新生成的 key: `p6o5n4m3l2k1j0i9h8g7f6e5d4c3b2a1`
5. 記錄時間: 09:47

**命令行操作** (如有 API):

```bash
# 撤銷舊 key
curl -X DELETE https://api.openweathermap.org/data/2.5/api_key \
  -H "Authorization: Bearer OLD_KEY"

# 生成新 key
curl -X POST https://api.openweathermap.org/data/2.5/api_key \
  -H "Authorization: Bearer MASTER_KEY"
```

---

### Step 3: 清理 Git 歷史 (5 分鐘)

**方法 1: Interactive Rebase (推薦)**

```bash
# 1. 開始 interactive rebase (最近 3 個 commits)
git rebase -i HEAD~3

# 編輯器會打開,顯示:
# pick 789abcd Add weather API integration  ← 要修改這個
# pick def5678 Update README
# pick abc1234 Add error handling

# 2. 將第一行改為 "edit"
# edit 789abcd Add weather API integration
# pick def5678 Update README
# pick abc1234 Add error handling

# 儲存並退出

# 3. Git 會停在該 commit,現在修復檔案
# (見 Step 4 的代碼修復)

# 4. 修復後,繼續 rebase
git add weather.py .env .gitignore
git commit --amend --no-edit
git rebase --continue

# 5. 驗證
git log -p | grep "a1b2c3d4e5f6"  # 應該沒有輸出
```

---

**方法 2: Reset 並重建 (更直接)**

```bash
# 1. 記錄後續 commits 的變更
git diff HEAD~3 HEAD > /tmp/changes.patch

# 2. Reset 到問題 commit 之前
git reset --hard HEAD~3

# 3. 修復 weather.py (見 Step 4)
# ... 修復代碼 ...

# 4. 提交修復版本
git add weather.py .env .gitignore
git commit -m "Add weather API integration (using env vars)"

# 5. 應用後續變更
git apply /tmp/changes.patch
git add .
git commit -m "Update README and add error handling"

# 6. 驗證
git log --oneline
# 應該看到新的 commit hashes
```

---

### Step 4: 修復代碼 (3 分鐘)

**修復後的 `weather.py`**:

```python
import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration from environment
API_KEY = os.getenv('OPENWEATHER_API_KEY')
if not API_KEY:
    raise ValueError(
        "OPENWEATHER_API_KEY not found. "
        "Please create a .env file with your API key."
    )

BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

def get_weather(city):
    """Get current weather for a city"""
    params = {
        'q': city,
        'appid': API_KEY,
        'units': 'metric'
    }

    response = requests.get(BASE_URL, params=params)
    response.raise_for_status()  # 添加錯誤處理
    return response.json()

if __name__ == "__main__":
    try:
        weather = get_weather("Taipei")
        temp = weather['main']['temp']
        print(f"Temperature in Taipei: {temp}°C")
    except requests.exceptions.RequestException as e:
        print(f"Error fetching weather data: {e}")
    except KeyError:
        print("Unexpected API response format")
```

---

**建立 `.env` 檔案**:

```bash
cat > .env << EOF
# OpenWeatherMap API Key
# Get your key from: https://home.openweathermap.org/api_keys
OPENWEATHER_API_KEY=p6o5n4m3l2k1j0i9h8g7f6e5d4c3b2a1
EOF
```

---

**更新 `.gitignore`**:

```bash
# 檢查 .env 是否已在 .gitignore
grep "^\.env$" .gitignore

# 如果沒有,添加
echo ".env" >> .gitignore

# 也添加其他敏感檔案模式
cat >> .gitignore << EOF
*.key
*.pem
*.log
__pycache__/
.DS_Store
EOF
```

---

**建立 `.env.example`** (給團隊參考):

```bash
cat > .env.example << EOF
# OpenWeatherMap API Key
# Get your key from: https://home.openweathermap.org/api_keys
OPENWEATHER_API_KEY=your_api_key_here
EOF

git add .env.example
```

---

**測試**:

```bash
# 1. 安裝依賴
pip install python-dotenv requests

# 2. 測試程式
python weather.py

# 預期輸出:
# Temperature in Taipei: 25.3°C

# 3. 測試錯誤處理 (暫時移除 .env)
mv .env .env.backup
python weather.py

# 預期輸出:
# ValueError: OPENWEATHER_API_KEY not found...

# 4. 恢復 .env
mv .env.backup .env
```

---

### Step 5: 建立防護 (2 分鐘)

**方法 1: git-secrets (推薦)**

```bash
# 1. 安裝 git-secrets (如未安裝)
# macOS
brew install git-secrets

# Linux
git clone https://github.com/awslabs/git-secrets.git
cd git-secrets && sudo make install

# 2. 在專案中啟用
cd /path/to/project
git secrets --install

# 3. 添加 API key 偵測規則
git secrets --add '[a-f0-9]{32}'  # 32 字元 hex (OpenWeather 格式)
git secrets --add 'OPENWEATHER_API_KEY\s*=\s*["\'][^"\']+["\']'

# 4. 測試
echo 'API_KEY = "a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6"' > test.txt
git add test.txt
git commit -m "test"

# 預期: commit 被阻止
# [ERROR] Matched one or more prohibited patterns

# 5. 清理測試檔案
git reset HEAD test.txt
rm test.txt
```

---

**方法 2: pre-commit hook (替代方案)**

```bash
# 1. 安裝 pre-commit
pip install pre-commit

# 2. 建立配置檔案
cat > .pre-commit-config.yaml << 'EOF'
repos:
  - repo: https://github.com/Yelp/detect-secrets
    rev: v1.4.0
    hooks:
      - id: detect-secrets
        args: ['--baseline', '.secrets.baseline']

  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: detect-private-key
      - id: check-added-large-files
EOF

# 3. 安裝 hooks
pre-commit install

# 4. 建立 baseline
detect-secrets scan > .secrets.baseline

# 5. 測試
echo 'password = "test123"' > test.py
git add test.py
git commit -m "test"

# 預期: commit 被阻止
```

---

### 最終驗證清單

```bash
# ✅ 所有檢查都應該通過

# 1. API key 不在 Git 歷史中
git log -p | grep -i "a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6"
# 輸出: (無)

# 2. 舊 API key 已撤銷
# (手動確認 OpenWeatherMap 控制台)

# 3. 新 API key 在 .env 中
cat .env | grep OPENWEATHER_API_KEY
# 輸出: OPENWEATHER_API_KEY=p6o5n4m3...

# 4. .env 在 .gitignore 中
git check-ignore .env
# 輸出: .env

# 5. 程式正常運行
python weather.py
# 輸出: Temperature in Taipei: XX.X°C

# 6. git-secrets 已設置
git secrets --list
# 輸出: 顯示設置的規則

# 7. 測試防護機制
echo 'TEST_KEY="abc123def456"' > test.txt
git add test.txt
git commit -m "test"
# 輸出: [ERROR] Matched one or more prohibited patterns
```

---

## 📊 時間分配檢討

**理想時間線** (共 15 分鐘):

| 時間 | 任務 | 完成標記 |
|------|------|----------|
| 09:45 | 發現問題 | - |
| 09:47 | 評估 + 撤銷 API key | ✅ |
| 09:52 | 清理 Git 歷史 | ✅ |
| 09:55 | 修復代碼 + 測試 | ✅ |
| 09:57 | 設置防護 | ✅ |
| 10:00 | 完成,安全 push | ✅ |

**實際上**: 如果你第一次做,可能需要 25-30 分鐘,這很正常。
**目標**: 練習 2-3 次後,能在 15 分鐘內完成。

---

## 🤔 延伸思考

### 問題 1: 如果已經 push 怎麼辦?

<details>
<summary>點擊查看答案</summary>

**如果已推送到私有倉庫**:

1. 立即撤銷 API key (最高優先)
2. 清理本地歷史 (同上述步驟)
3. 強制推送: `git push --force origin main`
4. 通知團隊成員重新 clone: `rm -rf project && git clone ...`
5. 檢查 GitHub secret scanning alerts

**如果已推送到公開倉庫**:

1. 立即撤銷 API key
2. 假設 key 已被洩漏
3. 清理歷史但不依賴它能完全解決問題
4. 監控 API 使用量 24-48 小時
5. 考慮換一個新的 API 提供商帳戶

</details>

---

### 問題 2: 為什麼不能只刪除檔案再 commit?

<details>
<summary>點擊查看答案</summary>

**錯誤做法**:
```bash
rm weather.py
git add weather.py
git commit -m "Remove sensitive file"
```

**問題**:
- API key 仍然存在於 Git 歷史中 (`git log -p` 可以看到)
- 任何人 clone 倉庫後可以用 `git log -p` 找回
- GitHub secret scanning 仍會偵測到

**正確做法**:
- 必須改寫 Git 歷史 (rebase 或 BFG)
- 確保 key 完全從所有 commits 中移除

</details>

---

### 問題 3: 為什麼需要 .env.example?

<details>
<summary>點擊查看答案</summary>

**目的**:
1. 讓團隊成員知道需要哪些環境變數
2. 提供環境變數的格式範例
3. 不包含真實值,可以安全 commit

**範例**:
```
# .env.example (可以 commit)
DATABASE_URL=postgresql://user:password@localhost/dbname
OPENWEATHER_API_KEY=your_api_key_here
DEBUG=False

# .env (不可 commit,在 .gitignore 中)
DATABASE_URL=postgresql://admin:P@ssw0rd@db.company.com/production
OPENWEATHER_API_KEY=p6o5n4m3l2k1j0i9h8g7f6e5d4c3b2a1
DEBUG=True
```

**團隊協作流程**:
```bash
# 新成員 clone 專案後
git clone https://github.com/team/project.git
cd project
cp .env.example .env
# 編輯 .env,填入自己的 API keys
```

</details>

---

## 📝 經驗總結

完成這個情境後,記錄你的學習:

### 學到的技能
- [ ] 快速評估憑證洩漏的影響範圍
- [ ] 使用 `git rebase -i` 安全地修改歷史
- [ ] 設置 git-secrets 自動防護
- [ ] 正確使用環境變數管理憑證

### 遇到的困難
- 哪個步驟花費時間最多?
- 哪個 Git 操作不熟悉?
- 是否在時間限制內完成?

### 可改進之處
- 如何能更快完成?
- 還有哪些防護措施可以添加?
- 如何避免類似問題再次發生?

---

## 🎯 下一步

完成這個情境後:

1. **練習**: 再做一次,爭取在 15 分鐘內完成
2. **應用**: 在你的實際專案中設置 git-secrets
3. **分享**: 把經驗分享給團隊,幫助他們避免同樣錯誤
4. **進階**: 完成 B02 情境,學習識別更多安全漏洞

---

**記住**: 憑證洩漏是可以預防的,但一旦發生,快速正確的應對至關重要!
