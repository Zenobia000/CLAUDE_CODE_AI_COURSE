# 進階擴展功能
# Advanced Feature Extensions

**用途**: 完成 MVP 後的可選擴展功能
**難度**: 中等到困難
**時間**: 每個功能 2-6 小時

---

## 擴展功能總覽

### 🔔 通知系統 (3 個功能)
### 👥 協作功能 (4 個功能)
### 📊 數據分析 (3 個功能)
### 🎨 UI/UX 增強 (4 個功能)
### ⚡ 性能優化 (3 個功能)
### 🔧 系統功能 (3 個功能)

**總計**: 20 個進階功能

---

## 功能難度分級

| 符號 | 難度 | 預計時間 | 適合 |
|-----|------|---------|------|
| ⭐ | 簡單 | 2-3h | 初學者 |
| ⭐⭐ | 中等 | 4-5h | 有基礎 |
| ⭐⭐⭐ | 困難 | 6-8h | 進階學習 |

---

## 🔔 通知系統

### E01: Email 通知 ⭐⭐

**功能描述**:
- 任務即將到期（1 天前）發送 Email 提醒
- 任務被分配時發送通知
- 註冊成功發送歡迎郵件

**技術方案**:
- 後端: FastAPI + `fastapi-mail`
- 定時任務: `APScheduler` (每小時檢查)
- Email 服務: Gmail SMTP / SendGrid / AWS SES

**實作步驟**:

**Step 1: 安裝依賴**
```bash
poetry add fastapi-mail apscheduler
```

**Step 2: 配置 Email**
```python
# app/config.py
class Settings(BaseSettings):
    # ... 其他配置
    MAIL_USERNAME: str
    MAIL_PASSWORD: str
    MAIL_FROM: str
    MAIL_SERVER: str = "smtp.gmail.com"
    MAIL_PORT: int = 587
```

**Step 3: 創建 Email 服務**
```python
# app/services/email_service.py
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig

conf = ConnectionConfig(
    MAIL_USERNAME=settings.MAIL_USERNAME,
    MAIL_PASSWORD=settings.MAIL_PASSWORD,
    MAIL_FROM=settings.MAIL_FROM,
    MAIL_PORT=settings.MAIL_PORT,
    MAIL_SERVER=settings.MAIL_SERVER,
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
)

async def send_task_due_reminder(user_email: str, task_title: str, due_date: date):
    message = MessageSchema(
        subject=f"任務即將到期: {task_title}",
        recipients=[user_email],
        body=f"你的任務「{task_title}」將在 {due_date} 到期，請盡快處理。",
        subtype="html"
    )
    fm = FastMail(conf)
    await fm.send_message(message)
```

**Step 4: 定時任務**
```python
# app/scheduler.py
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime, timedelta

scheduler = AsyncIOScheduler()

@scheduler.scheduled_job('cron', hour=9)  # 每天早上 9 點
async def check_due_tasks():
    # 查詢明天到期的任務
    tomorrow = datetime.now().date() + timedelta(days=1)
    tasks = await db.query(Task).filter(Task.due_date == tomorrow).all()

    for task in tasks:
        user = await db.query(User).filter(User.id == task.created_by).first()
        await send_task_due_reminder(user.email, task.title, task.due_date)
```

**Step 5: 啟動 Scheduler**
```python
# app/main.py
from app.scheduler import scheduler

@app.on_event("startup")
async def startup_event():
    scheduler.start()
```

**測試方法**:
```bash
# 手動觸發測試
curl -X POST http://localhost:8000/api/test/send-email \
  -H "Authorization: Bearer <token>"
```

**業務價值**: 提升用戶參與度，減少任務遺忘
**學習重點**: 定時任務、異步 Email 發送
**關聯模組**: Module 11 (實戰綜合)

---

### E02: 瀏覽器推送通知 ⭐⭐

**功能描述**:
- 使用 Web Push API 發送瀏覽器通知
- 任務狀態變更時即時通知
- 用戶可訂閱/取消訂閱

**技術方案**:
- 前端: Web Push API
- 後端: `pywebpush`
- Service Worker

**實作步驟**:

