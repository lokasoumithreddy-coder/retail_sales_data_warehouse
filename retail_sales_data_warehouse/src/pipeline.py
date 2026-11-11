from generate_data import generate_data
from ingestion import load_sales_data
from validation import validate_sales_data
from transform import transform_sales_data
from warehouse import load_warehouse

def run_pipeline(generate_sample=False, rows=1000):
    print("\n=== RETAIL SALES DATA WAREHOUSE PIPELINE ===")
    if generate_sample:
        generate_data(n=rows)

    raw = load_sales_data()
    valid, rejected = validate_sales_data(raw)
    if valid.empty:
        raise RuntimeError("Pipeline stopped: no valid records.")
    transform_sales_data()
    counts = load_warehouse()

    print("\n=== PIPELINE SUMMARY ===")
    print(f"Source rows: {len(raw)}")
    print(f"Valid rows: {len(valid)}")
    print(f"Rejected rows: {len(rejected)}")
    print(f"Warehouse fact rows: {counts['fact_sales']}")
    print("PIPELINE SUCCESS")

if __name__ == "__main__":
    run_pipeline(generate_sample=False)
