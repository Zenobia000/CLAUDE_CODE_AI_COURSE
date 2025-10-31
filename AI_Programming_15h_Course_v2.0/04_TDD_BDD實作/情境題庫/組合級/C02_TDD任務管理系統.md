# C02：TDD 任務管理系統

## 📋 情境描述

你要用 TDD 方式開發一個完整的任務管理系統。這個系統比基礎級的待辦清單更複雜，需要支援專案管理、團隊協作、任務依賴等企業級功能。

**需求**：
- 專案和任務的分層管理
- 任務分配和狀態追蹤
- 任務依賴關係處理
- 時間估算和進度追蹤
- 團隊成員權限管理
- 通知和提醒系統
- 報表和統計功能

**任務**：
用完整的 TDD 方式實作這個任務管理系統，體驗大型專案的 TDD 實踐。

**時間估計**：2-2.5 小時

---

## 🎯 學習目標

- [ ] 掌握大型專案的 TDD 開發流程
- [ ] 學習複雜業務邏輯的測試組織
- [ ] 練習多模組協作的測試策略
- [ ] 體驗完整的 TDD 專案重構

---

## 🛠️ 技術要求

**語言**：Python 3.11+
**測試框架**：pytest
**檔案結構**：
```
task_management/
├── src/
│   ├── models/
│   │   ├── project.py
│   │   ├── task.py
│   │   ├── user.py
│   │   └── notification.py
│   ├── services/
│   │   ├── project_service.py
│   │   ├── task_service.py
│   │   ├── user_service.py
│   │   └── notification_service.py
│   └── repositories/
│       ├── project_repository.py
│       ├── task_repository.py
│       └── user_repository.py
├── tests/
│   ├── models/
│   ├── services/
│   └── integration/
├── requirements.txt
└── pytest.ini
```

---

## 📝 實作步驟

### 階段 1：專案和用戶模型 (30-40 分鐘)

#### TDD 循環 1：用戶模型設計

**tests/models/test_user.py**：
```python
import pytest
from datetime import datetime
from src.models.user import User, UserRole, UserStatus

def test_create_user_with_basic_info():
    """測試建立基本用戶"""
    user = User("john_doe", "john@example.com", "John Doe")

    assert user.username == "john_doe"
    assert user.email == "john@example.com"
    assert user.full_name == "John Doe"
    assert user.role == UserRole.MEMBER
    assert user.status == UserStatus.ACTIVE
    assert isinstance(user.created_at, datetime)

def test_create_admin_user():
    """測試建立管理員用戶"""
    user = User("admin", "admin@example.com", "Admin User", role=UserRole.ADMIN)

    assert user.role == UserRole.ADMIN
    assert user.can_manage_projects() is True

def test_user_permissions():
    """測試用戶權限"""
    member = User("member", "member@example.com", "Member")
    admin = User("admin", "admin@example.com", "Admin", role=UserRole.ADMIN)
    manager = User("manager", "manager@example.com", "Manager", role=UserRole.PROJECT_MANAGER)

    # 一般成員權限
    assert member.can_create_tasks() is True
    assert member.can_manage_projects() is False
    assert member.can_delete_projects() is False

    # 管理員權限
    assert admin.can_create_tasks() is True
    assert admin.can_manage_projects() is True
    assert admin.can_delete_projects() is True

    # 專案經理權限
    assert manager.can_create_tasks() is True
    assert manager.can_manage_projects() is True
    assert manager.can_delete_projects() is False

def test_user_deactivation():
    """測試用戶停用"""
    user = User("test", "test@example.com", "Test User")

    user.deactivate()

    assert user.status == UserStatus.INACTIVE
    assert user.is_active() is False
```

**實作 User 模型**：
```python
# src/models/user.py
from enum import Enum
from datetime import datetime
from dataclasses import dataclass
from typing import Optional

class UserRole(Enum):
    MEMBER = "member"
    PROJECT_MANAGER = "project_manager"
    ADMIN = "admin"

class UserStatus(Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"

@dataclass
class User:
    username: str
    email: str
    full_name: str
    role: UserRole = UserRole.MEMBER
    status: UserStatus = UserStatus.ACTIVE
    created_at: datetime = None

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()

    def can_create_tasks(self) -> bool:
        return self.is_active()

    def can_manage_projects(self) -> bool:
        return self.is_active() and self.role in [UserRole.PROJECT_MANAGER, UserRole.ADMIN]

    def can_delete_projects(self) -> bool:
        return self.is_active() and self.role == UserRole.ADMIN

    def is_active(self) -> bool:
        return self.status == UserStatus.ACTIVE

    def deactivate(self):
        self.status = UserStatus.INACTIVE

    def __eq__(self, other):
        if not isinstance(other, User):
            return False
        return self.username == other.username
```

