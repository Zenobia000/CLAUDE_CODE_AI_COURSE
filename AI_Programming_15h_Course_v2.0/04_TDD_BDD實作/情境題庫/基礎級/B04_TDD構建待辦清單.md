# B04：TDD 構建待辦清單

## 📋 情境描述

你要開發一個待辦事項管理系統的核心類別。這個系統需要讓用戶管理他們的日常任務，包括新增、完成、刪除和查詢任務。

**需求**：
待辦清單需要支援：
- 新增任務（標題、描述、優先級）
- 標記任務完成/未完成
- 刪除任務
- 查詢任務（全部、已完成、未完成）
- 按優先級排序
- 統計功能

**任務**：
用 TDD 方式實作這個待辦清單管理系統。

**時間估計**：40-50 分鐘

---

## 🎯 學習目標

- [ ] 掌握 CRUD 操作的 TDD 實作
- [ ] 學習狀態管理和資料結構設計
- [ ] 練習複雜查詢邏輯的測試
- [ ] 體驗完整業務功能的 TDD 開發

---

## 🛠️ 技術要求

**語言**：Python 3.11+
**測試框架**：pytest
**檔案結構**：
```
todo_list/
├── todo_list.py           # 實作檔案
├── task.py               # 任務模型
└── test_todo_list.py     # 測試檔案
```

---

## 📝 實作步驟

### 準備工作

**建立專案目錄**：
```bash
mkdir -p todo_list
cd todo_list

# 建立虛擬環境
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安裝 pytest
pip install pytest
```

**建立檔案**：
```bash
touch todo_list.py
touch task.py
touch test_todo_list.py
```

---

### 循環 1：任務模型設計

#### 🔴 RED：測試任務建立

**test_todo_list.py**：
```python
import pytest
from datetime import datetime
from task import Task
from todo_list import TodoList

def test_create_task_with_title():
    """測試建立只有標題的任務"""
    task = Task("買牛奶")

    assert task.title == "買牛奶"
    assert task.description == ""
    assert task.priority == "medium"
    assert task.is_completed is False
    assert isinstance(task.created_at, datetime)

def test_create_task_with_full_details():
    """測試建立完整詳細的任務"""
    task = Task(
        title="完成專案報告",
        description="需要包含分析和建議",
        priority="high"
    )

    assert task.title == "完成專案報告"
    assert task.description == "需要包含分析和建議"
    assert task.priority == "high"
    assert task.is_completed is False
```

**執行測試**：
```bash
$ pytest test_todo_list.py -v

FAILED - ModuleNotFoundError: No module named 'task'
```

#### 🟢 GREEN：實作任務模型

**task.py**：
```python
from datetime import datetime
from typing import Literal

Priority = Literal["low", "medium", "high"]

class Task:
    """任務模型"""

    def __init__(self, title: str, description: str = "", priority: Priority = "medium"):
        self.title = title
        self.description = description
        self.priority = priority
        self.is_completed = False
        self.created_at = datetime.now()
        self.completed_at = None

    def mark_completed(self):
        """標記任務為已完成"""
        self.is_completed = True
        self.completed_at = datetime.now()

    def mark_pending(self):
        """標記任務為未完成"""
        self.is_completed = False
        self.completed_at = None

    def __str__(self):
        status = "✓" if self.is_completed else "○"
        return f"{status} [{self.priority}] {self.title}"

    def __repr__(self):
        return f"Task('{self.title}', priority='{self.priority}', completed={self.is_completed})"
```

**執行測試**：
```bash
$ pytest test_todo_list.py -v

PASSED ✓✓
```

---

### 循環 2：待辦清單建立和新增

#### 🔴 RED：測試清單管理

**test_todo_list.py**（新增）：
```python
def test_create_empty_todo_list():
    """測試建立空的待辦清單"""
    todo_list = TodoList()

    assert len(todo_list.get_all_tasks()) == 0

def test_add_task_to_list():
    """測試新增任務到清單"""
    todo_list = TodoList()
    task = Task("測試任務")

    todo_list.add_task(task)

    tasks = todo_list.get_all_tasks()
    assert len(tasks) == 1
    assert tasks[0].title == "測試任務"

def test_add_multiple_tasks():
    """測試新增多個任務"""
    todo_list = TodoList()

    todo_list.add_task(Task("任務 1"))
    todo_list.add_task(Task("任務 2"))
    todo_list.add_task(Task("任務 3"))

    assert len(todo_list.get_all_tasks()) == 3
```

