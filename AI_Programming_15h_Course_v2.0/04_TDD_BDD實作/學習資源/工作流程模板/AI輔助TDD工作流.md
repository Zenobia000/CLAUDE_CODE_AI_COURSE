# AI 輔助 TDD 工作流程模板

## 🤖 AI + TDD 完美協作流程

這個模板幫助你建立高效的 AI 輔助 TDD 工作流程，讓你既能享受 AI 的加速效果，又能保持 TDD 的核心價值。

---

## 📋 完整工作流程

### 階段 1：準備和規劃（人類主導）

#### Step 1：明確需求和設計意圖
```
✅ 我要做什麼？
   - 清楚描述要實作的功能
   - 定義成功標準
   - 考慮邊界情況

✅ 為什麼要這樣設計？
   - 思考 API 介面設計
   - 考慮使用者體驗
   - 評估技術可行性

✅ 準備好與 AI 溝通
   - 用清晰的語言描述需求
   - 準備技術上下文資訊
   - 確定使用的框架和工具
```

#### Step 2：設定開發環境
```bash
# 確保測試環境就緒
pytest --version
python -c "import pytest; print('Test environment ready')"

# 建立專案結構
mkdir -p src tests
touch src/__init__.py tests/__init__.py
```

---

### 階段 2：紅綠重構循環（AI 協作）

#### 🔴 RED 階段：寫失敗的測試

**人類的工作**：
```
1. 思考下一個最小的功能單元
2. 確定測試的邊界和範圍
3. 決定測試的輸入和預期輸出
```

**與 AI 的對話範例**：
```
你：「我要用 TDD 開發一個用戶註冊功能。

第一個測試：用戶可以用有效的 email 和密碼註冊帳號。

請幫我生成 pytest 測試程式碼，要求：
1. 使用 AAA（Arrange-Act-Assert）模式
2. 測試名稱要清楚描述行為
3. 包含基本的邊界檢查

技術環境：Python 3.11 + pytest」

AI：「好的，我幫你生成測試：

```python
import pytest
from src.user_registration import UserRegistration

def test_user_can_register_with_valid_email_and_password():
    """測試用戶可以用有效的 email 和密碼註冊"""
    # Arrange
    registration = UserRegistration()
    email = "test@example.com"
    password = "securepassword123"

    # Act
    result = registration.register(email, password)

    # Assert
    assert result.success is True
    assert result.user.email == email
    assert result.user.is_verified is False
```

還需要其他測試場景嗎？」

你：「很好，請再加上無效 email 的測試」
```

**人類檢查要點**：
```
✅ 測試真的會失敗嗎？
✅ 測試名稱清楚描述預期行為嗎？
✅ 測試只驗證一個行為嗎？
✅ 斷言足夠具體嗎？
✅ 有沒有過度設計？
```

**執行測試**：
```bash
$ pytest tests/test_user_registration.py::test_user_can_register_with_valid_email_and_password -v

# 應該看到失敗（這是好的！）
FAILED - ModuleNotFoundError: No module named 'src.user_registration'
```

#### 🟢 GREEN 階段：讓測試通過

**與 AI 的對話範例**：
```
你：「現在我有這個失敗的測試：

[貼上測試程式碼]

請幫我實作 UserRegistration 類別，用『最簡單』的方式讓測試通過。

要求：
1. 不要過度設計
2. 只實作測試需要的功能
3. 使用清晰的類別和方法名稱」

AI：「好的，這是最簡實作：

```python
# src/user_registration.py
from dataclasses import dataclass

@dataclass
class User:
    email: str
    is_verified: bool = False

@dataclass
class RegistrationResult:
    success: bool
    user: User = None

class UserRegistration:
    def register(self, email: str, password: str) -> RegistrationResult:
        user = User(email=email)
        return RegistrationResult(success=True, user=user)
```

這個實作保持最簡單，讓測試通過。」

你：「完美，讓我執行測試確認」
```

**人類檢查要點**：
```
✅ 實作真的是最簡單的嗎？
✅ 有沒有添加測試沒要求的功能？
✅ 類別和方法命名清楚嗎？
✅ 程式碼結構合理嗎？
```

**執行測試**：
```bash
$ pytest tests/test_user_registration.py::test_user_can_register_with_valid_email_and_password -v

# 應該通過了！
PASSED ✓
```

#### 🔵 REFACTOR 階段：改善程式碼

**人類主導的重構時機判斷**：
```
是否需要重構？
✅ 程式碼有重複嗎？
✅ 命名是否清晰？
✅ 結構是否合理？
✅ 有沒有明顯的改進空間？
```

**與 AI 的重構對話**：
```
你：「我注意到測試中有重複建立 UserRegistration 的程式碼。
請幫我重構，使用 pytest fixture。」

AI：「好的，這是重構版本：

```python
import pytest
from src.user_registration import UserRegistration

@pytest.fixture
def user_registration():
    return UserRegistration()

def test_user_can_register_with_valid_email_and_password(user_registration):
    # Arrange
    email = "test@example.com"
    password = "securepassword123"

    # Act
    result = user_registration.register(email, password)

    # Assert
    assert result.success is True
    assert result.user.email == email
