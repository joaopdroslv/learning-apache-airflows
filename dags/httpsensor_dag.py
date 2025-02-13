from airflow import DAG
from airflow.sensors.http_sensor import HttpSensor
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago
import requests


# Function that will be executed after the API is available
def process_data():
    response = requests.get('https://api.restful-api.dev/objects')
    if response.status_code == 200:
        print('API is available! Processing data...')
        print('Data processed.')
    else:
        print('Failed to process the data.')


dag = DAG(
    'httpsensor_example',
    default_args={'start_date': days_ago(1)},
    schedule_interval='@daily',
    catchup=False
)

# Sensor that checks if the API is responding correctly (WITHOUT using Connection)
wait_for_api = HttpSensor(
    task_id='wait_for_api',
    http_conn_id=None,  # We don't use an Airflow connection
    endpoint='https://api.restful-api.dev/objects',  # Full URL
    method='GET',
    response_check=lambda response: response.status_code == 200,  # Check if the status is 200
    poke_interval=30,  # Interval (in seconds) between checks
    timeout=600,  # Maximum waiting time (in seconds) before failing the task
    mode='poke',
    dag=dag
)

# Task that runs after the API is available
process_data_task = PythonOperator(
    task_id='process_data',
    python_callable=process_data,
    dag=dag
)


wait_for_api >> process_data_task