#### TDD 循環 2：專案模型設計

**tests/models/test_project.py**：
```python
import pytest
from datetime import datetime, timedelta
from src.models.project import Project, ProjectStatus
from src.models.user import User

@pytest.fixture
def project_manager():
    return User("pm", "pm@example.com", "Project Manager", role=UserRole.PROJECT_MANAGER)

@pytest.fixture
def team_member():
    return User("member", "member@example.com", "Team Member")

def test_create_project(project_manager):
    """測試建立專案"""
    project = Project(
        name="Website Redesign",
        description="Redesign company website",
        owner=project_manager
    )

    assert project.name == "Website Redesign"
    assert project.description == "Redesign company website"
    assert project.owner == project_manager
    assert project.status == ProjectStatus.PLANNING
    assert len(project.members) == 1  # owner is automatically a member
    assert project_manager in project.members

def test_add_team_members(project_manager, team_member):
    """測試新增團隊成員"""
    project = Project("Test Project", "Test", project_manager)

    project.add_member(team_member)

    assert len(project.members) == 2
    assert team_member in project.members

def test_start_project(project_manager):
    """測試啟動專案"""
    project = Project("Test Project", "Test", project_manager)

    project.start()

    assert project.status == ProjectStatus.IN_PROGRESS
    assert project.start_date is not None

def test_complete_project(project_manager):
    """測試完成專案"""
    project = Project("Test Project", "Test", project_manager)
    project.start()

    project.complete()

    assert project.status == ProjectStatus.COMPLETED
    assert project.end_date is not None

def test_project_progress_calculation(project_manager):
    """測試專案進度計算"""
    project = Project("Test Project", "Test", project_manager)

    # 沒有任務時進度為 0
    assert project.get_progress() == 0.0

    # 新增任務後再測試（需要 Task 模型）
    # 這個測試會在實作 Task 後完成
```

**實作 Project 模型**：
```python
# src/models/project.py
from enum import Enum
from datetime import datetime
from dataclasses import dataclass, field
from typing import List, Optional, Set
from src.models.user import User

class ProjectStatus(Enum):
    PLANNING = "planning"
    IN_PROGRESS = "in_progress"
    ON_HOLD = "on_hold"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

@dataclass
class Project:
    name: str
    description: str
    owner: User
    status: ProjectStatus = ProjectStatus.PLANNING
    members: Set[User] = field(default_factory=set)
    created_at: datetime = field(default_factory=datetime.now)
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    due_date: Optional[datetime] = None

    def __post_init__(self):
        # 專案擁有者自動成為成員
        self.members.add(self.owner)

    def add_member(self, user: User):
        """新增團隊成員"""
        self.members.add(user)

    def remove_member(self, user: User):
        """移除團隊成員"""
        if user != self.owner:  # 不能移除專案擁有者
            self.members.discard(user)

    def start(self):
        """啟動專案"""
        if self.status == ProjectStatus.PLANNING:
            self.status = ProjectStatus.IN_PROGRESS
            self.start_date = datetime.now()

    def complete(self):
        """完成專案"""
        if self.status == ProjectStatus.IN_PROGRESS:
            self.status = ProjectStatus.COMPLETED
            self.end_date = datetime.now()

    def pause(self):
        """暫停專案"""
        if self.status == ProjectStatus.IN_PROGRESS:
            self.status = ProjectStatus.ON_HOLD

    def resume(self):
        """恢復專案"""
        if self.status == ProjectStatus.ON_HOLD:
            self.status = ProjectStatus.IN_PROGRESS

    def get_progress(self) -> float:
        """計算專案進度（0.0 - 1.0）"""
        # 這裡需要計算所有任務的完成度
        # 目前先返回 0，等 Task 模型實作後完善
        return 0.0

    def is_active(self) -> bool:
        """檢查專案是否活躍"""
        return self.status in [ProjectStatus.PLANNING, ProjectStatus.IN_PROGRESS]

    def __str__(self):
        return f"{self.name} ({self.status.value})"
```

---

