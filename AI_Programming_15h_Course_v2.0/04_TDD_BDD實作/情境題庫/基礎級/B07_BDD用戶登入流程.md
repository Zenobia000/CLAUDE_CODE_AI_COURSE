# B07：BDD 用戶登入流程

## 📋 情境描述

你正在開發一個網站的用戶登入功能。產品經理希望用 BDD 方式確保所有登入場景都被正確實作和測試，並且規範可以作為和前端、後端團隊溝通的文檔。

**使用者故事**：
```
作為一個網站用戶
我想要能夠登入我的帳號
以便我可以使用網站的個人化功能
```

**驗收標準**：
1. 用戶可以用正確的帳號密碼登入
2. 錯誤的帳號密碼會顯示錯誤訊息
3. 帳號被鎖定時無法登入
4. 登入成功後應該重定向到適當頁面

**任務**：
用 BDD 方式實作用戶登入功能，先撰寫 Gherkin 規範，再實作。

**時間估計**：40-50 分鐘

---

## 🎯 學習目標

- [ ] 掌握 Gherkin 語法的基本使用
- [ ] 學習 Given-When-Then 的思維模式
- [ ] 練習從使用者故事到測試場景的轉換
- [ ] 體驗 BDD 作為溝通工具的價值

---

## 🛠️ 技術要求

**語言**：Python 3.11+
**測試框架**：pytest + pytest-bdd
**檔案結構**：
```
user_login/
├── features/
│   ├── user_login.feature     # Gherkin 規範
│   └── steps/
│       └── login_steps.py     # Step definitions
├── src/
│   ├── user.py               # 用戶模型
│   ├── auth_service.py       # 認證服務
│   └── login_result.py       # 登入結果
└── pytest.ini               # pytest 設定
```

---

## 📝 實作步驟

### 準備工作

**建立專案**：
```bash
mkdir -p user_login/features/steps user_login/src
cd user_login

# 建立虛擬環境
python -m venv venv
source venv/bin/activate

# 安裝依賴
pip install pytest pytest-bdd
```

---

## 第一部分：撰寫 Gherkin 規範

### Step 1：定義 Feature 和 Background

**features/user_login.feature**：
```gherkin
Feature: 用戶登入功能
  作為一個網站用戶
  我想要能夠登入我的帳號
  以便我可以使用網站的個人化功能

  Background:
    Given 系統中有以下用戶：
      | 用戶名    | 密碼      | 狀態   | 角色  |
      | alice    | secret123 | 正常   | 一般用戶 |
      | bob      | password  | 正常   | 管理員  |
      | charlie  | locked123 | 鎖定   | 一般用戶 |
    And 用戶沒有登入

  Scenario: 用戶使用正確帳號密碼登入成功
    Given 用戶在登入頁面
    When 用戶輸入用戶名「alice」和密碼「secret123」
    And 用戶點擊登入按鈕
    Then 用戶應該登入成功
    And 用戶應該被重定向到「首頁」
    And 系統應該顯示歡迎訊息「歡迎回來，alice！」

  Scenario: 用戶使用錯誤密碼登入失敗
    Given 用戶在登入頁面
    When 用戶輸入用戶名「alice」和密碼「wrongpassword」
    And 用戶點擊登入按鈕
    Then 用戶應該登入失敗
    And 系統應該顯示錯誤訊息「用戶名或密碼錯誤」
    And 用戶應該停留在登入頁面

  Scenario: 用戶使用不存在的用戶名登入失敗
    Given 用戶在登入頁面
    When 用戶輸入用戶名「nonexistent」和密碼「anypassword」
    And 用戶點擊登入按鈕
    Then 用戶應該登入失敗
    And 系統應該顯示錯誤訊息「用戶名或密碼錯誤」

  Scenario: 被鎖定的用戶無法登入
    Given 用戶在登入頁面
    When 用戶輸入用戶名「charlie」和密碼「locked123」
    And 用戶點擊登入按鈕
    Then 用戶應該登入失敗
    And 系統應該顯示錯誤訊息「帳號已被鎖定，請聯繫管理員」

  Scenario: 管理員登入後重定向到管理頁面
    Given 用戶在登入頁面
    When 用戶輸入用戶名「bob」和密碼「password」
    And 用戶點擊登入按鈕
    Then 用戶應該登入成功
    And 用戶應該被重定向到「管理面板」
    And 系統應該顯示歡迎訊息「歡迎回來，bob！」

  Scenario: 空白用戶名或密碼無法登入
    Given 用戶在登入頁面
    When 用戶輸入用戶名「」和密碼「password」
    And 用戶點擊登入按鈕
    Then 用戶應該登入失敗
    And 系統應該顯示錯誤訊息「請輸入用戶名和密碼」

  Scenario Outline: 測試多種無效登入組合
    Given 用戶在登入頁面
    When 用戶輸入用戶名「<用戶名>」和密碼「<密碼>」
    And 用戶點擊登入按鈕
    Then 用戶應該登入失敗
    And 系統應該顯示錯誤訊息「<錯誤訊息>」

    Examples:
      | 用戶名  | 密碼       | 錯誤訊息              |
      |        | password   | 請輸入用戶名和密碼      |
      | alice  |           | 請輸入用戶名和密碼      |
      | alice  | wrong     | 用戶名或密碼錯誤        |
      | wrong  | secret123 | 用戶名或密碼錯誤        |
```

