# 模組 10: 安全與最佳實踐

> **核心問題**: AI 輔助開發時,如何避免引入安全漏洞與隱私風險?
>
> **學習時數**: 0.5 小時核心內容 + 1 小時實作練習
>
> **課程權重**: 2%

---

## 模組概述

### 為什麼需要這個模組?

**真實事件**: 2023 年,某新創公司使用 ChatGPT 生成 API 整合代碼,直接採用了 AI 建議的範例代碼,其中包含硬編碼的 AWS 憑證。代碼被推送到公開 GitHub 倉庫後,兩小時內被掃描機器人發現,導致 $50,000 的雲端資源被盜用。

這不是個案。AI 工具強大的代碼生成能力,也帶來了新的安全風險:

- AI 生成的代碼可能包含常見安全漏洞
- 開發者容易過度信任 AI,跳過安全審查
- 與 AI 共享上下文時可能洩漏敏感資訊
- AI 訓練數據中的不安全模式被複製

**核心原則**: "驗證優於信任" (Verify over Trust)

就像 Linux 的 `sudo` 命令 — 賦予你強大權力的同時,也要求你承擔相應的責任。AI 輔助開發亦然。

---

## 學習目標

完成本模組後,你將能夠:

1. **識別風險**: 快速辨識 AI 生成代碼中的常見安全漏洞
2. **建立防線**: 在開發工作流中建立安全檢查點
3. **保護隱私**: 知道什麼資訊不該與 AI 共享
4. **應急處理**: 當安全事件發生時,知道如何快速應對

---

## 核心理念: 三層安全防護

本模組採用「三層防禦」架構:

```
┌─────────────────────────────────────────────┐
│  第一層: 代碼安全 (Code Security)           │
│  ─────────────────────────────────────────  │
│  • 識別 AI 生成的安全漏洞                   │
│  • 使用靜態分析工具掃描                     │
│  • 建立安全編碼檢查清單                     │
└─────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────┐
│  第二層: 數據隱私 (Data Privacy)            │
│  ─────────────────────────────────────────  │
│  • 識別敏感資訊類型                         │
│  • 在與 AI 互動前清理上下文                 │
│  • 遵守企業合規要求                         │
└─────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────┐
│  第三層: 工作流安全 (Workflow Safety)       │
│  ─────────────────────────────────────────  │
│  • 設置 pre-commit 鉤子                     │
│  • 使用 git-secrets 防止憑證洩漏            │
│  • 建立安全事件應急流程                     │
└─────────────────────────────────────────────┘
```

---

## 模組結構

### 理論內容 (0.3h)

1. **10.1 AI 生成代碼安全風險** (`理論/10.1_AI生成代碼安全風險.md`)
   - Top 5 AI 生成的安全漏洞
   - 真實案例分析
   - 驗證清單與檢測方法

2. **10.2 隱私與合規實踐** (`理論/10.2_隱私與合規實踐.md`)
   - 什麼資訊不該與 AI 共享
   - GDPR 與 License 合規考量
   - 3-Step 安全工作流

### 實踐工具 (0.2h)

3. **快速檢查清單** (`快速檢查清單/`)
   - Pre-Commit 安全檢查清單 (可列印版本)
   - AI 上下文清理指南
   - 安全事件應急模板

4. **工具整合指南** (`工具整合/`)
   - `git-secrets` 快速設置 (5 分鐘)
   - `pre-commit` 鉤子配置 (10 分鐘)
   - `semgrep` 安全規則 (15 分鐘)

### 情境練習

5. **情境題庫** (`情境題庫/`)
   - **基礎級** (2 題): 單一安全風險識別與修復
   - **組合級** (1 題): 綜合安全審計流程

6. **案例分析** (`案例分析/真實安全事件.md`)
   - 3 個真實世界的 AI 相關安全事件
   - 根本原因分析
   - 預防策略總結

### 記憶強化

7. **記憶卡庫** (`記憶卡庫/`)
   - 10 張情境式 Anki 閃卡
   - 聚焦於風險識別與應急反應

---

## 真實案例: ChatGPT API Key 洩漏事件

### 事件經過

**2023 年 3 月**,一名開發者在使用 ChatGPT 開發 Discord 機器人時:

