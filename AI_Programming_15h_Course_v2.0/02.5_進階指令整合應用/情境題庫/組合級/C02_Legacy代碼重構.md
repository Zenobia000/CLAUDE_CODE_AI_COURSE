# C02：Legacy 代碼重構（組合級）

## 情境資訊

**編號**：C02
**難度**：⭐⭐⭐☆☆（組合級）
**預計時間**：2.5 小時
**學習目標**：
- 掌握系統化重構老舊代碼的流程
- 學會在重構前建立安全網（測試）
- 理解 legacy 代碼分析到重構的完整工作流
- 整合多個 Agent 協作完成複雜重構任務

**適用對象**：
- 需要維護老舊系統的開發者
- 正在學習重構技巧的進階開發者
- 負責技術債務處理的技術主管

---

## 情境描述

### 背景

你剛加入一家有 10 年歷史的金融科技公司，被分配維護一個關鍵的風險評估系統。這個系統每天處理數千筆交易，但代碼已經 5 年沒有大幅更新，充滿了技術債務。

CTO 希望你在不影響現有功能的前提下，系統化地重構這個模組，提升代碼質量和可維護性。

### 現有代碼問題

你發現了一個核心的風險計算模組，包含以下問題：

```python
# src/risk_calculator.py
import json
import datetime
import sqlite3
from typing import Dict, Any

class RiskCalculator:
    """風險計算器 - 需要重構的 Legacy 代碼"""

    def __init__(self, db_path="risk.db"):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        self.setup_db()

        # 硬編碼的風險參數
        self.risk_params = {
            'age_factor': {
                '18-25': 1.8,
                '26-35': 1.4,
                '36-45': 1.1,
                '46-60': 0.9,
                '60+': 0.7
            },
            'income_factor': {
                'low': 2.0,    # < 30k
                'medium': 1.5,  # 30k-100k
                'high': 1.0,   # 100k-500k
                'vhigh': 0.8   # > 500k
            },
            'location_risk': {
                'tier1': 0.8,  # 一線城市
                'tier2': 1.0,  # 二線城市
                'tier3': 1.3,  # 三線城市
                'rural': 1.6   # 農村
            }
        }

    def setup_db(self):
        cursor = self.conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS risk_history (
                id INTEGER PRIMARY KEY,
                user_id TEXT,
                risk_score REAL,
                factors TEXT,
                timestamp TEXT
            )
        """)
        self.conn.commit()

    def calculate_risk(self, user_data):
        """計算用戶風險分數"""
        # 複雜的巢狀邏輯
        base_score = 100

        # 年齡因子
        age = user_data.get('age', 0)
        if age < 18:
            age_key = '18-25'  # 特殊處理
        elif age <= 25:
            age_key = '18-25'
        elif age <= 35:
            age_key = '26-35'
        elif age <= 45:
            age_key = '36-45'
        elif age <= 60:
            age_key = '46-60'
        else:
            age_key = '60+'

        age_factor = self.risk_params['age_factor'][age_key]

        # 收入因子
        income = user_data.get('annual_income', 0)
        if income < 30000:
            income_factor = self.risk_params['income_factor']['low']
        elif income < 100000:
            income_factor = self.risk_params['income_factor']['medium']
        elif income < 500000:
            income_factor = self.risk_params['income_factor']['high']
        else:
            income_factor = self.risk_params['income_factor']['vhigh']

        # 地區因子
        location = user_data.get('location_tier', 'tier2')
        location_factor = self.risk_params['location_risk'].get(location, 1.0)

        # 信用歷史（複雜邏輯）
        credit_history = user_data.get('credit_history', [])
        credit_score = 1.0
        if len(credit_history) == 0:
            credit_score = 2.0  # 無信用記錄
        else:
            defaults = sum(1 for record in credit_history if record.get('status') == 'default')
            if defaults > 0:
                credit_score = 1.5 + (defaults * 0.3)
            else:
                # 好的信用記錄
                good_records = len([r for r in credit_history if r.get('status') == 'paid'])
                if good_records > 10:
                    credit_score = 0.7
                elif good_records > 5:
                    credit_score = 0.8
                else:
                    credit_score = 0.9

        # 職業風險
        profession = user_data.get('profession', 'unknown')
        profession_risk = 1.0
        high_risk_jobs = ['freelancer', 'artist', 'startup_founder', 'consultant']
        stable_jobs = ['government', 'teacher', 'doctor', 'engineer_corporate']

        if profession in high_risk_jobs:
            profession_risk = 1.4
        elif profession in stable_jobs:
            profession_risk = 0.8
        elif profession == 'unemployed':
            profession_risk = 2.5
        # 其他職業默認 1.0

        # 計算最終分數（複雜公式）
        risk_score = base_score * age_factor * income_factor * location_factor * credit_score * profession_risk

        # 額外調整
        if user_data.get('has_dependents', False):
            risk_score *= 0.9  # 有家庭負擔，降低風險

        if user_data.get('owns_property', False):
            risk_score *= 0.85  # 有房產

        if user_data.get('education_level') == 'graduate':
            risk_score *= 0.9
        elif user_data.get('education_level') == 'postgraduate':
            risk_score *= 0.85

        # 存到資料庫
        self.save_risk_record(user_data.get('user_id'), risk_score, user_data)

        return {
            'user_id': user_data.get('user_id'),
            'risk_score': round(risk_score, 2),
            'risk_level': self.get_risk_level(risk_score),
            'factors': {
                'age_factor': age_factor,
                'income_factor': income_factor,
                'location_factor': location_factor,
                'credit_score': credit_score,
                'profession_risk': profession_risk
            }
        }

    def get_risk_level(self, score):
        """將風險分數轉換為等級"""
        if score <= 80:
            return 'LOW'
        elif score <= 120:
            return 'MEDIUM'
        elif score <= 160:
            return 'HIGH'
        else:
            return 'CRITICAL'

    def save_risk_record(self, user_id, risk_score, user_data):
        """儲存風險記錄"""
        cursor = self.conn.cursor()
        factors_json = json.dumps(user_data)
        timestamp = datetime.datetime.now().isoformat()

        # SQL Injection 風險
        query = f"""
            INSERT INTO risk_history (user_id, risk_score, factors, timestamp)
            VALUES ('{user_id}', {risk_score}, '{factors_json}', '{timestamp}')
        """
        cursor.execute(query)
        self.conn.commit()

    def get_user_risk_history(self, user_id):
        """取得用戶風險歷史"""
        cursor = self.conn.cursor()
        # 又一個 SQL Injection 風險
        query = f"SELECT * FROM risk_history WHERE user_id = '{user_id}' ORDER BY timestamp DESC"
        cursor.execute(query)
        return cursor.fetchall()

    def batch_calculate(self, users_file):
        """批量計算風險（效能有問題）"""
        results = []
        with open(users_file, 'r') as f:
            users = json.load(f)

        for user in users:
            # 每個用戶都重新連接資料庫
            result = self.calculate_risk(user)
            results.append(result)

            # 沒有錯誤處理
            print(f"Processed user {user['user_id']}")

        return results

# 使用範例
if __name__ == "__main__":
    calculator = RiskCalculator()

    sample_user = {
        'user_id': 'USER123',
        'age': 28,
        'annual_income': 75000,
        'location_tier': 'tier1',
        'profession': 'engineer_corporate',
        'credit_history': [
            {'status': 'paid', 'amount': 5000},
            {'status': 'paid', 'amount': 10000}
        ],
        'has_dependents': False,
        'owns_property': False,
        'education_level': 'graduate'
    }

    result = calculator.calculate_risk(sample_user)
    print(f"Risk assessment: {result}")
```

