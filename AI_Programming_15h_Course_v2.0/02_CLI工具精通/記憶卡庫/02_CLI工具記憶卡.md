# 模組 2 Claude Code CLI 工具記憶卡庫

## 📋 記憶卡使用指南

本記憶卡庫採用**情境驅動**設計，不是死背指令定義，而是透過實際場景建立長期記憶。

### 記憶法原理
```
傳統記憶卡（❌）:
Q: /context 指令的作用是什麼？
A: 檢查上下文使用情況

情境式記憶卡（✅）:
Q: 【情境】你載入了一個大型專案，Claude 開始回應很慢，
   懷疑是上下文過載。如何快速診斷和解決？
A: 【解決流程】
   1. 檢查當前狀況：/context
   2. 如果接近上限，壓縮：/compact
   3. 重新載入關鍵部分：--add-dir
   【記憶點】上下文滿了 → /context 診斷 → /compact 清理
```

### 使用建議
- **間隔重複**：Day 1 → Day 2 → Day 4 → Day 7 → Day 14 → Day 30
- **情境關聯**：每張卡片對應真實工作場景
- **命令發現**：通過問題解決自然學會指令組合

---

## 🎯 記憶卡分類體系

### A. 環境設置與基礎操作（6張）
### B. 上下文管理策略（8張）
### C. 程式碼分析與理解（7張）
### D. 工作流程與自動化（6張）
### E. 問題診斷與排查（5張）
### F. 協作與記憶管理（8張）

**總計：40張情境式記憶卡**

---

## A. 環境設置與基礎操作（6張）

### A01 - 首次安裝診斷
```markdown
Q: 【情境】你剛安裝完 Claude Code，輸入 `claude` 後出現錯誤。
   需要快速驗證安裝是否成功，如何診斷？

A: 【診斷流程】
   1. 檢查版本：claude --version
   2. 驗證登入：claude /login
   3. 全面診斷：claude /doctor
   4. 查看幫助：claude /help

   【記憶點】
   安裝問題 → --version 確認 → /doctor 診斷 → /login 授權

   【Linux 類比】
   就像 `which python` 確認安裝，`python --version` 確認版本
```

### A02 - 工作目錄選擇
```markdown
Q: 【情境】你有多個專案：frontend/、backend/、mobile/
   想用 Claude Code 分析 backend 專案，如何正確啟動？

A: 【正確流程】
   1. 進入專案目錄：cd backend/
   2. 啟動 Claude Code：claude
   3. 或直接指定：claude --add-dir ./backend

   【錯誤做法】
   在根目錄啟動，會載入所有專案（上下文浪費）

   【記憶點】
   分析特定專案 → 先 cd 到專案目錄 → 再啟動 claude

   【Linux 類比】
   就像 `cd` 到目標目錄再執行命令，作用域更精確
```

### A03 - 快速任務執行
```markdown
Q: 【情境】你只想快速問一個問題，不需要進入互動模式。
   比如「這個錯誤日誌是什麼意思？」，如何操作？

A: 【直接執行】
   claude "分析這個錯誤：RuntimeError: CUDA out of memory"

   【vs 互動模式】
   claude  # 進入互動模式，適合長時間對話

   【記憶點】
   快速問題 → 直接命令列執行
   深度分析 → 進入互動模式

   【Linux 類比】
   `grep "error" log.txt` vs `less log.txt`（查看 vs 互動）
```

### A04 - 設定檔管理
```markdown
Q: 【情境】你想為不同專案設定不同的預設行為
   （如輸出風格、記憶策略），如何管理？

A: 【設定策略】
   全域設定：~/.claude/config.json
   專案設定：./CLAUDE.md（專案根目錄）

   【優先順序】
   專案 CLAUDE.md > 全域設定 > 預設值

   【記憶點】
   全域設定 → ~/.claude/
   專案設定 → ./CLAUDE.md

   【Linux 類比】
   就像 ~/.bashrc（全域）vs ./.env（專案）
```

### A05 - 指令幫助查詢
```markdown
Q: 【情境】你忘記某個指令的參數，比如 /agents 有哪些可用代理，
   如何快速查詢？

A: 【查詢方法】
   1. 一般幫助：/help
   2. 指令幫助：/help agents
   3. 列出代理：/agents:list
   4. 探索模式：/agents:? （顯示可用選項）

   【記憶點】
   不確定參數 → /help [command] 查詢
   不確定選項 → [command]:? 探索

   【Linux 類比】
   就像 `man grep` 查手冊，`ls --help` 看選項
```

