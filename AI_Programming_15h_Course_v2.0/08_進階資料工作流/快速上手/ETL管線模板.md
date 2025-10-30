# ETL 管線模板

## 📋 可複製的 ETL 模板

這是一個通用的 ETL 管線模板，可直接複製使用。

---

## 🎯 適用場景

- CSV to Database
- Excel to CSV
- 多來源資料整合
- 定時資料同步

---

## 📝 完整模板

**`etl_template.py`**：
```python
#!/usr/bin/env python3
"""
ETL Pipeline Template

Customize this template for your specific needs.
"""

import pandas as pd
import logging
from datetime import datetime
from pathlib import Path

# ===== Configuration =====
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# ===== Extract =====
def extract(source_path: str) -> pd.DataFrame:
    """
    Extract data from source

    Customize: Change file type, add multiple sources
    """
    logger.info(f"[EXTRACT] Loading from {source_path}")

    try:
        # Option 1: CSV
        df = pd.read_csv(source_path)

        # Option 2: Excel
        # df = pd.read_excel(source_path)

        # Option 3: Database
        # from sqlalchemy import create_engine
        # engine = create_engine('postgresql://...')
        # df = pd.read_sql('SELECT * FROM table', engine)

        logger.info(f"[EXTRACT] Loaded {len(df)} rows")
        return df

    except Exception as e:
        logger.error(f"[EXTRACT] Failed: {str(e)}")
        raise


# ===== Transform =====
def transform(df: pd.DataFrame) -> pd.DataFrame:
    """
    Transform and clean data

    Customize: Add your transformation logic
    """
    logger.info("[TRANSFORM] Starting transformation")

    df_clean = df.copy()
    initial_rows = len(df_clean)

    try:
        # Step 1: Date standardization
        if 'date' in df_clean.columns:
            df_clean['date'] = pd.to_datetime(df_clean['date'], errors='coerce')

        # Step 2: Handle missing values
        # Option A: Fill with median/mean
        # df_clean['amount'].fillna(df_clean['amount'].median(), inplace=True)

        # Option B: Drop rows with missing values
        # df_clean.dropna(subset=['important_column'], inplace=True)

        # Step 3: Clean strings
        for col in df_clean.select_dtypes(include=['object']).columns:
            df_clean[col] = df_clean[col].str.strip()

        # Step 4: Remove duplicates
        df_clean.drop_duplicates(inplace=True)

        # Step 5: Data validation
        # Add your validation logic here

        final_rows = len(df_clean)
        logger.info(f"[TRANSFORM] Completed: {initial_rows} → {final_rows} rows")

        return df_clean

    except Exception as e:
        logger.error(f"[TRANSFORM] Failed: {str(e)}")
        raise


# ===== Load =====
def load(df: pd.DataFrame, target_path: str) -> None:
    """
    Load data to target

    Customize: Change target type
    """
    logger.info(f"[LOAD] Loading {len(df)} rows to {target_path}")

    try:
        # Option 1: CSV
        df.to_csv(target_path, index=False)

        # Option 2: Database
        # from sqlalchemy import create_engine
        # engine = create_engine('postgresql://...')
        # df.to_sql('table_name', engine, if_exists='append', index=False)

        # Option 3: Parquet (faster, compressed)
        # df.to_parquet(target_path, index=False)

        logger.info(f"[LOAD] Successfully loaded data")

    except Exception as e:
        logger.error(f"[LOAD] Failed: {str(e)}")
        raise


# ===== Main Pipeline =====
def run_etl(source: str, target: str) -> None:
    """Run complete ETL pipeline"""
    start_time = datetime.now()

    logger.info("=" * 50)
    logger.info("ETL Pipeline Started")
    logger.info("=" * 50)

    try:
        # Extract
        df_raw = extract(source)

        # Transform
        df_clean = transform(df_raw)

        # Load
        load(df_clean, target)

        elapsed = (datetime.now() - start_time).total_seconds()
        logger.info("=" * 50)
        logger.info(f"ETL Completed Successfully ({elapsed:.2f}s)")
        logger.info("=" * 50)

    except Exception as e:
        logger.error(f"ETL Failed: {str(e)}")
        raise


# ===== CLI =====
if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='ETL Pipeline')
    parser.add_argument('--source', required=True, help='Source file/database')
    parser.add_argument('--target', required=True, help='Target file/database')

    args = parser.parse_args()

    run_etl(args.source, args.target)
```

---

## 🔧 客製化指南

### 1. 更改資料來源

**從多個 CSV 讀取**：
```python
def extract_multiple(file_paths: list) -> pd.DataFrame:
    """Extract from multiple CSV files"""
    dfs = []
    for path in file_paths:
        df = pd.read_csv(path)
        dfs.append(df)
    return pd.concat(dfs, ignore_index=True)
```

### 2. 加入資料驗證

```python
def validate_data(df: pd.DataFrame) -> bool:
    """Validate data quality"""
    # Check required columns
    required_cols = ['date', 'amount', 'product']
    if not all(col in df.columns for col in required_cols):
        raise ValueError("Missing required columns")

    # Check data types
    assert df['amount'].dtype in ['int64', 'float64'], "Amount must be numeric"

    # Check value ranges
    assert (df['amount'] >= 0).all(), "Amount must be non-negative"

    return True
```

### 3. 錯誤重試

```python
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
def load_with_retry(df: pd.DataFrame, target: str) -> None:
    """Load with automatic retry on failure"""
    load(df, target)
```

---

## 📦 使用範例

### 範例 1：CSV to CSV
```bash
python etl_template.py \
    --source data/raw/sales.csv \
    --target data/clean/sales_cleaned.csv
```

### 範例 2：設定 Cron Job
```bash
# 每天凌晨 2 點執行
0 2 * * * /usr/bin/python3 /path/to/etl_template.py --source /data/raw.csv --target /data/clean.csv
```

---

**版本**：v1.0
**最後更新**：2025-10-30