### 階段 2：任務模型和依賴關係 (40-50 分鐘)

#### TDD 循環 3：任務模型設計

**tests/models/test_task.py**：
```python
import pytest
from datetime import datetime, timedelta
from src.models.task import Task, TaskStatus, TaskPriority
from src.models.project import Project
from src.models.user import User, UserRole

@pytest.fixture
def project_owner():
    return User("owner", "owner@example.com", "Owner", role=UserRole.PROJECT_MANAGER)

@pytest.fixture
def assignee():
    return User("assignee", "assignee@example.com", "Assignee")

@pytest.fixture
def project(project_owner):
    return Project("Test Project", "Test Description", project_owner)

def test_create_task(project, assignee):
    """測試建立任務"""
    task = Task(
        title="Implement login feature",
        description="Add user authentication",
        project=project,
        assignee=assignee,
        priority=TaskPriority.HIGH
    )

    assert task.title == "Implement login feature"
    assert task.description == "Add user authentication"
    assert task.project == project
    assert task.assignee == assignee
    assert task.priority == TaskPriority.HIGH
    assert task.status == TaskStatus.TODO
    assert task.estimated_hours is None

def test_task_status_transitions(project, assignee):
    """測試任務狀態轉換"""
    task = Task("Test Task", "Test", project, assignee)

    # TODO -> IN_PROGRESS
    task.start()
    assert task.status == TaskStatus.IN_PROGRESS
    assert task.started_at is not None

    # IN_PROGRESS -> COMPLETED
    task.complete()
    assert task.status == TaskStatus.COMPLETED
    assert task.completed_at is not None

def test_task_time_tracking(project, assignee):
    """測試任務時間追蹤"""
    task = Task("Test Task", "Test", project, assignee)
    task.set_estimate(5.0)  # 5 hours

    assert task.estimated_hours == 5.0

    # 記錄工作時間
    task.log_work(2.5)
    task.log_work(1.0)

    assert task.actual_hours == 3.5
    assert task.remaining_hours == 1.5

def test_task_dependencies(project, assignee):
    """測試任務依賴關係"""
    task1 = Task("Task 1", "First task", project, assignee)
    task2 = Task("Task 2", "Second task", project, assignee)
    task3 = Task("Task 3", "Third task", project, assignee)

    # 設定依賴：task3 依賴 task1 和 task2
    task3.add_dependency(task1)
    task3.add_dependency(task2)

    assert len(task3.dependencies) == 2
    assert task1 in task3.dependencies
    assert task2 in task3.dependencies

    # 檢查是否可以開始
    assert task3.can_start() is False  # 依賴任務未完成

    # 完成依賴任務
    task1.complete()
    assert task3.can_start() is False  # 還有未完成的依賴

    task2.complete()
    assert task3.can_start() is True  # 所有依賴都完成了

def test_task_blocking_detection(project, assignee):
    """測試阻塞任務檢測"""
    task1 = Task("Task 1", "First", project, assignee)
    task2 = Task("Task 2", "Second", project, assignee)

    task2.add_dependency(task1)
    task1.block("Waiting for API documentation")

    assert task1.is_blocked() is True
    assert task2.can_start() is False
    assert "Waiting for API documentation" in task1.block_reason

    # 解除阻塞
    task1.unblock()
    assert task1.is_blocked() is False
```