### A06 - 會話管理
```markdown
Q: 【情境】你在一個長時間會話中做了很多事情，
   想保存會話記錄以便下次繼續，如何操作？

A: 【會話保存】
   1. 保存會話：/save session_name
   2. 載入會話：/load session_name
   3. 列出會話：/sessions
   4. 刪除會話：/delete session_name

   【記憶點】
   長時間工作 → /save 保存進度
   下次繼續 → /load 恢復狀態

   【Linux 類比】
   就像 `screen` 或 `tmux` 會話管理
```

---

## B. 上下文管理策略（8張）

### B01 - 上下文容量診斷
```markdown
Q: 【情境】Claude Code 回應越來越慢，懷疑上下文太大。
   如何快速診斷當前上下文使用情況？

A: 【診斷指令】
   /context

   【輸出解讀】
   ┌─ 上下文使用情況 ─┐
   │ 程式碼檔案: 150K tokens (75%)  │
   │ 對話歷史: 30K tokens (15%)    │
   │ 專案記憶: 20K tokens (10%)    │
   │ 總計: 200K / 200K tokens      │
   └─────────────────────────────┘

   【警告指標】
   - 總使用率 > 85%：需要清理
   - 單一檔案 > 50K：檔案太大

   【記憶點】
   回應慢 → /context 檢查 → 超過 85% 需清理

   【Linux 類比】
   就像 `df -h` 檢查硬碟空間使用
```

### B02 - 上下文清理策略
```markdown
Q: 【情境】/context 顯示已使用 90%，但還需要載入新檔案。
   如何在不丟失重要資訊的情況下清理？

A: 【清理策略】
   1. 壓縮對話：/compact
      - 保留關鍵結論，壓縮細節
   2. 移除檔案：/remove path/to/file
      - 移除不相關的檔案
   3. 保存記憶：/memory
      - 重要發現寫入長期記憶
   4. 重新載入：--add-dir core/
      - 重新載入核心檔案

   【清理順序】
   /memory → /compact → /remove → 重新載入

   【記憶點】
   上下文滿 → 先保存重要資訊 → 再清理空間

   【Linux 類比】
   清理硬碟：備份重要資料 → 刪除暫存 → 重新整理
```

### B03 - 選擇性檔案載入
```markdown
Q: 【情境】大型專案有 500+ 檔案，只想分析認證模組。
   如何精確載入相關檔案？

A: 【精確載入】
   1. 按目錄：--add-dir ./src/auth
   2. 按模式：--add-glob "**/*auth*.py"
   3. 按檔案類型：--add-glob "*.{py,js,ts}"
   4. 排除檔案：--ignore "tests/,docs/"

   【範例組合】
   claude --add-dir ./src/auth --add-glob "**/*.test.py" --ignore "node_modules/"

   【記憶點】
   大專案 → 精確載入相關檔案，避免噪音

   【Linux 類比】
   就像 `find ./src -name "*auth*"` 精確搜尋
```

### B04 - 動態上下文調整
```markdown
Q: 【情境】開始分析 API 模組，後來需要查看資料庫模組。
   如何在不重啟的情況下調整上下文？

A: 【動態調整】
   1. 移除當前：/remove src/api/
   2. 載入新的：/add src/database/
   3. 檢查狀態：/context
   4. 如需要，壓縮：/compact

   【最佳實踐】
   分階段分析：API → DB → Frontend
   每階段結束：/memory 記錄 → /remove 清理

   【記憶點】
   切換分析焦點 → /remove 舊的 → /add 新的

   【Linux 類比】
   就像 `umount` 舊目錄，`mount` 新目錄
```

### B05 - 記憶系統使用
```markdown
Q: 【情境】花了 2 小時分析一個複雜 bug，找到根因和解決方案。
   如何確保這個知識可以長期保存？

A: 【記憶保存】
   1. 即時記憶：/memory "Redis 連線池設定錯誤導致超時"
   2. 結構化記憶：
      /memory --category="bug-fixes" --tags="redis,timeout"
      "問題：PaymentTimeout，原因：REDIS_POOL_SIZE=5太小，解決：改為50"

   【記憶查詢】
   /recall redis timeout
   /recall --category="bug-fixes"

   【記憶點】
   重要發現 → 立即 /memory 記錄
   結構化標籤 → 方便日後查詢

   【Linux 類比】
   就像在 ~/.bash_history 記錄常用命令
```

### B06 - 專案記憶檔案
```markdown
Q: 【情境】團隊新成員需要快速了解專案架構、常見問題、編碼規範。
   如何建立完整的專案知識庫？

A: 【CLAUDE.md 結構】
   ```markdown
   # 專案記憶檔案

   ## 技術棧
   FastAPI + PostgreSQL + Redis

   ## 常見問題
   ### Q1: Redis 超時
   症狀：PaymentTimeout 錯誤
   解決：REDIS_POOL_SIZE=50

   ## 編碼規範
   - 使用 Black 格式化
   - 80% 測試覆蓋率
   ```

   【記憶點】
   團隊知識 → 寫入 CLAUDE.md → 長期保存

   【Linux 類比】
   就像專案的 README.md，記錄重要資訊
```

### B07 - 上下文優化策略
```markdown
Q: 【情境】需要同時分析前端和後端，但上下文不夠大。
   如何優化上下文使用效率？

A: 【優化策略】
   1. 分層載入：
      第一層：介面定義（API契約）
      第二層：核心邏輯實作
      第三層：詳細實作

   2. 摘要載入：
      對大檔案：/summarize large_file.py
      載入摘要而非全文

   3. 索引模式：
      /index ./src --create-summary
      建立檔案索引，需要時再載入

   【記憶點】
   專案太大 → 分層載入 → 先載入介面和核心邏輯

   【Linux 類比】
   就像 `ls` 看目錄結構，`cat` 看檔案內容
```

### B08 - 上下文持久化
```markdown
Q: 【情境】為專案建立了完美的上下文配置（檔案組合、記憶、設定），
   希望團隊成員也能使用相同配置。如何持久化和分享？

A: 【持久化方法】
   1. 上下文快照：/snapshot save project_context
   2. 載入快照：/snapshot load project_context
   3. 匯出設定：/export config project_setup.json
   4. 匯入設定：/import config project_setup.json

   【團隊分享】
   將 project_setup.json 加入版本控制
   新成員：/import config project_setup.json

   【記憶點】
   完美配置 → /snapshot 保存 → 團隊共享

   【Linux 類比】
   就像 dotfiles 分享配置檔案
```

---

## C. 程式碼分析與理解（7張）

### C01 - 快速程式碼理解
```markdown
Q: 【情境】接手一個 Python 專案，500+ 檔案，需要在 30 分鐘內
   理解核心架構和關鍵模組。如何快速切入？

A: 【快速理解流程】
   1. 載入專案：claude --add-dir ./src
   2. 架構概覽：/analyze structure
   3. 關鍵檔案：/find --type="entry-points"
   4. 依賴關係：/analyze dependencies
   5. 總結記錄：/memory

   【分析問題】
   "請分析這個專案：
   1. 主要功能是什麼？
   2. 核心模組有哪些？
   3. 資料流向如何？
   4. 入口點在哪裡？
   5. 如果要修改 XX 功能，影響哪些檔案？"

   【記憶點】
   新專案 → 先看架構 → 再看核心 → 理解資料流

   【Linux 類比】
   就像 `tree` 看結構，`ldd` 看依賴關係
```

### C02 - 程式碼搜尋與定位
```markdown
Q: 【情境】在一個大型專案中，需要找到所有處理「用戶認證」的程式碼。
   如何快速定位相關檔案和函數？

A: 【搜尋策略】
   1. 關鍵字搜尋：/grep "auth" --type="function"
   2. 模式搜尋：/grep "def.*login\|class.*Auth" --regex
   3. 檔案搜尋：/find --name "*auth*" --type="file"
   4. 符號搜尋：/symbols auth

   【精確搜尋】
   /grep "def authenticate" --context=5 --files="*.py"

   【記憶點】
   找功能 → /grep 關鍵字 → /symbols 符號 → /find 檔案

   【Linux 類比】
   就像 `grep -r "pattern"` 遞迴搜尋
```

### C03 - 函數和類別分析
```markdown
Q: 【情境】發現一個複雜的 `process_payment()` 函數，
   需要理解它的作用、參數、返回值、潛在問題。

A: 【函數分析】
   問題：
   "分析 process_payment 函數：
   1. 函數職責是什麼？
   2. 參數類型和含義？
   3. 返回值格式？
   4. 有哪些異常情況？
   5. 依賴哪些外部服務？
   6. 有什麼潛在問題？"

   【深度分析】
   /analyze function process_payment --include-callers --include-tests

   【記憶點】
   複雜函數 → 分析職責 → 看參數返回值 → 找潛在問題

   【Linux 類比】
   就像 `man function_name` 看函數說明
```

### C04 - 資料流追蹤
```markdown
Q: 【情境】用戶回報「支付後金額不對」，需要追蹤資料流：
   從前端輸入 → API → 資料庫 → 第三方服務。如何分析？

A: 【資料流追蹤】
   1. 從入口開始：/trace "/api/payment" --direction="forward"
   2. 找資料變換：/analyze data-flow --start="payment_request"
   3. 找計算邏輯：/grep "amount.*calculate\|price.*compute"
   4. 找資料庫操作：/grep "INSERT\|UPDATE.*payment"

   【分析問題】
   "追蹤支付金額計算：
   1. 前端傳送什麼資料？
   2. API 如何處理？
   3. 在哪裡計算金額？
   4. 資料庫如何儲存？
   5. 可能的錯誤點？"

   【記憶點】
   資料問題 → 追蹤完整流程 → 找計算邏輯

   【Linux 類比】
   就像 `strace` 追蹤系統調用流程
```

### C05 - 程式碼品質檢查
```markdown
Q: 【情境】Code Review 時，需要快速識別程式碼品質問題：
   重複程式碼、複雜度、安全問題、效能問題。

A: 【品質檢查】
   1. 複雜度：/analyze complexity --threshold=10
   2. 重複：/analyze duplicates --similarity=80%
   3. 安全：/analyze security --include-sql-injection
   4. 效能：/analyze performance --include-n-plus-one
   5. 覆蓋率：/analyze coverage --missing-tests

   【自動檢查】
   /review ./src/payment.py --checklist="security,performance,maintainability"

   【記憶點】
   Code Review → 自動檢查 → 重點關注高風險區域

   【Linux 類比】
   就像 `lint` 工具檢查程式碼品質
```

### C06 - API 介面分析
```markdown
Q: 【情境】需要為前端同事快速生成 API 文檔，
   包括端點、參數、回應格式、錯誤碼。

A: 【API 分析】
   1. 找端點：/analyze endpoints --framework="fastapi"
   2. 提取 schema：/extract api-schema --format="openapi"
   3. 生成文檔：/generate docs --type="api" --format="markdown"
   4. 找範例：/generate examples --endpoint="/api/payment"

   【文檔生成】
   "為所有 /api/v1/ 端點生成文檔：
   - 請求參數（類型、必填、範例）
   - 回應格式（成功、錯誤）
   - 狀態碼說明
   - 使用範例"

   【記憶點】
   API 文檔 → 自動提取 → 生成標準格式

   【Linux 類比】
   就像 `swagger` 自動生成 API 文檔
```

### C07 - 重構分析
```markdown
Q: 【情境】一個 500 行的 `UserService` 類別變得難以維護，
   需要重構，但不確定如何拆分。

A: 【重構分析】
   1. 職責分析：/analyze responsibilities UserService
   2. 依賴分析：/analyze dependencies UserService --depth=2
   3. 拆分建議：/suggest refactor UserService --pattern="single-responsibility"
   4. 影響分析：/analyze impact --if-split="UserService"

   【重構計劃】
   "分析 UserService 重構：
   1. 目前有哪些職責？
   2. 哪些可以拆分？
   3. 拆分後的類別結構？
   4. 影響哪些呼叫者？
   5. 重構步驟計劃？"

   【記憶點】
   大類別重構 → 先分析職責 → 再設計拆分 → 評估影響

   【Linux 類比】
   就像把大腳本拆分成多個小工具
```

---

## D. 工作流程與自動化（6張）

### D01 - EPCV 工作流程
```markdown
Q: 【情境】需要為專案添加新功能「用戶頭像上傳」，
   涉及前端、後端、儲存。如何系統化進行？

A: 【EPCV 流程】

   **E - Explore（探索）**
   /analyze existing-features --similar="upload,avatar,file"
   問題：現有檔案上傳如何實作？有什麼可重用的？

   **P - Plan（規劃）**
   /generate plan --feature="avatar-upload" --include="frontend,backend,storage"
   問題：需要修改哪些檔案？API 如何設計？資料庫如何調整？

   **C - Code（編碼）**
   /implement plan --step-by-step --with-tests
   問題：按計劃實作，每步都有測試驗證

   **V - Verify（驗證）**
   /test implementation --integration --security
   問題：功能正確嗎？有安全問題嗎？效能如何？

   【記憶點】
   新功能開發 → EPCV 系統化流程 → 減少遺漏

   【Linux 類比】
   就像 make 的依賴管理：探索 → 規劃 → 編譯 → 測試
```

### D02 - 自動化測試生成
```markdown
Q: 【情境】完成了 payment API 實作，需要生成完整的測試：
   單元測試、整合測試、端到端測試。

A: 【測試生成流程】
   1. 單元測試：/generate tests --type="unit" --coverage=90%
   2. 整合測試：/generate tests --type="integration" --scenarios="happy-path,edge-cases"
   3. 端到端：/generate tests --type="e2e" --user-journeys="payment-flow"
   4. 負面測試：/generate tests --type="negative" --focus="security,validation"

   【測試策略】
   問題：
   "為 payment API 生成完整測試：
   1. 測試正常支付流程
   2. 測試異常情況（餘額不足、網路錯誤）
   3. 測試安全性（SQL 注入、XSS）
   4. 測試效能（併發、大量請求）"

   【記憶點】
   新 API → 自動生成測試 → 覆蓋多種場景

   【Linux 類比】
   就像 `make test` 自動執行測試套件
```

