# B02：GitHub Copilot 快速上手

## 📋 情境描述

### 背景故事

你剛加入一家新創公司擔任全端工程師，公司訂閱了 GitHub Copilot，希望你能快速掌握並應用在日常開發中。你的第一個任務是開發一個簡單的待辦事項 API。

**團隊資訊**：
- 團隊規模：5 人工程團隊
- 開發環境：VS Code + GitHub Copilot
- 技術棧：Node.js + Express + MongoDB
- 時間壓力：需在 2 小時內完成基本功能

**你的狀態**：
- 有基本的 Node.js 開發經驗
- 第一次使用 GitHub Copilot
- 需要快速上手並展示效率

---

## 🎯 學習目標

完成本情境後，你將能夠：

- ✅ 快速配置和啟動 GitHub Copilot
- ✅ 掌握基本的 Copilot 快捷鍵和操作
- ✅ 理解如何提供有效的上下文給 Copilot
- ✅ 學會接受、拒絕和修改 Copilot 的建議
- ✅ 在實際開發中應用 Copilot 提升效率

---

## 📝 具體任務

### 任務 1：環境設置（15 分鐘）

**目標**：安裝並配置 GitHub Copilot

**步驟**：

1. **安裝 Copilot 擴充套件**
   ```bash
   # 在 VS Code 中
   # 1. 開啟擴充套件市場
   # 2. 搜尋 "GitHub Copilot"
   # 3. 安裝 "GitHub Copilot" 和 "GitHub Copilot Chat"
   ```

2. **登入 GitHub 帳號**
   - 點擊 VS Code 右下角的 Copilot 圖示
   - 授權 VS Code 存取 GitHub
   - 確認訂閱狀態

3. **基本配置**
   ```json
   // settings.json
   {
     "github.copilot.enable": {
       "*": true,
       "yaml": true,
       "plaintext": false,
       "markdown": true
     },
     "editor.inlineSuggest.enabled": true
   }
   ```

4. **測試 Copilot**
   - 建立新檔案 `test.js`
   - 輸入註解：`// Function to calculate fibonacci`
   - 觀察 Copilot 是否提供建議（灰色文字）

**檢查點**：
- [ ] Copilot 圖示顯示為綠色（已啟用）
- [ ] 輸入註解時能看到灰色建議
- [ ] 可以按 Tab 接受建議

---

### 任務 2：基礎操作練習（20 分鐘）

**目標**：掌握 Copilot 的基本快捷鍵和互動方式

#### 練習 1：註解驅動開發

建立 `practice.js`，嘗試以下操作：

```javascript
// Create an Express server with the following routes:
// GET /api/health - returns health status
// GET /api/users - returns list of users
// POST /api/users - creates a new user
// GET /api/users/:id - returns a user by id
// PUT /api/users/:id - updates a user
// DELETE /api/users/:id - deletes a user

// [等待 Copilot 建議]
```

**操作技巧**：
- ✅ 寫完註解後，按 Enter，等待 1-2 秒
- ✅ 如果建議合適，按 Tab 接受
- ✅ 如果想看其他選項，按 `Alt+]` 或 `Alt+[`（Windows/Linux）或 `Option+]` 或 `Option+[`（Mac）
- ✅ 如果建議不合適，按 Esc 拒絕，繼續手動編寫

#### 練習 2：程式碼補全

```javascript
// Function to validate email address using regex
function validateEmail(email) {
  // [讓 Copilot 補全]
}

// Function to hash password using bcrypt
async function hashPassword(password) {
  // [讓 Copilot 補全]
}

// Function to generate JWT token
function generateToken(userId) {
  // [讓 Copilot 補全]
}
```

#### 練習 3：測試生成

```javascript
// Given the above functions, write unit tests using Jest

// [讓 Copilot 生成測試]
```

**學習要點**：
- 註解越具體，Copilot 建議越準確
- Copilot 會參考檔案中已有的程式碼風格
- 多個相關函數會提供更好的上下文

