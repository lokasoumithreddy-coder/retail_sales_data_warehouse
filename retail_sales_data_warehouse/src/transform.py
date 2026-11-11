from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = BASE_DIR / "output"

def transform_sales_data():
    source = OUTPUT_DIR / "validated_sales.csv"
    if not source.exists():
        raise FileNotFoundError("Run validation first: python src/validation.py")

    df = pd.read_csv(source)
    if df.empty:
        raise ValueError("No valid sales rows available to transform.")

    # One row per unique customer, product, and calendar date.
    dim_customer = (
        df[["customer_id"]].drop_duplicates().sort_values("customer_id")
        .reset_index(drop=True)
    )
    dim_customer.insert(0, "customer_key", range(1, len(dim_customer) + 1))

    dim_product = (
        df[["product_id", "product_name", "category"]]
        .drop_duplicates().sort_values("product_id").reset_index(drop=True)
    )
    if dim_product["product_id"].duplicated().any():
        raise ValueError("A product_id maps to more than one product description.")
    dim_product.insert(0, "product_key", range(1, len(dim_product) + 1))

    dates = pd.to_datetime(df["order_date"]).drop_duplicates().sort_values()
    dim_date = pd.DataFrame({"full_date": dates.dt.strftime("%Y-%m-%d")})
    parsed = pd.to_datetime(dim_date["full_date"])
    dim_date.insert(0, "date_key", parsed.dt.strftime("%Y%m%d").astype(int))
    dim_date["day"] = parsed.dt.day
    dim_date["month"] = parsed.dt.month
    dim_date["month_name"] = parsed.dt.month_name()
    dim_date["quarter"] = parsed.dt.quarter
    dim_date["year"] = parsed.dt.year

    fact = df.merge(dim_customer, on="customer_id", validate="many_to_one")
    fact = fact.merge(
        dim_product, on=["product_id", "product_name", "category"],
        validate="many_to_one"
    )
    fact["date_key"] = pd.to_datetime(fact["order_date"]).dt.strftime("%Y%m%d").astype(int)
    fact = fact[[
        "transaction_id", "customer_key", "product_key", "date_key",
        "quantity", "unit_price", "sales_amount"
    ]]

    outputs = {
        "dim_customer.csv": dim_customer,
        "dim_product.csv": dim_product,
        "dim_date.csv": dim_date,
        "fact_sales.csv": fact,
    }
    for filename, table in outputs.items():
        table.to_csv(OUTPUT_DIR / filename, index=False)

    print("Transformation complete:")
    for filename, table in outputs.items():
        print(f"  {filename}: {len(table)} rows")
    return outputs

if __name__ == "__main__":
    transform_sales_data()
