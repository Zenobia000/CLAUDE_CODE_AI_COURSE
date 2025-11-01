# B01: 配置 GitHub MCP - 第一次讓 AI 自主調用 API

## 📋 情境描述

### 你遇到的問題

你是一個開源專案的維護者，每天需要處理大量的 GitHub issues 和 PRs：

**每天重複的苦力活**：
1. 打開瀏覽器 → 登入 GitHub
2. 一個個點開 issues → 複製標題和內容
3. 貼到筆記軟體或 Slack
4. 手動分類：bug / feature / question
5. 手動分配給對應的開發者
6. 重複 30 次...

**時間成本**：每天 1-2 小時浪費在這些機械性操作上。

### 你想要的解決方案

> "如果我能直接問 Claude：'有哪些新的 issues？'，它自動去 GitHub 抓資料、分析、分類，那該多好..."

這就是 **MCP（Model Context Protocol）** 的威力！

---

## 🎯 學習目標

完成本情境後，你將能夠：

- [ ] 理解 MCP 的核心概念（不是普通的 API）
- [ ] 取得並安全管理 GitHub Personal Access Token
- [ ] 配置你的第一個 MCP server
- [ ] 讓 Claude 自主調用 GitHub API
- [ ] 建立 API keys 管理的良好習慣

**時間預估**：45 分鐘
- 理解概念：10 分鐘
- 配置 MCP：15 分鐘
- 測試與驗證：15 分鐘
- 擴展實驗：5 分鐘

---

## 第一部分：理解 MCP（10 分鐘）

### MCP 不是什麼？

**❌ MCP ≠ 普通的 API 包裝**

傳統方式（REST API）：
```python
# 你需要寫程式碼
import requests

response = requests.get(
    "https://api.github.com/repos/owner/repo/issues",
    headers={"Authorization": f"token {GITHUB_TOKEN}"}
)
issues = response.json()

# 然後手動貼給 Claude
prompt = f"分析這些 issues：{issues}"
```

### MCP 是什麼？

**✅ MCP = AI 的「掛載點」**

類比 Linux 的 `mount`：
```bash
# Linux: 掛載外部磁碟
mount /dev/sdb1 /mnt/external

# 之後 /mnt/external 就像本地目錄一樣
cd /mnt/external
ls
```

**MCP 做同樣的事**：
```json
// 配置一次 GitHub MCP
{
  "mcpServers": {
    "github": { /* 配置 */ }
  }
}

// 之後，Claude 可以「像本地操作一樣」存取 GitHub
```

**關鍵差異**：
- 傳統方式：**你寫程式碼** → 調用 API → 貼給 AI
- MCP 方式：**AI 自主決定** → 需要資料時主動調用 → 動態探索

---

## 第二部分：取得 GitHub Token（15 分鐘）

### Step 1：前往 GitHub Settings

1. 登入 GitHub
2. 點擊右上角頭像 → Settings
3. 左側選單最下方 → Developer settings
4. Personal access tokens → Tokens (classic)
5. 點擊 "Generate new token (classic)"

### Step 2：配置 Token 權限

**關鍵問題**：給 Claude 多少權限？

遵循 **權限最小化原則**：

#### 場景 A：只讀取資訊（推薦新手）

```
✅ 選擇以下 scopes：
- repo:status （查看 repo 狀態）
- public_repo （存取公開 repos）
- read:user （讀取用戶資訊）
- read:org （讀取組織資訊，如果需要）

✅ 能做什麼：
- 列出 repositories
- 讀取 issues、PRs、commits
- 搜尋程式碼
- 查看 repo 統計

❌ 不能做什麼：
- 創建 issues
- 修改程式碼
- 刪除任何東西
```

#### 場景 B：可以創建 issues 和 PRs

```
✅ 額外加上：
- repo （完整 repo 控制）

⚠️ 風險：
- Claude 可以創建、修改、刪除 issues/PRs
- 需要更謹慎地使用
```

**本教學選擇**：場景 A（只讀），先確保安全。

### Step 3：生成並保存 Token

1. 設定 Expiration（過期時間）
   - **推薦**：90 days（定期輪換）
   - 避免：No expiration（不安全）

2. 點擊 "Generate token"

3. **立即複製 token**（只會顯示一次！）
   ```
   格式：ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
   ```

4. 暫時儲存到安全的地方（稍後會用到）

### Step 4：安全檢查清單

複製 token 後，立即檢查：

- [ ] Token 已複製到安全的地方？
- [ ] 沒有把 token 貼到公開的地方（Slack、Email）？
- [ ] 瀏覽器視窗已關閉（避免截圖洩漏）？
- [ ] 設定了過期時間？

---

## 第三部分：配置 MCP（15 分鐘）

### Step 1：找到或建立配置檔

**檔案位置**：`.claude/mcp-config.json`（專案根目錄）

```bash
# 檢查是否已存在
ls -la .claude/

# 如果不存在，建立它
mkdir -p .claude
touch .claude/mcp-config.json
```

