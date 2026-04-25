# 🛒 E-commerce Data Pipeline (PostgreSQL + dbt + Docker + Airflow)

## 📌 Overview

This project builds a modern end-to-end data engineering pipeline for an e-commerce dataset using PostgreSQL, Python, Docker, dbt, and Airflow.

The goal is to simulate a real-world data engineering workflow by ingesting raw CSV files into PostgreSQL, transforming them using dbt, applying data quality tests, building an analytics-ready star schema, and orchestrating the full pipeline with Airflow.

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
- Apache Airflow
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
- Contains analytics-ready fact, dimension, and KPI models
- Designed as a star schema for reporting and BI tools

### 🔹 Orchestration Layer

- Built using Airflow
- Automates the full pipeline execution:
  - Load raw data
  - Run dbt transformations
  - Run dbt data quality tests

---

## 📂 Project Structure

```text
project/
│
├── airflow/
│   └── dags/
│       └── pipeline_dag.py          # Airflow DAG
│
├── assets/
│   └── airflow_dag_success.png      # Airflow successful DAG screenshot
│
├── datasets/                        # Raw CSV files (ignored in Git)
│
├── scripts/
│   ├── data_exploration.ipynb       # Initial data exploration
│   └── load_raw_data.py             # Python ingestion script
│
├── dbt_ecommerce/
│   ├── models/
│   │   ├── staging/                 # Staging dbt models
│   │   └── marts/                   # Fact, dimension, and KPI models
│   ├── profiles.yml                 # dbt profile used inside Airflow container
│   └── dbt_project.yml
│
├── Dockerfile.airflow               # Custom Airflow image with dbt installed
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

### 9. Airflow Orchestration

Integrated Airflow to automate the full data pipeline execution.

The DAG runs the pipeline in the following order:

```text
load_data → dbt_run → dbt_test
```

- `load_data`: runs the Python ingestion script and loads raw CSV data into PostgreSQL
- `dbt_run`: runs dbt transformations
- `dbt_test`: runs dbt data quality tests

### Airflow DAG Run

![Airflow DAG Success](assets/airflow_dag_success.png)

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

## ▶️ How to Run Locally

### 1. Start Docker Services

```bash
docker compose up -d
```

### 2. Run Airflow

Open Airflow:

```text
http://localhost:8081
```

Default local credentials:

```text
username: admin
password: admin
```

### 3. Trigger the DAG

Trigger the Airflow DAG:

```text
ecommerce_pipeline
```

The DAG will run:

```text
load_data → dbt_run → dbt_test
```

### 4. Run dbt Manually (Optional)

From inside the dbt project folder:

```bash
cd dbt_ecommerce
dbt run
dbt test
```

---

## ⚠️ Challenges Faced & Fixes

### 1. PowerShell Command Differences

**Issue:**  
Some Linux-style commands did not work on Windows PowerShell.

Example:

```powershell
touch .gitignore
```

**Cause:**  
`touch` is a Unix/Linux command, while the project was developed on Windows using PowerShell.

**Fix:**  
Used PowerShell-compatible commands instead:

```powershell
New-Item .gitignore
```

or created files directly from VS Code.

---

### 2. `.gitignore` and Raw Dataset Handling

**Issue:**  
Raw CSV datasets were almost pushed to GitHub.

**Cause:**  
The `.gitignore` file was not configured correctly at first.

**Fix:**  
Added dataset and generated-file rules to `.gitignore`:

```gitignore
.venv/
__pycache__/
*.pyc
.env
dbt_packages/
target/
logs/
datasets/*
!datasets/sample/
```

---

### 3. Docker Desktop Not Running

**Issue:**  
Running Docker Compose failed with a Docker API connection error.

**Cause:**  
Docker Desktop was not running.

**Fix:**  
Started Docker Desktop, waited until the Docker engine was ready, then ran:

```bash
docker compose up -d
```

---

### 4. Docker & PostgreSQL Port Conflicts

**Issue:**  
The project connected to a different PostgreSQL instance running on the default port.

**Cause:**  
Port `5432` is the default PostgreSQL port and may already be used by another local PostgreSQL instance or another project.

**Fix:**  
Changed the exposed PostgreSQL port from `5432` to `5433`:

```yaml
ports:
  - "5433:5432"
```

---

### 5. PostgreSQL Authentication Issue

**Issue:**  

```text
password authentication failed for user "postgres"
```

**Cause:**  
Existing PostgreSQL credentials or cached Docker configuration caused a mismatch.

**Fix:**  
Isolated the project connection using a dedicated Docker port and recreated the container when needed.

A stronger fix, when data loss is acceptable:

```bash
docker compose down -v
docker compose up -d
```

> Note: `down -v` removes Docker volumes and deletes persisted database data.

---

### 6. dbt Not Recognized Locally

**Issue:**  

```text
dbt is not recognized as the name of a cmdlet
```

**Cause:**  
dbt was not installed inside the active Python environment, or its executable path was not available.

**Fix:**  
Created and activated a virtual environment:

```powershell
python -m venv .venv
.venv\Scripts\activate
```

Then installed dbt for PostgreSQL:

```bash
pip install dbt-postgres
```

---

### 7. dbt Project Path Error

**Issue:**  

```text
No dbt_project.yml found
```

**Cause:**  
dbt commands were executed from the project root instead of the dbt project folder.

**Fix:**  

```bash
cd dbt_ecommerce
dbt run
dbt test
```

---

### 8. dbt `source()` vs `ref()` Confusion

**Issue:**  
There was initial confusion between:

```sql
{{ source() }}
```

and:

```sql
{{ ref() }}
```

**Fix:**  

```text
source() → raw/source tables
ref()    → dbt models
```

Example:

```sql
from {{ source('raw', 'orders') }}
```

for raw tables.

```sql
from {{ ref('stg_orders') }}
```

for dbt models.

---

### 9. dbt Relationship Test Misconfiguration

**Issue:**  
A relationship test failed because `product_id` was accidentally tested against `dim_customers.customer_id`.

**Cause:**  
Incorrect YAML configuration in `marts.yml`.

**Fix:**  
Corrected the relationship test:

```yaml
- name: product_id
  tests:
    - relationships:
        arguments:
          to: ref('dim_products')
          field: product_id
```

Also updated relationship tests to use the newer dbt `arguments:` syntax.

---

### 10. GitHub Language Stats Showing Mostly Jupyter Notebook

**Issue:**  
GitHub language stats showed mostly Jupyter Notebook instead of SQL.

**Cause:**  
`.ipynb` files can be large because they store outputs, metadata, and execution results.

**Fix Attempts:**  

- Cleared notebook outputs in VS Code
- Considered excluding notebooks using `.gitattributes`

Example:

```text
*.ipynb linguist-vendored
```

> Note: `.gitattributes` should be placed in the project root if used.

---

### 11. Airflow Port Conflict

**Issue:**  
Airflow did not open correctly on the default port:

```text
localhost:8080
```

Sometimes the browser showed an old dbt docs page or a connection error.

**Cause:**  
Port `8080` was already used by another service, such as dbt docs or another local process.

**Fix:**  
Changed the Airflow port mapping:

```yaml
ports:
  - "8081:8080"
```

Then opened Airflow using:

```text
http://localhost:8081
```

---

### 12. Airflow Metadata Database Error

**Issue:**  

```text
FATAL: database "airflow" does not exist
```

**Cause:**  
Airflow was configured to use a PostgreSQL metadata database named `airflow`, but that database had not been created.

**Attempted Fix:**  

```yaml
AIRFLOW__DATABASE__SQL_ALCHEMY_CONN: postgresql+psycopg2://postgres:postgres@postgres:5432/airflow
```

**Final Fix:**  
Removed the custom Airflow metadata database connection and allowed Airflow to use SQLite for local development.

> Note: SQLite is acceptable for local development/testing, but PostgreSQL should be used for production Airflow deployments.

---

### 13. Airflow Webserver PID Issue

**Issue:**  

```text
Already running on PID ... or pid file is stale
```

**Cause:**  
A stale Airflow webserver PID file remained inside the container.

**Fix:**  
Removed the PID file before starting the webserver:

```bash
rm -f /opt/airflow/airflow-webserver.pid
```

This was added to the Airflow command in `docker-compose.yml`.

---

### 14. Airflow DAG Not Appearing

**Issue:**  
Airflow UI opened successfully, but no DAG appeared.

**Cause:**  
The DAG file was not initially placed in the correct mounted folder.

**Fix:**  
Created the correct structure:

```text
airflow/
└── dags/
    └── pipeline_dag.py
```

Verified that Airflow could see the DAG file:

```bash
docker exec -it airflow ls /opt/airflow/dags
```

Expected result:

```text
pipeline_dag.py
```

---

### 15. VS Code Airflow Import Warning

**Issue:**  
VS Code showed import warnings under:

```python
from airflow import DAG
from airflow.operators.bash import BashOperator
```

**Cause:**  
Airflow was installed inside the Docker container, not inside the local `.venv`.

**Fix:**  
Ignored the VS Code warning because the DAG runs inside the Airflow container.

No local Airflow installation was required.

---

### 16. Airflow `load_data` Failed Because Dataset Path Was Wrong

**Issue:**  

```text
FileNotFoundError: No such file or directory: 'datasets/olist_customers_dataset.csv'
```

**Cause:**  
Inside the Airflow container, the local project path `datasets/` does not exist in the same way it does on the host machine.

The datasets folder was mounted inside the container as:

```text
/opt/datasets
```

**Fix:**  
Updated `load_raw_data.py` to read the dataset path from an environment variable:

```python
import os
from pathlib import Path

DATA_PATH = Path(os.getenv("DATA_PATH", "datasets"))
```

Added the environment variable to the Airflow service:

```yaml
DATA_PATH: /opt/datasets
```

---

### 17. Airflow `load_data` Failed Because of Docker Networking

**Issue:**  
The ingestion script originally used:

```text
localhost:5433
```

**Cause:**  
Inside a Docker container, `localhost` refers to the container itself, not the host machine.

**Fix:**  
Updated `load_raw_data.py` to read the database URL from an environment variable:

```python
DB_URL = os.getenv(
    "DB_URL",
    "postgresql+psycopg2://postgres:postgres@localhost:5433/ecommerce_dw"
)
```

Added this environment variable to the Airflow service:

```yaml
DB_URL: postgresql+psycopg2://postgres:postgres@postgres:5432/ecommerce_dw
```

In Docker Compose, the service name `postgres` is used as the hostname.

---

### 18. Airflow Environment Variables Not Applied After Restart

**Issue:**  
After updating environment variables in `docker-compose.yml`, Airflow still behaved as if it was using the old values.

**Cause:**  
A normal restart does not always recreate the container with updated environment variables.

**Fix:**  

```bash
docker compose up -d --force-recreate airflow
```

Verified the variable inside the container:

```bash
docker exec -it airflow printenv DATA_PATH
```

Expected result:

```text
/opt/datasets
```

---

### 19. Raw Table Replacement Failed Due to dbt Views

**Issue:**  

```text
cannot drop table raw.customers because other objects depend on it
```

**Cause:**  
The ingestion script originally used:

```python
if_exists="replace"
```

This makes Pandas drop and recreate the raw table.

However, dbt staging views depended on the raw tables, such as:

```text
marts.stg_customers depends on raw.customers
```

PostgreSQL prevents dropping a table that has dependent views.

**Fix:**  
Changed the ingestion logic from replacing tables to truncating and appending data:

```python
from sqlalchemy import text

with engine.begin() as conn:
    conn.execute(text(f"TRUNCATE TABLE raw.{table_name} RESTART IDENTITY CASCADE"))

df.to_sql(
    table_name,
    engine,
    schema="raw",
    if_exists="append",
    index=False
)
```

This refreshes the data without dropping the table structure.

---

### 20. Airflow `dbt_run` Failed Because dbt Was Not Installed

**Issue:**  

```text
dbt: command not found
```

**Cause:**  
The base Airflow Docker image does not include dbt.

**Attempted Fix:**  
Tried installing dbt inside the running container:

```bash
docker exec -it airflow bash -c "python -m pip install dbt-postgres"
```

This was not reproducible and could be lost when the container is recreated.

**Final Fix:**  
Created a custom Airflow Docker image.

File:

```text
Dockerfile.airflow
```

Content:

```dockerfile
FROM apache/airflow:2.9.1

RUN pip install --no-cache-dir dbt-postgres
```

Updated `docker-compose.yml`:

```yaml
airflow:
  build:
    context: .
    dockerfile: Dockerfile.airflow
```

Then rebuilt Airflow:

```bash
docker compose down
docker compose build airflow
docker compose up -d
```

Verified dbt installation:

```bash
docker exec -it airflow dbt --version
```

---

### 21. Airflow `dbt_run` Failed Because dbt Profile Was Missing

**Issue:**  

```text
Path '/home/airflow/.dbt' does not exist
```

**Cause:**  
dbt inside the Airflow container needed a `profiles.yml` file to connect to PostgreSQL.

**Fix:**  
Created:

```text
dbt_ecommerce/profiles.yml
```

Configured it with Docker networking:

```yaml
dbt_ecommerce:
  target: dev
  outputs:
    dev:
      type: postgres
      host: postgres
      user: postgres
      password: postgres
      port: 5432
      dbname: ecommerce_dw
      schema: marts
      threads: 1
```

Updated the Airflow DAG commands to pass the profiles directory explicitly:

```bash
dbt run --profiles-dir /opt/dbt
dbt test --profiles-dir /opt/dbt
```

---

### 22. dbt Debug Git Permission Warning Inside Airflow

**Issue:**  
Running dbt debug inside the Airflow container showed a Git-related error.

**Cause:**  
The Airflow image did not have full permission for the `git` command in that environment.

**Result:**  
The database connection still passed successfully, and `dbt run` / `dbt test` worked.

**Fix:**  
No blocking fix was required for this local setup because the project did not rely on dbt packages from Git.

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
- How Airflow orchestrates ingestion, transformation, and testing
- How Docker networking works between services
- Why containerized pipelines need environment variables and mounted volumes

---

## 🧠 Personal Learnings

Through this project, I gained hands-on experience building a complete data pipeline from scratch, including data ingestion, transformation, testing, data modeling, KPI development, and orchestration.

The most valuable learning was understanding how real-world data engineering systems are structured using layered architecture and how dbt helps enforce clean transformations, data quality, and maintainability.

Debugging environment issues such as Docker port conflicts, PostgreSQL authentication, dbt setup on Windows, and Airflow container networking improved my ability to troubleshoot real-world data engineering problems.

---

## 📊 Next Steps

- Generate and review dbt documentation
- Add screenshots of dbt lineage graph to the README
- Connect marts layer to Power BI
- Improve Airflow setup for production:
  - Use PostgreSQL as Airflow metadata database
  - Add task retries
  - Add failure alerts
  - Add pipeline monitoring

---

## 👨‍💻 Author

Tarek Mahmoud Abdelrady