### D03 - 程式碼審查自動化
```markdown
Q: 【情境】提交 Pull Request 前，需要自我審查程式碼：
   品質、安全、效能、可維護性。

A: 【自動審查流程】
   1. 品質檢查：/review --checklist="code-quality"
   2. 安全掃描：/review --checklist="security"
   3. 效能分析：/review --checklist="performance"
   4. 可維護性：/review --checklist="maintainability"
   5. 生成報告：/generate review-report --format="markdown"

   【審查問題】
   "審查這次修改：
   1. 有重複程式碼嗎？
   2. 有安全風險嗎？
   3. 效能是否最佳化？
   4. 程式碼是否易讀？
   5. 測試是否充分？"

   【記憶點】
   提交前 → 自動審查 → 生成報告 → 修正問題

   【Linux 類比】
   就像 `pre-commit` hooks 在提交前檢查
```

### D04 - 文檔自動生成
```markdown
Q: 【情境】完成功能開發，需要更新多種文檔：
   API 文檔、使用者手冊、開發者指南、部署說明。

A: 【文檔生成】
   1. API 文檔：/generate docs --type="api" --format="openapi"
   2. 使用者手冊：/generate docs --type="user-guide" --audience="end-user"
   3. 開發者指南：/generate docs --type="dev-guide" --include="setup,api,examples"
   4. 部署說明：/generate docs --type="deployment" --platforms="docker,k8s"

   【文檔策略】
   問題：
   "為新功能生成文檔：
   1. 使用者如何使用？
   2. 開發者如何整合？
   3. 如何部署到生產？
   4. 有什麼注意事項？"

   【記憶點】
   功能完成 → 自動生成文檔 → 減少文檔欠債

   【Linux 類比】
   就像 `make docs` 自動生成手冊
```

### D05 - 持續整合配置
```markdown
Q: 【情境】需要設定 GitHub Actions，自動執行：
   測試、程式碼品質檢查、安全掃描、部署。

A: 【CI/CD 生成】
   1. 測試管線：/generate ci --type="test" --platforms="python,node"
   2. 品質檢查：/generate ci --type="quality" --tools="eslint,pylint,sonarqube"
   3. 安全掃描：/generate ci --type="security" --tools="codeql,snyk"
   4. 部署管線：/generate ci --type="deploy" --environments="staging,production"

   【CI 配置】
   問題：
   "設定完整 CI/CD：
   1. 每次 push 執行什麼檢查？
   2. PR 合併前需要什麼條件？
   3. 如何自動部署到 staging？
   4. 生產部署需要什麼審查？"

   【記憶點】
   新專案 → 設定 CI/CD → 自動化品質保證

   【Linux 類比】
   就像 crontab 定時執行任務
```

### D06 - 專案模板生成
```markdown
Q: 【情境】需要創建新的微服務，希望遵循團隊標準：
   目錄結構、程式碼風格、測試框架、CI/CD 配置。

A: 【模板生成】
   1. 分析現有：/analyze project-structure --reference="existing-service"
   2. 生成模板：/generate template --type="microservice" --framework="fastapi"
   3. 自訂配置：/customize template --team-standards --include="linting,testing,ci"
   4. 初始化專案：/init project --from-template="team-microservice"

   【模板內容】
   問題：
   "創建微服務模板：
   1. 標準目錄結構是什麼？
   2. 需要哪些配置檔案？
   3. 預設的測試框架？
   4. CI/CD 管線設定？
   5. Docker 配置？"

   【記憶點】
   新專案 → 使用標準模板 → 確保一致性

   【Linux 類比】
   就像 cookiecutter 專案模板
```

---

## E. 問題診斷與排查（5張）

### E01 - 錯誤日誌分析
```markdown
Q: 【情境】生產環境出現大量 500 錯誤，拿到錯誤日誌檔案，
   需要快速定位問題根因。

A: 【日誌分析流程】
   1. 載入日誌：claude --add-file error.log
   2. 錯誤統計：/analyze logs --type="error" --group-by="error_type"
   3. 時間分析：/analyze logs --timeline --peak-detection
   4. 關聯分析：/analyze logs --correlate="request_id"
   5. 根因分析：/analyze root-cause --based-on="error-patterns"

   【分析問題】
   "分析這個錯誤日誌：
   1. 最常見的錯誤類型？
   2. 錯誤開始時間？
   3. 影響多少使用者？
   4. 可能的根本原因？
   5. 如何修復？"

   【記憶點】
   生產錯誤 → 分析日誌模式 → 快速定位根因

   【Linux 類比】
   就像 `grep` + `awk` 分析日誌檔案
```