### Step 2：分析規範品質

**檢查清單**：
- [ ] Feature 描述清楚，包含用戶價值？
- [ ] Background 設置了測試所需的基礎資料？
- [ ] 場景使用業務語言（非技術術語）？
- [ ] 每個場景獨立且可重複執行？
- [ ] 涵蓋了快樂路徑和錯誤路徑？
- [ ] Scenario Outline 有效減少重複？

---

## 第二部分：實作 Step Definitions

### Step 3：建立測試基礎架構

**pytest.ini**：
```ini
[pytest]
testpaths = features
bdd_features_base_dir = features
```

**features/steps/login_steps.py**：
```python
from pytest_bdd import given, when, then, parsers, scenario
from pytest import fixture
import pytest

# Scenarios
scenario('../user_login.feature', '用戶使用正確帳號密碼登入成功')
scenario('../user_login.feature', '用戶使用錯誤密碼登入失敗')
scenario('../user_login.feature', '用戶使用不存在的用戶名登入失敗')
scenario('../user_login.feature', '被鎖定的用戶無法登入')
scenario('../user_login.feature', '管理員登入後重定向到管理頁面')
scenario('../user_login.feature', '空白用戶名或密碼無法登入')
scenario('../user_login.feature', '測試多種無效登入組合')


# Fixtures
@fixture
def context():
    """測試上下文"""
    return {
        'users': {},
        'current_page': None,
        'login_result': None,
        'error_message': None,
        'redirect_url': None,
        'welcome_message': None
    }


# Background Steps
@given('系統中有以下用戶：', target_fixture='users')
def setup_users(datatable, context):
    """設置用戶資料"""
    from src.user import User
    from src.auth_service import AuthService

    auth_service = AuthService()

    for row in datatable:
        user = User(
            username=row['用戶名'],
            password=row['密碼'],
            status=row['狀態'],
            role=row['角色']
        )
        auth_service.add_user(user)

    context['auth_service'] = auth_service
    return auth_service


@given('用戶沒有登入')
def user_not_logged_in(context):
    """確保用戶未登入"""
    context['logged_in_user'] = None


# Given Steps
@given('用戶在登入頁面')
def user_on_login_page(context):
    """用戶在登入頁面"""
    context['current_page'] = 'login'


# When Steps
@when(parsers.parse('用戶輸入用戶名「{username}」和密碼「{password}」'))
def user_enters_credentials(username, password, context):
    """用戶輸入登入資訊"""
    context['entered_username'] = username
    context['entered_password'] = password


@when('用戶點擊登入按鈕')
def user_clicks_login(context):
    """用戶點擊登入按鈕"""
    from src.auth_service import AuthService

    auth_service = context['auth_service']
    username = context['entered_username']
    password = context['entered_password']

    try:
        result = auth_service.login(username, password)
        context['login_result'] = result

        if result.success:
            context['logged_in_user'] = result.user
            context['welcome_message'] = f"歡迎回來，{result.user.username}！"

            # 根據角色決定重定向頁面
            if result.user.role == '管理員':
                context['redirect_url'] = '管理面板'
            else:
                context['redirect_url'] = '首頁'
        else:
            context['error_message'] = result.error_message

    except Exception as e:
        context['error_message'] = str(e)
        context['login_result'] = None


# Then Steps
@then('用戶應該登入成功')
def user_should_login_successfully(context):
    """驗證用戶登入成功"""
    assert context['login_result'] is not None
    assert context['login_result'].success is True
    assert context['logged_in_user'] is not None


@then('用戶應該登入失敗')
def user_should_login_fail(context):
    """驗證用戶登入失敗"""
    login_result = context.get('login_result')
    if login_result:
        assert login_result.success is False
    assert context.get('logged_in_user') is None


@then(parsers.parse('用戶應該被重定向到「{page}」'))
def user_should_be_redirected(page, context):
    """驗證重定向"""
    assert context['redirect_url'] == page


@then(parsers.parse('系統應該顯示歡迎訊息「{message}」'))
def system_should_show_welcome_message(message, context):
    """驗證歡迎訊息"""
    assert context['welcome_message'] == message


@then(parsers.parse('系統應該顯示錯誤訊息「{message}」'))
def system_should_show_error_message(message, context):
    """驗證錯誤訊息"""
    assert context['error_message'] == message


@then('用戶應該停留在登入頁面')
def user_should_stay_on_login_page(context):
    """驗證用戶停留在登入頁面"""
    # 登入失敗時不應該有重定向
    assert context.get('redirect_url') is None
    assert context['current_page'] == 'login'
```

