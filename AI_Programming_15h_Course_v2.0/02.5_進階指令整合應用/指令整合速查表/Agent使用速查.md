# Agent 使用速查表

## 🚀 快速啟動

### 基本 Agent 切換
```bash
/agents:code-reviewer          # 程式碼審查專家
/agents:documentation-writer   # 文檔撰寫專家
/agents:security-auditor      # 安全審查專家
/agents:test-generator        # 測試生成專家
/agents:performance-analyzer  # 效能分析專家
/agents:off                   # 回到一般模式
```

### Agent 狀態查詢
```bash
/agents                       # 列出所有可用 Agent
/agents:current              # 查看當前 Agent
/agents:help [agent-name]    # 查看特定 Agent 說明
```

---

## 📋 專業 Agent 詳細指南

### 🔍 code-reviewer (程式碼審查專家)

**適用場景**：
- PR 審查前的自我檢查
- 程式碼品質評估
- 重構前的現狀分析
- 團隊程式碼規範檢查

**常用提示詞範本**：
```bash
/agents:code-reviewer

# 基礎審查
"請審查這個檔案的程式碼品質"

# 深度審查
"請按以下維度審查程式碼：
1. 可讀性和命名規範
2. 錯誤處理和邊界情況
3. 效能考量
4. 最佳實踐遵循
請按嚴重程度分類問題"

# 特定關注點
"重點關注這段程式碼的安全性和效能問題"
```

**預期輸出格式**：
- 問題嚴重程度分級（Critical/High/Medium/Low）
- 具體問題描述和位置
- 改進建議和範例代碼
- 最佳實踐建議

---

### 📚 documentation-writer (文檔撰寫專家)

**適用場景**：
- API 文檔生成
- README 檔案撰寫
- 技術規格說明
- 使用者手冊製作

**常用提示詞範本**：
```bash
/agents:documentation-writer

# API 文檔
"為這個 REST API 生成完整文檔，包含所有端點"

# 專案文檔
"為這個專案生成 README.md，包含：
- 專案簡介
- 安裝指南
- 使用範例
- 貢獻指南"

# 技術文檔
"撰寫這個模組的技術文檔，目標讀者是其他開發者"
```

**搭配輸出風格**：
```bash
/output-style:api-documentation    # API 文檔格式
/output-style:technical-blog       # 技術部落格格式
/output-style:tutorial            # 教學文件格式
```

---

### 🔒 security-auditor (安全審查專家)

**適用場景**：
- 上線前安全檢查
- 漏洞掃描和評估
- 安全配置審查
- 安全培訓材料準備

**常用提示詞範本**：
```bash
/agents:security-auditor

# 全面安全審查
"對這個應用進行全面安全審計，重點檢查：
1. 注入攻擊風險
2. 認證和授權機制
3. 敏感資料處理
4. 配置安全性"

# 特定漏洞檢查
"檢查這段程式碼是否存在 SQL 注入漏洞"

# 安全配置審查
"審查這個部署配置的安全性"
```

**風險評估標準**：
- **Critical**：立即修復，可能導致資料洩露
- **High**：優先修復，存在重大安全風險
- **Medium**：建議修復，有潛在安全隱患
- **Low**：可選修復，最佳實踐建議

---

### 🧪 test-generator (測試生成專家)

**適用場景**：
- TDD 測試先行開發
- 測試覆蓋率提升
- 邊界條件測試設計
- 自動化測試腳本生成

**常用提示詞範本**：
```bash
/agents:test-generator

# 基礎測試生成
"為這個函數生成完整的單元測試"

# TDD 模式
"為尚未實作的功能生成測試案例：[功能描述]"

# 邊界測試
"生成邊界條件和異常情況的測試案例"

# 整合測試
"設計這個模組的整合測試策略"
```

**測試類型覆蓋**：
- 單元測試（Unit Tests）
- 整合測試（Integration Tests）
- 端到端測試（E2E Tests）
- 效能測試（Performance Tests）

---

### ⚡ performance-analyzer (效能分析專家)

**適用場景**：
- 效能瓶頸診斷
- 程式碼優化建議
- 資源使用分析
- 擴展性評估

