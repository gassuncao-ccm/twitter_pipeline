from airflow.operators.dummy_operator import DummyOperator
from datetime import datetime as dtime
from airflow import DAG

def_args = {
    "owner": "airflow",
    "start_date": dtime(2023, 1, 5)
}

with DAG ("ETL",
          catchup=False,
          default_args= def_args
    ) as dag:

    start = DummyOperator(task_id = "START")
    e = DummyOperator(task_id = "EXTRACTION")
    t = DummyOperator(task_id = "TRANSFORM")
    l = DummyOperator(task_id = "LOAD")
    end = DummyOperator(task_id = "END")

start >> e >> t >> l >> end