# B01：CSV 資料清洗與轉換

## 📋 情境描述

### 背景

你是一家電商公司的資料分析師。公司每天收到供應商提供的銷售資料 CSV 檔案，但資料品質不佳，需要清洗後才能載入資料庫進行分析。

**問題**：
- 日期格式不統一（`2025-01-30`, `30/01/2025`, `01-30-2025`）
- 金額欄位有空值
- 產品名稱有多餘的空格
- 存在重複記錄
- 部分欄位型別錯誤

**目前狀況**：
- 手動清洗需要 1 小時
- 容易出錯，需要反覆檢查
- 無法自動化

### 目標

用 AI 輔助建立自動化清洗流程，5 分鐘內完成清洗作業。

---

## 🎯 任務目標

### 主要任務

1. **資料品質分析**（5 分鐘）
   - 載入 CSV 檔案
   - 分析資料問題（空值、格式、異常值）
   - 生成品質報告

2. **設計清洗邏輯**（10 分鐘）
   - 日期格式標準化
   - 處理空值
   - 清理字串
   - 移除重複記錄

3. **實現清洗腳本**（10 分鐘）
   - 用 AI 生成清洗代碼
   - 加入錯誤處理
   - 加入日誌記錄

4. **驗證結果**（5 分鐘）
   - 檢查清洗後的資料品質
   - 對比清洗前後
   - 確認沒有遺漏

**總時間**：30 分鐘

---

## 📂 準備工作

### 測試資料

**`dirty_sales_data.csv`**（範例）：
```csv
date,product_name,category,amount,region
2025-01-30,  iPhone 15  Pro ,Electronics,1299.99,North
30/01/2025,Samsung  Galaxy,Electronics,,South
01-30-2025,MacBook Pro,Electronics,2499.99,East
2025-01-30,iPhone 15 Pro,Electronics,1299.99,North
2025-01-31,iPad Air  ,Electronics,799.99,West
invalid_date,Dell XPS,Electronics,1599.99,North
2025-02-01,  iPhone 15  Pro ,Electronics,1299.99,South
```

**資料問題**：
1. 日期格式不統一（3 種格式）
2. `amount` 欄位有空值（第 3 行）
3. `product_name` 有多餘空格
4. 第 1 行和第 4 行是重複記錄
5. 第 6 行日期無效

---

## 🚀 實作步驟

### 步驟 1：與 AI 對話，分析資料

**與 Claude Code 對話**：
```
我有一個髒亂的 CSV 檔案 dirty_sales_data.csv，請幫我：
1. 讀取檔案
2. 顯示前 10 行
3. 分析資料品質問題
4. 生成品質報告
```

**AI 生成的代碼**：
```python
import pandas as pd
import numpy as np

# Load data
df = pd.read_csv('dirty_sales_data.csv')

print("=" * 50)
print("Data Quality Report")
print("=" * 50)

# Basic info
print(f"\n1. Basic Information:")
print(f"   - Total rows: {len(df)}")
print(f"   - Total columns: {len(df.columns)}")
print(f"   - Columns: {list(df.columns)}")

# Data preview
print(f"\n2. Data Preview:")
print(df.head(10))

# Missing values
print(f"\n3. Missing Values:")
missing = df.isnull().sum()
if missing.sum() == 0:
    print("   ✅ No missing values")
else:
    for col, count in missing[missing > 0].items():
        pct = count / len(df) * 100
        print(f"   - {col}: {count} ({pct:.1f}%)")

# Data types
print(f"\n4. Data Types:")
print(df.dtypes)

# Duplicates
dup_count = df.duplicated().sum()
print(f"\n5. Duplicate Records: {dup_count}")

# String issues (extra spaces)
print(f"\n6. String Issues:")
for col in df.select_dtypes(include=['object']).columns:
    has_spaces = df[col].str.contains(r'^\s+|\s+$', na=False).sum()
    if has_spaces > 0:
        print(f"   - {col}: {has_spaces} records with leading/trailing spaces")

print("\n" + "=" * 50)
```

**輸出範例**：
```
==================================================
Data Quality Report
==================================================

1. Basic Information:
   - Total rows: 7
   - Total columns: 5
   - Columns: ['date', 'product_name', 'category', 'amount', 'region']

2. Data Preview:
           date      product_name      category   amount region
0  2025-01-30    iPhone 15  Pro   Electronics  1299.99  North
1  30/01/2025   Samsung  Galaxy   Electronics      NaN  South
2  01-30-2025      MacBook Pro    Electronics  2499.99   East
3  2025-01-30    iPhone 15 Pro    Electronics  1299.99  North
4  2025-01-31        iPad Air     Electronics   799.99   West
5  invalid_date        Dell XPS    Electronics  1599.99  North
6  2025-02-01   iPhone 15  Pro   Electronics  1299.99  South

3. Missing Values:
   - amount: 1 (14.3%)

4. Data Types:
date             object
product_name     object
category         object
amount          float64
region           object

5. Duplicate Records: 1

6. String Issues:
   - product_name: 4 records with leading/trailing spaces

==================================================
```

---

### 步驟 2：設計清洗邏輯

**與 Claude Code 對話**：
```
基於品質報告，請幫我設計清洗邏輯：
1. 統一日期格式為 YYYY-MM-DD
2. 處理 amount 空值（用中位數填充）
3. 清理 product_name 的空格
4. 移除重複記錄
5. 過濾掉無效日期的記錄

請生成完整的清洗函數
```

**AI 生成的清洗代碼**：
```python
def clean_sales_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean sales data

    Args:
        df: Raw DataFrame

    Returns:
        Cleaned DataFrame
    """
    print("\n🧹 Cleaning data...\n")

    df_clean = df.copy()
    initial_rows = len(df_clean)

    # 1. Standardize date format
    print("1️⃣ Standardizing date format...")
    def parse_date(date_str):
        """Try multiple date formats"""
        if pd.isna(date_str):
            return pd.NaT

        formats = ['%Y-%m-%d', '%d/%m/%Y', '%m-%d-%Y']
        for fmt in formats:
            try:
                return pd.to_datetime(date_str, format=fmt)
            except:
                continue
        return pd.NaT

    df_clean['date'] = df_clean['date'].apply(parse_date)
    invalid_dates = df_clean['date'].isna().sum()
    print(f"   - Converted dates, {invalid_dates} invalid dates found")

    # 2. Handle missing amounts
    print("\n2️⃣ Handling missing amounts...")
    missing_count = df_clean['amount'].isna().sum()
    if missing_count > 0:
        median_amount = df_clean['amount'].median()
        df_clean['amount'].fillna(median_amount, inplace=True)
        print(f"   - Filled {missing_count} missing values with median: ${median_amount:.2f}")
    else:
        print(f"   - No missing amounts")

    # 3. Clean product names
    print("\n3️⃣ Cleaning product names...")
    df_clean['product_name'] = df_clean['product_name'].str.strip()
    df_clean['product_name'] = df_clean['product_name'].str.replace(r'\s+', ' ', regex=True)
    print(f"   - Removed extra spaces")

    # 4. Remove duplicates
    print("\n4️⃣ Removing duplicates...")
    before_dedup = len(df_clean)
    df_clean.drop_duplicates(inplace=True)
    after_dedup = len(df_clean)
    removed = before_dedup - after_dedup
    print(f"   - Removed {removed} duplicate records")

    # 5. Filter invalid dates
    print("\n5️⃣ Filtering invalid records...")
    df_clean = df_clean[df_clean['date'].notna()]
    final_rows = len(df_clean)
    filtered = initial_rows - final_rows
    print(f"   - Filtered {filtered} records with invalid dates")

    print(f"\n✅ Cleaning completed: {initial_rows} → {final_rows} rows")

    return df_clean

# Apply cleaning
df_cleaned = clean_sales_data(df)

# Display cleaned data
print("\n" + "=" * 50)
print("Cleaned Data Preview")
print("=" * 50)
print(df_cleaned)
```