**Step 1: 生成 VAPID Keys**
```bash
poetry add pywebpush
python -c "from pywebpush import webpush, generate_vapid_keys; print(generate_vapid_keys())"
# 保存到 .env
```

**Step 2: 前端訂閱**
```javascript
// src/services/pushService.js
export const subscribeToPush = async () => {
  const registration = await navigator.serviceWorker.ready;
  const subscription = await registration.pushManager.subscribe({
    userVisibleOnly: true,
    applicationServerKey: VAPID_PUBLIC_KEY
  });

  // 發送訂閱資訊到後端
  await api.post('/api/push/subscribe', subscription.toJSON());
};
```

**Step 3: 後端發送推送**
```python
# app/services/push_service.py
from pywebpush import webpush, WebPushException

def send_push_notification(subscription_info, message):
    try:
        webpush(
            subscription_info=subscription_info,
            data=message,
            vapid_private_key=settings.VAPID_PRIVATE_KEY,
            vapid_claims={"sub": f"mailto:{settings.MAIL_FROM}"}
        )
    except WebPushException as e:
        print(f"Push failed: {e}")
```

**業務價值**: 即時性強，用戶體驗佳
**學習重點**: Web Push API, Service Worker
**關聯模組**: 前端進階技術

---

### E03: 應用內通知中心 ⭐

**功能描述**:
- 通知列表頁面（類似 GitHub Notifications）
- 未讀通知數量顯示
- 標記為已讀/全部已讀

**技術方案**:
- 新增 Notification 數據表
- API: GET /api/notifications, PATCH /api/notifications/:id/read

**實作步驟**:

**Step 1: 數據模型**
```python
# models/notification.py
class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    title = Column(String(200))
    message = Column(Text)
    type = Column(Enum("info", "warning", "success"))
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
```

**Step 2: API Endpoints**
```python
@router.get("/notifications")
async def get_notifications(
    unread_only: bool = False,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    query = db.query(Notification).filter(Notification.user_id == current_user.id)
    if unread_only:
        query = query.filter(Notification.is_read == False)
    notifications = query.order_by(Notification.created_at.desc()).all()
    return notifications

@router.patch("/notifications/{notification_id}/read")
async def mark_as_read(
    notification_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    notification = db.query(Notification).filter(
        Notification.id == notification_id,
        Notification.user_id == current_user.id
    ).first()
    if not notification:
        raise HTTPException(404)
    notification.is_read = True
    db.commit()
    return {"message": "Marked as read"}
```

**Step 3: 前端 UI**
```javascript
// components/Notifications/NotificationBell.jsx
const NotificationBell = () => {
  const [unreadCount, setUnreadCount] = useState(0);

  useEffect(() => {
    const fetchUnread = async () => {
      const response = await api.get('/api/notifications?unread_only=true');
      setUnreadCount(response.data.length);
    };
    fetchUnread();
    const interval = setInterval(fetchUnread, 30000);  // 每 30 秒刷新
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="notification-bell">
      <FaBell />
      {unreadCount > 0 && <span className="badge">{unreadCount}</span>}
    </div>
  );
};
```

**業務價值**: 用戶不會錯過重要通知
**學習重點**: 通知系統設計、輪詢 vs WebSocket
**關聯模組**: 全棧開發

---

## 👥 協作功能

### E04: 任務分配給其他用戶 ⭐⭐

**功能描述**:
- 任務可分配給其他用戶
- 被分配者可以查看和更新任務
- 任務創建者保留刪除權限

**技術方案**:
- 新增 `assigned_to` 欄位到 Task 表
- 修改權限邏輯（創建者 OR 被分配者可以操作）

**實作步驟**:

**Step 1: 數據模型更新**
```python
# models/task.py
class Task(Base):
    # ... 其他欄位
    assigned_to = Column(Integer, ForeignKey("users.id"), nullable=True)

    # 關聯關係
    creator = relationship("User", foreign_keys=[created_by])
    assignee = relationship("User", foreign_keys=[assigned_to])
```

**Step 2: API 更新**
```python
# schemas/task.py
class TaskCreate(BaseModel):
    title: str
    description: Optional[str]
    priority: TaskPriority
    due_date: Optional[date]
    assigned_to: Optional[int]  # ✅ 新增

class TaskResponse(BaseModel):
    # ... 其他欄位
    assigned_to: Optional[int]
    assignee: Optional[UserResponse]  # 完整的用戶資訊
```