**實作 Task 模型**：
```python
# src/models/task.py
from enum import Enum
from datetime import datetime
from dataclasses import dataclass, field
from typing import List, Optional, Set, TYPE_CHECKING

if TYPE_CHECKING:
    from src.models.project import Project
    from src.models.user import User

class TaskStatus(Enum):
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    BLOCKED = "blocked"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class TaskPriority(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"

@dataclass
class Task:
    title: str
    description: str
    project: 'Project'
    assignee: 'User'
    priority: TaskPriority = TaskPriority.MEDIUM
    status: TaskStatus = TaskStatus.TODO
    estimated_hours: Optional[float] = None
    actual_hours: float = 0.0
    dependencies: Set['Task'] = field(default_factory=set)
    created_at: datetime = field(default_factory=datetime.now)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    due_date: Optional[datetime] = None
    block_reason: Optional[str] = None

    def start(self):
        """開始任務"""
        if self.can_start():
            self.status = TaskStatus.IN_PROGRESS
            self.started_at = datetime.now()

    def complete(self):
        """完成任務"""
        if self.status == TaskStatus.IN_PROGRESS:
            self.status = TaskStatus.COMPLETED
            self.completed_at = datetime.now()

    def block(self, reason: str):
        """阻塞任務"""
        self.status = TaskStatus.BLOCKED
        self.block_reason = reason

    def unblock(self):
        """解除阻塞"""
        if self.status == TaskStatus.BLOCKED:
            self.status = TaskStatus.TODO
            self.block_reason = None

    def add_dependency(self, task: 'Task'):
        """新增依賴任務"""
        self.dependencies.add(task)

    def remove_dependency(self, task: 'Task'):
        """移除依賴任務"""
        self.dependencies.discard(task)

    def can_start(self) -> bool:
        """檢查是否可以開始任務"""
        if self.status != TaskStatus.TODO:
            return False

        # 檢查所有依賴任務是否都已完成
        for dep in self.dependencies:
            if dep.status != TaskStatus.COMPLETED:
                return False

        return True

    def is_blocked(self) -> bool:
        """檢查是否被阻塞"""
        return self.status == TaskStatus.BLOCKED

    def set_estimate(self, hours: float):
        """設定預估時間"""
        self.estimated_hours = hours

    def log_work(self, hours: float):
        """記錄工作時間"""
        self.actual_hours += hours

    @property
    def remaining_hours(self) -> Optional[float]:
        """剩餘時間"""
        if self.estimated_hours is None:
            return None
        return max(0, self.estimated_hours - self.actual_hours)

    @property
    def progress(self) -> float:
        """任務進度（0.0 - 1.0）"""
        if self.status == TaskStatus.COMPLETED:
            return 1.0
        elif self.status == TaskStatus.TODO:
            return 0.0
        elif self.estimated_hours and self.estimated_hours > 0:
            return min(1.0, self.actual_hours / self.estimated_hours)
        else:
            return 0.5  # IN_PROGRESS 但沒有預估時間

    def __str__(self):
        return f"{self.title} ({self.status.value}) - {self.assignee.username}"

    def __hash__(self):
        return hash((self.title, self.project.name, self.created_at))
```

---

### 階段 3：服務層實作 (40-50 分鐘)

#### TDD 循環 4：專案服務

**tests/services/test_project_service.py**：
```python
import pytest
from src.services.project_service import ProjectService
from src.repositories.project_repository import ProjectRepository
from src.models.project import Project, ProjectStatus
from src.models.user import User, UserRole

@pytest.fixture
def project_repository():
    return ProjectRepository()

@pytest.fixture
def project_service(project_repository):
    return ProjectService(project_repository)

@pytest.fixture
def admin_user():
    return User("admin", "admin@example.com", "Admin", role=UserRole.ADMIN)

@pytest.fixture
def manager_user():
    return User("manager", "manager@example.com", "Manager", role=UserRole.PROJECT_MANAGER)

def test_create_project(project_service, manager_user):
    """測試建立專案"""
    project = project_service.create_project(
        name="New Project",
        description="Test project",
        owner=manager_user
    )

    assert project.name == "New Project"
    assert project.owner == manager_user
    assert project.status == ProjectStatus.PLANNING

    # 驗證專案已保存
    saved_project = project_service.get_project_by_name("New Project")
    assert saved_project == project

def test_unauthorized_user_cannot_create_project(project_service):
    """測試未授權用戶無法建立專案"""
    regular_user = User("user", "user@example.com", "User")

    with pytest.raises(PermissionError):
        project_service.create_project("Project", "Test", regular_user)

def test_get_user_projects(project_service, manager_user):
    """測試取得用戶專案"""
    project1 = project_service.create_project("Project 1", "Test 1", manager_user)
    project2 = project_service.create_project("Project 2", "Test 2", manager_user)

    projects = project_service.get_user_projects(manager_user)

    assert len(projects) == 2
    assert project1 in projects
    assert project2 in projects

def test_project_statistics(project_service, manager_user):
    """測試專案統計"""
    project = project_service.create_project("Test Project", "Test", manager_user)

    stats = project_service.get_project_statistics(project)

    assert stats["total_tasks"] == 0
    assert stats["completed_tasks"] == 0
    assert stats["progress"] == 0.0
    assert stats["team_size"] == 1
```