### 發現的問題

初步分析發現以下問題：
1. **單一巨大方法**：`calculate_risk()` 超過 100 行
2. **複雜的巢狀邏輯**：難以理解和測試
3. **硬編碼參數**：風險參數散落在代碼中
4. **SQL Injection 漏洞**：字串拼接 SQL
5. **缺乏錯誤處理**：沒有異常處理機制
6. **效能問題**：批量處理時重複連接資料庫
7. **缺乏測試**：無法確保重構後功能正確

### 你的任務

設計並執行一套完整的重構流程：

1. **Legacy 代碼分析**：深度分析現有問題
2. **測試安全網建立**：為現有代碼寫測試
3. **系統化重構**：按步驟重構，保持功能不變
4. **重構驗證**：確保重構後功能正確、性能提升

---

## 學習重點

### 目標 1：Legacy 代碼分析方法論

學會系統化分析老舊代碼的方法：
- **代碼味道識別**：長方法、複雜條件、重複代碼
- **依賴關係分析**：找出耦合點
- **安全風險評估**：識別潛在漏洞
- **效能瓶頸分析**：找出性能問題

### 目標 2：重構前的安全網建立

理解為什麼要先寫測試：
- **行為保護**：確保重構不改變功能
- **回歸檢測**：快速發現破壞性變更
- **文檔作用**：測試即代碼規範
- **信心建立**：敢於大幅重構

### 目標 3：漸進式重構策略

掌握安全的重構步驟：
- **提取方法**：拆分大方法
- **提取類別**：分離職責
- **移除重複**：DRY 原則
- **優化演算法**：性能改善

### 目標 4：代碼品質提升

學會現代化代碼的特徵：
- **SOLID 原則**：單一職責、開閉原則等
- **設計模式**：Strategy, Factory 等
- **錯誤處理**：異常處理與日誌
- **安全性**：防止 SQL Injection 等

---

## 建議解決流程

### 階段一：深度代碼分析（45 分鐘）

**目標**：全面理解現有代碼的問題

```bash
# 切換到代碼分析專家
/agents:code-reviewer

# 深度分析指令
請對 src/risk_calculator.py 進行全面的代碼分析。

分析重點：
1. 代碼結構問題
   - 方法長度和複雜度
   - 職責劃分是否清晰
   - 耦合度和內聚性

2. 代碼味道識別
   - 長參數列表
   - 複雜的條件邏輯
   - 重複代碼
   - 魔術數字/字串

3. 安全風險
   - SQL Injection 漏洞
   - 輸入驗證缺失
   - 敏感資料處理

4. 效能問題
   - 資料庫操作效率
   - 記憶體使用
   - 批量處理邏輯

5. 可維護性問題
   - 硬編碼配置
   - 錯誤處理缺失
   - 測試困難度

請提供：
- 問題清單（按嚴重性分級）
- 重構建議（具體方案）
- 風險評估（重構複雜度）
```

**預期輸出範例**：

```markdown
# Legacy 代碼分析報告

## 🔴 Critical 問題

### C1: SQL Injection 漏洞（2處）
**位置**：save_risk_record(), get_user_risk_history()
**問題**：使用字串拼接構建 SQL 查詢
**風險**：高 - 可能導致資料洩露或破壞
**重構建議**：使用參數化查詢

### C2: 單一巨大方法（calculate_risk）
**問題**：方法超過 100 行，職責不清
**影響**：難以理解、測試、維護
**重構建議**：使用提取方法重構

## 🟠 High 問題

### H1: 複雜的巢狀條件邏輯
**位置**：年齡、收入、信用評估邏輯
**問題**：if-elif-else 嵌套過深
**重構建議**：使用 Strategy 模式

### H2: 硬編碼風險參數
**問題**：參數散落在代碼中，難以調整
**重構建議**：提取到設定檔或資料庫

### H3: 缺乏錯誤處理
**問題**：檔案讀取、資料庫操作無異常處理
**風險**：程式容易崩潰

## 🟡 Medium 問題

### M1: 效能問題（批量處理）
**問題**：每個用戶重新連接資料庫
**影響**：批量處理時性能差
**重構建議**：使用連接池或批量操作

### M2: 職責混亂
**問題**：計算邏輯、資料存取、配置管理混在一起
**重構建議**：分層架構

## 重構計畫建議

### Phase 1: 安全網建立（先寫測試）
1. 為現有 calculate_risk() 寫綜合測試
2. 為資料庫操作寫測試
3. 為批量處理寫測試

### Phase 2: 安全修復（優先處理 Critical）
1. 修復 SQL Injection（參數化查詢）
2. 添加輸入驗證
3. 添加異常處理

### Phase 3: 結構重構
1. 提取風險計算策略
2. 分離資料存取層
3. 提取配置管理

### Phase 4: 性能優化
1. 優化資料庫操作
2. 改進批量處理
3. 添加快取機制

預估重構時間：2-3 天
風險級別：Medium（有測試保護）
```

**自然學到的分析技巧**：
- 如何系統化識別代碼問題
- 重構的優先級排序原則
- 風險評估的方法

**記憶沉澱**：
```bash
/memory save

主題：Legacy 代碼分析檢查清單

Critical 級別問題（必須優先修復）：
1. 安全漏洞（SQL Injection, XSS 等）
2. 單一巨大方法（>50 行且邏輯複雜）
3. 缺乏錯誤處理的關鍵操作

High 級別問題：
1. 複雜的巢狀邏輯（循環複雜度 >10）
2. 硬編碼配置或魔術數字
3. 職責不清的類別

Medium 級別問題：
1. 性能瓶頸
2. 重複代碼
3. 命名不清晰

分析工具：code-reviewer agent
記憶技巧：從外到內，從安全到性能
```

---

### 階段二：測試安全網建立（40 分鐘）

**目標**：為現有代碼建立完整測試，確保重構安全

