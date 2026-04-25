# 🛒 E-commerce Data Pipeline (PostgreSQL + dbt + Docker)

## 📌 Overview

This project builds a modern data engineering pipeline for an e-commerce dataset using PostgreSQL, Python, Docker, and dbt.

The goal is to simulate a real-world data engineering workflow by ingesting raw CSV files into PostgreSQL, transforming them using dbt, applying data quality tests, and building an analytics-ready star schema.

The pipeline follows a layered architecture:

```text
raw → staging → marts
(bronze → silver → gold)
```

---

## 📦 Dataset

This project uses the **Brazilian E-Commerce Public Dataset by Olist** from Kaggle.

Dataset link: https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce

The dataset contains around 100,000 orders and includes information about customers, orders, order items, payments, reviews, products, sellers, and geolocation data.

---

## ⚙️ Tech Stack

- Python
- PostgreSQL
- Docker & Docker Compose
- dbt (data build tool)
- Pandas
- SQLAlchemy
- psycopg2

---

## 🧱 Architecture

### 🔹 Raw Layer

- Source CSV files are loaded into PostgreSQL
- Data is stored under the `raw` schema
- This layer keeps the data close to its original source format
- Loaded using a Python ingestion script

### 🔹 Staging Layer

- Built using dbt
- One staging model per raw table
- Responsible for:
  - Column selection
  - Column renaming
  - Data type casting
  - Basic cleanup and standardization

### 🔹 Marts Layer

- Built using dbt
- Contains analytics-ready fact and dimension tables
- Designed as a star schema for reporting and BI tools

---

## 📂 Project Structure

```text
project/
│
├── datasets/                    # Raw CSV files (ignored in Git)
│
├── scripts/
│   ├── data_exploration.ipynb   # Initial data exploration
│   └── load_raw_data.py         # Python ingestion script
│
├── dbt_ecommerce/
│   ├── models/
│   │   ├── staging/             # Staging dbt models
│   │   └── marts/               # Fact, dimension, and KPI models
│   └── dbt_project.yml
│
├── docker-compose.yml
├── README.md
└── .gitignore
```

---

## 🚀 Steps Completed

### 1. Data Exploration

- Explored the dataset structure
- Identified key entities and relationships
- Classified tables into:
  - Facts
  - Dimensions
  - Supporting facts
- Defined the main business process: e-commerce sales analysis

---

### 2. Environment Setup

- Set up PostgreSQL using Docker
- Created database:

```text
ecommerce_dw
```

- Configured schemas:

```text
raw
staging
marts
```

---

### 3. Data Ingestion

- Built a Python ingestion script using:
  - Pandas
  - SQLAlchemy
  - psycopg2
- Loaded all CSV files into PostgreSQL under the `raw` schema

Loaded raw tables:

```text
raw.customers
raw.geolocation
raw.order_items
raw.order_payments
raw.order_reviews
raw.orders
raw.product_category_translation
raw.products
raw.sellers
```

---

### 4. dbt Setup

- Initialized a dbt project
- Connected dbt to PostgreSQL
- Verified the connection using:

```bash
dbt debug
```

---

### 5. Staging Layer

Built staging models for all raw tables:

```text
stg_customers
stg_geolocation
stg_order_items
stg_order_payments
stg_order_reviews
stg_orders
stg_product_category_translation
stg_products
stg_sellers
```

Applied:

- Column selection
- Renaming conventions
- Data type casting:
  - `timestamp`
  - `date`
  - `numeric`
  - `int`

Used:

- `source()` to reference raw tables
- `ref()` to reference dbt models

---

### 6. Marts Layer

Built analytics-ready fact and dimension tables.

#### Dimensions

```text
dim_customers
dim_products
dim_sellers
```

#### Facts

```text
fct_order_items
fct_payments
fct_reviews
```

Main fact table:

```text
fct_order_items
```

Grain:

```text
One row per order item
```

This model supports analysis such as:

- Revenue by product
- Revenue by seller
- Revenue by customer location
- Delivery performance
- Product category performance

---

### 7. KPI Models

Built business-level KPI models for analytics and reporting:

```text
sales_per_day
revenue_by_category
revenue_by_seller
```

These models help answer common business questions such as:

- What is the daily revenue trend?
- Which product categories generate the most revenue?
- Which sellers generate the highest revenue?

---

### 8. Data Quality Testing

Implemented dbt tests including:

- `not_null`
- `unique`
- `relationships`

Validated:

- Primary keys in dimension tables
- Required fields in fact tables
- Relationships between facts and dimensions

Example relationships tested:

```text
fct_order_items.customer_id → dim_customers.customer_id
fct_order_items.product_id  → dim_products.product_id
fct_order_items.seller_id   → dim_sellers.seller_id
```

---

## ⭐ Star Schema

The final marts layer follows a star schema design:

```text
              dim_customers
                    |
dim_products — fct_order_items — dim_sellers
```

Supporting facts:

```text
fct_payments
fct_reviews
```

The star schema makes the data easier to query, analyze, and connect to BI tools such as Power BI.

---

## ⚠️ Challenges Faced

### 1. Docker & Port Conflicts

- Issue: Connection was established to a different PostgreSQL instance running on the default port.
- Fix: Changed the exposed PostgreSQL port from `5432` to `5433` to isolate the project environment.

---

### 2. PostgreSQL Authentication Issue

```text
password authentication failed for user "postgres"
```

- Cause: Existing PostgreSQL credentials or cached Docker configuration caused a mismatch.
- Fix: Isolated the project connection using a dedicated port and recreated the container.

---

### 3. Environment & Dependency Management

- Issue: dbt was not recognized due to environment and PATH issues on Windows.
- Fix: Created an isolated virtual environment and installed dbt inside it.

```bash
python -m venv .venv
.venv\Scripts\activate
pip install dbt-postgres
```

---

### 4. Understanding dbt Concepts

- Issue: Initial confusion between `source()` and `ref()`
- Fix:
  - `source()` is used for raw source tables
  - `ref()` is used for dbt models

---

### 5. Data Modeling Decisions

- Issue: Deciding which tables should be facts, dimensions, or supporting facts.
- Fix:
  - Used grain analysis to define the main fact table
  - Selected `fct_order_items` as the main fact because it represents product-level sales transactions
  - Kept payments and reviews as separate supporting facts because they have different grains

---

## 🧠 Key Learnings

- Difference between ingestion and transformation
- Difference between raw, staging, and marts layers
- How to use Docker for a reproducible database environment
- How Docker volumes can persist data and credentials
- How to use dbt for transformation, testing, and documentation
- How to design a star schema
- How to define fact table grain
- How to apply dbt tests for data quality
- Why `source()` and `ref()` are important for lineage and dependency tracking
- How KPI models can turn warehouse data into business-ready insights

---

## 🧠 Personal Learnings

Through this project, I gained hands-on experience building a complete data pipeline from scratch, including data ingestion, transformation, testing, data modeling, and KPI development.

The most valuable learning was understanding how real-world data engineering systems are structured using layered architecture and how dbt helps enforce clean transformations, data quality, and maintainability.

Debugging environment issues such as Docker port conflicts, PostgreSQL authentication, and dbt setup on Windows improved my ability to troubleshoot real-world data engineering problems.

---

## 📊 Next Steps

- Generate and review dbt documentation
- Add screenshots of dbt lineage graph to the README
- Connect marts layer to Power BI
- Integrate Airflow for orchestration:
  - Run ingestion script
  - Run dbt models
  - Run dbt tests

---

## 👨‍💻 Author

Tarek Mahmoud Abdelrady