### E02 - 效能瓶頸診斷
```markdown
Q: 【情境】API 回應時間從 100ms 變成 2000ms，需要找出效能瓶頸：
   資料庫、快取、網路、還是程式碼邏輯？

A: 【效能分析】
   1. 載入程式碼：claude --add-dir ./src/api
   2. 效能分析：/analyze performance --identify-bottlenecks
   3. 資料庫查詢：/analyze sql-queries --slow-queries
   4. 快取使用：/analyze cache-usage --hit-rate
   5. 併發問題：/analyze concurrency --race-conditions

   【診斷問題】
   "診斷 API 效能問題：
   1. 最耗時的操作是什麼？
   2. 資料庫查詢是否最佳化？
   3. 快取命中率如何？
   4. 有沒有 N+1 問題？
   5. 建議的優化策略？"

   【記憶點】
   效能問題 → 分析各層瓶頸 → 針對性優化

   【Linux 類比】
   就像 `top` + `iostat` 分析系統效能
```

### E03 - 記憶體洩漏排查
```markdown
Q: 【情境】長時間運行的服務記憶體使用量持續上升，
   懷疑有記憶體洩漏，如何排查？

A: 【記憶體分析】
   1. 程式碼分析：/analyze memory-usage --detect-leaks
   2. 物件生命週期：/analyze object-lifecycle --long-lived
   3. 循環引用：/analyze circular-references
   4. 快取策略：/analyze cache-strategy --unbounded-growth
   5. 第三方函式庫：/analyze dependencies --memory-leaks

   【排查問題】
   "排查記憶體洩漏：
   1. 有長期存在的物件嗎？
   2. 有循環引用嗎？
   3. 快取是否無限制增長？
   4. 第三方函式庫問題？
   5. 如何修復？"

   【記憶點】
   記憶體洩漏 → 分析物件生命週期 → 找無法釋放的引用

   【Linux 類比】
   就像 `valgrind` 檢測記憶體問題
```

### E04 - 併發問題診斷
```markdown
Q: 【情境】多用戶同時操作時偶爾出現資料不一致，
   懷疑有競態條件（race condition），如何診斷？

A: 【併發分析】
   1. 共享資源：/analyze shared-resources --critical-sections
   2. 鎖使用：/analyze locks --deadlock-potential
   3. 競態條件：/analyze race-conditions --data-races
   4. 原子操作：/analyze atomic-operations --missing-synchronization
   5. 併發模式：/analyze concurrency-patterns --thread-safety

   【診斷問題】
   "診斷併發問題：
   1. 有哪些共享資源？
   2. 鎖的使用是否正確？
   3. 有潛在的競態條件嗎？
   4. 資料庫操作是否原子？
   5. 如何確保線程安全？"

   【記憶點】
   併發問題 → 分析共享資源 → 確保正確同步

   【Linux 類比】
   就像 `strace` 追蹤系統調用的併發行為
```

### E05 - 第三方整合問題
```markdown
Q: 【情境】與第三方 API 整合後，偶爾出現超時、錯誤回應，
   需要診斷是網路問題、API 問題、還是程式碼問題？

A: 【整合診斷】
   1. 網路連線：/analyze network-calls --timeout-patterns
   2. 錯誤處理：/analyze error-handling --retry-strategy
   3. API 使用：/analyze api-usage --rate-limits
   4. 資料格式：/analyze data-format --validation
   5. 降級策略：/analyze fallback-strategy --failure-modes

   【診斷問題】
   "診斷第三方整合：
   1. 網路調用是否穩定？
   2. 錯誤處理是否完整？
   3. 是否遵守 API 限制？
   4. 資料驗證是否充分？
   5. 有降級方案嗎？"

   【記憶點】
   第三方整合 → 分析網路穩定性 → 完善錯誤處理

   【Linux 類比】
   就像 `curl` + `tcpdump` 診斷網路問題
```

---

## F. 協作與記憶管理（8張）

### F01 - 團隊知識分享
```markdown
Q: 【情境】團隊成員發現了一個重要的 bug 修復方法，
   需要分享給整個團隊並建立知識庫。

A: 【知識分享流程】
   1. 記錄發現：/memory --shared --category="bug-fixes"
   2. 生成文檔：/generate knowledge-doc --from-memory="bug-fixes"
   3. 建立模板：/template create --type="bug-report" --based-on="recent-fix"
   4. 更新 CLAUDE.md：將重要資訊加入專案記憶
   5. 通知團隊：/generate summary --for-team --highlight="critical-fixes"

   【分享模板】
   "建立團隊知識：
   ## Bug: Redis 連線池超時
   ### 症狀：PaymentTimeout 錯誤
   ### 根因：REDIS_POOL_SIZE=5 太小
   ### 解決：修改為 REDIS_POOL_SIZE=50
   ### 預防：監控連線池使用率"

   【記憶點】
   重要發現 → 記錄到共享記憶 → 生成團隊文檔

   【Linux 類比】
   就像 wiki 記錄團隊知識
```