```

這樣可以避免重複，讓測試更乾淨。」
```

**重構後驗證**：
```bash
$ pytest tests/test_user_registration.py -v

# 所有測試都應該還是通過
PASSED ✓✓
```

---

### 階段 3：循環和擴展（持續協作）

#### 下一個循環的規劃
```
人類思考：
✅ 下一個最重要的功能是什麼？
✅ 哪個測試會帶來最大價值？
✅ 有沒有遺漏的邊界情況？

AI 建議：
「基於目前的實作，我建議下一個測試：
1. 無效 email 格式的處理
2. 密碼強度驗證
3. 重複 email 檢查

你想從哪個開始？」
```

#### 多個測試的管理
```
組織策略：
✅ 一次專注一個測試
✅ 相關測試放在同一個檔案
✅ 使用描述性的測試類別分組
✅ 保持測試獨立性
```

---

## 🎯 AI 協作最佳實踐

### DO（推薦做法）

#### ✅ 清楚的溝通
```
好的提示：
「我要用 TDD 開發購物車功能。
第一個測試：用戶可以將商品加入空購物車。
請生成 pytest 測試，使用 Decimal 處理金額。」

為什麼好：
- 明確說明使用 TDD
- 具體描述測試場景
- 提供技術要求
```

#### ✅ 階段性驗證
```
每個階段都驗證：
1. RED：確認測試真的失敗
2. GREEN：確認測試通過
3. REFACTOR：確認重構後測試依然通過
```

#### ✅ 人類把關關鍵決策
```
人類決定：
- 測試的範圍和邊界
- API 設計的方向
- 重構的時機和方式
- 程式碼品質標準
```

### DON'T（避免做法）

#### ❌ 完全依賴 AI
```
錯誤做法：
「AI，幫我寫一個完整的用戶管理系統，包含所有測試」

為什麼不好：
- 失去 TDD 的循序漸進精神
- 無法學習設計思考過程
- 可能產生過度設計
```

#### ❌ 跳過驗證步驟
```
錯誤做法：
- 不執行測試就接受 AI 程式碼
- 不檢查測試是否真的失敗
- 不驗證實作是否最簡
```

#### ❌ 忽略測試品質
```
錯誤做法：
- 接受 AI 生成的低品質測試
- 不檢查測試的可讀性
- 不確保測試的獨立性
```

---

## 📊 效率優化技巧

### 快速模板

#### 新功能開始模板
```
「我要用 TDD 開發 [功能名稱]。

需求：[簡潔描述]

第一個測試：[具體場景]

技術環境：[框架/工具]

請生成測試程式碼，要求：
1. 使用 AAA 模式
2. 清晰的測試名稱
3. 適當的斷言」
```

#### 實作請求模板
```
「現在我有失敗的測試：
[貼上測試程式碼]

請實作 [類別名稱]，要求：
1. 最簡單的實作
2. 只滿足測試需求
3. 清晰的命名」
```

#### 重構請求模板
```
「請幫我重構這段程式碼：
[貼上程式碼]

目標：
1. [具體改進目標]
2. 保持所有測試通過
3. 提升可讀性」
```

### 時間管理

#### 單個循環時間控制
```
⏰ RED 階段：5-10 分鐘
⏰ GREEN 階段：5-15 分鐘
⏰ REFACTOR 階段：5-10 分鐘

總計：15-35 分鐘/循環
```

#### 每日目標設定
```
新手：3-5 個循環/天
熟練：5-8 個循環/天
專家：8-12 個循環/天
```

---

## 🔧 疑難排解

### 常見問題和解決方案

#### 問題：AI 生成的測試太複雜
```
解決方案：
1. 重新描述需求，更加具體
2. 強調「最簡單」的要求
3. 拆分複雜功能為更小單元
```

#### 問題：測試沒有真正失敗
```
解決方案：
1. 檢查 import 路徑
2. 確認測試邏輯正確
3. 執行測試前確認模組不存在
```

#### 問題：AI 生成過度設計的實作
```
解決方案：
1. 強調 YAGNI 原則
2. 明確說明只實作測試要求的功能
3. 要求最簡實作
```

#### 問題：重構破壞了測試
```
解決方案：
1. 小步進行重構
2. 每次重構後立即執行測試
3. 如果測試失敗，立即回退
```

---

## 📈 成功指標

### 短期指標（每天）
```
✅ 完成 3+ TDD 循環
✅ 所有測試保持通過
✅ 程式碼覆蓋率 > 90%
✅ 沒有跳過測試步驟
```

### 中期指標（每週）
```
✅ 完成一個完整功能模組
✅ 重構至少 2 次
✅ 學會新的測試技巧
✅ 提升 AI 協作效率
```

### 長期指標（每月）
```
✅ TDD 成為自然習慣
✅ 能指導他人使用 TDD
✅ 建立個人 TDD 最佳實踐
✅ 在實際專案中成功應用
```

---

**記住：AI 是你的助手，但你才是船長！**
**讓 AI 加速你的 TDD 實踐，但不要失去思考的主導權！**