**Step 3: 權限邏輯更新**
```python
# services/task_service.py
def check_task_permission(task: Task, user_id: int, action: str):
    if action == "delete":
        # 只有創建者可以刪除
        if task.created_by != user_id:
            raise HTTPException(403, "Only creator can delete task")
    elif action in ["read", "update"]:
        # 創建者或被分配者可以查看/更新
        if task.created_by != user_id and task.assigned_to != user_id:
            raise HTTPException(403, "Permission denied")
```

**Step 4: 前端 UI**
```javascript
// components/Tasks/TaskForm.jsx
const TaskForm = () => {
  const [users, setUsers] = useState([]);

  useEffect(() => {
    // 獲取可分配的用戶列表
    api.get('/api/users').then(response => setUsers(response.data));
  }, []);

  return (
    <form>
      {/* ... 其他欄位 */}
      <select name="assigned_to">
        <option value="">不分配</option>
        {users.map(user => (
          <option key={user.id} value={user.id}>{user.username}</option>
        ))}
      </select>
    </form>
  );
};
```

**業務價值**: 支援團隊協作
**學習重點**: 權限設計、多對多關係
**關聯模組**: Module 7 (DDD)

---

### E05: 任務評論功能 ⭐

**功能描述**:
- 用戶可以對任務發表評論
- 評論列表按時間排序
- 評論可以編輯和刪除

**技術方案**:
- 新增 Comment 數據表
- API: GET/POST/PUT/DELETE /api/tasks/:id/comments

**數據模型**:
```python
# models/comment.py
class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True)
    task_id = Column(Integer, ForeignKey("tasks.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)

    task = relationship("Task", back_populates="comments")
    user = relationship("User")
```

**業務價值**: 增強任務溝通
**學習重點**: 關聯數據查詢
**關聯模組**: SQL 關聯查詢

---

### E06: 任務標籤 (Tags) ⭐⭐

**功能描述**:
- 任務可以添加多個標籤（如 "bug", "feature", "urgent"）
- 按標籤過濾任務
- 標籤可以自定義顏色

**技術方案**:
- 新增 Tag 表
- Task ←→ Tag 多對多關係（關聯表 task_tags）

**數據模型**:
```python
# models/tag.py
class Tag(Base):
    __tablename__ = "tags"
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    color = Column(String(7), default="#3B82F6")  # Hex 顏色

# 關聯表
task_tags = Table('task_tags', Base.metadata,
    Column('task_id', Integer, ForeignKey('tasks.id')),
    Column('tag_id', Integer, ForeignKey('tags.id'))
)

class Task(Base):
    # ... 其他欄位
    tags = relationship("Tag", secondary=task_tags, back_populates="tasks")
```

**業務價值**: 更靈活的任務分類
**學習重點**: 多對多關係、關聯表
**關聯模組**: SQL 進階

---

### E07: 即時協作 (WebSocket) ⭐⭐⭐

**功能描述**:
- 多用戶同時查看任務時，看到即時更新
- 任務狀態變更時，其他用戶立即看到
- 使用 WebSocket 實現

**技術方案**:
- FastAPI WebSocket
- 前端: WebSocket API 或 Socket.io

**後端實作**:
```python
# app/websocket.py
from fastapi import WebSocket
from typing import List

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            await connection.send_json(message)

manager = ConnectionManager()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_json()
            # 處理數據
            await manager.broadcast({"type": "task_update", "data": data})
    except WebSocketDisconnect:
        manager.disconnect(websocket)
```

**前端實作**:
```javascript
// src/services/websocketService.js
const ws = new WebSocket('ws://localhost:8000/ws');

ws.onmessage = (event) => {
  const message = JSON.parse(event.data);
  if (message.type === 'task_update') {
    // 更新 UI
    updateTaskInList(message.data);
  }
};

ws.send(JSON.stringify({ action: 'subscribe', task_id: 123 }));
```

**業務價值**: 真正的即時協作體驗
**學習重點**: WebSocket 協議、即時通信
**關聯模組**: 前後端進階技術

