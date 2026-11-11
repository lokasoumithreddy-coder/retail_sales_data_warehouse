from pathlib import Path
import pandas as pd
from ingestion import load_sales_data

BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = BASE_DIR / "output"

def validate_sales_data(df=None):
    df = load_sales_data() if df is None else df.copy()
    OUTPUT_DIR.mkdir(exist_ok=True)

    required = [
        "transaction_id", "customer_id", "product_id", "product_name",
        "category", "quantity", "unit_price", "sales_amount", "order_date"
    ]
    reasons = pd.Series("", index=df.index, dtype="object")

    for col in required:
        missing = df[col].isna() | df[col].astype(str).str.strip().eq("")
        reasons.loc[missing] += f"Missing {col}; "

    for col in ["quantity", "unit_price", "sales_amount"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")
        reasons.loc[df[col].isna()] += f"Invalid {col}; "

    duplicate = df["transaction_id"].duplicated(keep=False)
    reasons.loc[duplicate] += "Duplicate transaction_id; "

    reasons.loc[df["quantity"].notna() & (df["quantity"] <= 0)] += "Quantity must be positive; "
    reasons.loc[df["unit_price"].notna() & (df["unit_price"] < 0)] += "Unit price cannot be negative; "
    reasons.loc[df["sales_amount"].notna() & (df["sales_amount"] < 0)] += "Sales amount cannot be negative; "

    expected = df["quantity"] * df["unit_price"]
    mismatch = (
        df["quantity"].notna() & df["unit_price"].notna()
        & df["sales_amount"].notna()
        & ((df["sales_amount"] - expected).abs() > 0.02)
    )
    reasons.loc[mismatch] += "Sales amount mismatch; "

    parsed_dates = pd.to_datetime(df["order_date"], errors="coerce")
    reasons.loc[parsed_dates.isna()] += "Invalid order_date; "
    df["order_date"] = parsed_dates.dt.strftime("%Y-%m-%d")

    df["rejection_reason"] = reasons
    valid = df.loc[reasons.eq("")].drop(columns=["rejection_reason"]).copy()
    rejected = df.loc[reasons.ne("")].copy()

    valid.to_csv(OUTPUT_DIR / "validated_sales.csv", index=False)
    rejected.to_csv(OUTPUT_DIR / "rejected_sales.csv", index=False)

    print(f"Validation complete | total={len(df)} valid={len(valid)} rejected={len(rejected)}")
    return valid, rejected

if __name__ == "__main__":
    validate_sales_data()
