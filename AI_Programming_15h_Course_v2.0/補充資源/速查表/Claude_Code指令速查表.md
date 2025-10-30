# Claude Code 指令速查表 - 情境驅動版

## 🎯 使用哲學

> **記住情境，而非指令**
>
> 就像 Linux 高手不會死背 `find` 的所有參數，
> 而是知道「要找檔案時用 find」，遇到具體需求再查細節。

---

## 🔥 緊急情況快速參考

### 生產環境救火
```bash
# 快速載入相關程式碼
claude --add-dir ./src/payment

# 檢查上下文使用
claude /context

# 開始多個監控任務
claude /bashes

# 生成事後報告
claude /output-style:incident-report
```

### 開源專案快速貢獻
```bash
# 理解專案
claude --add-dir ./src --add-dir ./tests
claude /agents:code-reviewer

# 生成測試
claude /agents:test-generator

# 自我審查
claude /review src/new-feature.py
claude /security-review src/new-feature.py
```

---

## 📚 按情境分類的指令

### 🗂️ 檔案與專案管理

#### 情境：整理混亂的專案資料夾
```bash
# 基本操作（不需要特殊指令）
提示詞：請整理 ./downloads 資料夾：
1. 按檔案類型分類
2. 找出重複檔案
3. 給我建議，等我確認後執行
```

#### 情境：快速理解新專案
```bash
claude --add-dir ./src          # 載入主要程式碼
claude /context                 # 檢查上下文使用
claude /compact                 # 壓縮上下文（如果超載）
```

#### 情境：建立專案記憶
```bash
claude /init                    # 初始化 CLAUDE.md
claude /memory                  # 編輯專案記憶
```

### 🤖 代理人與專家模式

#### 情境：需要專業分析
```bash
claude /agents:code-reviewer    # 程式碼審查專家
claude /agents:security-auditor # 安全審計專家
claude /agents:test-generator   # 測試生成專家
claude /agents:off              # 關閉代理人模式
```

#### 情境：查看可用代理人
```bash
claude /agents                  # 管理代理人配置
```

### 🎨 輸出格式控制

#### 情境：需要特定格式的輸出
```bash
claude /output-style:detailed          # 詳細說明風格
claude /output-style:concise           # 簡潔風格
claude /output-style:api-documentation # API 文檔風格
claude /output-style:incident-report   # 事件報告風格
claude /output-style:new my-style      # 創建自訂風格
```

### 🔧 系統管理

#### 情境：管理多個背景任務
```bash
claude /bashes                  # 管理背景 Bash 終端
```

#### 情境：檢查系統狀態
```bash
claude /status                  # 顯示連接狀態
claude /cost                    # 顯示會話成本
claude /doctor                  # 診斷安裝問題
```

### 🔐 權限與安全

#### 情境：管理 Claude 的權限
```bash
claude /permissions             # 管理工具權限
claude /security-review ./src   # 安全審查
```

### 🔗 工具整合

#### 情境：整合外部工具
```bash
claude /mcp                     # 管理 MCP 伺服器
claude /ide                     # 管理 IDE 整合
claude /install-github-app      # 設置 GitHub Actions
```

### 📊 程式碼分析與審查

#### 情境：程式碼品質檢查
```bash
claude /review ./src/module.py  # 程式碼審查
claude /pr-comments #123        # 獲取 PR 評論
```

### ⚙️ 配置與客製化

#### 情境：客製化工作環境
```bash
claude /config                  # 打開配置面板
claude /model claude-3-5-sonnet # 切換 AI 模型
claude /statusline              # 配置狀態列
claude /hooks                   # 管理鉤子配置
```

### 📝 會話管理

#### 情境：管理對話歷史
```bash
claude /clear                   # 清除對話歷史
claude /compact                 # 壓縮上下文
claude /export conversation.md  # 匯出對話記錄
claude /resume session-id       # 恢復會話
```

### 🆘 幫助與故障排除

#### 情境：需要幫助
```bash
claude /help                    # 顯示所有指令
claude /release-notes           # 查看更新日誌
claude /bug                     # 提交反饋
```

### 🎮 互動模式

#### 情境：特殊輸入需求
```bash
claude /vim                     # 切換 Vim 模式
claude /terminal-setup          # 配置換行快捷鍵
```

### 👤 帳號管理

#### 情境：帳號相關操作
```bash
claude /login                   # 登入帳號
claude /logout                  # 登出帳號
claude /upgrade                 # 升級到 Max 版本
```

---

## 🐧 Linux 類比記憶法

| Claude Code 指令 | Linux 類比 | 記憶連結 |
|-----------------|-----------|---------|
| `/help` | `man` | 查手冊 |
| `--add-dir` | `source` | 載入配置 |
| `/context` | `df -h` | 檢查容量 |
| `/compact` | 清理快取 | 釋放空間 |
| `/memory` | `.bashrc` | 持久化設定 |
| `/agents:xxx` | `sudo -u xxx` | 切換使用者/角色 |
| `/mcp` | `mount` | 掛載外部系統 |
| `/bashes` | `screen`/`tmux` | 多終端管理 |
| `/clear` | `clear` | 清除螢幕 |
| `/status` | `ps`/`top` | 檢查進程狀態 |

