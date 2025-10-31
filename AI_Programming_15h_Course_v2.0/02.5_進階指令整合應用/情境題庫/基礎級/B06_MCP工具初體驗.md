# B06：MCP 工具初體驗 - 外部世界的橋樑

## 🎯 學習目標

**知識目標**：
- [ ] 理解 MCP (Model Context Protocol) 的概念
- [ ] 掌握 MCP server 的基本配置
- [ ] 了解 Claude Code 與外部工具的整合能力

**技能目標**：
- [ ] 能配置並使用第一個 MCP server
- [ ] 能通過 MCP 操作外部系統
- [ ] 能理解 MCP 與普通工具的差異

**時間估計**：30-35 分鐘

---

## 📋 情境描述

### 背景故事
你正在開發一個專案，需要經常操作檔案系統、查詢網路資訊，以及與 GitHub 互動。每次都要離開 Claude Code 去使用其他工具很麻煩，你想試試看能否直接在 Claude Code 中完成這些操作。

### 問題陳述
你需要完成以下任務，但希望都在 Claude Code 中完成：
1. 檢查專案檔案結構
2. 搜尋網路上的技術資訊
3. 操作 GitHub repository
4. 管理本地檔案

傳統方式需要：
- 終端機命令
- 瀏覽器搜尋
- GitHub 網頁介面
- 檔案管理器

### 任務要求
1. 配置 MCP servers 連接外部工具
2. 體驗通過 Claude Code 操作外部系統
3. 理解 MCP 的便利性和局限性
4. 完成實際的檔案和網路操作任務

---

## 🛠️ 實作步驟

### 步驟 1：理解 MCP 概念
```bash
claude
```

**提示詞**：
```
在開始實作之前，請解釋：

1. 什麼是 MCP (Model Context Protocol)？
2. MCP 與傳統的 API 調用有什麼差異？
3. 為什麼 Claude Code 需要 MCP？
4. MCP 能為我提供什麼價值？

請用類比的方式幫我理解這個概念。
```

### 步驟 2：檢查可用的 MCP Servers
**提示詞**：
```
請列出目前可用的 MCP servers，並説明：

1. 每個 server 的主要功能
2. 適用的使用場景
3. 配置的複雜程度
4. 推薦新手先試用哪幾個

我想先從最簡單的開始學習。
```

### 步驟 3：配置第一個 MCP Server（檔案系統）

**設定檔案系統 MCP**：
```bash
# 檢查是否已安裝
claude --mcp-list

# 如果沒有，需要配置 MCP servers
```

**提示詞**：
```
請幫我配置檔案系統 MCP server，我想要能夠：

1. 瀏覽檔案和目錄
2. 讀取檔案內容
3. 創建和修改檔案
4. 搜尋檔案

請提供詳細的配置步驟，並確保配置成功。
```

### 步驟 4：測試檔案系統操作

**提示詞**：
```
現在請使用 MCP 幫我完成以下檔案操作：

1. 創建一個測試專案目錄：./mcp_test_project
2. 在其中創建以下結構：
   ```
   mcp_test_project/
   ├── src/
   │   ├── main.py
   │   └── utils.py
   ├── tests/
   │   └── test_main.py
   ├── README.md
   └── requirements.txt
   ```

3. 在 main.py 中寫一個簡單的 Hello World 程式
4. 在 README.md 中寫專案說明
5. 列出整個專案的檔案樹狀結構

請全程使用 MCP 檔案操作，不要讓我手動創建檔案。
```

### 步驟 5：配置網路搜尋 MCP

**提示詞**：
```
現在請幫我配置網路搜尋 MCP server，我想要能夠：

1. 搜尋最新的技術資訊
2. 查詢程式設計相關問題
3. 獲取官方文檔資訊

然後使用這個 MCP 搜尋以下內容：
- "Python 3.12 新功能"
- "FastAPI vs Flask 2024 比較"
- "Claude Code MCP servers 列表"

請展示搜尋結果，並說明與普通搜尋的差異。
```

### 步驟 6：整合操作體驗

**提示詞**：
```
結合檔案系統和網路搜尋 MCP，請幫我完成：

1. 搜尋 "Python 專案最佳實踐 2024"
2. 基於搜尋結果，優化我們剛創建的專案結構
3. 添加適當的配置檔案（如 .gitignore, pyproject.toml）
4. 在 README.md 中添加最佳實踐的相關內容
5. 創建一個簡單的測試檔案

這個過程展示了 MCP 如何將外部資訊無縫整合到檔案操作中。
```

---

## ✅ 成功檢查點

完成此情境後，你應該能夠：

**理解檢查點**：
- [ ] 我理解 MCP 的基本概念和價值
- [ ] 我知道 MCP 與傳統工具調用的差異
- [ ] 我明白 Claude Code 如何成為「平台」而非「工具」

