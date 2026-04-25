# import os
# import pandas as pd
# from sqlalchemy import create_engine
# from pathlib import Path

# DATA_PATH = Path(os.getenv("DATA_PATH", "datasets"))

# DB_URL = os.getenv(
#     "DB_URL",
#     "postgresql+psycopg2://postgres:postgres@localhost:5433/ecommerce_dw"
# )


# TABLES = {
#     "olist_customers_dataset.csv": "customers",
#     "olist_geolocation_dataset.csv": "geolocation",
#     "olist_order_items_dataset.csv": "order_items",
#     "olist_order_payments_dataset.csv": "order_payments",
#     "olist_order_reviews_dataset.csv": "order_reviews",
#     "olist_orders_dataset.csv": "orders",
#     "olist_products_dataset.csv": "products",
#     "olist_sellers_dataset.csv": "sellers",
#     "product_category_name_translation.csv": "product_category_translation",
# }

# engine = create_engine(DB_URL)

# for file_name, table_name in TABLES.items():
#     file_path = DATA_PATH / file_name
#     print(f"Loading {file_name} -> raw.{table_name}")

#     df = pd.read_csv(file_path)

#     df.to_sql(
#         table_name,
#         engine,
#         schema="raw",
#         if_exists="replace",
#         index=False
#     )

#     print(f"Loaded {len(df)} rows into raw.{table_name}")

# print("All raw tables loaded successfully.")

import os
import pandas as pd
from sqlalchemy import create_engine, text
from pathlib import Path

DATA_PATH = Path(os.getenv("DATA_PATH", "datasets"))

DB_URL = os.getenv(
    "DB_URL",
    "postgresql+psycopg2://postgres:postgres@localhost:5433/ecommerce_dw"
)

TABLES = {
    "olist_customers_dataset.csv": "customers",
    "olist_geolocation_dataset.csv": "geolocation",
    "olist_order_items_dataset.csv": "order_items",
    "olist_order_payments_dataset.csv": "order_payments",
    "olist_order_reviews_dataset.csv": "order_reviews",
    "olist_orders_dataset.csv": "orders",
    "olist_products_dataset.csv": "products",
    "olist_sellers_dataset.csv": "sellers",
    "product_category_name_translation.csv": "product_category_translation",
}

engine = create_engine(DB_URL)

for file_name, table_name in TABLES.items():
    file_path = DATA_PATH / file_name
    print(f"Loading {file_name} -> raw.{table_name}")

    df = pd.read_csv(file_path)

    with engine.begin() as conn:
        conn.execute(text(f'TRUNCATE TABLE raw.{table_name} RESTART IDENTITY CASCADE'))

    df.to_sql(
        table_name,
        engine,
        schema="raw",
        if_exists="append",
        index=False
    )

    print(f"Loaded {len(df)} rows into raw.{table_name}")

print("All raw tables loaded successfully.")