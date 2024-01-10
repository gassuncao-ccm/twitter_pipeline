from airflow import DAG
import pendulum
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from airflow.macros import ds_add
from os.path import join
import pandas as pd
from datetime import datetime, timedelta

with DAG(
    "dados_climaticos",
    start_date=pendulum.datetime(2023, 12, 1, tz= "UTC"),
    schedule_interval='0 0 * * 1', # executar toda segunda-feira
)as dag:
    
    tarefa_1 = BashOperator(
        task_id = 'cria_pasta',
        bash_command = 'mkdir -p "/home/gabrielsa/data_pipeline/airflowalura/semana={{data_interval_end.strftime("%Y-%m-%d")}}"'
    )

    def extrai_dados(data_interval_end):
        # intervalo de datas
        data_inicio = datetime.today()
        data_fim = data_inicio + timedelta(days=7)

        # formatando as datas
        data_inicio = data_inicio.strftime('%Y-%m-%d')
        data_fim = data_fim.strftime('%Y-%m-%d')

        city = 'RiodeJaneiro'
        key = 'YM36QYKECS3HV5GLE4VPC8WN3'

        URL = join('https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline'
                    f'/{city}/{data_interval_end}/{ds_add(data_interval_end, 7)}?unitGroup=metric&include=days&key={key}&contentType=csv')

        dados = pd.read_csv(URL)

        file_path = f'/home/gabrielsa/data_pipeline/airflowalura/semana={data_interval_end}/'

        dados.to_csv(file_path + 'dados_brutos.csv')
        dados[['datetime', 'tempmin', 'temp', 'tempmax']].to_csv(file_path + 'temperaturas.csv')
        dados[['datetime', 'description', 'icon']].to_csv(file_path + 'condicoes.csv')


    tarefa_2 = PythonOperator(
        task_id = 'extrai_dados',
        python_callable = extrai_dados,
        op_kwargs = {'data_interval_end': '{{data_interval_end.strftime("%Y-%m-%d")}}'}
    )

    tarefa_1 >> tarefa_2