---

## 📊 數據分析

### E08: 任務完成趨勢圖 ⭐⭐

**功能描述**:
- 顯示過去 30 天的任務完成數量趨勢
- 折線圖展示
- 支援按週/月聚合

**技術方案**:
- 後端: SQL GROUP BY 查詢
- 前端: Recharts / Chart.js

**API 實作**:
```python
@router.get("/analytics/completion-trend")
async def get_completion_trend(
    days: int = 30,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)

    # 查詢每天完成的任務數
    query = db.query(
        func.date(Task.updated_at).label('date'),
        func.count(Task.id).label('count')
    ).filter(
        Task.created_by == current_user.id,
        Task.status == TaskStatus.DONE,
        Task.updated_at >= start_date
    ).group_by(func.date(Task.updated_at)).all()

    return [{"date": str(row.date), "count": row.count} for row in query]
```

**前端圖表**:
```javascript
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip } from 'recharts';

const CompletionTrend = () => {
  const [data, setData] = useState([]);

  useEffect(() => {
    api.get('/api/analytics/completion-trend').then(res => setData(res.data));
  }, []);

  return (
    <LineChart width={600} height={300} data={data}>
      <CartesianGrid strokeDasharray="3 3" />
      <XAxis dataKey="date" />
      <YAxis />
      <Tooltip />
      <Line type="monotone" dataKey="count" stroke="#3B82F6" />
    </LineChart>
  );
};
```

**業務價值**: 數據驅動決策
**學習重點**: SQL 聚合查詢、圖表庫
**關聯模組**: 數據可視化

---

### E09: 任務效率報告 ⭐⭐

**功能描述**:
- 平均完成時間（從創建到完成）
- 逾期率
- 各優先級任務完成情況

**API 實作**:
```python
@router.get("/analytics/efficiency")
async def get_efficiency_report(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # 平均完成時間
    completed_tasks = db.query(Task).filter(
        Task.created_by == current_user.id,
        Task.status == TaskStatus.DONE
    ).all()

    avg_completion_time = sum([
        (task.updated_at - task.created_at).days
        for task in completed_tasks
    ]) / len(completed_tasks) if completed_tasks else 0

    # 逾期率
    total_with_due_date = db.query(Task).filter(
        Task.created_by == current_user.id,
        Task.due_date.isnot(None),
        Task.status == TaskStatus.DONE
    ).count()

    overdue_count = db.query(Task).filter(
        Task.created_by == current_user.id,
        Task.due_date < Task.updated_at,
        Task.status == TaskStatus.DONE
    ).count()

    overdue_rate = (overdue_count / total_with_due_date * 100) if total_with_due_date else 0

    return {
        "avg_completion_days": round(avg_completion_time, 1),
        "overdue_rate": round(overdue_rate, 1),
        "total_completed": len(completed_tasks)
    }
```

**業務價值**: 了解工作效率，發現瓶頸
**學習重點**: 業務指標計算
**關聯模組**: 數據分析

---

### E10: 導出報表 (Excel/PDF) ⭐⭐

**功能描述**:
- 導出任務列表為 Excel
- 生成 PDF 報告
- 支援自定義時間範圍和過濾條件

**技術方案**:
- Excel: `openpyxl` 或 `pandas`
- PDF: `ReportLab` 或 `WeasyPrint`

**實作範例**:
```python
from openpyxl import Workbook
from fastapi.responses import StreamingResponse
import io

@router.get("/export/tasks")
async def export_tasks(
    format: str = "excel",  # excel 或 pdf
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    tasks = db.query(Task).filter(Task.created_by == current_user.id).all()

    if format == "excel":
        wb = Workbook()
        ws = wb.active
        ws.append(["標題", "狀態", "優先級", "截止日期", "創建時間"])
        for task in tasks:
            ws.append([task.title, task.status.value, task.priority.value,
                      str(task.due_date), str(task.created_at)])

        stream = io.BytesIO()
        wb.save(stream)
        stream.seek(0)

        return StreamingResponse(
            stream,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={"Content-Disposition": "attachment; filename=tasks.xlsx"}
        )
```

**業務價值**: 便於離線分析和分享
**學習重點**: 文件生成、流式響應
**關聯模組**: 後端進階技術