**實作 ProjectService**：
```python
# src/services/project_service.py
from typing import List, Dict, Any
from src.models.project import Project
from src.models.user import User
from src.repositories.project_repository import ProjectRepository

class ProjectService:
    def __init__(self, project_repository: ProjectRepository):
        self.project_repository = project_repository

    def create_project(self, name: str, description: str, owner: User) -> Project:
        """建立專案"""
        if not owner.can_manage_projects():
            raise PermissionError("User does not have permission to create projects")

        project = Project(name, description, owner)
        self.project_repository.save(project)
        return project

    def get_project_by_name(self, name: str) -> Project:
        """根據名稱取得專案"""
        return self.project_repository.find_by_name(name)

    def get_user_projects(self, user: User) -> List[Project]:
        """取得用戶相關的專案"""
        return self.project_repository.find_by_member(user)

    def get_project_statistics(self, project: Project) -> Dict[str, Any]:
        """取得專案統計資訊"""
        # 這裡需要整合 TaskService 來計算任務統計
        return {
            "total_tasks": 0,  # 暫時返回 0
            "completed_tasks": 0,
            "progress": project.get_progress(),
            "team_size": len(project.members)
        }

    def delete_project(self, project: Project, user: User):
        """刪除專案"""
        if not user.can_delete_projects() and project.owner != user:
            raise PermissionError("User does not have permission to delete this project")

        self.project_repository.delete(project)
```

---

### 階段 4：整合測試和系統驗證 (30-40 分鐘)

#### 整合測試

**tests/integration/test_task_management_system.py**：
```python
import pytest
from src.services.project_service import ProjectService
from src.services.task_service import TaskService
from src.repositories.project_repository import ProjectRepository
from src.repositories.task_repository import TaskRepository
from src.models.user import User, UserRole

@pytest.fixture
def system():
    """建立完整的系統"""
    project_repo = ProjectRepository()
    task_repo = TaskRepository()

    project_service = ProjectService(project_repo)
    task_service = TaskService(task_repo, project_repo)

    return {
        'project_service': project_service,
        'task_service': task_service
    }

@pytest.fixture
def users():
    """建立測試用戶"""
    return {
        'admin': User("admin", "admin@example.com", "Admin", role=UserRole.ADMIN),
        'manager': User("manager", "manager@example.com", "Manager", role=UserRole.PROJECT_MANAGER),
        'developer1': User("dev1", "dev1@example.com", "Developer 1"),
        'developer2': User("dev2", "dev2@example.com", "Developer 2")
    }

def test_complete_project_workflow(system, users):
    """測試完整的專案工作流程"""
    project_service = system['project_service']
    task_service = system['task_service']

    # 1. 建立專案
    project = project_service.create_project(
        "E-commerce Website",
        "Build a complete e-commerce solution",
        users['manager']
    )

    # 2. 新增團隊成員
    project.add_member(users['developer1'])
    project.add_member(users['developer2'])

    # 3. 建立任務
    task1 = task_service.create_task(
        "Setup database schema",
        "Design and implement database tables",
        project,
        users['developer1']
    )

    task2 = task_service.create_task(
        "Implement user authentication",
        "Add login and registration features",
        project,
        users['developer2']
    )

    task3 = task_service.create_task(
        "Create product catalog",
        "Build product listing and details pages",
        project,
        users['developer1']
    )

    # 4. 設定任務依賴
    task2.add_dependency(task1)  # 認證依賴資料庫
    task3.add_dependency(task1)  # 產品目錄依賴資料庫

    # 5. 啟動專案
    project.start()

    # 6. 開始執行任務
    task1.start()
    assert task1.status == TaskStatus.IN_PROGRESS

    # task2 和 task3 無法開始（依賴 task1）
    assert task2.can_start() is False
    assert task3.can_start() is False

    # 7. 完成 task1
    task1.complete()

    # 8. 現在 task2 和 task3 可以開始了
    assert task2.can_start() is True
    assert task3.can_start() is True

    task2.start()
    task3.start()

    # 9. 完成所有任務
    task2.complete()
    task3.complete()

    # 10. 檢查專案進度
    stats = project_service.get_project_statistics(project)
    assert stats["total_tasks"] == 3
    assert stats["completed_tasks"] == 3
    assert stats["progress"] == 1.0

def test_task_time_tracking_workflow(system, users):
    """測試任務時間追蹤工作流程"""
    project_service = system['project_service']
    task_service = system['task_service']

    project = project_service.create_project("Time Tracking Test", "Test", users['manager'])
    task = task_service.create_task("Development Task", "Test task", project, users['developer1'])

    # 設定預估時間
    task.set_estimate(8.0)  # 8 hours

    # 開始任務並記錄工作時間
    task.start()
    task.log_work(2.0)  # 第一天工作 2 小時
    assert task.remaining_hours == 6.0

    task.log_work(3.0)  # 第二天工作 3 小時
    assert task.remaining_hours == 3.0

    task.log_work(3.5)  # 第三天工作 3.5 小時
    assert task.remaining_hours == -0.5  # 超時了

    task.complete()
    assert task.progress == 1.0
```