**檢查點**：
- [ ] 能夠接受 Copilot 建議（Tab 鍵）
- [ ] 能夠瀏覽多個建議（Alt+] / Alt+[）
- [ ] 能夠拒絕不適合的建議（Esc 鍵）
- [ ] Copilot 能根據註解生成合理的程式碼

---

### 任務 3：實戰開發 - 待辦事項 API（60 分鐘）

**目標**：使用 Copilot 快速開發一個完整的 REST API

#### 步驟 1：專案初始化（10 分鐘）

```bash
mkdir todo-api
cd todo-api
npm init -y
npm install express mongoose dotenv cors
npm install --save-dev nodemon
```

建立 `.env` 檔案：
```env
PORT=3000
MONGODB_URI=mongodb://localhost:27017/todo-db
```

#### 步驟 2：設置 Express 伺服器（15 分鐘）

建立 `src/server.js`，使用 Copilot 輔助：

```javascript
// Import required modules: express, mongoose, dotenv, cors
// [讓 Copilot 補全]

// Load environment variables
// [讓 Copilot 補全]

// Create Express app
// [讓 Copilot 補全]

// Middleware setup: cors, json parser
// [讓 Copilot 補全]

// Connect to MongoDB
// [讓 Copilot 補全]

// Define routes
// [讓 Copilot 補全]

// Error handling middleware
// [讓 Copilot 補全]

// Start server
// [讓 Copilot 補全]
```

**技巧**：
- 每寫一個註解後暫停，讓 Copilot 提供建議
- 接受合理的建議，修改不合適的部分
- 保持程式碼風格一致

#### 步驟 3：建立 Todo Model（15 分鐘）

建立 `src/models/Todo.js`：

```javascript
// Import mongoose
// [讓 Copilot 補全]

// Define Todo schema with the following fields:
// - title: String, required
// - description: String
// - completed: Boolean, default false
// - priority: String, enum ['low', 'medium', 'high'], default 'medium'
// - dueDate: Date
// - createdAt: Date, default Date.now
// - updatedAt: Date
// [讓 Copilot 補全]

// Add pre-save hook to update updatedAt
// [讓 Copilot 補全]

// Export the model
// [讓 Copilot 補全]
```

#### 步驟 4：建立 Routes（20 分鐘）

建立 `src/routes/todos.js`：

```javascript
// Import express Router and Todo model
// [讓 Copilot 補全]

// GET /api/todos - Get all todos with optional filtering and sorting
// Query params: completed (boolean), priority (string), sortBy (string)
// [讓 Copilot 補全]

// GET /api/todos/:id - Get a single todo by id
// [讓 Copilot 補全]

// POST /api/todos - Create a new todo
// Body: { title, description, priority, dueDate }
// [讓 Copilot 補全]

// PUT /api/todos/:id - Update a todo
// [讓 Copilot 補全]

// DELETE /api/todos/:id - Delete a todo
// [讓 Copilot 補全]

// PATCH /api/todos/:id/toggle - Toggle completed status
// [讓 Copilot 補全]

// Export router
// [讓 Copilot 補全]
```

**Copilot 使用技巧**：
1. **逐個路由編寫**：不要一次寫完所有註解，逐個完成
2. **觀察模式**：Copilot 會學習你的程式碼風格
3. **錯誤處理**：注意 Copilot 是否包含 try-catch
4. **驗證**：檢查是否有輸入驗證

**檢查點**：
- [ ] 所有路由都有基本的錯誤處理
- [ ] 程式碼風格一致
- [ ] 包含適當的 HTTP 狀態碼
- [ ] 有輸入驗證

---

### 任務 4：程式碼審查與優化（25 分鐘）

**目標**：學習如何評估和改進 Copilot 生成的程式碼

#### 審查清單

使用以下清單檢查 Copilot 生成的程式碼：

**安全性**：
- [ ] 是否有 SQL/NoSQL 注入風險？
- [ ] 敏感資料是否正確處理？
- [ ] 是否有適當的輸入驗證？

**錯誤處理**：
- [ ] 所有非同步操作是否有 try-catch？
- [ ] 錯誤訊息是否友善且資訊充足？
- [ ] 是否正確處理邊界情況？

**效能**：
- [ ] 資料庫查詢是否優化？
- [ ] 是否有不必要的重複操作？
- [ ] 是否需要快取？

**程式碼品質**：
- [ ] 變數命名是否清晰？
- [ ] 函數是否單一職責？
- [ ] 是否有適當的註解？

#### 常見問題與修復

**問題 1：缺少錯誤處理**

Copilot 生成：
```javascript
router.get('/api/todos/:id', async (req, res) => {
  const todo = await Todo.findById(req.params.id);
  res.json(todo);
});
```

改進版本：
```javascript
router.get('/api/todos/:id', async (req, res) => {
  try {
    const todo = await Todo.findById(req.params.id);
    if (!todo) {
      return res.status(404).json({ error: 'Todo not found' });
    }
    res.json(todo);
  } catch (error) {
    res.status(500).json({ error: 'Server error', message: error.message });
  }
});
```

**問題 2：缺少輸入驗證**

Copilot 生成：
```javascript
router.post('/api/todos', async (req, res) => {
  const todo = new Todo(req.body);
  await todo.save();
  res.status(201).json(todo);
});
```

改進版本：
```javascript
router.post('/api/todos', async (req, res) => {
  try {
    // 輸入驗證
    const { title, description, priority, dueDate } = req.body;
    if (!title || title.trim() === '') {
      return res.status(400).json({ error: 'Title is required' });
    }

    const todo = new Todo({ title, description, priority, dueDate });
    await todo.save();
    res.status(201).json(todo);
  } catch (error) {
    res.status(400).json({ error: 'Invalid input', message: error.message });
  }
});
```

**問題 3：效能優化**

使用 Copilot 輔助添加索引：
```javascript
// In Todo.js model
// Add index for frequently queried fields
// [讓 Copilot 建議索引配置]
TodoSchema.index({ completed: 1, priority: 1 });
TodoSchema.index({ dueDate: 1 });
```

---

## 🎓 關鍵學習點

### Copilot 的優勢

1. **快速原型開發**
   - 能快速生成 CRUD 操作的樣板程式碼
   - 減少重複性工作
   - 本案例：2 小時完成原本需要 4-5 小時的工作

2. **程式碼風格一致性**
   - 學習專案中已有的風格
   - 保持命名規範一致
   - 減少團隊 Code Review 時間

3. **降低學習曲線**
   - 提供 API 使用範例
   - 自動補全不熟悉的語法
   - 即時學習最佳實踐

### Copilot 的限制

1. **不是萬能的**
   - ❌ 不理解業務邏輯
   - ❌ 可能生成不安全的程式碼
   - ❌ 需要人工驗證和調整

2. **需要良好的上下文**
   - 註解要清晰具體
   - 檔案結構要合理
   - 相關程式碼要在同一檔案或已開啟的檔案中

3. **仍需程式碼審查**
   - 必須檢查安全性
   - 必須驗證邏輯正確性
   - 必須確保符合專案規範

---

## ⚡ 自然學到的技能

在這個情境中，你自然學會了：

### Copilot 操作技能
- ✅ 快捷鍵：Tab（接受）、Alt+]（下一個建議）、Esc（拒絕）
- ✅ 註解驅動開發的技巧
- ✅ 如何提供有效的上下文
- ✅ 如何瀏覽和選擇多個建議