---

## 🎨 UI/UX 增強

### E11: 拖拽式看板視圖 (Kanban) ⭐⭐⭐

**功能描述**:
- 類似 Trello 的看板界面
- 拖拽任務卡片改變狀態
- 三列: TODO / IN_PROGRESS / DONE

**技術方案**:
- React DnD 或 `react-beautiful-dnd`

**前端實作**:
```javascript
import { DragDropContext, Droppable, Draggable } from 'react-beautiful-dnd';

const KanbanBoard = () => {
  const [columns, setColumns] = useState({
    TODO: { id: 'TODO', title: '待辦', tasks: [] },
    IN_PROGRESS: { id: 'IN_PROGRESS', title: '進行中', tasks: [] },
    DONE: { id: 'DONE', title: '完成', tasks: [] }
  });

  const onDragEnd = async (result) => {
    if (!result.destination) return;

    const { source, destination, draggableId } = result;

    if (source.droppableId !== destination.droppableId) {
      // 更新任務狀態
      await api.put(`/api/tasks/${draggableId}`, {
        status: destination.droppableId
      });

      // 更新本地狀態
      // ...
    }
  };

  return (
    <DragDropContext onDragEnd={onDragEnd}>
      <div className="kanban-board">
        {Object.values(columns).map(column => (
          <Droppable key={column.id} droppableId={column.id}>
            {(provided) => (
              <div ref={provided.innerRef} {...provided.droppableProps}>
                <h2>{column.title}</h2>
                {column.tasks.map((task, index) => (
                  <Draggable key={task.id} draggableId={task.id} index={index}>
                    {(provided) => (
                      <div ref={provided.innerRef} {...provided.draggableProps} {...provided.dragHandleProps}>
                        <TaskCard task={task} />
                      </div>
                    )}
                  </Draggable>
                ))}
                {provided.placeholder}
              </div>
            )}
          </Droppable>
        ))}
      </div>
    </DragDropContext>
  );
};
```

**業務價值**: 視覺化任務流程，提升用戶體驗
**學習重點**: React 拖拽庫、狀態同步
**關聯模組**: React 進階

---

### E12: 暗色模式 (Dark Mode) ⭐

**功能描述**:
- 切換淺色/深色主題
- 記住用戶偏好
- 平滑過渡動畫

**技術方案**:
- CSS 變數 + JavaScript
- 或 Tailwind CSS Dark Mode

**實作範例**:
```javascript
// src/contexts/ThemeContext.jsx
const ThemeContext = createContext();

export const ThemeProvider = ({ children }) => {
  const [darkMode, setDarkMode] = useState(() => {
    return localStorage.getItem('darkMode') === 'true';
  });

  useEffect(() => {
    localStorage.setItem('darkMode', darkMode);
    if (darkMode) {
      document.documentElement.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
    }
  }, [darkMode]);

  return (
    <ThemeContext.Provider value={{ darkMode, setDarkMode }}>
      {children}
    </ThemeContext.Provider>
  );
};

// Tailwind CSS 配置
// tailwind.config.js
module.exports = {
  darkMode: 'class',  // 啟用 class 模式
  // ...
};

// 使用 dark: 前綴
<div className="bg-white dark:bg-gray-800 text-black dark:text-white">
```

**業務價值**: 提升用戶體驗，保護眼睛
**學習重點**: CSS 變數、主題切換
**關聯模組**: 前端 UI/UX

---

### E13: 任務搜尋功能 ⭐

**功能描述**:
- 全文搜尋任務標題和描述
- 實時搜尋（輸入時即搜尋）
- 高亮顯示匹配文字

**後端實作**:
```python
@router.get("/tasks/search")
async def search_tasks(
    q: str,  # 搜尋關鍵字
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    tasks = db.query(Task).filter(
        Task.created_by == current_user.id,
        or_(
            Task.title.ilike(f"%{q}%"),
            Task.description.ilike(f"%{q}%")
        )
    ).all()
    return tasks
```