### F02 - 程式碼審查協作
```markdown
Q: 【情境】審查同事的 Pull Request，需要提供建設性的回饋：
   找出問題、建議改進、提供範例。

A: 【審查協作】
   1. 載入 PR：claude --add-pr="https://github.com/repo/pull/123"
   2. 結構分析：/review structure --highlight-concerns
   3. 安全檢查：/review security --potential-vulnerabilities
   4. 最佳實踐：/review best-practices --suggest-improvements
   5. 生成回饋：/generate review-feedback --constructive --with-examples

   【審查重點】
   "審查這個 PR：
   1. 程式碼結構是否清晰？
   2. 有安全風險嗎？
   3. 是否遵循團隊規範？
   4. 測試是否充分？
   5. 有改進建議嗎？"

   【記憶點】
   PR 審查 → 多面向檢查 → 提供建設性回饋

   【Linux 類比】
   就像 `diff` 比較變更，但加上智慧分析
```

### F03 - 新人 Onboarding
```markdown
Q: 【情境】新同事加入，需要快速熟悉專案：
   架構、編碼規範、常見問題、開發流程。

A: 【Onboarding 套件】
   1. 專案概覽：/generate onboarding-guide --level="newcomer"
   2. 環境設定：/generate setup-guide --os="auto-detect"
   3. 常見問題：/extract faqs --from-memory="team-knowledge"
   4. 練習任務：/generate starter-tasks --difficulty="beginner"
   5. 學習路徑：/generate learning-path --role="backend-developer"

   【Onboarding 內容】
   "新人指南：
   1. 專案是做什麼的？
   2. 如何設定開發環境？
   3. 編碼規範是什麼？
   4. 第一個任務做什麼？
   5. 遇到問題找誰？"

   【記憶點】
   新人加入 → 自動生成指南 → 快速上手

   【Linux 類比】
   就像 dotfiles 一鍵設定開發環境
```

### F04 - 跨專案知識複用
```markdown
Q: 【情境】在專案 A 實作了優秀的快取策略，
   想在專案 B 複用，如何提取和適配？

A: 【知識複用】
   1. 提取模式：/extract pattern --from="project-a/cache" --type="implementation"
   2. 抽象化：/abstract pattern --remove-specific-details
   3. 適配建議：/adapt pattern --for="project-b" --constraints="different-db"
   4. 生成模板：/generate template --from-pattern --customizable
   5. 記錄知識：/memory --category="reusable-patterns" --tags="cache,performance"

   【複用流程】
   "複用快取策略：
   1. 專案 A 的核心邏輯？
   2. 可以抽象的部分？
   3. 專案 B 需要調整什麼？
   4. 如何測試適配結果？
   5. 如何避免重複工作？"

   【記憶點】
   好的實作 → 提取模式 → 跨專案複用

   【Linux 類比】
   就像創建可複用的 shell script
```

### F05 - 會議記錄與追蹤
```markdown
Q: 【情境】技術會議討論了多個議題，需要記錄決策、
   分配任務、追蹤進度。

A: 【會議管理】
   1. 記錄會議：/meeting start --topic="API redesign"
   2. 記錄決策：/decision "使用 GraphQL 替代 REST"
   3. 分配任務：/task assign --to="Alice" --deadline="2024-02-15" --description="設計 GraphQL schema"
   4. 生成摘要：/meeting summary --include="decisions,tasks,next-steps"
   5. 追蹤進度：/task status --overdue --this-week

   【會議範本】
   ```markdown
   # 技術會議記錄 - 2024-02-01

   ## 決策
   - ✅ 使用 GraphQL 替代 REST API
   - ✅ 採用 TypeScript 重構前端

   ## 任務分配
   - Alice: GraphQL schema 設計 (2/15)
   - Bob: 前端 TypeScript 遷移 (2/20)

   ## 下次會議
   - 時間：2024-02-08
   - 議題：GraphQL 實作進度檢討
   ```

   【記憶點】
   技術會議 → 記錄決策任務 → 追蹤執行進度

   【Linux 類比】
   就像 issue tracker 管理任務
```