```bash
# 切換到測試專家
/agents:test-engineer

# 測試策略設計
基於上述代碼分析，請設計完整的測試策略。

要求：
1. 為現有的 RiskCalculator 建立測試套件
2. 覆蓋所有主要功能路徑
3. 包含邊界條件和異常情況
4. 測試應該通過現有代碼（即使代碼有問題）

測試重點：
1. calculate_risk() 的各種輸入組合
2. 風險等級分類邏輯
3. 資料庫操作（需要 mock）
4. 批量處理功能
5. 邊界條件（空輸入、極值等）

請提供：
1. 測試檔案結構
2. 完整的測試代碼
3. Mock 策略
4. 測試資料準備
```

**預期輸出範例**：

```python
# tests/test_risk_calculator.py
import pytest
import tempfile
import sqlite3
import json
from unittest.mock import patch, MagicMock
from src.risk_calculator import RiskCalculator

class TestRiskCalculator:
    """RiskCalculator 測試套件 - 為重構建立安全網"""

    @pytest.fixture
    def temp_db(self):
        """建立臨時資料庫用於測試"""
        with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as f:
            yield f.name

    @pytest.fixture
    def calculator(self, temp_db):
        """建立測試用的 RiskCalculator 實例"""
        return RiskCalculator(db_path=temp_db)

    def test_calculate_risk_standard_user(self, calculator):
        """測試標準用戶的風險計算"""
        user_data = {
            'user_id': 'TEST001',
            'age': 30,
            'annual_income': 60000,
            'location_tier': 'tier2',
            'profession': 'engineer_corporate',
            'credit_history': [
                {'status': 'paid', 'amount': 5000}
            ],
            'has_dependents': False,
            'owns_property': False,
            'education_level': 'graduate'
        }

        result = calculator.calculate_risk(user_data)

        # 驗證回傳結構
        assert 'user_id' in result
        assert 'risk_score' in result
        assert 'risk_level' in result
        assert 'factors' in result

        # 驗證基本邏輯（現有代碼的行為）
        assert result['user_id'] == 'TEST001'
        assert isinstance(result['risk_score'], (int, float))
        assert result['risk_level'] in ['LOW', 'MEDIUM', 'HIGH', 'CRITICAL']

    def test_calculate_risk_high_risk_user(self, calculator):
        """測試高風險用戶"""
        user_data = {
            'user_id': 'TEST002',
            'age': 22,  # 年輕
            'annual_income': 25000,  # 低收入
            'location_tier': 'rural',  # 農村
            'profession': 'freelancer',  # 高風險職業
            'credit_history': [
                {'status': 'default', 'amount': 10000}  # 有違約記錄
            ],
            'has_dependents': False,
            'owns_property': False,
            'education_level': 'high_school'
        }

        result = calculator.calculate_risk(user_data)

        # 高風險用戶應該有更高的分數
        assert result['risk_score'] > 100  # 基於現有邏輯
        assert result['risk_level'] in ['HIGH', 'CRITICAL']

    def test_calculate_risk_low_risk_user(self, calculator):
        """測試低風險用戶"""
        user_data = {
            'user_id': 'TEST003',
            'age': 45,  # 中年
            'annual_income': 200000,  # 高收入
            'location_tier': 'tier1',  # 一線城市
            'profession': 'doctor',  # 穩定職業
            'credit_history': [
                {'status': 'paid', 'amount': 5000} for _ in range(15)  # 良好信用
            ],
            'has_dependents': True,  # 有家庭
            'owns_property': True,  # 有房產
            'education_level': 'postgraduate'
        }

        result = calculator.calculate_risk(user_data)

        # 低風險用戶應該有較低分數
        assert result['risk_score'] < 100
        assert result['risk_level'] in ['LOW', 'MEDIUM']

    def test_risk_level_classification(self, calculator):
        """測試風險等級分類邏輯"""
        assert calculator.get_risk_level(50) == 'LOW'
        assert calculator.get_risk_level(80) == 'LOW'
        assert calculator.get_risk_level(100) == 'MEDIUM'
        assert calculator.get_risk_level(120) == 'MEDIUM'
        assert calculator.get_risk_level(140) == 'HIGH'
        assert calculator.get_risk_level(160) == 'HIGH'
        assert calculator.get_risk_level(200) == 'CRITICAL'

    def test_calculate_risk_edge_cases(self, calculator):
        """測試邊界條件"""
        # 最小年齡
        young_user = {
            'user_id': 'YOUNG',
            'age': 16,  # 小於 18
            'annual_income': 50000,
            'location_tier': 'tier2',
            'profession': 'student',
            'credit_history': []
        }
        result = calculator.calculate_risk(young_user)
        assert result['risk_score'] > 0

        # 無信用記錄
        no_credit_user = {
            'user_id': 'NOCREDIT',
            'age': 25,
            'annual_income': 50000,
            'location_tier': 'tier2',
            'profession': 'engineer_corporate',
            'credit_history': []  # 空的信用記錄
        }
        result = calculator.calculate_risk(no_credit_user)
        assert result['risk_score'] > 100  # 無信用應該增加風險

    def test_calculate_risk_missing_fields(self, calculator):
        """測試缺少欄位的情況"""
        minimal_user = {
            'user_id': 'MINIMAL'
            # 其他欄位都缺少，測試預設值處理
        }

        # 現有代碼應該能處理（雖然可能不完美）
        result = calculator.calculate_risk(minimal_user)
        assert 'risk_score' in result

    @patch('sqlite3.connect')
    def test_save_risk_record(self, mock_connect, calculator):
        """測試風險記錄保存（Mock 資料庫）"""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        calculator.save_risk_record('TEST', 95.5, {'test': 'data'})

        # 驗證 SQL 執行（即使有 injection 風險）
        mock_cursor.execute.assert_called_once()
        mock_conn.commit.assert_called_once()

    def test_batch_calculate_functionality(self, calculator, tmp_path):
        """測試批量計算功能"""
        # 準備測試資料檔案
        test_users = [
            {
                'user_id': 'BATCH001',
                'age': 30,
                'annual_income': 50000,
                'location_tier': 'tier2',
                'profession': 'teacher',
                'credit_history': []
            },
            {
                'user_id': 'BATCH002',
                'age': 25,
                'annual_income': 40000,
                'location_tier': 'tier3',
                'profession': 'nurse',
                'credit_history': []
            }
        ]

        users_file = tmp_path / "test_users.json"
        users_file.write_text(json.dumps(test_users))

        results = calculator.batch_calculate(str(users_file))

        assert len(results) == 2
        assert results[0]['user_id'] == 'BATCH001'
        assert results[1]['user_id'] == 'BATCH002'

    def test_get_user_risk_history(self, calculator):
        """測試獲取用戶風險歷史"""
        # 先儲存一些記錄
        calculator.save_risk_record('HISTORY_TEST', 85.0, {'test': 'data'})

        history = calculator.get_user_risk_history('HISTORY_TEST')
        assert len(history) >= 1

# 整合測試
class TestRiskCalculatorIntegration:
    """整合測試 - 測試完整工作流程"""

    def test_complete_workflow(self, tmp_path):
        """測試完整的風險評估工作流程"""
        # 建立臨時資料庫
        db_path = tmp_path / "test.db"
        calculator = RiskCalculator(str(db_path))

        # 準備多個用戶
        users = [
            {
                'user_id': f'USER{i:03d}',
                'age': 20 + i,
                'annual_income': 30000 + (i * 5000),
                'location_tier': ['tier1', 'tier2', 'tier3'][i % 3],
                'profession': 'engineer_corporate',
                'credit_history': []
            }
            for i in range(5)
        ]

        # 逐一計算風險
        results = []
        for user in users:
            result = calculator.calculate_risk(user)
            results.append(result)

            # 驗證每個結果
            assert result['user_id'] == user['user_id']
            assert result['risk_score'] > 0

        # 驗證歷史記錄
        for user in users:
            history = calculator.get_user_risk_history(user['user_id'])
            assert len(history) >= 1

# 效能測試
class TestRiskCalculatorPerformance:
    """效能基準測試 - 為重構後比較"""

    def test_single_calculation_performance(self, calculator, benchmark):
        """測試單一計算的效能基準"""
        user_data = {
            'user_id': 'PERF_TEST',
            'age': 30,
            'annual_income': 60000,
            'location_tier': 'tier2',
            'profession': 'engineer_corporate',
            'credit_history': [{'status': 'paid', 'amount': 5000}] * 5,
            'has_dependents': False,
            'owns_property': False,
            'education_level': 'graduate'
        }

        # 使用 pytest-benchmark 測量基準性能
        result = benchmark(calculator.calculate_risk, user_data)
        assert result['risk_score'] > 0

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
```

**測試執行與驗證**：

```bash
# 執行測試套件
pytest tests/test_risk_calculator.py -v

# 測試覆蓋率報告
pytest --cov=src tests/ --cov-report=html

# 效能基準測試
pytest tests/test_risk_calculator.py::TestRiskCalculatorPerformance -v
```

**自然學到的測試策略**：
- 為什麼要先測試再重構？保證行為不變
- 如何為 Legacy 代碼寫測試？接受現有行為，即使有問題
- Mock 的使用時機：外部依賴（資料庫、檔案系統）

---

### 階段三：系統化重構執行（60 分鐘）

**目標**：按階段安全重構，每步都有測試保護

```bash
# 切換到重構專家
/agents:refactoring-specialist

# 重構執行計畫
現在有了測試安全網，請開始系統化重構 RiskCalculator。

重構原則：
1. 小步快跑：每次只改一個問題
2. 測試先行：每步重構後立即跑測試
3. 功能保持：不改變對外行為
4. 逐步改善：從 Critical → High → Medium

第一輪重構目標：
1. 修復 SQL Injection 漏洞
2. 提取風險計算邏輯
3. 分離資料存取層
4. 添加異常處理

請提供：
1. 詳細的重構步驟
2. 每步的代碼變更
3. 測試驗證方法
4. 重構前後的比較
```

**步驟 1：修復安全漏洞**

