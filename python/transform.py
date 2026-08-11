import pandas as pd
from pathlib import Path


# =========================
# PATHS
# =========================

RAW_DIR = Path("data/raw")
CLEAN_DIR = Path("data/cleaned")

CLEAN_DIR.mkdir(parents=True, exist_ok=True)


# =========================
# HELPER FUNCTIONS
# =========================

def clean_datetime(df, columns):
    for col in columns:
        df[col] = pd.to_datetime(df[col], errors="coerce")
    return df


def save(df, filename):
    path = CLEAN_DIR / filename
    df.to_csv(path, index=False)
    print(f"Saved: {path} ({len(df):,} rows)")


# =========================
# 1. CUSTOMERS
# =========================

print("\nCleaning customers...")

customers = pd.read_csv(
    RAW_DIR / "olist_customers_dataset.csv"
)

customers = customers.drop_duplicates(subset=["customer_id"])

customers["customer_city"] = customers["customer_city"].str.strip().str.lower()
customers["customer_state"] = customers["customer_state"].str.strip().str.upper()

save(customers, "customers_clean.csv")


# =========================
# 2. SELLERS
# =========================

print("\nCleaning sellers...")

sellers = pd.read_csv(
    RAW_DIR / "olist_sellers_dataset.csv"
)

sellers = sellers.drop_duplicates(subset=["seller_id"])

sellers["seller_city"] = sellers["seller_city"].str.strip().str.lower()
sellers["seller_state"] = sellers["seller_state"].str.strip().str.upper()

save(sellers, "sellers_clean.csv")


# =========================
# 3. PRODUCTS
# =========================

print("\nCleaning products...")

products = pd.read_csv(
    RAW_DIR / "olist_products_dataset.csv"
)

products = products.drop_duplicates(subset=["product_id"])

products["product_category_name"] = (
    products["product_category_name"]
    .str.strip()
    .str.lower()
)

# Keep missing category/attributes as NULL.
# They represent unavailable information rather than bad records.

numeric_product_columns = [
    "product_name_lenght",
    "product_description_lenght",
    "product_photos_qty",
    "product_weight_g",
    "product_length_cm",
    "product_height_cm",
    "product_width_cm"
]

for col in numeric_product_columns:
    products[col] = pd.to_numeric(products[col], errors="coerce")

# Rename misspelled source columns to match our SQL schema
products = products.rename(columns={
    "product_name_lenght": "product_name_length",
    "product_description_lenght": "product_description_length"
})

save(products, "products_clean.csv")


# =========================
# 4. CATEGORY TRANSLATION
# =========================

print("\nCleaning category translation...")

categories = pd.read_csv(
    RAW_DIR / "product_category_name_translation.csv"
)

categories = categories.drop_duplicates(
    subset=["product_category_name"]
)

categories["product_category_name"] = (
    categories["product_category_name"]
    .str.strip()
    .str.lower()
)

categories["product_category_name_english"] = (
    categories["product_category_name_english"]
    .str.strip()
    .str.lower()
)

save(categories, "category_translation_clean.csv")


# =========================
# 5. ORDERS
# =========================

print("\nCleaning orders...")

orders = pd.read_csv(
    RAW_DIR / "olist_orders_dataset.csv"
)

orders = orders.drop_duplicates(subset=["order_id"])

datetime_columns = [
    "order_purchase_timestamp",
    "order_approved_at",
    "order_delivered_carrier_date",
    "order_delivered_customer_date",
    "order_estimated_delivery_date"
]

orders = clean_datetime(orders, datetime_columns)

orders["order_status"] = (
    orders["order_status"]
    .str.strip()
    .str.lower()
)

# Create date dimension key
orders["order_purchase_date_id"] = (
    orders["order_purchase_timestamp"]
    .dt.strftime("%Y%m%d")
    .astype(int)
)

save(orders, "orders_clean.csv")


# =========================
# 6. ORDER ITEMS
# =========================

print("\nCleaning order items...")

order_items = pd.read_csv(
    RAW_DIR / "olist_order_items_dataset.csv"
)

order_items = order_items.drop_duplicates(
    subset=["order_id", "order_item_id"]
)

order_items["shipping_limit_date"] = pd.to_datetime(
    order_items["shipping_limit_date"],
    errors="coerce"
)

order_items["price"] = pd.to_numeric(
    order_items["price"],
    errors="coerce"
)

order_items["freight_value"] = pd.to_numeric(
    order_items["freight_value"],
    errors="coerce"
)

# Remove impossible financial values
order_items = order_items[
    (order_items["price"] >= 0) &
    (order_items["freight_value"] >= 0)
]

save(order_items, "order_items_clean.csv")


# =========================
# 7. ORDER PAYMENTS
# =========================

print("\nCleaning order payments...")

payments = pd.read_csv(
    RAW_DIR / "olist_order_payments_dataset.csv"
)

payments = payments.drop_duplicates(
    subset=["order_id", "payment_sequential"]
)

payments["payment_type"] = (
    payments["payment_type"]
    .str.strip()
    .str.lower()
)

payments["payment_installments"] = pd.to_numeric(
    payments["payment_installments"],
    errors="coerce"
)

payments["payment_value"] = pd.to_numeric(
    payments["payment_value"],
    errors="coerce"
)

payments = payments[
    (payments["payment_installments"] >= 0) &
    (payments["payment_value"] >= 0)
]

save(payments, "order_payments_clean.csv")


# =========================
# 8. ORDER REVIEWS
# =========================

print("\nCleaning order reviews...")

reviews = pd.read_csv(
    RAW_DIR / "olist_order_reviews_dataset.csv"
)

reviews = reviews.drop_duplicates(subset=["review_id"])

reviews["review_score"] = pd.to_numeric(
    reviews["review_score"],
    errors="coerce"
)

# Keep only valid review scores
reviews = reviews[
    reviews["review_score"].between(1, 5)
]

review_datetime_columns = [
    "review_creation_date",
    "review_answer_timestamp"
]

reviews = clean_datetime(
    reviews,
    review_datetime_columns
)

# Empty comments are treated as NULL
reviews["review_comment_title"] = (
    reviews["review_comment_title"]
    .replace(r"^\s*$", pd.NA, regex=True)
)

reviews["review_comment_message"] = (
    reviews["review_comment_message"]
    .replace(r"^\s*$", pd.NA, regex=True)
)

save(reviews, "order_reviews_clean.csv")


print("\n===================================")
print("DATA CLEANING COMPLETE")
print("===================================")