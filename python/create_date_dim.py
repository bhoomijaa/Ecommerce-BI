import pandas as pd
import mysql.connector


# =========================
# CONFIGURATION
# =========================

import os
from dotenv import load_dotenv

load_dotenv()

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
# GENERATE DATE RANGE
# =========================

dates = pd.date_range(
    start="2016-01-01",
    end="2018-12-31",
    freq="D"
)


# =========================
# INSERT DATES
# =========================

query = """
INSERT INTO date_dim
(
    date_id,
    full_date,
    day,
    day_name,
    day_of_week,
    is_weekend,
    month,
    month_name,
    quarter,
    year
)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
"""

data = []

for date in dates:

    data.append((
        int(date.strftime("%Y%m%d")),
        date.strftime("%Y-%m-%d"),
        date.day,
        date.strftime("%A"),
        date.dayofweek + 1,
        1 if date.dayofweek >= 5 else 0,
        date.month,
        date.strftime("%B"),
        (date.month - 1) // 3 + 1,
        date.year
    ))


cursor.executemany(query, data)
connection.commit()

print(f"Loaded {len(data):,} dates into date_dim.")


cursor.close()
connection.close()

print("Date dimension created successfully!")