#### 🟢 GREEN：實作待辦清單

**todo_list.py**：
```python
from typing import List
from task import Task

class TodoList:
    """待辦清單管理器"""

    def __init__(self):
        self.tasks: List[Task] = []

    def add_task(self, task: Task):
        """新增任務"""
        self.tasks.append(task)

    def get_all_tasks(self) -> List[Task]:
        """取得所有任務"""
        return self.tasks.copy()
```

**執行測試**：
```bash
$ pytest test_todo_list.py -v

PASSED ✓✓✓✓✓
```

---

### 循環 3：任務完成和查詢

#### 🔴 RED：測試任務狀態管理

**test_todo_list.py**（新增）：
```python
def test_mark_task_completed():
    """測試標記任務完成"""
    todo_list = TodoList()
    task = Task("完成作業")
    todo_list.add_task(task)

    todo_list.mark_task_completed(0)

    completed_tasks = todo_list.get_completed_tasks()
    assert len(completed_tasks) == 1
    assert completed_tasks[0].is_completed is True

def test_get_pending_tasks():
    """測試取得未完成任務"""
    todo_list = TodoList()
    todo_list.add_task(Task("任務 1"))
    todo_list.add_task(Task("任務 2"))
    todo_list.mark_task_completed(0)

    pending_tasks = todo_list.get_pending_tasks()

    assert len(pending_tasks) == 1
    assert pending_tasks[0].title == "任務 2"
    assert pending_tasks[0].is_completed is False

def test_mark_task_pending():
    """測試將已完成任務標記為未完成"""
    todo_list = TodoList()
    task = Task("可重複任務")
    todo_list.add_task(task)
    todo_list.mark_task_completed(0)

    todo_list.mark_task_pending(0)

    pending_tasks = todo_list.get_pending_tasks()
    assert len(pending_tasks) == 1
    assert pending_tasks[0].is_completed is False
```

#### 🟢 GREEN：實作狀態管理

**todo_list.py**（更新）：
```python
from typing import List
from task import Task

class TodoList:
    """待辦清單管理器"""

    def __init__(self):
        self.tasks: List[Task] = []

    def add_task(self, task: Task):
        """新增任務"""
        self.tasks.append(task)

    def get_all_tasks(self) -> List[Task]:
        """取得所有任務"""
        return self.tasks.copy()

    def mark_task_completed(self, index: int):
        """標記任務為已完成"""
        if 0 <= index < len(self.tasks):
            self.tasks[index].mark_completed()

    def mark_task_pending(self, index: int):
        """標記任務為未完成"""
        if 0 <= index < len(self.tasks):
            self.tasks[index].mark_pending()

    def get_completed_tasks(self) -> List[Task]:
        """取得已完成的任務"""
        return [task for task in self.tasks if task.is_completed]

    def get_pending_tasks(self) -> List[Task]:
        """取得未完成的任務"""
        return [task for task in self.tasks if not task.is_completed]
```

**執行測試**：
```bash
$ pytest test_todo_list.py -v

PASSED ✓✓✓✓✓✓✓✓
```

---

### 循環 4：刪除任務

#### 🔴 RED：測試任務刪除

**test_todo_list.py**（新增）：
```python
def test_remove_task_by_index():
    """測試按索引刪除任務"""
    todo_list = TodoList()
    todo_list.add_task(Task("任務 1"))
    todo_list.add_task(Task("任務 2"))
    todo_list.add_task(Task("任務 3"))

    removed_task = todo_list.remove_task(1)

    assert removed_task.title == "任務 2"
    remaining_tasks = todo_list.get_all_tasks()
    assert len(remaining_tasks) == 2
    assert remaining_tasks[0].title == "任務 1"
    assert remaining_tasks[1].title == "任務 3"

def test_remove_task_invalid_index():
    """測試刪除無效索引的任務"""
    todo_list = TodoList()
    todo_list.add_task(Task("唯一任務"))

    result = todo_list.remove_task(5)

    assert result is None
    assert len(todo_list.get_all_tasks()) == 1

def test_remove_task_by_title():
    """測試按標題刪除任務"""
    todo_list = TodoList()
    todo_list.add_task(Task("買菜"))
    todo_list.add_task(Task("做飯"))

    removed = todo_list.remove_task_by_title("買菜")

    assert removed is True
    remaining_tasks = todo_list.get_all_tasks()
    assert len(remaining_tasks) == 1
    assert remaining_tasks[0].title == "做飯"
```

#### 🟢 GREEN：實作刪除功能

**todo_list.py**（更新）：
```python
def remove_task(self, index: int) -> Task:
    """按索引刪除任務"""
    if 0 <= index < len(self.tasks):
        return self.tasks.pop(index)
    return None

def remove_task_by_title(self, title: str) -> bool:
    """按標題刪除任務"""
    for i, task in enumerate(self.tasks):
        if task.title == title:
            self.tasks.pop(i)
            return True
    return False
```

**執行測試**：
```bash
$ pytest test_todo_list.py -v

PASSED ✓✓✓✓✓✓✓✓✓✓✓
```

---

### 循環 5：優先級排序和統計

#### 🔴 RED：測試排序和統計

**test_todo_list.py**（新增）：
```python
def test_sort_tasks_by_priority():
    """測試按優先級排序任務"""
    todo_list = TodoList()
    todo_list.add_task(Task("低優先級", priority="low"))
    todo_list.add_task(Task("高優先級", priority="high"))
    todo_list.add_task(Task("中優先級", priority="medium"))

    sorted_tasks = todo_list.get_tasks_by_priority()

    assert len(sorted_tasks) == 3
    assert sorted_tasks[0].priority == "high"
    assert sorted_tasks[1].priority == "medium"
    assert sorted_tasks[2].priority == "low"

def test_task_statistics():
    """測試任務統計"""
    todo_list = TodoList()
    todo_list.add_task(Task("任務 1", priority="high"))
    todo_list.add_task(Task("任務 2", priority="medium"))
    todo_list.add_task(Task("任務 3", priority="low"))
    todo_list.mark_task_completed(0)
    todo_list.mark_task_completed(1)

    stats = todo_list.get_statistics()

    assert stats["total"] == 3
    assert stats["completed"] == 2
    assert stats["pending"] == 1
    assert stats["high_priority"] == 1
    assert stats["medium_priority"] == 1
    assert stats["low_priority"] == 1

def test_get_tasks_by_priority_level():
    """測試按優先級篩選任務"""
    todo_list = TodoList()
    todo_list.add_task(Task("重要任務 1", priority="high"))
    todo_list.add_task(Task("普通任務", priority="medium"))
    todo_list.add_task(Task("重要任務 2", priority="high"))

    high_priority_tasks = todo_list.get_tasks_by_priority_level("high")

    assert len(high_priority_tasks) == 2
    assert all(task.priority == "high" for task in high_priority_tasks)
```

#### 🟢 GREEN：實作排序和統計

**todo_list.py**（更新）：
```python
def get_tasks_by_priority(self) -> List[Task]:
    """按優先級排序取得任務（高 → 中 → 低）"""
    priority_order = {"high": 0, "medium": 1, "low": 2}
    return sorted(self.tasks, key=lambda task: priority_order[task.priority])

def get_tasks_by_priority_level(self, priority: str) -> List[Task]:
    """取得指定優先級的任務"""
    return [task for task in self.tasks if task.priority == priority]

def get_statistics(self) -> dict:
    """取得任務統計資訊"""
    total = len(self.tasks)
    completed = len(self.get_completed_tasks())
    pending = len(self.get_pending_tasks())

    priority_counts = {"high": 0, "medium": 0, "low": 0}
    for task in self.tasks:
        priority_counts[task.priority] += 1

    return {
        "total": total,
        "completed": completed,
        "pending": pending,
        "high_priority": priority_counts["high"],
        "medium_priority": priority_counts["medium"],
        "low_priority": priority_counts["low"]
    }
```