---

## 🚀 常用指令組合

### 新專案 onboarding 流程
```bash
claude /init                    # 1. 初始化記憶
claude --add-dir ./src          # 2. 載入程式碼
claude /context                 # 3. 檢查容量
# 4. 分析並更新記憶
claude /memory                  # 5. 保存理解
```

### 程式碼審查完整流程
```bash
claude /agents:code-reviewer    # 1. 切換審查模式
claude /review ./src/new-file.py # 2. 程式碼審查
claude /security-review ./src   # 3. 安全審查
claude /output-style:report     # 4. 生成報告
```

### 緊急救火流程
```bash
claude --add-dir ./problem-area # 1. 載入相關程式碼
claude /bashes                  # 2. 開始監控
# 3. 分析問題和解決方案
claude /output-style:incident-report # 4. 生成報告
claude /memory                  # 5. 記錄教訓
```

### 開源貢獻流程
```bash
claude /init                    # 1. 專案記憶
claude --add-dir ./src ./tests  # 2. 載入程式碼
claude /agents:code-reviewer    # 3. 學習風格
claude /agents:test-generator   # 4. 生成測試
claude /agents:off              # 5. 實作功能
claude /review ./my-code.py     # 6. 自我審查
claude /output-style:pr-description # 7. PR 描述
```

---

## ⌨️ 快捷鍵速查

### 基礎操作
| 快捷鍵 | 功能 |
|--------|------|
| `Ctrl+C` | 取消當前輸入 |
| `Ctrl+D` | 退出會話 |
| `Ctrl+L` | 清除終端 |
| `↑` / `↓` | 瀏覽輸入歷史 |

### 多行輸入
| 系統 | 快捷鍵 |
|------|--------|
| **Windows** | `Shift + Enter` |
| **macOS** | `Option + Enter` |
| **Linux/WSL** | `\ + Enter` |

### 特殊模式
| 快捷鍵 | 功能 |
|--------|------|
| `Shift + TAB` | 開啟 Plan 模式 |
| `Shift + TAB` ×2 | 開啟思考模式 |
| `Esc + Esc` | 編輯上一條訊息 |

---

## 💡 情境記憶訣竅

### 不要這樣記（❌）
```
/agents 是用來管理代理人的指令
/mcp 是用來管理 MCP 伺服器的指令
/output-style 是用來控制輸出格式的指令
```

### 而要這樣記（✅）
```
需要專業分析 → 想到 /agents
需要連接外部系統 → 想到 /mcp
需要特定格式輸出 → 想到 /output-style

記住使用時機，而非指令定義
```

### 記憶卡片示例
```
Q: 【情境】你需要審查一個複雜的金融系統程式碼，
   涉及多種安全考量。你會怎麼做？

A: 1. 切換到安全專家：/agents:security-auditor
   2. 執行安全審查：/security-review ./src
   3. 生成專業報告：/output-style:security-report
   4. 記錄發現：/memory

記憶點：專業任務 → 專業 agent → 專業格式
```

---

## 🔍 故障排除

### 常見問題快速解決

#### 上下文超出限制
```bash
claude /context                # 檢查使用情況
claude /compact                # 壓縮上下文
# 或
claude /clear                  # 重新開始
```

#### API 金鑰問題
```bash
claude /doctor                 # 診斷問題
claude /logout                 # 登出
claude /login                  # 重新登入
```

#### 回應速度慢
```bash
claude /model claude-3-haiku   # 切換更快的模型
claude /status                 # 檢查服務狀態
```

#### 指令不工作
```bash
claude /help                   # 確認指令名稱
claude /doctor                 # 診斷安裝問題
claude --version               # 檢查版本
```

---

## 📈 學習建議

### 漸進式學習路徑

#### 第1週：基礎指令
- 專注於檔案操作和專案理解
- 重點：`--add-dir`, `/context`, `/memory`

#### 第2週：進階功能
- 學習代理人和輸出控制
- 重點：`/agents`, `/output-style`, `/review`

#### 第3週：整合應用
- 掌握工作流程編排
- 重點：指令組合、MCP 整合

### 實踐建議
1. **每天使用**：將 Claude Code 整合到日常工作
2. **記錄問題**：遇到問題時記錄解決過程
3. **分享經驗**：與團隊分享有用的指令組合
4. **持續學習**：關注新功能和最佳實踐

---

**版本**：v2.0 情境驅動版
**更新日期**：2025年1月
**維護者**：AI 編程課程開發團隊

---

💡 **提示**：將此速查表加入書籤，或列印出來放在桌邊！