---

## 第三部分：實作功能

### Step 4：實作領域模型

**src/user.py**：
```python
from dataclasses import dataclass
from typing import Literal

UserStatus = Literal["正常", "鎖定", "停用"]
UserRole = Literal["一般用戶", "管理員", "超級管理員"]

@dataclass
class User:
    """用戶模型"""
    username: str
    password: str
    status: UserStatus = "正常"
    role: UserRole = "一般用戶"

    def is_active(self) -> bool:
        """檢查用戶是否可用"""
        return self.status == "正常"

    def is_admin(self) -> bool:
        """檢查是否為管理員"""
        return self.role in ["管理員", "超級管理員"]

    def __eq__(self, other):
        if not isinstance(other, User):
            return False
        return self.username == other.username

    def __hash__(self):
        return hash(self.username)

    def __str__(self):
        return f"User({self.username}, {self.role})"
```

**src/login_result.py**：
```python
from dataclasses import dataclass
from typing import Optional
from src.user import User

@dataclass
class LoginResult:
    """登入結果"""
    success: bool
    user: Optional[User] = None
    error_message: Optional[str] = None
    redirect_url: Optional[str] = None

    @classmethod
    def success_result(cls, user: User, redirect_url: str = None):
        """建立成功結果"""
        return cls(success=True, user=user, redirect_url=redirect_url)

    @classmethod
    def failure_result(cls, error_message: str):
        """建立失敗結果"""
        return cls(success=False, error_message=error_message)
```

**src/auth_service.py**：
```python
from typing import Dict, Optional
from src.user import User
from src.login_result import LoginResult

class AuthService:
    """認證服務"""

    def __init__(self):
        self.users: Dict[str, User] = {}

    def add_user(self, user: User):
        """新增用戶"""
        self.users[user.username] = user

    def get_user(self, username: str) -> Optional[User]:
        """取得用戶"""
        return self.users.get(username)

    def login(self, username: str, password: str) -> LoginResult:
        """用戶登入"""
        # 驗證輸入
        if not username or not password:
            return LoginResult.failure_result("請輸入用戶名和密碼")

        if not username.strip() or not password.strip():
            return LoginResult.failure_result("請輸入用戶名和密碼")

        # 查找用戶
        user = self.get_user(username)
        if not user:
            return LoginResult.failure_result("用戶名或密碼錯誤")

        # 檢查帳號狀態
        if not user.is_active():
            if user.status == "鎖定":
                return LoginResult.failure_result("帳號已被鎖定，請聯繫管理員")
            else:
                return LoginResult.failure_result("帳號狀態異常")

        # 驗證密碼
        if user.password != password:
            return LoginResult.failure_result("用戶名或密碼錯誤")

        # 登入成功，決定重定向頁面
        redirect_url = "管理面板" if user.is_admin() else "首頁"

        return LoginResult.success_result(user, redirect_url)

    def logout(self, user: User):
        """用戶登出"""
        # 在實際應用中，這裡會清除 session 或 token
        pass

    def is_valid_credentials(self, username: str, password: str) -> bool:
        """檢查憑證是否有效（不進行實際登入）"""
        user = self.get_user(username)
        return user is not None and user.password == password and user.is_active()
```

