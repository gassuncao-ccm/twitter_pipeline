from airflow.models import DAG
from airflow.utils.dates import days_ago
from airflow.operators.python_operator import PythonOperator

with DAG(
    'atividade_aula_4',
    start_date=days_ago(1),
    schedule_interval='@daily'
) as dag:
    
    def cumprimentos():
        print("Boas-vindas ao Airflow!")

    task_1 = PythonOperator(
        task_id='print_cumprimentos',
        python_callable=cumprimentos
    )
# with DAG(
#     'meu_primeiro_dag', # DAG ID
#     start_date=days_ago(1), # Date de inicio
#     schedule_interval='@daily' # De quanto e quanto tempo ele deve ser executado
# ) as dag: