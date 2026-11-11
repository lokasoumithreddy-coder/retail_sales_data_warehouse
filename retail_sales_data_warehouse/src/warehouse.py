from pathlib import Path
import sqlite3
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
DB_FILE = BASE_DIR / "output" / "retail_warehouse.db"
SQL_FILE = BASE_DIR / "sql" / "schema.sql"
OUTPUT_DIR = BASE_DIR / "output"

def create_warehouse():
    OUTPUT_DIR.mkdir(exist_ok=True)
    with sqlite3.connect(DB_FILE) as conn:
        conn.execute("PRAGMA foreign_keys = ON")
        conn.executescript(SQL_FILE.read_text(encoding="utf-8"))
    print(f"Warehouse ready: {DB_FILE}")

def load_warehouse():
    required_files = [
        "dim_customer.csv", "dim_product.csv", "dim_date.csv", "fact_sales.csv"
    ]
    for name in required_files:
        if not (OUTPUT_DIR / name).exists():
            raise FileNotFoundError(f"Missing {name}. Run transformation first.")

    create_warehouse()
    with sqlite3.connect(DB_FILE) as conn:
        conn.execute("PRAGMA foreign_keys = ON")
        # Idempotent load: existing dimension/fact keys are not duplicated.
        for table in ["dim_customer", "dim_product", "dim_date"]:
            frame = pd.read_csv(OUTPUT_DIR / f"{table}.csv")
            frame.to_sql(f"staging_{table}", conn, if_exists="replace", index=False)
            cols = list(frame.columns)
            col_sql = ", ".join(f'"{c}"' for c in cols)
            conn.execute(
                f'INSERT OR IGNORE INTO "{table}" ({col_sql}) '
                f'SELECT {col_sql} FROM "staging_{table}"'
            )
            conn.execute(f'DROP TABLE "staging_{table}"')

        fact = pd.read_csv(OUTPUT_DIR / "fact_sales.csv")
        fact.to_sql("staging_fact_sales", conn, if_exists="replace", index=False)
        cols = list(fact.columns)
        col_sql = ", ".join(f'"{c}"' for c in cols)
        conn.execute(
            f'INSERT OR IGNORE INTO fact_sales ({col_sql}) '
            f'SELECT {col_sql} FROM staging_fact_sales'
        )
        conn.execute("DROP TABLE staging_fact_sales")

        counts = {}
        for table in ["dim_customer", "dim_product", "dim_date", "fact_sales"]:
            counts[table] = conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]

    print("Warehouse load complete:")
    for table, count in counts.items():
        print(f"  {table}: {count} rows")
    return counts

if __name__ == "__main__":
    load_warehouse()
