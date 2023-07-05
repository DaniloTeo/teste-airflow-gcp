from airflow import DAG
from airflow.operators.python import PythonOperator, get_current_context
from datetime import datetime
from numpy import random
import zipfile

default_args = {
    'owner': 'Danilo Téo',
    "depends_on_past": False,
    "email": ["airflow@airflow.com"],
    "email_on_failure": False,
    "email_on_retry": False
    #"retries": 1,
    #"retry_delay": timedelta(minutes=1),
}

dag = DAG(
    "ENADE", 
    description="Uma dag para processamento de um dado maior",
    default_args=default_args, 
    schedule_interval=None
)

def get_data():
    return random.randint(42, size=5).tolist()

get_data = PythonOperator(
    task_id='get_data',
    python_callable=get_data,
    dag=dag
)

def get_odds():
    context = get_current_context()
    arr = context['task_instance'].xcom_pull(task_ids='get_data')
    return list(filter(lambda x: x % 2 != 0, arr))

get_odds = PythonOperator(
    task_id='get_odds',
    python_callable=get_odds,
    dag=dag
)

def get_evens():
    context = get_current_context()
    arr = context['task_instance'].xcom_pull(task_ids='get_data')
    return list(filter(lambda x: x % 2 == 0, arr))

get_evens = PythonOperator(
    task_id='get_evens',
    python_callable=get_evens,
    dag=dag
)

def join_numbers():
    context = get_current_context()
    odds = context['task_instance'].xcom_pull(task_ids='get_odds')
    evens = context['task_instance'].xcom_pull(task_ids='get_evens')
    print({odds, evens})

join_numbers = PythonOperator(
    task_id='join_numbers',
    python_callable=join_numbers,
    dag=dag
)


get_data >> [get_odds, get_evens] >> join_numbers