```python
# src/risk_calculator.py (重構第一步：安全修復)

import json
import datetime
import sqlite3
from typing import Dict, Any, List, Optional
import logging

# 添加日誌
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RiskCalculator:
    """風險計算器 - 第一輪重構：安全修復"""

    def __init__(self, db_path: str = "risk.db"):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        self.setup_db()

        # 風險參數保持不變（下一步再重構）
        self.risk_params = {
            'age_factor': {
                '18-25': 1.8,
                '26-35': 1.4,
                '36-45': 1.1,
                '46-60': 0.9,
                '60+': 0.7
            },
            'income_factor': {
                'low': 2.0,
                'medium': 1.5,
                'high': 1.0,
                'vhigh': 0.8
            },
            'location_risk': {
                'tier1': 0.8,
                'tier2': 1.0,
                'tier3': 1.3,
                'rural': 1.6
            }
        }

    def setup_db(self):
        """初始化資料庫"""
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS risk_history (
                    id INTEGER PRIMARY KEY,
                    user_id TEXT,
                    risk_score REAL,
                    factors TEXT,
                    timestamp TEXT
                )
            """)
            self.conn.commit()
            logger.info("Database setup completed")
        except sqlite3.Error as e:
            logger.error(f"Database setup failed: {e}")
            raise

    def save_risk_record(self, user_id: str, risk_score: float, user_data: Dict[str, Any]):
        """儲存風險記錄 - 修復 SQL Injection"""
        try:
            cursor = self.conn.cursor()
            factors_json = json.dumps(user_data)
            timestamp = datetime.datetime.now().isoformat()

            # ✅ 使用參數化查詢修復 SQL Injection
            query = """
                INSERT INTO risk_history (user_id, risk_score, factors, timestamp)
                VALUES (?, ?, ?, ?)
            """
            cursor.execute(query, (user_id, risk_score, factors_json, timestamp))
            self.conn.commit()
            logger.info(f"Risk record saved for user {user_id}")

        except sqlite3.Error as e:
            logger.error(f"Failed to save risk record for {user_id}: {e}")
            raise
        except json.JSONEncodeError as e:
            logger.error(f"Failed to serialize user data: {e}")
            raise

    def get_user_risk_history(self, user_id: str) -> List[tuple]:
        """取得用戶風險歷史 - 修復 SQL Injection"""
        try:
            cursor = self.conn.cursor()
            # ✅ 使用參數化查詢修復 SQL Injection
            query = "SELECT * FROM risk_history WHERE user_id = ? ORDER BY timestamp DESC"
            cursor.execute(query, (user_id,))
            results = cursor.fetchall()
            logger.info(f"Retrieved {len(results)} risk records for user {user_id}")
            return results

        except sqlite3.Error as e:
            logger.error(f"Failed to get risk history for {user_id}: {e}")
            raise

    # calculate_risk 方法暫時保持不變，下一步再重構
    def calculate_risk(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """計算用戶風險分數 - 添加輸入驗證和異常處理"""
        try:
            # ✅ 添加輸入驗證
            if not user_data:
                raise ValueError("User data cannot be empty")

            if not user_data.get('user_id'):
                raise ValueError("User ID is required")

            # 原有計算邏輯（暫時保持不變）
            base_score = 100

            # 年齡因子（添加異常處理）
            age = user_data.get('age', 0)
            if not isinstance(age, (int, float)) or age < 0:
                logger.warning(f"Invalid age value: {age}, using default")
                age = 30  # 預設值

            if age < 18:
                age_key = '18-25'
            elif age <= 25:
                age_key = '18-25'
            elif age <= 35:
                age_key = '26-35'
            elif age <= 45:
                age_key = '36-45'
            elif age <= 60:
                age_key = '46-60'
            else:
                age_key = '60+'

            age_factor = self.risk_params['age_factor'][age_key]

            # 收入因子（添加驗證）
            income = user_data.get('annual_income', 0)
            if not isinstance(income, (int, float)) or income < 0:
                logger.warning(f"Invalid income value: {income}, using default")
                income = 50000  # 預設值

            if income < 30000:
                income_factor = self.risk_params['income_factor']['low']
            elif income < 100000:
                income_factor = self.risk_params['income_factor']['medium']
            elif income < 500000:
                income_factor = self.risk_params['income_factor']['high']
            else:
                income_factor = self.risk_params['income_factor']['vhigh']

            # 地區因子
            location = user_data.get('location_tier', 'tier2')
            location_factor = self.risk_params['location_risk'].get(location, 1.0)

            # 信用歷史（保持原邏輯，下一步再重構）
            credit_history = user_data.get('credit_history', [])
            if not isinstance(credit_history, list):
                logger.warning("Invalid credit_history format, using empty list")
                credit_history = []

            credit_score = 1.0
            if len(credit_history) == 0:
                credit_score = 2.0
            else:
                defaults = sum(1 for record in credit_history
                             if isinstance(record, dict) and record.get('status') == 'default')
                if defaults > 0:
                    credit_score = 1.5 + (defaults * 0.3)
                else:
                    good_records = len([r for r in credit_history
                                      if isinstance(r, dict) and r.get('status') == 'paid'])
                    if good_records > 10:
                        credit_score = 0.7
                    elif good_records > 5:
                        credit_score = 0.8
                    else:
                        credit_score = 0.9

            # 職業風險
            profession = user_data.get('profession', 'unknown')
            profession_risk = 1.0
            high_risk_jobs = ['freelancer', 'artist', 'startup_founder', 'consultant']
            stable_jobs = ['government', 'teacher', 'doctor', 'engineer_corporate']

            if profession in high_risk_jobs:
                profession_risk = 1.4
            elif profession in stable_jobs:
                profession_risk = 0.8
            elif profession == 'unemployed':
                profession_risk = 2.5

            # 計算最終分數
            risk_score = base_score * age_factor * income_factor * location_factor * credit_score * profession_risk

            # 額外調整
            if user_data.get('has_dependents', False):
                risk_score *= 0.9

            if user_data.get('owns_property', False):
                risk_score *= 0.85

            education = user_data.get('education_level')
            if education == 'graduate':
                risk_score *= 0.9
            elif education == 'postgraduate':
                risk_score *= 0.85

            # 儲存記錄
            self.save_risk_record(user_data.get('user_id'), risk_score, user_data)

            result = {
                'user_id': user_data.get('user_id'),
                'risk_score': round(risk_score, 2),
                'risk_level': self.get_risk_level(risk_score),
                'factors': {
                    'age_factor': age_factor,
                    'income_factor': income_factor,
                    'location_factor': location_factor,
                    'credit_score': credit_score,
                    'profession_risk': profession_risk
                }
            }

            logger.info(f"Risk calculated for user {user_data.get('user_id')}: {result['risk_level']}")
            return result

        except Exception as e:
            logger.error(f"Risk calculation failed for user {user_data.get('user_id', 'unknown')}: {e}")
            raise

    def get_risk_level(self, score: float) -> str:
        """將風險分數轉換為等級"""
        if score <= 80:
            return 'LOW'
        elif score <= 120:
            return 'MEDIUM'
        elif score <= 160:
            return 'HIGH'
        else:
            return 'CRITICAL'

    def batch_calculate(self, users_file: str) -> List[Dict[str, Any]]:
        """批量計算風險 - 添加異常處理"""
        results = []
        try:
            with open(users_file, 'r', encoding='utf-8') as f:
                users = json.load(f)

            if not isinstance(users, list):
                raise ValueError("Users file must contain a list of user objects")

            logger.info(f"Starting batch calculation for {len(users)} users")

            for i, user in enumerate(users):
                try:
                    result = self.calculate_risk(user)
                    results.append(result)
                    logger.info(f"Processed user {i+1}/{len(users)}: {user.get('user_id', 'unknown')}")

                except Exception as e:
                    logger.error(f"Failed to process user {i+1}: {e}")
                    # 繼續處理其他用戶，而不是中斷整個批量
                    continue

            logger.info(f"Batch calculation completed: {len(results)}/{len(users)} successful")
            return results

        except FileNotFoundError:
            logger.error(f"Users file not found: {users_file}")
            raise
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in users file: {e}")
            raise
        except Exception as e:
            logger.error(f"Batch calculation failed: {e}")
            raise

    def __del__(self):
        """確保資料庫連接正確關閉"""
        if hasattr(self, 'conn'):
            self.conn.close()
```

**驗證第一步重構**：

```bash
# 執行測試確保功能不變
pytest tests/test_risk_calculator.py -v

# 安全掃描驗證
bandit src/risk_calculator.py

# 如果測試通過，提交這一步
git add src/risk_calculator.py
git commit -m "refactor: fix SQL injection vulnerabilities and add error handling"
```

**步驟 2：提取風險計算策略**