### Step 2：寫入 GitHub MCP 配置

使用 Claude Code 的 Write 工具（或手動編輯）：

```json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-github"
      ],
      "env": {
        "GITHUB_TOKEN": "ghp_把你的token貼在這裡"
      }
    }
  }
}
```

**欄位說明**：

| 欄位 | 說明 | 為什麼這樣設定 |
|-----|------|--------------|
| `"github"` | 自訂的 server 名稱 | 可以隨便取，但建議用服務名稱 |
| `"command": "npx"` | 執行指令 | npx 會自動下載並執行 npm 套件 |
| `"-y"` | 自動確認 | 避免需要手動輸入 y |
| `"@modelcontextprotocol/server-github"` | 官方 GitHub MCP | Anthropic 官方維護的 MCP server |
| `"GITHUB_TOKEN"` | 環境變數 | 傳遞 token 給 MCP server |

### Step 3：確保配置檔安全

**Critical**：絕不能把 token 上傳到 Git！

```bash
# 檢查 .gitignore
cat .gitignore | grep mcp-config

# 如果沒有，加入這一行
echo ".claude/mcp-config.json" >> .gitignore
```

**驗證**：
```bash
# 這個指令應該要看不到 mcp-config.json
git status
```

### Step 4：重新啟動 Claude Code

**為什麼需要重啟？**
- Claude Code 只在啟動時讀取 MCP 配置
- 修改配置後必須重啟才會生效

**如何重啟**：
- CLI：重新執行 `claude` 指令
- VSCode Extension：重新載入視窗（Cmd/Ctrl + Shift + P → "Reload Window"）

---

## 第四部分：測試與驗證（15 分鐘）

### 測試 1：基本連線測試

**指令**：
```
幫我列出我的 GitHub repositories
```

**預期結果**：
```
找到你的 repositories：
1. username/awesome-project
2. username/another-repo
3. username/learning-notes
...

每個 repo 的基本資訊：
- 星星數
- 最後更新時間
- 主要語言
```

**如果成功**：🎉 恭喜！MCP 已經正確配置！

**如果失敗**：跳到「故障排除」章節

---

### 測試 2：讀取 Issues

**指令**：
```
查看 username/awesome-project 的所有 open issues
```

**預期結果**：
```
找到 5 個 open issues：

#42: 修復登入 bug
- 作者：user123
- 建立時間：2 天前
- 標籤：bug, high-priority

#41: 新增深色模式
- 作者：user456
- 建立時間：5 天前
- 標籤：feature

...
```

**自然學到的概念**：
- ✅ Claude 自動調用了 GitHub API
- ✅ Claude 知道如何過濾 issues（state=open）
- ✅ Claude 格式化了資料讓你容易閱讀

---

### 測試 3：分析與洞察

**指令**：
```
分析這個 repo 的 issues，告訴我：
1. 最常見的問題類型
2. 哪些 issues 應該優先處理
3. 有沒有重複的問題
```

**預期結果**：
```
分析結果：

【問題類型分布】
- Bug：60% (12 個)
- Feature Request：30% (6 個)
- Question：10% (2 個)

【優先處理建議】
1. Issue #42：登入 bug（影響所有用戶）
2. Issue #38：安全漏洞（標註 security）
3. Issue #35：效能問題（多人回報）

【重複問題】
- Issue #30 和 #25 都在講同一個深色模式功能
  建議：合併為一個，關閉其中一個

【趨勢洞察】
- 最近一週 bug 回報增加 40%
- 建議：檢查最近的程式碼變更
```

**關鍵觀察**：
- ✅ Claude **主動調用** GitHub API 多次
- ✅ Claude **動態探索** 資料（可能調用了 10+ 次 API）
- ✅ Claude **自主決定** 需要什麼資訊
- ✅ 你不需要寫任何程式碼！

---

### 測試 4：多輪對話

**Round 1**：
```
You: "這個 repo 有哪些 open PRs？"

Claude: [調用 GitHub MCP，列出 3 個 open PRs]
```

**Round 2**：
```
You: "PR #15 改了哪些檔案？"

Claude: [再次調用 GitHub MCP，獲取 PR 詳細資訊]
改動的檔案：
- src/auth/login.js (34 行新增, 12 行刪除)
- tests/auth.test.js (50 行新增)
- README.md (5 行新增)
```

**Round 3**：
```
You: "這個 PR 的程式碼品質如何？"

Claude: [調用 GitHub MCP 獲取 diff，然後分析]
程式碼品質評估：
- 測試覆蓋率：良好（有新增測試）
- 程式碼風格：符合專案規範
- 潛在問題：login.js 第 45 行可能有空指標風險
- 建議：加入輸入驗證
```

**這就是 MCP 的威力**：
- 多輪對話，持續探索
- Claude 自主決定需要什麼資料
- 無縫整合到對話流程中

---

## 第五部分：常見問題與陷阱

### 問題 1：配置後沒反應

