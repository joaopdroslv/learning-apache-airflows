from airflow import DAG
from airflow.sensors.filesystem import FileSensor
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago


# Path to the file that the DAG will monitor
FILE_PATH = '/opt/airflow/data/my_csv.csv'


def process_file():
    print('File available, processing it...')


dag = DAG(
    'filesensor_example',
    default_args={'start_date': days_ago(1)},
    schedule_interval='@daily',
    catchup=False
)

# Sensor task that waits until the file is available in the specified path
wait_for_file = FileSensor(
    task_id='wait_for_file',
    filepath=FILE_PATH,
    fs_conn_id=None,
    poke_interval=30,  # Interval (in seconds) between checks
    timeout=600,  # Maximum waiting time (in seconds) before failing the task
    mode='poke',
    dag=dag
)


# Our FileSensor will fail because we haven't defined a filesystem connection in Airflow.  
# Since the FileSensor fails, the downstream task 'process_file_task' will not be executed.  
#  
# To fix this, define a filesystem connection:  
#  
# wait_for_file = FileSensor(  
#     task_id='wait_for_file',  
#     filepath=FILE_PATH,  
#     fs_conn_id='local_filesystem',  # Set a valid fs_conn_id  
#     poke_interval=30,  
#     timeout=600,  
#     mode='poke',  
#     dag=dag  
# )  
#  
# Then, add the following command to the Webserver or Scheduler in Docker Compose:  
#  
# "airflow connections add local_filesystem --conn-type fs --conn-extra '{"path": "/"}'"  


# Task to process the file after the sensor detects it
process_file_task = PythonOperator(
    task_id='process_file_task',
    python_callable=process_file,
    dag=dag
)


# Wait for the file before processing it
wait_for_file >> process_file_task