```python
# src/risk_strategies.py (新檔案：提取風險計算邏輯)

from abc import ABC, abstractmethod
from typing import Dict, Any, List
import logging

logger = logging.getLogger(__name__)

class RiskFactor(ABC):
    """風險因子抽象基類"""

    @abstractmethod
    def calculate(self, user_data: Dict[str, Any]) -> float:
        """計算該因子的風險係數"""
        pass

    @abstractmethod
    def get_factor_name(self) -> str:
        """取得因子名稱"""
        pass

class AgeFactor(RiskFactor):
    """年齡風險因子"""

    def __init__(self):
        self.age_mapping = {
            '18-25': 1.8,
            '26-35': 1.4,
            '36-45': 1.1,
            '46-60': 0.9,
            '60+': 0.7
        }

    def calculate(self, user_data: Dict[str, Any]) -> float:
        age = user_data.get('age', 30)

        if not isinstance(age, (int, float)) or age < 0:
            logger.warning(f"Invalid age value: {age}, using default 30")
            age = 30

        if age < 18:
            age_key = '18-25'
        elif age <= 25:
            age_key = '18-25'
        elif age <= 35:
            age_key = '26-35'
        elif age <= 45:
            age_key = '36-45'
        elif age <= 60:
            age_key = '46-60'
        else:
            age_key = '60+'

        return self.age_mapping[age_key]

    def get_factor_name(self) -> str:
        return "age_factor"

class IncomeFactor(RiskFactor):
    """收入風險因子"""

    def __init__(self):
        self.income_thresholds = [
            (30000, 2.0),    # low
            (100000, 1.5),   # medium
            (500000, 1.0),   # high
            (float('inf'), 0.8)  # very high
        ]

    def calculate(self, user_data: Dict[str, Any]) -> float:
        income = user_data.get('annual_income', 50000)

        if not isinstance(income, (int, float)) or income < 0:
            logger.warning(f"Invalid income value: {income}, using default 50000")
            income = 50000

        for threshold, factor in self.income_thresholds:
            if income < threshold:
                return factor

        return 0.8  # fallback

    def get_factor_name(self) -> str:
        return "income_factor"

class LocationFactor(RiskFactor):
    """地區風險因子"""

    def __init__(self):
        self.location_mapping = {
            'tier1': 0.8,
            'tier2': 1.0,
            'tier3': 1.3,
            'rural': 1.6
        }

    def calculate(self, user_data: Dict[str, Any]) -> float:
        location = user_data.get('location_tier', 'tier2')
        return self.location_mapping.get(location, 1.0)

    def get_factor_name(self) -> str:
        return "location_factor"

class CreditFactor(RiskFactor):
    """信用歷史風險因子"""

    def calculate(self, user_data: Dict[str, Any]) -> float:
        credit_history = user_data.get('credit_history', [])

        if not isinstance(credit_history, list):
            logger.warning("Invalid credit_history format, using empty list")
            credit_history = []

        if len(credit_history) == 0:
            return 2.0  # 無信用記錄風險較高

        defaults = sum(1 for record in credit_history
                      if isinstance(record, dict) and record.get('status') == 'default')

        if defaults > 0:
            return 1.5 + (defaults * 0.3)

        # 良好信用記錄
        good_records = len([r for r in credit_history
                           if isinstance(r, dict) and r.get('status') == 'paid'])

        if good_records > 10:
            return 0.7
        elif good_records > 5:
            return 0.8
        else:
            return 0.9

    def get_factor_name(self) -> str:
        return "credit_score"

class ProfessionFactor(RiskFactor):
    """職業風險因子"""

    def __init__(self):
        self.profession_mapping = {
            'high_risk': ['freelancer', 'artist', 'startup_founder', 'consultant'],
            'stable': ['government', 'teacher', 'doctor', 'engineer_corporate'],
            'unemployed': ['unemployed']
        }

        self.risk_scores = {
            'high_risk': 1.4,
            'stable': 0.8,
            'unemployed': 2.5,
            'default': 1.0
        }

    def calculate(self, user_data: Dict[str, Any]) -> float:
        profession = user_data.get('profession', 'unknown')

        for category, jobs in self.profession_mapping.items():
            if profession in jobs:
                return self.risk_scores[category]

        return self.risk_scores['default']

    def get_factor_name(self) -> str:
        return "profession_risk"

class BonusAdjustment:
    """額外調整因子（非核心風險因子）"""

    @staticmethod
    def calculate_adjustments(user_data: Dict[str, Any]) -> float:
        """計算所有額外調整的累積係數"""
        adjustment = 1.0

        # 家庭負擔
        if user_data.get('has_dependents', False):
            adjustment *= 0.9

        # 房產擁有
        if user_data.get('owns_property', False):
            adjustment *= 0.85

        # 教育程度
        education = user_data.get('education_level')
        if education == 'graduate':
            adjustment *= 0.9
        elif education == 'postgraduate':
            adjustment *= 0.85

        return adjustment

class RiskCalculationEngine:
    """風險計算引擎 - 組合所有風險因子"""

    def __init__(self, base_score: float = 100.0):
        self.base_score = base_score
        self.risk_factors: List[RiskFactor] = [
            AgeFactor(),
            IncomeFactor(),
            LocationFactor(),
            CreditFactor(),
            ProfessionFactor()
        ]

    def calculate_risk_score(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """計算風險分數和各因子貢獻"""

        # 計算各風險因子
        factors = {}
        total_factor = 1.0

        for risk_factor in self.risk_factors:
            factor_value = risk_factor.calculate(user_data)
            factor_name = risk_factor.get_factor_name()
            factors[factor_name] = factor_value
            total_factor *= factor_value

        # 基礎分數
        risk_score = self.base_score * total_factor

        # 額外調整
        bonus_adjustment = BonusAdjustment.calculate_adjustments(user_data)
        risk_score *= bonus_adjustment

        return {
            'risk_score': round(risk_score, 2),
            'factors': factors,
            'bonus_adjustment': bonus_adjustment
        }

    def add_risk_factor(self, factor: RiskFactor):
        """動態添加新的風險因子"""
        self.risk_factors.append(factor)

    def remove_risk_factor(self, factor_name: str):
        """移除風險因子"""
        self.risk_factors = [f for f in self.risk_factors
                           if f.get_factor_name() != factor_name]
```

**更新主要計算器**：