**執行測試**：
```bash
$ pytest test_todo_list.py -v

PASSED ✓✓✓✓✓✓✓✓✓✓✓✓✓✓
```

---

### 🔵 REFACTOR：優化和重構

**test_todo_list.py**（重構，新增 fixture）：
```python
import pytest
from datetime import datetime
from task import Task
from todo_list import TodoList

@pytest.fixture
def empty_todo_list():
    """建立空的待辦清單"""
    return TodoList()

@pytest.fixture
def todo_list_with_tasks():
    """建立有任務的待辦清單"""
    todo_list = TodoList()
    todo_list.add_task(Task("買牛奶", priority="medium"))
    todo_list.add_task(Task("寫報告", priority="high"))
    todo_list.add_task(Task("運動", priority="low"))
    return todo_list

# 使用 fixture 重構測試...
def test_create_empty_todo_list(empty_todo_list):
    assert len(empty_todo_list.get_all_tasks()) == 0

def test_add_task_to_list(empty_todo_list):
    task = Task("測試任務")
    empty_todo_list.add_task(task)

    tasks = empty_todo_list.get_all_tasks()
    assert len(tasks) == 1
    assert tasks[0].title == "測試任務"

# ... 其他測試也可以重構
```

---

## ✅ 完整程式碼

### task.py（最終版本）

```python
from datetime import datetime
from typing import Literal, Optional

Priority = Literal["low", "medium", "high"]

class Task:
    """任務模型"""

    def __init__(self, title: str, description: str = "", priority: Priority = "medium"):
        if not title.strip():
            raise ValueError("任務標題不能為空")

        self.title = title.strip()
        self.description = description.strip()
        self.priority = priority
        self.is_completed = False
        self.created_at = datetime.now()
        self.completed_at: Optional[datetime] = None

    def mark_completed(self):
        """標記任務為已完成"""
        self.is_completed = True
        self.completed_at = datetime.now()

    def mark_pending(self):
        """標記任務為未完成"""
        self.is_completed = False
        self.completed_at = None

    def __str__(self):
        status = "✓" if self.is_completed else "○"
        return f"{status} [{self.priority}] {self.title}"

    def __repr__(self):
        return f"Task('{self.title}', priority='{self.priority}', completed={self.is_completed})"

    def __eq__(self, other):
        if not isinstance(other, Task):
            return False
        return (
            self.title == other.title and
            self.description == other.description and
            self.priority == other.priority
        )
```

### todo_list.py（最終版本）

