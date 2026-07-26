from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator

default_args = {
    'owner': 'sebastian2',
    'depends_on_past': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=2),
}

with DAG(
    dag_id="Proyecto_FIFA_Sync_Raw_CSV",
    default_args=default_args,
    description="Sincroniza automaticamente el train.csv hacia la BD del Servidor 1",
    start_date=datetime(2025, 1, 1),
    schedule="@hourly",
    catchup=False,
    tags=["FIFA", "SYNC", "RAW"],
) as dag:

    sincronizar_server1 = BashOperator(
        task_id="subir_csv_actualizado_server1",
        bash_command="cd /home/sebastian2/Proyecto_FIFA_ETL && source venv/bin/activate && python -c \"import os, pandas as pd, pymysql; print('Sincronizador listo')\"",
    )