```python
# src/risk_calculator.py (重構第二步：使用策略模式)

import json
import datetime
import sqlite3
from typing import Dict, Any, List, Optional
import logging

from .risk_strategies import RiskCalculationEngine

logger = logging.getLogger(__name__)

class RiskCalculator:
    """風險計算器 - 第二輪重構：策略模式"""

    def __init__(self, db_path: str = "risk.db"):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        self.setup_db()

        # ✅ 使用風險計算引擎
        self.calculation_engine = RiskCalculationEngine()

    def setup_db(self):
        """初始化資料庫"""
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS risk_history (
                    id INTEGER PRIMARY KEY,
                    user_id TEXT,
                    risk_score REAL,
                    factors TEXT,
                    timestamp TEXT
                )
            """)
            self.conn.commit()
            logger.info("Database setup completed")
        except sqlite3.Error as e:
            logger.error(f"Database setup failed: {e}")
            raise

    def calculate_risk(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """計算用戶風險分數 - 簡化後的主邏輯"""
        try:
            # 輸入驗證
            if not user_data or not user_data.get('user_id'):
                raise ValueError("User data and user_id are required")

            # ✅ 使用策略模式計算風險
            calculation_result = self.calculation_engine.calculate_risk_score(user_data)

            risk_score = calculation_result['risk_score']
            factors = calculation_result['factors']

            # 儲存記錄
            self.save_risk_record(user_data.get('user_id'), risk_score, user_data)

            result = {
                'user_id': user_data.get('user_id'),
                'risk_score': risk_score,
                'risk_level': self.get_risk_level(risk_score),
                'factors': factors
            }

            logger.info(f"Risk calculated for user {user_data.get('user_id')}: {result['risk_level']}")
            return result

        except Exception as e:
            logger.error(f"Risk calculation failed for user {user_data.get('user_id', 'unknown')}: {e}")
            raise

    def get_risk_level(self, score: float) -> str:
        """將風險分數轉換為等級"""
        if score <= 80:
            return 'LOW'
        elif score <= 120:
            return 'MEDIUM'
        elif score <= 160:
            return 'HIGH'
        else:
            return 'CRITICAL'

    # 資料存取方法保持不變...
    def save_risk_record(self, user_id: str, risk_score: float, user_data: Dict[str, Any]):
        """儲存風險記錄"""
        try:
            cursor = self.conn.cursor()
            factors_json = json.dumps(user_data)
            timestamp = datetime.datetime.now().isoformat()

            query = """
                INSERT INTO risk_history (user_id, risk_score, factors, timestamp)
                VALUES (?, ?, ?, ?)
            """
            cursor.execute(query, (user_id, risk_score, factors_json, timestamp))
            self.conn.commit()
            logger.info(f"Risk record saved for user {user_id}")

        except sqlite3.Error as e:
            logger.error(f"Failed to save risk record for {user_id}: {e}")
            raise

    def get_user_risk_history(self, user_id: str) -> List[tuple]:
        """取得用戶風險歷史"""
        try:
            cursor = self.conn.cursor()
            query = "SELECT * FROM risk_history WHERE user_id = ? ORDER BY timestamp DESC"
            cursor.execute(query, (user_id,))
            results = cursor.fetchall()
            logger.info(f"Retrieved {len(results)} risk records for user {user_id}")
            return results

        except sqlite3.Error as e:
            logger.error(f"Failed to get risk history for {user_id}: {e}")
            raise

    def batch_calculate(self, users_file: str) -> List[Dict[str, Any]]:
        """批量計算風險"""
        results = []
        try:
            with open(users_file, 'r', encoding='utf-8') as f:
                users = json.load(f)

            if not isinstance(users, list):
                raise ValueError("Users file must contain a list of user objects")

            logger.info(f"Starting batch calculation for {len(users)} users")

            for i, user in enumerate(users):
                try:
                    result = self.calculate_risk(user)
                    results.append(result)
                    logger.info(f"Processed user {i+1}/{len(users)}: {user.get('user_id', 'unknown')}")

                except Exception as e:
                    logger.error(f"Failed to process user {i+1}: {e}")
                    continue

            logger.info(f"Batch calculation completed: {len(results)}/{len(users)} successful")
            return results

        except Exception as e:
            logger.error(f"Batch calculation failed: {e}")
            raise

    def __del__(self):
        """確保資料庫連接正確關閉"""
        if hasattr(self, 'conn'):
            self.conn.close()
```

**自然學到的重構技巧**：
- 提取方法：將複雜邏輯拆分為小方法
- 策略模式：將演算法封裝成可替換的策略
- 單一職責：每個類別只負責一件事
- 開閉原則：對擴展開放，對修改關閉

---

### 階段四：重構驗證與優化（25 分鐘）

**目標**：驗證重構效果，確保質量和性能提升

```bash
# 切換到架構師視角進行最終評估
/agents:architect

# 全面評估重構成果
請評估重構後的代碼架構和品質。

評估重點：
1. 代碼結構改善程度
2. 可維護性提升
3. 可測試性改善
4. 性能對比
5. 安全性提升
6. 未來擴展性

請提供：
1. 重構前後對比分析
2. 架構改善評估
3. 剩餘技術債務
4. 後續改進建議
5. 學習要點總結
```

**最終架構評估**：

```markdown
# 重構成果評估報告

## 📊 重構前後對比

### 代碼結構對比

**重構前**：
```
RiskCalculator (God Object)
├── calculate_risk() [100+ lines]
├── 硬編碼風險參數
├── SQL 字串拼接
└── 無異常處理
```

**重構後**：
```
RiskCalculator (Orchestrator)
├── calculate_risk() [30 lines]
└── 使用 RiskCalculationEngine

RiskCalculationEngine (Strategy Coordinator)
├── AgeFactor
├── IncomeFactor
├── LocationFactor
├── CreditFactor
├── ProfessionFactor
└── BonusAdjustment

Database Layer
├── 參數化查詢
├── 異常處理
└── 日誌記錄
```

### 品質指標改善

| 指標 | 重構前 | 重構後 | 改善 |
|------|--------|--------|------|
| 循環複雜度 | 15+ | 3-5 | ✅ 大幅改善 |
| 方法長度 | 100+ 行 | 30 行以下 | ✅ 顯著改善 |
| 測試覆蓋率 | 0% | 85%+ | ✅ 新增測試 |
| SQL 安全性 | 高風險 | 安全 | ✅ 修復漏洞 |
| 錯誤處理 | 無 | 完整 | ✅ 新增處理 |

## 🏗️ 架構改善評估

### ✅ 成功改善的部分

1. **單一職責原則**
   - 每個 Factor 類別只負責一種風險計算
   - RiskCalculator 只負責協調和資料存取
   - 職責清晰，易於理解

2. **開閉原則**
   - 新增風險因子：實作 RiskFactor 介面即可
   - 修改現有因子：不影響其他部分
   - 擴展性大幅提升

3. **依賴倒轉**
   - 高層模組（RiskCalculator）不依賴低層細節
   - 依賴抽象（RiskFactor 介面）
   - 可注入不同的計算引擎

4. **可測試性**
   - 每個 Factor 可獨立測試
   - Mock 和 Stub 容易實現
   - 測試覆蓋率顯著提升

### 🚀 性能提升

```python
# 重構前性能測試結果
單次計算：~0.5ms
批量 1000 用戶：~2.3s（包含 SQL 問題）

# 重構後性能測試結果
單次計算：~0.3ms（提升 40%）
批量 1000 用戶：~1.8s（提升 22%）

