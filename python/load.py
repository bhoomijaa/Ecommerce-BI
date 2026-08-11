import pandas as pd
import mysql.connector
from pathlib import Path


# =========================
# CONFIGURATION
# =========================
import os
from dotenv import load_dotenv

load_dotenv()
CLEAN_DIR = Path("data/cleaned")

DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = "ecommerce_bi"


# =========================
# CONNECT TO MYSQL
# =========================

connection = mysql.connector.connect(
    host=DB_HOST,
    user=DB_USER,
    password=DB_PASSWORD,
    database=DB_NAME
)

cursor = connection.cursor()

print("Connected to MySQL successfully!")


# =========================
# HELPER FUNCTION
# =========================

def load_table(csv_file, table_name, columns):

    print(f"\nLoading {table_name}...")

    df = pd.read_csv(CLEAN_DIR / csv_file)

    placeholders = ", ".join(["%s"] * len(columns))
    column_names = ", ".join(columns)

    query = f"""
        INSERT INTO {table_name} ({column_names})
        VALUES ({placeholders})
    """

    data = []

    for _, row in df.iterrows():

        values = []

        for column in columns:

            value = row[column]

            if pd.isna(value):
                value = None

            # Convert timestamps to MySQL-compatible strings
            elif isinstance(value, pd.Timestamp):
                value = value.strftime("%Y-%m-%d %H:%M:%S")

            values.append(value)

        data.append(tuple(values))

    cursor.executemany(query, data)
    connection.commit()

    print(f"Loaded {len(data):,} rows into {table_name}")


# =========================
# LOAD TABLES
# =========================

load_table(
    "customers_clean.csv",
    "customers",
    [
        "customer_id",
        "customer_unique_id",
        "customer_zip_code_prefix",
        "customer_city",
        "customer_state"
    ]
)


load_table(
    "sellers_clean.csv",
    "sellers",
    [
        "seller_id",
        "seller_zip_code_prefix",
        "seller_city",
        "seller_state"
    ]
)

load_table(
    "category_translation_clean.csv",
    "product_category_translation",
    [
        "product_category_name",
        "product_category_name_english"
    ]
)

load_table(
    "products_clean.csv",
    "products",
    [
        "product_id",
        "product_category_name",
        "product_name_length",
        "product_description_length",
        "product_photos_qty",
        "product_weight_g",
        "product_length_cm",
        "product_height_cm",
        "product_width_cm"
    ]
)





load_table(
    "orders_clean.csv",
    "orders",
    [
        "order_id",
        "customer_id",
        "order_status",
        "order_purchase_timestamp",
        "order_approved_at",
        "order_delivered_carrier_date",
        "order_delivered_customer_date",
        "order_estimated_delivery_date",
        "order_purchase_date_id"
    ]
)


load_table(
    "order_items_clean.csv",
    "order_items",
    [
        "order_id",
        "order_item_id",
        "product_id",
        "seller_id",
        "shipping_limit_date",
        "price",
        "freight_value"
    ]
)


load_table(
    "order_payments_clean.csv",
    "order_payments",
    [
        "order_id",
        "payment_sequential",
        "payment_type",
        "payment_installments",
        "payment_value"
    ]
)


load_table(
    "order_reviews_clean.csv",
    "order_reviews",
    [
        "review_id",
        "order_id",
        "review_score",
        "review_comment_title",
        "review_comment_message",
        "review_creation_date",
        "review_answer_timestamp"
    ]
)


# =========================
# CLOSE CONNECTION
# =========================

cursor.close()
connection.close()

print("\n===================================")
print("ALL DATA LOADED SUCCESSFULLY")
print("===================================")