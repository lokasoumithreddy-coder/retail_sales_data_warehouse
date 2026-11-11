from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
SOURCE_FILE = BASE_DIR / "data" / "retail_sales.csv"

REQUIRED_COLUMNS = [
    "transaction_id", "customer_id", "product_id", "product_name",
    "category", "quantity", "unit_price", "sales_amount", "order_date"
]

def load_sales_data():
    if not SOURCE_FILE.exists():
        raise FileNotFoundError(
            f"Source file not found: {SOURCE_FILE}. Run python src/generate_data.py first."
        )
    df = pd.read_csv(SOURCE_FILE)
    missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")
    print(f"Ingested {len(df)} rows from {SOURCE_FILE.name}")
    return df