**常用提示詞範本**：
```bash
/agents:performance-analyzer

# 效能問題診斷
"分析這段程式碼的效能瓶頸"

# 全面效能評估
"評估這個系統的效能表現，包含：
1. 時間複雜度分析
2. 空間複雜度分析
3. I/O 操作效率
4. 並發處理能力"

# 優化建議
"提供具體的效能優化方案，包含預期提升幅度"
```

**分析維度**：
- 演算法複雜度
- 記憶體使用模式
- I/O 操作效率
- 資料庫查詢效能
- 網路請求優化

---

## 🔄 Agent 組合使用模式

### 模式 1：程式碼品質全檢
```bash
# 1. 基礎品質檢查
/agents:code-reviewer
"分析程式碼品質問題"

# 2. 安全性檢查
/agents:security-auditor
"基於程式碼審查結果，深入檢查安全問題"

# 3. 效能檢查
/agents:performance-analyzer
"分析效能瓶頸和優化機會"

# 4. 測試補強
/agents:test-generator
"為發現問題的部分生成測試案例"
```

### 模式 2：新功能開發流程
```bash
# 1. 設計階段
/agents:off
"設計 [功能] 的架構"

# 2. 測試先行
/agents:test-generator
"為新功能生成測試案例"

# 3. 實作後檢查
/agents:code-reviewer
"審查實作的程式碼品質"

# 4. 文檔產出
/agents:documentation-writer
"生成功能文檔和使用說明"
```

### 模式 3：發布前檢查
```bash
# 1. 全面安全檢查
/agents:security-auditor
"執行發布前安全審計"

# 2. 效能驗證
/agents:performance-analyzer
"確認效能指標符合要求"

# 3. 文檔完整性檢查
/agents:documentation-writer
"檢查並補完發布文檔"
```

---

## ⚠️ 常見問題與解決方案

### 問題 1：Agent 沒有按預期工作
**可能原因**：
- 提示詞不夠具體
- 上下文資訊不足
- Agent 選擇不當

**解決方案**：
```bash
# 1. 確認當前 Agent
/agents:current

# 2. 提供更具體的指令
"請按以下步驟執行..."

# 3. 提供充足的上下文
"基於以下程式碼和需求..."
```

### 問題 2：不知道該用哪個 Agent
**決策樹**：
```
需要審查程式碼？ → code-reviewer
需要寫文檔？ → documentation-writer
關注安全性？ → security-auditor
需要測試？ → test-generator
有效能問題？ → performance-analyzer
一般對話？ → /agents:off
```

### 問題 3：Agent 輸出格式不一致
**解決方案**：
```bash
# 組合使用輸出風格
/agents:security-auditor
/output-style:security-report
"執行安全審計"
```

---

## 🎯 Agent 使用最佳實踐

### 1. 明確的任務描述
```bash
❌ "幫我看看這個程式碼"
✅ "請審查這個 API 端點的程式碼品質，重點關注錯誤處理和輸入驗證"
```

### 2. 提供充足的上下文
```bash
❌ "生成測試"
✅ "為這個用戶認證模組生成測試，需要涵蓋成功登入、密碼錯誤、帳號鎖定等場景"
```

### 3. 分階段執行複雜任務
```bash
# 第一階段
/agents:code-reviewer
"先進行基礎程式碼審查"

# 第二階段
/agents:security-auditor
"基於審查結果，深入分析安全問題"
```

### 4. 記錄重要發現
```bash
# 使用 /memory 記錄重要資訊
/memory
"記錄今天發現的關鍵安全問題和解決方案"
```

---

## 📊 Agent 效率統計

| Agent | 平均節省時間 | 適用頻率 | 學習曲線 |
|-------|------------|---------|---------|
| code-reviewer | 85% | 每日 | 容易 |
| documentation-writer | 90% | 每週 | 容易 |
| security-auditor | 80% | 每月 | 中等 |
| test-generator | 75% | 每日 | 中等 |
| performance-analyzer | 70% | 每月 | 困難 |

---

## 🔗 相關速查表

- [MCP配置速查](./MCP配置速查.md) - MCP 工具整合
- [輸出風格速查](./輸出風格速查.md) - 格式控制
- [常用組合模式](./常用組合模式.md) - 工作流程範本
- [問題排查速查](./問題排查速查.md) - 故障診斷

---

**最後更新**：2025年1月
**版本**：v1.0
**維護者**：Claude Code 課程團隊