### 開發工作流程
- ✅ 從註解到程式碼的快速迭代
- ✅ 程式碼審查的系統性檢查
- ✅ 安全性和品質把關

### 決策能力
- ✅ 何時接受 Copilot 建議
- ✅ 何時需要手動修改
- ✅ 如何平衡速度和品質

---

## ✅ 檢查點與驗證

### 功能驗證

使用以下指令測試 API：

```bash
# 啟動伺服器
npm start

# 測試 Health Check
curl http://localhost:3000/api/health

# 建立待辦事項
curl -X POST http://localhost:3000/api/todos \
  -H "Content-Type: application/json" \
  -d '{"title": "Learn Copilot", "priority": "high"}'

# 獲取所有待辦事項
curl http://localhost:3000/api/todos

# 更新待辦事項
curl -X PUT http://localhost:3000/api/todos/[id] \
  -H "Content-Type: application/json" \
  -d '{"completed": true}'

# 刪除待辦事項
curl -X DELETE http://localhost:3000/api/todos/[id]
```

### 學習成果檢查

- [ ] 能夠獨立安裝和配置 Copilot
- [ ] 掌握基本快捷鍵操作
- [ ] 能夠使用註解驅動開發
- [ ] 會審查和改進 Copilot 生成的程式碼
- [ ] 理解 Copilot 的優勢和限制
- [ ] 開發效率提升至少 30%

---

## 💡 延伸練習

### 進階挑戰 1：添加認證系統

使用 Copilot 添加 JWT 認證：
```javascript
// Implement JWT authentication middleware
// - Generate token on login
// - Verify token on protected routes
// - Refresh token mechanism
```

### 進階挑戰 2：添加測試

使用 Copilot 生成測試：
```javascript
// Write integration tests for all todo endpoints using Jest and Supertest
// - Test success cases
// - Test error cases (invalid input, not found, etc.)
// - Test edge cases
```

### 進階挑戰 3：性能優化

使用 Copilot 添加快取：
```javascript
// Implement Redis caching for todo list
// - Cache GET /api/todos response
// - Invalidate cache on CREATE, UPDATE, DELETE
// - Set appropriate TTL
```

---

## 📚 參考資源

**官方文檔**：
- [GitHub Copilot Docs](https://docs.github.com/en/copilot)
- [Copilot快捷鍵](https://docs.github.com/en/copilot/getting-started-with-github-copilot)

**最佳實踐**：
- [Copilot 使用技巧](https://github.blog/2023-06-20-how-to-write-better-prompts-for-github-copilot/)
- [程式碼審查清單](https://google.github.io/eng-practices/review/)

**相關課程內容**：
- 模組 1.2：三大工具哲學對比
- 模組 3.1：GitHub Copilot 快速掌握
- 模組 3.3：工具選擇決策樹

---

**情境難度**：⭐ 基礎
**預計時間**：2 小時
**工具重點**：GitHub Copilot
**學習收穫**：快速上手 Copilot，提升日常編碼效率 30-50%
