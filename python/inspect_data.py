import pandas as pd
from pathlib import Path


# Location of our raw CSV files
DATA_DIR = Path("data/raw")


# CSV files that we want to inspect
files = {
    "customers": "olist_customers_dataset.csv",
    "sellers": "olist_sellers_dataset.csv",
    "products": "olist_products_dataset.csv",
    "orders": "olist_orders_dataset.csv",
    "order_items": "olist_order_items_dataset.csv",
    "order_payments": "olist_order_payments_dataset.csv",
    "order_reviews": "olist_order_reviews_dataset.csv",
    "category_translation": "product_category_name_translation.csv"
}


for table_name, filename in files.items():

    print("\n" + "=" * 70)
    print(f"TABLE: {table_name}")
    print("=" * 70)

    # Read CSV
    file_path = DATA_DIR / filename
    df = pd.read_csv(file_path, encoding="utf-8")
    # Number of rows and columns
    print(f"\nRows: {len(df):,}")
    print(f"Columns: {len(df.columns)}")

    # Column names
    print("\nColumns:")
    print(df.columns.tolist())

    # Data types
    print("\nData Types:")
    print(df.dtypes)

    # Missing values
    print("\nMissing Values:")
    print(df.isnull().sum())

    # Duplicate rows
    print("\nDuplicate Rows:")
    print(df.duplicated().sum())

    # First 3 rows
    print("\nFirst 3 Rows:")
    print(df.head(3))