**前端實作**:
```javascript
const SearchBar = () => {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState([]);

  useEffect(() => {
    if (query.length > 2) {  // 至少 3 個字元才搜尋
      const debounce = setTimeout(async () => {
        const res = await api.get(`/api/tasks/search?q=${query}`);
        setResults(res.data);
      }, 300);  // 300ms debounce

      return () => clearTimeout(debounce);
    }
  }, [query]);

  return (
    <input
      type="text"
      value={query}
      onChange={(e) => setQuery(e.target.value)}
      placeholder="搜尋任務..."
    />
  );
};
```

**業務價值**: 快速找到任務
**學習重點**: 全文搜尋、Debounce
**關聯模組**: 搜尋最佳實踐

---

### E14: 任務附件上傳 ⭐⭐

**功能描述**:
- 上傳圖片、PDF、文件到任務
- 顯示附件列表
- 下載附件

**技術方案**:
- 後端: FastAPI 文件上傳
- 存儲: 本地文件系統 或 AWS S3 / MinIO

**後端實作**:
```python
@router.post("/tasks/{task_id}/attachments")
async def upload_attachment(
    task_id: int,
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # 驗證任務權限
    task = await get_task_by_id(db, task_id, current_user.id)

    # 保存文件
    file_path = f"uploads/{task_id}/{file.filename}"
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    with open(file_path, "wb") as f:
        content = await file.read()
        f.write(content)

    # 創建附件記錄
    attachment = Attachment(
        task_id=task_id,
        filename=file.filename,
        file_path=file_path,
        file_size=len(content)
    )
    db.add(attachment)
    db.commit()

    return attachment
```

**業務價值**: 完整的任務信息
**學習重點**: 文件上傳、雲存儲
**關聯模組**: 後端文件處理

---

## ⚡ 性能優化

### E15: Redis 快取 ⭐⭐

**功能描述**:
- 快取熱點數據（如 Dashboard 統計）
- 減少數據庫查詢
- 設置過期時間

**技術方案**:
- Redis
- `aioredis` (異步 Redis 客戶端)

**實作範例**:
```python
import aioredis
from fastapi import Depends

async def get_redis():
    redis = await aioredis.create_redis_pool('redis://localhost')
    try:
        yield redis
    finally:
        redis.close()
        await redis.wait_closed()

@router.get("/dashboard/stats")
async def get_stats_cached(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    redis = Depends(get_redis)
):
    cache_key = f"stats:{current_user.id}"

    # 嘗試從快取讀取
    cached = await redis.get(cache_key)
    if cached:
        return json.loads(cached)

    # 快取未命中，從數據庫查詢
    stats = await calculate_stats(db, current_user.id)

    # 寫入快取（過期時間 5 分鐘）
    await redis.setex(cache_key, 300, json.dumps(stats))

    return stats
```

**業務價值**: 提升 API 響應速度 10-100 倍
**學習重點**: 快取策略、Redis
**關聯模組**: 性能優化

---

### E16: 數據庫查詢優化 ⭐⭐

**功能描述**:
- 添加索引
- N+1 查詢問題解決
- 使用 Eager Loading

**實作範例**:
```python
# ❌ N+1 問題
tasks = db.query(Task).all()
for task in tasks:
    print(task.creator.username)  # 每次都查詢數據庫

# ✅ Eager Loading
from sqlalchemy.orm import joinedload

tasks = db.query(Task).options(
    joinedload(Task.creator),
    joinedload(Task.assignee)
).all()
for task in tasks:
    print(task.creator.username)  # 不會額外查詢

# ✅ 添加索引
# models/task.py
class Task(Base):
    # ...
    __table_args__ = (
        Index('idx_created_by', 'created_by'),
        Index('idx_status', 'status'),
        Index('idx_due_date', 'due_date'),
    )
```

**業務價值**: 支援更多並發用戶
**學習重點**: SQL 優化、ORM 最佳實踐
**關聯模組**: 數據庫性能優化

---

### E17: 分頁查詢優化 ⭐

**功能描述**:
- 使用 Cursor-based Pagination 替代 Offset
- 更快的大數據量分頁