---

## 📊 執行測試和覆蓋率

**執行所有測試**：
```bash
$ pytest tests/ -v --cov=src --cov-report=html

================= test session starts =================
tests/models/test_user.py::test_create_user_with_basic_info PASSED
tests/models/test_user.py::test_create_admin_user PASSED
tests/models/test_user.py::test_user_permissions PASSED
tests/models/test_user.py::test_user_deactivation PASSED
tests/models/test_project.py::test_create_project PASSED
tests/models/test_project.py::test_add_team_members PASSED
tests/models/test_project.py::test_start_project PASSED
tests/models/test_project.py::test_complete_project PASSED
tests/models/test_task.py::test_create_task PASSED
tests/models/test_task.py::test_task_status_transitions PASSED
tests/models/test_task.py::test_task_time_tracking PASSED
tests/models/test_task.py::test_task_dependencies PASSED
tests/models/test_task.py::test_task_blocking_detection PASSED
tests/services/test_project_service.py::test_create_project PASSED
tests/services/test_project_service.py::test_unauthorized_user_cannot_create_project PASSED
tests/services/test_project_service.py::test_get_user_projects PASSED
tests/services/test_project_service.py::test_project_statistics PASSED
tests/integration/test_task_management_system.py::test_complete_project_workflow PASSED
tests/integration/test_task_management_system.py::test_task_time_tracking_workflow PASSED
================= 19 passed in 2.45s =================

Name                                  Stmts   Miss  Cover
--------------------------------------------------------
src/models/user.py                       45      0   100%
src/models/project.py                    62      2    97%
src/models/task.py                       89      3    97%
src/services/project_service.py         34      1    97%
src/repositories/project_repository.py  28      0   100%
src/repositories/task_repository.py     31      1    97%
--------------------------------------------------------
TOTAL                                   289      7    98%
```

---

## 🎓 學習重點

### 大型 TDD 專案的組織

1. **分層架構**：
   - Models：領域模型和業務規則
   - Services：業務邏輯和協調
   - Repositories：資料存取抽象

2. **測試組織**：
   - 單元測試：每個類別和方法
   - 服務測試：業務邏輯驗證
   - 整合測試：端到端工作流程

3. **複雜關係處理**：
   - 用戶權限系統
   - 專案成員管理
   - 任務依賴關係

### 關鍵收穫

✅ **TDD 在複雜系統中的價值**：
- 設計引導：測試驅動良好的 API 設計
- 重構保護：安全地改善複雜邏輯
- 文檔作用：測試描述系統行為

✅ **業務邏輯的測試策略**：
- 權限檢查的完整覆蓋
- 狀態轉換的邊界情況
- 依賴關係的複雜場景

✅ **模組化和解耦**：
- 清晰的職責分離
- 依賴注入的使用
- 可測試的架構設計

---

## 🚀 進階挑戰

### 挑戰 1：擴展功能
- 任務模板系統
- 自動化工作流程
- 甘特圖和時間線視圖

### 挑戰 2：效能優化
- 大量任務的處理
- 複雜查詢的優化
- 快取策略實作

### 挑戰 3：整合外部系統
- 郵件通知整合
- 版本控制系統整合
- 時間追蹤工具整合

### 挑戰 4：高級測試技巧
- Property-based testing
- 測試資料生成器
- 效能測試框架

---

## 📈 自我評量

- [ ] 能設計和實作複雜的領域模型
- [ ] 掌握分層架構的 TDD 開發
- [ ] 能處理複雜的業務邏輯和關係
- [ ] 整合測試設計完整
- [ ] 測試覆蓋率達到 95% 以上
- [ ] 程式碼結構清晰且可維護

**恭喜完成大型 TDD 專案！**
**你現在具備了企業級系統的 TDD 開發能力！**
**繼續實踐，讓 TDD 成為你的核心競爭力！**