**輸出範例**：
```
🧹 Cleaning data...

1️⃣ Standardizing date format...
   - Converted dates, 1 invalid dates found

2️⃣ Handling missing amounts...
   - Filled 1 missing values with median: $1299.99

3️⃣ Cleaning product names...
   - Removed extra spaces

4️⃣ Removing duplicates...
   - Removed 1 duplicate records

5️⃣ Filtering invalid records...
   - Filtered 1 records with invalid dates

✅ Cleaning completed: 7 → 5 rows

==================================================
Cleaned Data Preview
==================================================
        date  product_name      category   amount region
0 2025-01-30  iPhone 15 Pro  Electronics  1299.99  North
1 2025-01-30  Samsung Galaxy  Electronics  1299.99  South
2 2025-01-30    MacBook Pro   Electronics  2499.99   East
3 2025-01-31       iPad Air   Electronics   799.99   West
4 2025-02-01  iPhone 15 Pro  Electronics  1299.99  South
```

---

### 步驟 3：完整腳本（含錯誤處理）

**`clean_data.py`**：
```python
#!/usr/bin/env python3
"""
CSV Data Cleaning Script

Automatically clean dirty CSV files.
"""

import pandas as pd
import logging
from pathlib import Path

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def clean_sales_data(df: pd.DataFrame) -> pd.DataFrame:
    """Clean sales data with comprehensive error handling"""
    logger.info("Starting data cleaning process")

    df_clean = df.copy()
    initial_rows = len(df_clean)

    try:
        # Date standardization
        def parse_date(date_str):
            if pd.isna(date_str):
                return pd.NaT
            formats = ['%Y-%m-%d', '%d/%m/%Y', '%m-%d-%Y']
            for fmt in formats:
                try:
                    return pd.to_datetime(date_str, format=fmt)
                except:
                    continue
            return pd.NaT

        df_clean['date'] = df_clean['date'].apply(parse_date)
        logger.info(f"Date standardization completed")

        # Handle missing amounts
        missing_count = df_clean['amount'].isna().sum()
        if missing_count > 0:
            median_amount = df_clean['amount'].median()
            df_clean['amount'].fillna(median_amount, inplace=True)
            logger.info(f"Filled {missing_count} missing amounts")

        # Clean strings
        df_clean['product_name'] = df_clean['product_name'].str.strip()
        df_clean['product_name'] = df_clean['product_name'].str.replace(r'\s+', ' ', regex=True)
        logger.info("String cleaning completed")

        # Remove duplicates
        before = len(df_clean)
        df_clean.drop_duplicates(inplace=True)
        after = len(df_clean)
        logger.info(f"Removed {before - after} duplicates")

        # Filter invalid dates
        df_clean = df_clean[df_clean['date'].notna()]
        final_rows = len(df_clean)
        logger.info(f"Filtering completed: {initial_rows} → {final_rows} rows")

        return df_clean

    except Exception as e:
        logger.error(f"Error during cleaning: {str(e)}")
        raise


def main(input_file: str, output_file: str):
    """Main cleaning pipeline"""
    try:
        # Load data
        logger.info(f"Loading data from {input_file}")
        df = pd.read_csv(input_file)
        logger.info(f"Loaded {len(df)} rows")

        # Clean data
        df_clean = clean_sales_data(df)

        # Save cleaned data
        logger.info(f"Saving cleaned data to {output_file}")
        df_clean.to_csv(output_file, index=False)
        logger.info(f"✅ Cleaning completed successfully!")

        # Summary
        logger.info(f"\nSummary:")
        logger.info(f"  Input rows:  {len(df)}")
        logger.info(f"  Output rows: {len(df_clean)}")
        logger.info(f"  Removed:     {len(df) - len(df_clean)}")

    except FileNotFoundError:
        logger.error(f"Input file not found: {input_file}")
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Clean CSV data')
    parser.add_argument('--input', required=True, help='Input CSV file')
    parser.add_argument('--output', required=True, help='Output CSV file')

    args = parser.parse_args()

    main(args.input, args.output)
```

