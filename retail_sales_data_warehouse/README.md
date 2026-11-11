# Retail Sales Data Warehouse

A small end-to-end data engineering project that ingests retail transaction CSV data, validates records, transforms them into a star schema, and loads the result into SQLite.

## Architecture

CSV source -> ingestion -> validation -> transformation -> SQLite warehouse -> SQL analytics

## Dimensional model

- `fact_sales`: one row per sales transaction; measures are quantity, unit_price, sales_amount.
- `dim_customer`: customer descriptive dimension.
- `dim_product`: product name and category.
- `dim_date`: calendar attributes.
- Fact table uses surrogate foreign keys to the dimensions.

## Requirements

Python 3.10+.

```bash
python -m pip install -r requirements.txt
```

## Run from project root

```bash
python src/generate_data.py
python src/validation.py
python src/transform.py
python src/warehouse.py
```

Or run the complete pipeline (expects `data/retail_sales.csv` to exist):

```bash
python src/pipeline.py
```

Generate fresh sample data and run the pipeline in one command:

```bash
python -c "import sys; sys.path.insert(0, 'src'); from pipeline import run_pipeline; run_pipeline(generate_sample=True, rows=1000)"
```

## Run tests

```bash
python -m pytest -v
```

## Run SQL analytics

Open `output/retail_warehouse.db` with DB Browser for SQLite, then run the queries in `sql/analytics.sql`.

Alternatively, from Python:

```bash
python -c "import sqlite3; c=sqlite3.connect('output/retail_warehouse.db'); print(*c.execute('SELECT COUNT(*), ROUND(SUM(sales_amount),2) FROM fact_sales'), sep='\\n')"
```

## Data quality

The validation stage checks required fields, numeric values, duplicate transaction IDs, positive quantities, non-negative prices and amounts, arithmetic consistency, and valid dates. Rejected records are saved with rejection reasons.

## Idempotency

Warehouse tables use unique keys and `INSERT OR IGNORE` so rerunning the same load does not create duplicate transactions.

## Limitations and next steps

This is a local SQLite demonstration using synthetic data. A production implementation could add incremental source ingestion, slowly changing dimensions, orchestration, cloud object storage, and monitoring.
