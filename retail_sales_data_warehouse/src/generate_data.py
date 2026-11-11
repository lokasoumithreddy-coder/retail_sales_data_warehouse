import random
from datetime import date, timedelta
from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

def generate_data(n=1000, seed=42):
    random.seed(seed)
    products = [
        ("P001", "Laptop", "Electronics"),
        ("P002", "Mobile", "Electronics"),
        ("P003", "Shirt", "Fashion"),
        ("P004", "Shoes", "Fashion"),
        ("P005", "Chair", "Furniture"),
    ]
    customers = [f"C{i:03d}" for i in range(1, 21)]
    start = date(2026, 1, 1)
    rows = []
    for i in range(1, n + 1):
        pid, pname, category = random.choice(products)
        qty = random.randint(1, 5)
        price = round(random.uniform(100, 50000), 2)
        order_date = start + timedelta(days=random.randint(0, 299))
        rows.append({
            "transaction_id": f"T{i:05d}",
            "customer_id": random.choice(customers),
            "product_id": pid,
            "product_name": pname,
            "category": category,
            "quantity": qty,
            "unit_price": price,
            "sales_amount": round(qty * price, 2),
            "order_date": order_date.isoformat(),
        })
    path = DATA_DIR / "retail_sales.csv"
    pd.DataFrame(rows).to_csv(path, index=False)
    print(f"Generated {n} records: {path}")

if __name__ == "__main__":
    generate_data()