**執行**：
```bash
python clean_data.py --input dirty_sales_data.csv --output cleaned_sales_data.csv
```

**輸出**：
```
2025-10-30 10:30:00 - INFO - Loading data from dirty_sales_data.csv
2025-10-30 10:30:00 - INFO - Loaded 7 rows
2025-10-30 10:30:00 - INFO - Starting data cleaning process
2025-10-30 10:30:00 - INFO - Date standardization completed
2025-10-30 10:30:00 - INFO - Filled 1 missing amounts
2025-10-30 10:30:00 - INFO - String cleaning completed
2025-10-30 10:30:00 - INFO - Removed 1 duplicates
2025-10-30 10:30:00 - INFO - Filtering completed: 7 → 5 rows
2025-10-30 10:30:00 - INFO - Saving cleaned data to cleaned_sales_data.csv
2025-10-30 10:30:00 - INFO - ✅ Cleaning completed successfully!

2025-10-30 10:30:00 - INFO - Summary:
2025-10-30 10:30:00 - INFO -   Input rows:  7
2025-10-30 10:30:00 - INFO -   Output rows: 5
2025-10-30 10:30:00 - INFO -   Removed:     2
```

---

## ✅ 驗證結果

### 檢查清洗後資料

**`verify_cleaned_data.py`**：
```python
import pandas as pd

# Load cleaned data
df = pd.read_csv('cleaned_sales_data.csv')

print("=" * 50)
print("Verification Report")
print("=" * 50)

# Check 1: No missing values
print("\n1. Missing Values Check:")
missing = df.isnull().sum()
if missing.sum() == 0:
    print("   ✅ No missing values")
else:
    print("   ❌ Still has missing values:")
    print(missing[missing > 0])

# Check 2: Date format
print("\n2. Date Format Check:")
try:
    df['date'] = pd.to_datetime(df['date'])
    print(f"   ✅ All dates are valid (from {df['date'].min()} to {df['date'].max()})")
except:
    print("   ❌ Invalid dates found")

# Check 3: No duplicates
print("\n3. Duplicate Check:")
dup_count = df.duplicated().sum()
if dup_count == 0:
    print("   ✅ No duplicates")
else:
    print(f"   ❌ {dup_count} duplicates found")

# Check 4: String quality
print("\n4. String Quality Check:")
has_extra_spaces = df['product_name'].str.contains(r'^\s+|\s+$|\s{2,}', na=False).sum()
if has_extra_spaces == 0:
    print("   ✅ No extra spaces in product names")
else:
    print(f"   ❌ {has_extra_spaces} records still have extra spaces")

# Check 5: Data types
print("\n5. Data Types:")
print(df.dtypes)

print("\n" + "=" * 50)
print("✅ Verification completed!")
print("=" * 50)
```

---

## 🎯 學習檢查點

完成本情境題後，你應該能夠：

- [ ] 用 Pandas 分析資料品質問題
- [ ] 設計資料清洗邏輯
- [ ] 用 AI 快速生成清洗代碼
- [ ] 加入完善的錯誤處理與日誌
- [ ] 驗證清洗結果

---

## 💡 延伸挑戰

### 挑戰 1：自動化排程

設定 Cron job，每天自動執行清洗腳本。

### 挑戰 2：清洗規則配置化

將清洗規則寫成 YAML 配置檔，讓腳本更靈活。

### 挑戰 3：清洗報告

生成詳細的清洗報告（Markdown 或 HTML）。

---

**情境版本**：v1.0
**難度**：⭐⭐ 基礎至中級
**預計時間**：30-45 分鐘