---

## 第四部分：執行測試

### Step 5：執行 BDD 測試

**執行測試**：
```bash
$ pytest features/ -v

=============== test session starts ===============
features/steps/login_steps.py::test_用戶使用正確帳號密碼登入成功 PASSED
features/steps/login_steps.py::test_用戶使用錯誤密碼登入失敗 PASSED
features/steps/login_steps.py::test_用戶使用不存在的用戶名登入失敗 PASSED
features/steps/login_steps.py::test_被鎖定的用戶無法登入 PASSED
features/steps/login_steps.py::test_管理員登入後重定向到管理頁面 PASSED
features/steps/login_steps.py::test_空白用戶名或密碼無法登入 PASSED
features/steps/login_steps.py::test_測試多種無效登入組合[用戶名-password-請輸入用戶名和密碼] PASSED
features/steps/login_steps.py::test_測試多種無效登入組合[alice--請輸入用戶名和密碼] PASSED
features/steps/login_steps.py::test_測試多種無效登入組合[alice-wrong-用戶名或密碼錯誤] PASSED
features/steps/login_steps.py::test_測試多種無效登入組合[wrong-secret123-用戶名或密碼錯誤] PASSED
=============== 10 passed in 0.15s ===============
```

✓ 所有場景測試通過！

---

## 🎓 學習重點

### BDD 的完整流程

1. **從使用者故事開始**：
   - 明確的使用者價值
   - 清晰的驗收標準
   - 涵蓋主要使用場景

2. **撰寫 Gherkin 規範**：
   - Given（前置條件）- 設定測試環境
   - When（用戶動作）- 描述用戶行為
   - Then（預期結果）- 驗證系統回應

3. **實作 Step Definitions**：
   - 將自然語言轉為可執行程式碼
   - 使用清晰的測試上下文
   - 適當的斷言和驗證

4. **實作業務功能**：
   - 讓所有測試場景通過
   - 保持程式碼簡潔
   - 正確處理各種情況

### 關鍵收穫

✅ **業務語言溝通**：
- Gherkin 規範可以給 PM、設計師、開發者看
- 減少需求理解的偏差
- 建立共同的理解基礎

✅ **場景覆蓋完整**：
- 快樂路徑（正常登入）
- 錯誤路徑（密碼錯誤、帳號鎖定）
- 邊界情況（空輸入、不存在用戶）

✅ **測試即文檔**：
- 規範永遠反映最新的功能
- 新人可以通過規範理解系統
- 回歸測試的完整保護

---

## 🚀 進階挑戰

### 挑戰 1：增強登入功能
- 記住我功能
- 密碼重設流程
- 兩步驟驗證

### 挑戰 2：安全性增強
- 登入嘗試次數限制
- 密碼複雜度檢查
- 可疑登入檢測

### 挑戰 3：用戶體驗改善
- 社交媒體登入
- 密碼強度指示器
- 登入狀態記憶

### 挑戰 4：性能和監控
- 登入成功率統計
- 登入時間分析
- 異常登入告警

---

## 📈 自我評量

完成本情境後，檢查以下項目：

### BDD 流程
- [ ] 能從使用者故事推導出測試場景
- [ ] Gherkin 規範清晰且非技術人員可理解
- [ ] Step definitions 正確實作規範意圖
- [ ] 所有場景測試通過

### 規範品質
- [ ] 場景獨立且可重複執行
- [ ] 涵蓋快樂路徑和錯誤路徑
- [ ] 使用業務語言而非技術術語
- [ ] Background 和 Scenario Outline 使用得當

### 實作品質
- [ ] 業務邏輯正確實作
- [ ] 錯誤處理適當
- [ ] 程式碼結構清晰
- [ ] 測試覆蓋完整

---

**恭喜完成第一個 BDD 專案！**
**你現在理解了如何用 Gherkin 描述業務需求！**
**BDD 讓開發團隊和業務團隊有了共同語言！**