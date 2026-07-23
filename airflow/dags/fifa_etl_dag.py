from datetime import datetime

from airflow import DAG
from airflow.operators.bash import BashOperator

with DAG(
    dag_id="Proyecto_FIFA_ETL",
    start_date=datetime(2025, 1, 1),
    schedule=@daily,
    catchup=False,
    tags=["FIFA", "ETL"],
) as dag:

    BashOperator(
        task_id="ejecutar_etl",
        bash_command="""
cd /home/kgrefa2026a/Proyecto_FIFA/etl
source /home/kgrefa2026a/Proyecto_FIFA/venv/bin/activate
python main.py
""",
    )