1. **第一步**: 詢問 ChatGPT 如何連接 Discord API
2. **第二步**: AI 回覆包含範例代碼,其中有 `TOKEN = "your-token-here"`
3. **第三步**: 開發者直接複製代碼,並將真實 token 填入
4. **第四步**: 提交到 GitHub,並推送到公開倉庫
5. **第五步**: 15 分鐘內,自動掃描機器人發現該 token
6. **第六步**: 攻擊者使用該 token 控制機器人發送垃圾訊息

### 根本原因

- ❌ **過度信任 AI**: 直接使用範例代碼,未經安全審查
- ❌ **缺乏安全意識**: 不知道 token 應該用環境變數
- ❌ **無防護機制**: 沒有設置 git-secrets 或 pre-commit 鉤子
- ❌ **應急準備不足**: 事件發生後不知如何快速撤銷 token

### 正確做法

```python
# ❌ 錯誤做法 (AI 常見建議)
TOKEN = "MTA1NzYwNzk5ODg4MjM2NTQ4MA.GxYz..."
client.run(TOKEN)

# ✅ 正確做法
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
if not TOKEN:
    raise ValueError("DISCORD_TOKEN not found in environment")
client.run(TOKEN)
```

**防護措施**:
1. 使用 `.env` 檔案存儲 token
2. 確保 `.env` 在 `.gitignore` 中
3. 設置 `git-secrets` 掃描 commit
4. 在 CI/CD 中集成安全掃描

### 學到的教訓

> **「AI 生成的代碼像是別人給你的 sudo 密碼 — 在使用前必須驗證它的安全性」**

這個事件催生了本模組的核心原則: **驗證優於信任**。

---

## Linux 學習類比: `sudo` 與安全意識

在 Linux 學習中,`sudo` 是一個關鍵轉折點:

```bash
# 新手階段: 不理解為什麼需要 sudo
$ rm /var/log/important.log
Permission denied

# 學習階段: 知道 sudo 能解決問題,但不理解風險
$ sudo rm -rf /var/log/*
# 糟糕... 刪除了重要日誌

# 成熟階段: 理解權限是保護機制,謹慎使用 sudo
$ sudo -v  # 先驗證權限
$ sudo rm /var/log/old.log  # 只刪除特定檔案
$ sudo -k  # 用完立即撤銷權限
```

**AI 輔助開發的安全意識亦然**:

| 階段 | Linux (`sudo`) | AI 開發 |
|------|----------------|---------|
| **新手** | 不理解為何需要權限 | 直接複製 AI 代碼,不檢查安全性 |
| **學習** | 知道 `sudo` 但濫用 | 知道要檢查,但不知道檢查什麼 |
| **成熟** | 謹慎使用 sudo,理解風險 | 建立驗證流程,使用自動化工具 |

本模組的目標: **將你從「新手」推進到「成熟」階段**。

---

## 學習路徑

### 第一階段: 認識風險 (0.15h)

**目標**: 識別 AI 生成代碼中的 Top 5 安全漏洞

1. 閱讀 `理論/10.1_AI生成代碼安全風險.md`
2. 重點關注:
   - 硬編碼憑證
   - SQL 注入
   - 路徑遍歷
   - 不安全的反序列化
   - 過度權限

**驗證點**: 能在 5 分鐘內識別這 5 種漏洞

---

### 第二階段: 建立防線 (0.15h)

**目標**: 設置自動化安全檢查工具

1. 閱讀 `理論/10.2_隱私與合規實踐.md`
2. 設置工具:
   - `git-secrets` (5 分鐘)
   - `pre-commit` hooks (10 分鐘)
   - `semgrep` 規則 (15 分鐘)

**驗證點**: 當你嘗試 commit 含有 `API_KEY = "sk-..."` 的代碼時,commit 會被阻止

---

### 第三階段: 實戰演練 (1h)

**目標**: 通過情境題鞏固知識

1. 完成 `情境題庫/基礎級/` 的 2 個情境
2. 完成 `情境題庫/組合級/` 的 1 個綜合情境
3. 閱讀 `案例分析/真實安全事件.md` 學習實戰經驗

**驗證點**: 能獨立完成一次完整的安全審計流程

---

## 核心清單: 使用 AI 前必問的 5 個問題

在接受 AI 生成的代碼前,逐項檢查:

### 1. 是否有硬編碼的憑證?

```python
# ⚠️ 危險信號
password = "admin123"
api_key = "sk-proj-..."
db_url = "postgresql://user:pass@localhost"

# ✅ 安全做法
password = os.getenv('DB_PASSWORD')
api_key = os.getenv('OPENAI_API_KEY')
db_url = os.getenv('DATABASE_URL')
```