**症狀**：
```
You: "列出我的 repos"
Claude: "我無法存取你的 GitHub repositories..."
```

**診斷步驟**：

1. **檢查 MCP server 是否可執行**
```bash
npx -y @modelcontextprotocol/server-github
```
應該會啟動（不會報錯）

2. **檢查 JSON 格式**
```bash
cat .claude/mcp-config.json | jq .
```
如果報錯 → JSON 格式錯誤（檢查逗號、引號）

3. **檢查 token 是否正確**
```bash
# 測試 token 是否有效
curl -H "Authorization: token YOUR_TOKEN" https://api.github.com/user
```
如果返回 401 → token 無效或過期

4. **確認有重啟 Claude Code**
- 修改配置後必須重啟

---

### 問題 2：權限不足

**症狀**：
```
Error: 403 Forbidden
Resource not accessible by personal access token
```

**原因**：Token 權限不足

**解決方案**：
1. 回到 GitHub → Settings → Personal access tokens
2. 編輯你的 token
3. 加上需要的 scopes（如 `repo`）
4. 重新生成 token
5. 更新 `.claude/mcp-config.json`
6. 重啟 Claude Code

---

### 問題 3：Rate Limit

**症狀**：
```
Error: API rate limit exceeded
```

**原因**：GitHub API 有速率限制
- 未認證：60 次/小時
- 已認證：5000 次/小時

**通常不會遇到**（因為有 token），但如果遇到：

**解決方案**：
```
You: "檢查我的 GitHub API rate limit"

Claude: [調用 API]
Rate Limit 狀態：
- 限制：5000 次/小時
- 已使用：4950 次
- 重置時間：15 分鐘後

建議：等待 15 分鐘後再繼續
```

---

### 問題 4：Token 洩漏

**症狀**：GitHub 寄信警告 token 被公開

**立即行動**：
1. **撤銷 token**（Settings → Tokens → Revoke）
2. 生成新的 token
3. 更新配置
4. 檢查 Git 歷史是否有 token
   ```bash
   git log -p | grep "ghp_"
   ```
5. 如果有，使用 `git filter-branch` 清除歷史

**預防措施**：
- ✅ `.claude/mcp-config.json` 在 `.gitignore`
- ✅ 定期輪換 token（90 天）
- ✅ 使用權限最小化原則

---

## 第六部分：擴展挑戰（5 分鐘）

完成基礎測試後，試試這些進階操作：

### 挑戰 1：自動化 Issue 分類

```
You: "幫我把所有 open issues 分成三類：
- 緊急（有 security 或 critical 標籤）
- 重要（有 bug 或 high-priority 標籤）
- 一般（其他）

列出每一類的 issues，並給出處理建議"
```

### 挑戰 2：PR 審查助手

```
You: "審查 PR #15，檢查：
1. 是否有測試
2. 是否有文檔更新
3. 程式碼品質如何
4. 有沒有潛在的安全問題

給我一份完整的審查報告"
```

### 挑戰 3：程式碼搜尋

```
You: "在這個 repo 中搜尋所有使用 'password' 的地方
檢查是否有安全問題（如明文儲存）"
```

### 挑戰 4：貢獻者分析

```
You: "分析這個 repo 最近 3 個月的 commits
告訴我：
1. 最活躍的貢獻者
2. 主要修改的檔案
3. 程式碼變更趨勢"
```

---

## 🎓 學習檢查點

完成本情境後，檢查你是否掌握：

### 概念層面
- [ ] 理解 MCP 與傳統 API 的差異
- [ ] 知道 MCP 的「掛載」類比
- [ ] 理解 AI 主動調用 vs 被動等待

### 技能層面
- [ ] 能取得 GitHub Personal Access Token
- [ ] 能配置 `.claude/mcp-config.json`
- [ ] 能診斷常見的連線問題
- [ ] 知道如何管理 API keys 安全

### 安全層面
- [ ] 遵循權限最小化原則
- [ ] 配置檔在 `.gitignore` 中
- [ ] 設定 token 過期時間
- [ ] 知道 token 洩漏時如何處理

---

## 📚 延伸閱讀

- 理論文件：`理論/6.1_MCP協議深入.md`
- 下一步：`B02_配置Database_MCP.md`
- 進階應用：`組合級/C01_自動化週報生成系統.md`

---

## 💡 關鍵收穫

**記住這三點**：

1. **MCP ≠ API**
   - API：你寫程式碼調用
   - MCP：AI 自主決定調用

2. **安全第一**
   - 權限最小化
   - 絕不上傳 token
   - 定期輪換

3. **這只是開始**
   - 單一 MCP 就很強大
   - 多 MCP 協同更驚人（後面會學）
   - 想像一下：GitHub + Database + Slack + Notion 一起工作...

**恭喜你配置了第一個 MCP！** 🎉

現在你已經解鎖了 AI 自主工作的能力。接下來讓我們配置更多 MCP，建立完整的自動化工作流程！