# 性能提升原因：
1. 減少不必要的計算邏輯
2. 更好的異常處理避免重試
3. 策略模式減少條件判斷
```

### 🔒 安全性提升

1. **SQL Injection 完全修復**
   - 所有資料庫操作使用參數化查詢
   - Bandit 掃描 0 個安全問題

2. **輸入驗證強化**
   - 所有用戶輸入都經過驗證
   - 預設值處理邊界情況
   - 類型檢查防止運行時錯誤

3. **錯誤處理完善**
   - 不會洩露敏感資訊
   - 異常記錄但不中斷服務
   - 優雅降級處理

## 📋 剩餘技術債務

### 🟡 Medium 優先級

1. **配置管理**
   ```python
   # 當前：硬編碼在類別中
   self.age_mapping = {'18-25': 1.8, ...}

   # 建議：外部設定檔
   # config/risk_factors.yaml
   age_factor:
     ranges:
       - age_range: [18, 25]
         factor: 1.8
   ```

2. **資料庫連接管理**
   ```python
   # 當前：單一連接
   self.conn = sqlite3.connect(db_path)

   # 建議：連接池
   from sqlalchemy import create_engine
   self.engine = create_engine(db_url, pool_size=10)
   ```

3. **快取機制**
   ```python
   # 建議：為重複計算添加快取
   @lru_cache(maxsize=1000)
   def calculate_risk_cached(self, user_data_hash):
       return self.calculate_risk(user_data)
   ```

### 🟢 Low 優先級

1. **非同步處理**
   - 批量計算可改為非同步
   - 提升大批量處理性能

2. **監控和指標**
   - 添加計算時間監控
   - 風險分布統計
   - 異常率追蹤

## 🎯 學習要點總結

### 重構策略

1. **測試先行**
   - 建立測試安全網是重構成功的關鍵
   - 測試保證功能不變，給重構信心

2. **小步快跑**
   - 每次只改一個問題
   - 立即驗證，及時回饋

3. **從安全到架構**
   - 優先修復安全問題
   - 再改善架構和性能

### 設計模式應用

1. **策略模式**
   - 將算法封裝成可替換的策略
   - 符合開閉原則，易於擴展

2. **工廠模式**（可進一步應用）
   - 動態創建不同類型的風險因子
   - 配置驅動的因子組合

### 代碼品質原則

1. **SOLID 原則**
   - 單一職責：每個類別一個職責
   - 開閉原則：對擴展開放，對修改關閉
   - 依賴倒轉：依賴抽象，不依賴具體實現

2. **Clean Code**
   - 方法名稱清晰表達意圖
   - 參數數量合理（<3 個）
   - 避免深層嵌套

## 📈 後續改進建議

### Phase 3: 配置外部化（1 天）
```python
# 實現配置驅動的風險因子
class ConfigurableRiskEngine:
    def load_config(self, config_path: str):
        # 從 YAML/JSON 載入風險參數

    def create_factors_from_config(self):
        # 根據配置創建因子實例
```

### Phase 4: 機器學習集成（1 週）
```python
# 集成 ML 模型
class MLRiskFactor(RiskFactor):
    def __init__(self, model_path: str):
        self.model = joblib.load(model_path)

    def calculate(self, user_data: Dict[str, Any]) -> float:
        features = self.extract_features(user_data)
        return self.model.predict([features])[0]
```

### Phase 5: 微服務架構（2 週）
```python
# 拆分為微服務
- risk-calculation-service
- risk-history-service
- user-profile-service
- notification-service
```

## 🏆 重構成功指標

✅ **功能完整性**：所有原有功能保持不變
✅ **代碼品質**：從 2/10 提升到 8/10
✅ **安全性**：修復所有 Critical 安全問題
✅ **可維護性**：新需求實現時間減少 60%
✅ **可測試性**：測試覆蓋率從 0% 到 85%+
✅ **性能**：計算速度提升 40%
✅ **擴展性**：新增風險因子只需 1 小時

這次重構是一個 **成功的案例**，展示了如何系統化地改善 Legacy 代碼。
```

**最終記憶沉澱**：

```bash
/memory save

主題：Legacy 代碼重構完整工作流程

4階段重構法：

1️⃣ 分析階段（code-reviewer）
   - 系統化識別問題（Critical/High/Medium）
   - 評估重構風險和複雜度
   - 制定重構優先級

2️⃣ 測試階段（test-engineer）
   - 建立測試安全網
   - 覆蓋所有主要功能路徑
   - 接受現有行為（即使有問題）

3️⃣ 重構階段（refactoring-specialist）
   - 小步快跑，優先修復安全問題
   - 使用設計模式改善架構
   - 每步都要通過測試

4️⃣ 驗證階段（architect）
   - 評估重構成果
   - 對比性能和品質指標
   - 制定後續改進計畫

關鍵原則：
- 測試先行：重構的安全網
- 小步前進：降低風險
- 功能不變：保證業務連續性
- 逐步改善：從安全到架構到性能

成功指標：
- 功能完整性保持
- 代碼品質顯著提升
- 安全漏洞完全修復
- 可維護性大幅改善

適用場景：維護老舊系統、技術債務處理、代碼現代化
相關 Agent：code-reviewer, test-engineer, refactoring-specialist, architect
```

---

## 驗證標準

### ✅ 必須達成

- [ ] 成功完成四階段重構流程
- [ ] 修復所有 SQL Injection 漏洞
- [ ] 建立完整測試安全網（覆蓋率 >80%）
- [ ] 重構後代碼品質顯著提升
- [ ] 功能行為保持完全一致
- [ ] 使用 `/memory` 沉澱至少 2 個重構模式

### ⭐ 額外成就

- [ ] 性能提升超過 30%
- [ ] 實現 SOLID 原則應用
- [ ] 新增風險因子只需修改一個文件
- [ ] 建立自動化重構檢查腳本
- [ ] 設計完整的遷移部署計畫

---

## 學習反思

### 反思問題

1. **重構順序**：
   - 為什麼要先安全，後架構，最後性能？
   - 如果順序顛倒會有什麼問題？

2. **測試策略**：
   - 為什麼要先寫測試再重構？
   - 如何平衡測試完整性與重構速度？

3. **設計模式**：
   - 策略模式在這個場景的優勢是什麼？
   - 還可以應用哪些其他模式？

4. **技術債務**：
   - 如何評估技術債務的優先級？
   - 什麼情況下應該重寫而不是重構？

### 延伸練習

1. **配置外部化**：
   - 將風險參數提取到 YAML 配置文件
   - 實現配置熱更新機制

2. **機器學習集成**：
   - 設計 ML 模型風險因子
   - 實現模型版本管理

3. **微服務拆分**：
   - 設計風險計算的微服務架構
   - 處理分散式事務問題

---

## 相關資源

### 下一步學習

- **C04**：Full-Stack Feature Development - 學習新功能的完整開發流程
- **C05**：Performance Optimization Workflow - 深入性能優化技巧
- **C10**：Code Quality & Security Audit - 建立持續的代碼審查機制

### 重構參考資料

- **《Refactoring（Martin Fowler）》**：經典重構模式
- **《Working Effectively with Legacy Code》**：Legacy 代碼處理策略
- **《Clean Code》**：代碼品質標準
- **SOLID 原則**：面向對象設計原則

### 工具推薦

- **SonarQube**：代碼品質持續監控
- **Bandit**：Python 安全掃描器
- **pytest-cov**：測試覆蓋率工具
- **Black**：Python 代碼格式化

---

**建議完成時間**：2.5-3 小時（含反思）
**難度評估**：4/5
**重要度**：5/5（企業必備技能）
**可複用性**：5/5（任何 Legacy 系統都適用）