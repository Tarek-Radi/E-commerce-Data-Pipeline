# 🛒 E-commerce Data Pipeline (dbt + Airflow)

## 📌 Overview

This project builds a modern data pipeline for an e-commerce dataset using:

* PostgreSQL (Dockerized)
* dbt (Data Transformation)
* Python (Data Ingestion)
* Docker (Environment Setup)

The pipeline follows a layered architecture:

```
raw → staging → marts
(bronze → silver → gold)
```

---

## ⚙️ Tech Stack

* Python
* PostgreSQL
* Docker & Docker Compose
* dbt (data build tool)
* Pandas & SQLAlchemy

---

## 🧱 Architecture

### 🔹 Raw Layer

* Source data loaded from CSV files
* Stored in PostgreSQL under `raw` schema
* Loaded using Python ingestion script

### 🔹 Staging Layer (dbt)

* Data cleaning
* Column renaming
* Type casting

### 🔹 Marts Layer (dbt)

* Fact and dimension tables
* Business-ready models

---

## 📂 Project Structure

```
project/
│
├── datasets/              # raw CSV files (ignored in Git)
├── scripts/
│   └── load_raw_data.py   # ingestion script
│
├── dbt_ecommerce/
│   ├── models/
│   │   ├── staging/
│   │   └── marts/
│   └── dbt_project.yml
│
├── docker-compose.yml
└── .gitignore
```

---

## 🚀 Steps Completed

### 1. Data Exploration

* Analyzed dataset structure
* Identified fact & dimension tables

### 2. Environment Setup

* Dockerized PostgreSQL
* Configured database and schemas:
  * `raw`
  * `staging`
  * `marts`

### 3. Data Ingestion

* Built Python ingestion script using:
  * Pandas
  * SQLAlchemy
* Loaded CSV files into the `raw` schema

### 4. dbt Setup

* Initialized dbt project
* Connected dbt to PostgreSQL
* Verified connection using `dbt debug`

### 5. Data Transformation (dbt - Staging Layer)

* Built staging models for all raw tables
* Applied:
  * Column selection
  * Renaming conventions
  * Data type casting (`timestamp`, `numeric`, `int`)
* Used dbt `source()` for raw data references
* Used dbt `ref()` for model dependencies

### 6. Data Quality Testing

* Implemented dbt tests:
  * `not_null`
  * `unique`
* Validated key columns across staging models
* Ensured important fields such as IDs and prices meet quality constraints

---

## ⚠️ Challenges Faced

### ❌ 1. Docker & Port Conflicts

* Issue: Connection was established to a different PostgreSQL instance running on the default port.
* Fix: Changed exposed port from `5432` to `5433` to isolate the project environment.

---

### ❌ 2. PostgreSQL Authentication Issue

```text
password authentication failed for user "postgres"
```

* Cause: Docker volume persisted old credentials.
* Fix:

```bash
docker compose down -v
docker compose up -d
```

---

### ❌ 3. Environment & Dependency Management

* Issue: dbt was not recognized due to environment and dependency conflicts (especially on Windows).
* Fix: Created an isolated virtual environment to ensure clean dependency management.

```bash
python -m venv .venv
.venv\Scripts\activate
pip install dbt-postgres
```
### ❌ 4. Understanding dbt Concepts

* Issue: Initial confusion between `source()` and `ref()`
* Fix:
  - `source()` → used for raw tables
  - `ref()` → used for dbt models
---

### 5. Data Transformation (dbt - Staging Layer)

- Built staging models for all raw tables
- Applied:
  - Column selection
  - Renaming conventions
  - Data type casting (timestamp, numeric, int)
- Used dbt `source()` for raw data and `ref()` for model dependencies
- Created a clean and consistent semantic layer

---

### 6. Data Quality Testing

- Implemented dbt tests:
  - `not_null`
  - `unique`
- Validated data integrity across staging models
- Ensured key columns (IDs, price, etc.) meet quality constraints

## 🧠 Key Learnings

* Difference between ingestion (Python) vs transformation (dbt)
* Importance of layered architecture
* Docker volumes persist data across runs
* Separation between raw and transformed data
* Importance of environment isolation (venv)

---

## 📊 Next Steps

- Build marts layer (fact & dimension tables)
- Create main fact table (order_items)
- Design star schema
- Add advanced dbt tests:
  - relationships
  - accepted_values
- Generate dbt documentation & lineage graph
- Integrate Airflow for orchestration
---

## 🧠 Personal Learnings

Through this project, I gained hands-on experience in building a complete data pipeline from scratch, including data ingestion, transformation, and validation.

The most valuable learning was understanding how real-world data engineering systems are structured using layered architecture (raw → staging → marts), and how tools like dbt help enforce data quality and maintainability.

Debugging environment issues (Docker, PostgreSQL authentication, and dbt setup on Windows) was challenging but significantly improved my problem-solving skills and understanding of real production scenarios.

## 👨‍💻 Author

Tarek Mahmoud Abdelrady