### F06 - 文檔版本控制
```markdown
Q: 【情境】API 文檔需要跟著程式碼版本更新，
   如何確保文檔與程式碼同步？

A: 【文檔同步】
   1. 提取 API：/extract api-spec --version="current"
   2. 對比變更：/diff api-spec --previous-version
   3. 更新文檔：/update docs --based-on="api-changes"
   4. 生成 changelog：/generate changelog --api-breaking-changes
   5. 版本標記：/tag docs --version="v2.1.0" --sync-with-code

   【同步策略】
   "文檔同步檢查：
   1. API 有哪些變更？
   2. 哪些是破壞性變更？
   3. 文檔需要更新什麼？
   4. 如何通知 API 使用者？
   5. 版本號如何標記？"

   【記憶點】
   程式碼變更 → 自動更新文檔 → 維持同步

   【Linux 類比】
   就像 git hooks 在提交時自動更新
```

### F07 - 錯誤知識庫建立
```markdown
Q: 【情境】團隊經常遇到相似的錯誤，希望建立錯誤知識庫，
   方便快速查詢解決方案。

A: 【錯誤知識庫】
   1. 收集錯誤：/collect errors --from="logs,issues,support-tickets"
   2. 分類錯誤：/categorize errors --by="component,severity,frequency"
   3. 提取解決方案：/extract solutions --from="resolved-issues"
   4. 建立索引：/index error-kb --searchable
   5. 生成工具：/generate error-lookup-tool --cli-interface

   【知識庫結構】
   ```markdown
   # 錯誤知識庫

   ## 資料庫錯誤
   ### ConnectionTimeout
   **症狀**：connection timeout after 30s
   **原因**：連線池耗盡
   **解決**：增加 MAX_CONNECTIONS=50

   ## API 錯誤
   ### RateLimitExceeded
   **症狀**：429 Too Many Requests
   **原因**：超過 API 限制
   **解決**：實作 exponential backoff
   ```

   【記憶點】
   常見錯誤 → 建立知識庫 → 快速查詢解決方案

   【Linux 類比】
   就像 man pages 提供標準解決方案
```

### F08 - 技術債務追蹤
```markdown
Q: 【情境】專案累積了技術債務：過時的依賴、
   重複程式碼、缺少測試，需要系統性管理。

A: 【技術債務管理】
   1. 掃描債務：/scan technical-debt --comprehensive
   2. 評估影響：/assess impact --by="maintainability,security,performance"
   3. 優先順序：/prioritize debt --by="risk-score,effort-required"
   4. 規劃清理：/plan debt-cleanup --timeline="6-months"
   5. 追蹤進度：/track debt-reduction --monthly-report

   【債務報告】
   ```markdown
   # 技術債務報告 - 2024-02

   ## 高優先順序
   1. 過時依賴：React 16 → 18（安全風險）
   2. 缺少測試：payment 模組覆蓋率 30%

   ## 中優先順序
   3. 重複程式碼：3 個相似的驗證函數
   4. 效能問題：N+1 查詢問題

   ## 清理計劃
   - Q1: 升級 React + 增加測試
   - Q2: 重構重複程式碼
   ```

   【記憶點】
   技術債務 → 系統性掃描 → 優先順序管理

   【Linux 類比】
   就像定期清理系統垃圾和更新套件
```

---

## 📊 記憶卡使用統計

### 完成情況
- ✅ **A類 - 環境設置**：6張
- ✅ **B類 - 上下文管理**：8張
- ✅ **C類 - 程式碼分析**：7張
- ✅ **D類 - 工作流程**：6張
- ✅ **E類 - 問題診斷**：5張
- ✅ **F類 - 協作管理**：8張

**總計：40張情境式記憶卡** ✨

### 記憶強化建議

1. **每日復習**：5-10 張卡片
2. **週週實踐**：選 1-2 個情境實際操作
3. **月月總結**：回顧學習進度，調整難度
4. **季季更新**：根據實際工作需要增加新卡片

### Anki 匯入建議

這些記憶卡可以匯入 Anki 軟體：
1. 使用「基本（正面和反面）」卡片類型
2. 標籤分類：`claude-code`, `module-2`, `scenario-based`
3. 自訂 CSS 樣式突出「情境」和「解決方案」
4. 設定間隔重複參數：初始間隔 1 天，容易度 2.5

---

## 🎯 學習路徑建議

### 週次 1-2：基礎操作熟練
- 重點：A類（環境設置）+ B類（上下文管理）
- 目標：能流暢進行基本操作和上下文管理

### 週次 3-4：程式碼分析進階
- 重點：C類（程式碼分析）+ E類（問題診斷）
- 目標：能系統性分析和診斷程式碼問題

### 週次 5-6：工作流程整合
- 重點：D類（工作流程）+ F類（協作管理）
- 目標：能建立完整的開發和協作流程

記住：**不要背誦指令，要理解情境和解決思路！** 🚀