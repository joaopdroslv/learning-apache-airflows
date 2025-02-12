from airflow import DAG
from airflow.sensors.filesystem import FileSensorAsync  # NOTE: This import is wrong
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago


# Path to the file that the DAG will monitor
FILE_PATH = '/opt/airflow/data/my_csv.csv'


def process_file():
    print('File available, processing it...')


# Creating the DAG
dag = DAG(
    'deferrable_filesensor_native',
    default_args={'start_date': days_ago(1)},
    schedule_interval='@daily',
    catchup=False,
)

# Asynchronous sensor that waits for the file without blocking the worker
wait_for_file = FileSensorAsync(
    task_id='wait_for_file',
    filepath=FILE_PATH,
    fs_conn_id=None,
    poke_interval=10,
    timeout=600,
    mode='reschedule',
    dag=dag,
)

# Our FileSensorAsync will fail because we haven't defined a filesystem connection in Airflow.  
#
# How does FileSensorAsync work?
#
# - The DAG starts and executes FileSensorAsync.
# - Instead of blocking a worker, FileSensorAsync registers a trigger (FileTrigger).
# - The trigger runs in the Triggerer process, continuously checking if the file exists.
# - Once the trigger detects the file, it 'wakes up' the DAG and allows the next task to run.


# Task that will run once the file is detected
process_file_task = PythonOperator(
    task_id='process_file_task',
    python_callable=process_file,
    dag=dag,
)

# Define task dependency: the file must exist before processing it
wait_for_file >> process_file_task
