from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

with DAG(
    dag_id="ecommerce_pipeline",
    start_date=datetime(2024, 1, 1),
    schedule_interval="@daily",
    catchup=False
) as dag:

    ingest = BashOperator(
        task_id="load_data",
        bash_command="python /opt/scripts/load_raw_data.py"
    )

    dbt_run = BashOperator(
        task_id="dbt_run",
        bash_command="cd /opt/dbt && /home/airflow/.local/bin/dbt run --profiles-dir /opt/dbt"
    )

    dbt_test = BashOperator(
        task_id="dbt_test",
        bash_command="cd /opt/dbt && /home/airflow/.local/bin/dbt test --profiles-dir /opt/dbt"
    )

    ingest >> dbt_run >> dbt_test