```python
from typing import List, Optional
from task import Task, Priority

class TodoList:
    """待辦清單管理器"""

    def __init__(self):
        self.tasks: List[Task] = []

    def add_task(self, task: Task):
        """新增任務"""
        if not isinstance(task, Task):
            raise TypeError("只能新增 Task 類型的物件")
        self.tasks.append(task)

    def get_all_tasks(self) -> List[Task]:
        """取得所有任務"""
        return self.tasks.copy()

    def mark_task_completed(self, index: int) -> bool:
        """標記任務為已完成"""
        if 0 <= index < len(self.tasks):
            self.tasks[index].mark_completed()
            return True
        return False

    def mark_task_pending(self, index: int) -> bool:
        """標記任務為未完成"""
        if 0 <= index < len(self.tasks):
            self.tasks[index].mark_pending()
            return True
        return False

    def remove_task(self, index: int) -> Optional[Task]:
        """按索引刪除任務"""
        if 0 <= index < len(self.tasks):
            return self.tasks.pop(index)
        return None

    def remove_task_by_title(self, title: str) -> bool:
        """按標題刪除任務"""
        for i, task in enumerate(self.tasks):
            if task.title == title:
                self.tasks.pop(i)
                return True
        return False

    def get_completed_tasks(self) -> List[Task]:
        """取得已完成的任務"""
        return [task for task in self.tasks if task.is_completed]

    def get_pending_tasks(self) -> List[Task]:
        """取得未完成的任務"""
        return [task for task in self.tasks if not task.is_completed]

    def get_tasks_by_priority(self) -> List[Task]:
        """按優先級排序取得任務（高 → 中 → 低）"""
        priority_order = {"high": 0, "medium": 1, "low": 2}
        return sorted(self.tasks, key=lambda task: priority_order[task.priority])

    def get_tasks_by_priority_level(self, priority: Priority) -> List[Task]:
        """取得指定優先級的任務"""
        return [task for task in self.tasks if task.priority == priority]

    def get_statistics(self) -> dict:
        """取得任務統計資訊"""
        total = len(self.tasks)
        completed = len(self.get_completed_tasks())
        pending = len(self.get_pending_tasks())

        priority_counts = {"high": 0, "medium": 0, "low": 0}
        for task in self.tasks:
            priority_counts[task.priority] += 1

        return {
            "total": total,
            "completed": completed,
            "pending": pending,
            "completion_rate": completed / total if total > 0 else 0,
            "high_priority": priority_counts["high"],
            "medium_priority": priority_counts["medium"],
            "low_priority": priority_counts["low"]
        }

    def clear_completed_tasks(self) -> int:
        """清除所有已完成的任務，返回清除的數量"""
        initial_count = len(self.tasks)
        self.tasks = [task for task in self.tasks if not task.is_completed]
        return initial_count - len(self.tasks)

    def __len__(self):
        """返回任務總數"""
        return len(self.tasks)

    def __str__(self):
        """返回清單的字串表示"""
        if not self.tasks:
            return "待辦清單是空的"

        lines = ["待辦清單："]
        for i, task in enumerate(self.tasks):
            lines.append(f"{i + 1}. {task}")
        return "\n".join(lines)
```

---

## 📊 執行測試

**執行所有測試**：
```bash
$ pytest test_todo_list.py -v

================= test session starts =================
# 所有測試都應該通過
================= XX passed in X.XXs =================
```

**測試覆蓋率**：
```bash
$ pytest --cov=todo_list --cov=task --cov-report=term-missing

Name           Stmts   Miss  Cover
----------------------------------
task.py           XX      0   100%
todo_list.py      XX      0   100%
----------------------------------
TOTAL            XX      0   100%
```

---

## 🎓 學習重點

### CRUD 操作的 TDD 設計

1. **資料模型先行**：
   - 先設計 Task 模型
   - 明確定義資料結構
   - 包含必要的驗證

2. **逐步建構功能**：
   - Create（新增）→ Read（查詢）→ Update（更新）→ Delete（刪除）
   - 每個功能都有完整的測試覆蓋
   - 考慮各種邊界情況

3. **狀態管理**：
   - 任務完成狀態的轉換
   - 狀態查詢和過濾
   - 狀態變更的正確性

### 關鍵收穫

✅ **複雜業務邏輯的測試**：
- 多種查詢需求的實作
- 排序和過濾邏輯
- 統計功能的驗證

✅ **資料結構設計**：
- 清晰的類別職責分工
- 適當的封裝和介面
- 類型提示的使用

✅ **錯誤處理和驗證**：
- 輸入驗證（空標題檢查）
- 索引邊界檢查
- 類型檢查

---

## 🚀 進階挑戰

### 挑戰 1：任務分類和標籤
- 支援多個標籤
- 按分類過濾任務
- 標籤統計功能

### 挑戰 2：任務依賴關係
- 任務之間的依賴
- 父子任務關係
- 依賴完成檢查

### 挑戰 3：任務持久化
- 儲存到檔案
- 從檔案載入
- JSON/CSV 格式支援

### 挑戰 4：任務排程
- 到期日設定
- 提醒功能
- 重複任務支援

---

## 📈 自我評量

- [ ] 能設計合理的資料模型
- [ ] CRUD 操作實作完整
- [ ] 查詢和過濾功能正確
- [ ] 統計功能準確
- [ ] 錯誤處理適當
- [ ] 程式碼結構清晰

**恭喜完成待辦清單的 TDD 實作！**
**你現在能用 TDD 開發完整的業務功能了！**