from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime


# Passing small data between tasks using XCom


def push_data(**context):
    # 'ti' is the task instance, which allows interaction with XCom and other task-level functions
    # The 'context' argument is passed automatically by Airflow, 
    #   containing contextual information for the task
    context['ti'].xcom_push(key='my_key', value='Hello from task A')

def pull_data(**context):
    # Accessing the task instance 'ti' to pull data from XCom
    ti = context['ti']
    value = ti.xcom_pull(task_ids='task_a', key='my_key')  # Pulling data from the task 'task_a' using the key 'my_key'
    print(f'Received data: {value}')


with DAG(
    'xcom_example', 
    start_date=datetime(2025, 1, 1),
    schedule_interval=None
) as DAG:
    task_a = PythonOperator(
        task_id='task_a',
        python_callable=push_data,
        provide_context=True  # This tells Airflow to pass task-related context (like 'ti') to the function
    )

    task_b = PythonOperator(
        task_id='task_b',
        python_callable=pull_data,
        provide_context=True  # This tells Airflow to pass task-related context (like 'ti') to the function
    )

    task_a >> task_b