---

### 2. 是否有 SQL 注入風險?

```python
# ⚠️ 危險信號
query = f"SELECT * FROM users WHERE name = '{user_input}'"

# ✅ 安全做法
query = "SELECT * FROM users WHERE name = %s"
cursor.execute(query, (user_input,))
```

---

### 3. 是否有路徑遍歷風險?

```python
# ⚠️ 危險信號
file_path = f"/uploads/{filename}"
with open(file_path) as f:
    content = f.read()

# ✅ 安全做法
from pathlib import Path
safe_path = Path("/uploads") / filename
if not safe_path.resolve().is_relative_to(Path("/uploads")):
    raise ValueError("Invalid file path")
```

---

### 4. 是否使用了不安全的反序列化?

```python
# ⚠️ 危險信號
import pickle
data = pickle.loads(user_input)

# ✅ 安全做法
import json
data = json.loads(user_input)  # 或使用 pydantic 驗證
```

---

### 5. 是否有過度權限?

```bash
# ⚠️ 危險信號
chmod 777 config.json
sudo python script.py

# ✅ 安全做法
chmod 600 config.json  # 只有擁有者可讀寫
python script.py  # 不需要 sudo
```

---

## 快速參考

### 什麼資訊不該與 AI 共享?

| ❌ 絕對不可 | ⚠️ 謹慎處理 | ✅ 安全共享 |
|-------------|-------------|-------------|
| 生產環境憑證 | 程式碼結構 | 錯誤訊息 (已清理) |
| 客戶個人資料 | API 設計 | 公開文檔 |
| 內部商業邏輯 | 演算法邏輯 | 技術問題描述 |
| SSL 憑證/金鑰 | 測試數據 | 合成數據範例 |

### 安全工具快速設置

```bash
# 1. 安裝 git-secrets (5 分鐘)
git clone https://github.com/awslabs/git-secrets.git
cd git-secrets
sudo make install
git secrets --install
git secrets --register-aws

# 2. 安裝 pre-commit (2 分鐘)
pip install pre-commit
pre-commit install

# 3. 安裝 semgrep (3 分鐘)
pip install semgrep
semgrep --config auto .
```

---

## 學習成效評估

完成本模組後,你應該能夠:

- [ ] **識別風險**: 在 AI 生成的代碼中快速識別 Top 5 安全漏洞
- [ ] **建立防線**: 設置至少 2 個自動化安全工具 (git-secrets, pre-commit)
- [ ] **隱私意識**: 列舉 5 種不該與 AI 共享的資訊類型
- [ ] **應急反應**: 當發現憑證洩漏時,能在 15 分鐘內完成應急處理
- [ ] **工作流整合**: 將安全檢查嵌入日常開發流程

---

## 延伸學習資源

### 官方工具文檔
- [git-secrets](https://github.com/awslabs/git-secrets) - AWS 憑證掃描工具
- [pre-commit](https://pre-commit.com/) - Git hook 管理框架
- [semgrep](https://semgrep.dev/) - 靜態代碼分析工具
- [TruffleHog](https://github.com/trufflesecurity/trufflehog) - 歷史 commit 憑證掃描

### 安全資源
- [OWASP Top 10](https://owasp.org/www-project-top-ten/) - Web 應用常見安全風險
- [CWE Top 25](https://cwe.mitre.org/top25/) - 最危險的軟體弱點
- [Snyk Learn](https://learn.snyk.io/) - 互動式安全學習平台

### 案例研究
- [GitHub Secret Scanning](https://docs.github.com/en/code-security/secret-scanning) - GitHub 如何自動掃描洩漏的憑證
- [NPM Package Vulnerabilities](https://socket.dev/) - npm 套件安全追蹤

---

## 下一步

完成本模組後,建議你:

1. **立即行動**: 在你的專案中設置 git-secrets 和 pre-commit
2. **建立習慣**: 每次接受 AI 代碼前,過一遍 5 個核心問題
3. **深入學習**: 閱讀 `案例分析/真實安全事件.md` 了解真實世界的教訓
4. **實戰演練**: 完成所有情境題,特別是組合級情境

---

**記住**:

> **「AI 是你的副駕駛,但你是機長 — 最終的安全責任在你身上」**

安全不是一次性的任務,而是持續的實踐。每一行代碼,每一次 commit,都是培養安全意識的機會。

從今天開始,讓「驗證優於信任」成為你的本能反應。