**實作範例**:
```python
@router.get("/tasks")
async def get_tasks_cursor(
    cursor: Optional[int] = None,  # 上次查詢的最後一個 task_id
    limit: int = 20,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    query = db.query(Task).filter(Task.created_by == current_user.id)

    if cursor:
        query = query.filter(Task.id < cursor)  # 查詢 id 小於 cursor 的任務

    tasks = query.order_by(Task.id.desc()).limit(limit).all()

    next_cursor = tasks[-1].id if tasks else None

    return {
        "tasks": tasks,
        "next_cursor": next_cursor,
        "has_more": len(tasks) == limit
    }
```

**業務價值**: 大數據量時仍然快速
**學習重點**: 分頁策略
**關聯模組**: 性能優化

---

## 🔧 系統功能

### E18: API 版本控制 ⭐⭐

**功能描述**:
- 支援多個 API 版本（v1, v2）
- 平滑升級，向後兼容

**實作範例**:
```python
# app/main.py
from fastapi import APIRouter

api_v1 = APIRouter(prefix="/api/v1")
api_v2 = APIRouter(prefix="/api/v2")

# v1 endpoints
@api_v1.get("/tasks")
async def get_tasks_v1():
    # 舊版 API
    pass

# v2 endpoints (新增欄位)
@api_v2.get("/tasks")
async def get_tasks_v2():
    # 新版 API，返回更多欄位
    pass

app.include_router(api_v1)
app.include_router(api_v2)
```

**業務價值**: 不破壞現有客戶端
**學習重點**: API 設計最佳實踐
**關聯模組**: RESTful API 設計

---

### E19: 日誌與監控 ⭐⭐

**功能描述**:
- 結構化日誌
- 錯誤追蹤 (Sentry)
- 效能監控 (Prometheus)

**實作範例**:
```python
import logging
from pythonjsonlogger import jsonlogger

# 結構化日誌
logHandler = logging.StreamHandler()
formatter = jsonlogger.JsonFormatter()
logHandler.setFormatter(formatter)
logger = logging.getLogger()
logger.addHandler(logHandler)

# 使用
logger.info("User logged in", extra={"user_id": user.id, "ip": request.client.host})

# Sentry 集成
import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration

sentry_sdk.init(
    dsn="your-sentry-dsn",
    integrations=[FastApiIntegration()],
)
```

**業務價值**: 快速定位生產環境問題
**學習重點**: 可觀測性 (Observability)
**關聯模組**: DevOps

---

### E20: 多租戶支援 (Multi-Tenancy) ⭐⭐⭐

**功能描述**:
- 支援多個組織/團隊
- 數據隔離
- 每個組織獨立的用戶和任務

**技術方案**:
- 新增 Organization 表
- 所有數據關聯到 Organization

**數據模型**:
```python
class Organization(Base):
    __tablename__ = "organizations"
    id = Column(Integer, primary_key=True)
    name = Column(String(100))

class User(Base):
    # ...
    org_id = Column(Integer, ForeignKey("organizations.id"))
    organization = relationship("Organization")

class Task(Base):
    # ...
    org_id = Column(Integer, ForeignKey("organizations.id"))
```

**權限檢查**:
```python
def check_org_permission(resource, user):
    if resource.org_id != user.org_id:
        raise HTTPException(403, "Cross-organization access denied")
```

**業務價值**: 產品 SaaS 化
**學習重點**: 多租戶架構
**關聯模組**: 企業級架構

---

## 選擇建議

### 如果你時間有限，優先做這些:

**快速提升用戶體驗** (4-6h):
- E12: 暗色模式 ⭐
- E13: 任務搜尋 ⭐
- E03: 應用內通知 ⭐

**展示技術能力** (6-8h):
- E08: 任務完成趨勢圖 ⭐⭐
- E11: Kanban 看板 ⭐⭐⭐
- E15: Redis 快取 ⭐⭐

**為求職加分** (選一個深入做):
- E07: 即時協作 (WebSocket) ⭐⭐⭐
- E20: 多租戶支援 ⭐⭐⭐

---

## 學習路徑建議

**第一週**: 完成 MVP
**第二週**: 選擇 2-3 個進階功能實作
**第三週**: 優化和部署

**記住**: 寧願做好 3 個功能，也不要做 10 個半成品！

每完成一個進階功能，都是一次**深度學習**的機會。
把它做到極致，寫成技術文章，這就是你的差異化競爭力！ 🚀
