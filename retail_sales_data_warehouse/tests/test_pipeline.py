import sys
from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR / "src"))

from validation import validate_sales_data

def sample():
    return pd.DataFrame([
        {
            "transaction_id": "T00001", "customer_id": "C001",
            "product_id": "P001", "product_name": "Laptop",
            "category": "Electronics", "quantity": 2,
            "unit_price": 100.0, "sales_amount": 200.0,
            "order_date": "2026-01-01"
        }
    ])

def test_valid_record():
    valid, rejected = validate_sales_data(sample())
    assert len(valid) == 1
    assert len(rejected) == 0

def test_duplicate_transaction_rejected():
    df = pd.concat([sample(), sample()], ignore_index=True)
    valid, rejected = validate_sales_data(df)
    assert len(valid) == 0
    assert len(rejected) == 2

def test_wrong_sales_amount_rejected():
    df = sample()
    df.loc[0, "sales_amount"] = 999
    valid, rejected = validate_sales_data(df)
    assert len(valid) == 0
    assert len(rejected) == 1

def test_invalid_quantity_rejected():
    df = sample()
    df.loc[0, "quantity"] = 0
    valid, rejected = validate_sales_data(df)
    assert len(valid) == 0
    assert len(rejected) == 1

def test_invalid_date_rejected():
    df = sample()
    df.loc[0, "order_date"] = "not-a-date"
    valid, rejected = validate_sales_data(df)
    assert len(valid) == 0
    assert len(rejected) == 1
