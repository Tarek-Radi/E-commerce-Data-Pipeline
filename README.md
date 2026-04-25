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

* Built Python script using:

  * Pandas
  * SQLAlchemy
* Loaded CSV files into `raw` schema

### 4. dbt Setup

* Initialized dbt project
* Connected dbt to PostgreSQL
* Verified connection using `dbt debug`

## ⚠️ Challenges Faced

### ❌ 1. Docker & Port Conflicts

* Issue: Connection was established to a different PostgreSQL instance running on the default port.
* Fix: Changed exposed port from `5432` → `5433` to isolate the project environment.

---

### ❌ 2. PostgreSQL Authentication Issue

```
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

---


## 🧠 Key Learnings

* Difference between ingestion (Python) vs transformation (dbt)
* Importance of layered architecture
* Docker volumes persist data across runs
* Separation between raw and transformed data
* Importance of environment isolation (venv)

---

## 📊 Next Steps

* Build staging models in dbt
* Create fact & dimension tables
* Add dbt tests (not_null, unique, relationships)
* Generate dbt docs & lineage
* Integrate Airflow

---

## 👨‍💻 Author

Tarek Mahmoud Abdelrady