**技能檢查點**：
- [ ] 我成功配置了至少一個 MCP server
- [ ] 我能通過 Claude Code 操作外部系統
- [ ] 我能組合多個 MCP 完成複雜任務

**實戰檢查點**：
- [ ] 我創建了完整的專案結構
- [ ] 我搜尋並應用了外部資訊
- [ ] 我體驗到了整合工作流程的便利性

---

## 🎓 學習收穫

### 核心概念
1. **MCP 的本質**：不是簡單的 API 封裝，而是讓 AI 能「感知」和「操作」外部世界
2. **整合的價值**：減少上下文切換，保持工作流程的連續性
3. **平台思維**：Claude Code 變成了統一的操作介面

### MCP vs 傳統方式對比

| 操作 | 傳統方式 | MCP 方式 |
|------|---------|---------|
| 檔案操作 | 終端機 + 編輯器 | 自然語言描述 |
| 網路搜尋 | 瀏覽器 + 複製貼上 | 直接整合到工作流程 |
| 工具切換 | 多個應用程式 | 單一介面 |
| 上下文保持 | 手動記憶 | 自動維護 |

### 實用場景
1. **開發工作流程**：檔案操作 + 程式碼生成 + 文檔查詢
2. **學習研究**：資訊搜尋 + 筆記整理 + 知識整合
3. **專案管理**：任務追蹤 + 檔案組織 + 進度報告

---

## 🚀 進階挑戰

### 挑戰 1：多 MCP 協作
**提示詞**：
```
配置並整合以下 MCP servers：
1. GitHub MCP - 操作 repository
2. Database MCP - 查詢資料
3. Slack MCP - 團隊溝通

然後設計一個工作流程：
- 從 GitHub 獲取 issue 列表
- 查詢相關的資料庫記錄
- 向 Slack 發送進度更新

展示多個系統的無縫整合。
```

### 挑戰 2：自訂 MCP Server
**提示詞**：
```
假設我想創建一個自訂的 MCP server 來管理：
- 個人待辦事項
- 時間追蹤
- 學習進度

請設計：
1. MCP server 的功能規格
2. 實作架構
3. 與 Claude Code 的整合方式
4. 使用範例

這展示了 MCP 的擴展性。
```

### 挑戰 3：工作流程自動化
**提示詞**：
```
設計一個完整的「每日工作流程」自動化：

早上：
- 檢查 Email（Email MCP）
- 查看日曆（Calendar MCP）
- 獲取天氣資訊（Weather MCP）
- 生成每日計畫

下午：
- 檢查專案進度（GitHub MCP）
- 更新任務狀態（Project Management MCP）
- 整理學習筆記（File System MCP）

展示 MCP 如何改變工作方式。
```

---

## 📚 相關資源

**MCP 相關**：
- [MCP 官方文檔](https://modelcontextprotocol.io/)
- [Available MCP Servers](https://github.com/modelcontextprotocol/servers)
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)

**社群資源**：
- [MCP Server 列表](https://github.com/awesome-mcp/awesome-mcp)
- [自訂 MCP 教學](https://docs.anthropic.com/en/docs/build-with-claude/tool-use)

**後續學習**：
- B07：指令組合入門 - 結合 Agent + MCP
- C05：複雜 MCP 工作流程設計

---

## 💭 反思問題

1. **效率提升**：使用 MCP 與傳統工具切換相比，效率提升了多少？
2. **學習曲線**：MCP 的學習成本 vs 長期收益，你怎麼看？
3. **依賴考量**：過度依賴 MCP 是否會有風險？
4. **未來想像**：你還希望有哪些 MCP servers？

---

## 🔗 與前面情境的連結

**能力擴展軌跡**：
- B01-B05：掌握不同 Agent 的專業能力
- **B06**：學習 MCP 整合外部工具
- B07：開始組合 Agent + MCP

**思維轉變**：
```
工具使用者 → Agent 用戶 → MCP 整合者 → 平台編排者
```

---

## 🔍 故障排除

### 常見問題
1. **MCP 配置失敗**
   ```bash
   # 檢查配置
   claude --mcp-check

   # 重新初始化
   claude --mcp-reset
   ```

2. **權限問題**
   - 確保 MCP server 有適當的系統權限
   - 檢查網路連接和 API keys

3. **效能問題**
   - 某些 MCP 操作可能較慢
   - 注意 API 速率限制

---

**完成時間記錄**：___ 分鐘
**配置成功的 MCP 數量**：___
**最有用的 MCP**：___
**筆記區域**：
```
記錄你對 MCP 的理解和使用心得...
```

---

*本情境是 Claude Code 平台能力的重要體驗，MCP 讓 AI 從「對話工具」變成「操作平台」。*