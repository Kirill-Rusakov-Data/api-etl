from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
import sys

sys.path.insert(0, "/opt/airflow/scripts")
import etl_functions as etl

default_args = {
    "owner": "kirill",
    "retries": 1,
    "retry_delay": timedelta(minutes=1),
}

with DAG(
    dag_id="api_to_postgres_etl",
    default_args=default_args,
    start_date=datetime(2026, 1, 1),
    schedule="@daily",
    catchup=False,
    tags=["etl", "junior"],
) as dag:

    extract_task = PythonOperator(
        task_id="extract_from_api",
        python_callable=etl.extract,
    )

    transform_task = PythonOperator(
        task_id="transform_dedup",
        python_callable=etl.transform,
        op_args=[extract_task.output],
    )

    load_task = PythonOperator(
        task_id="load_to_postgres",
        python_callable=etl.load,
        op_args=[transform_task.output],
    )

    extract_task >> transform_task >> load_task