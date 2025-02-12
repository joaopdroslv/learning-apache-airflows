# XCOM

**XCom** (short for **Cross-Communication**) in Apache Airflow is a mechanism that **allows tasks to exchange messages or share data** during the execution of a Directed Acyclic Graph (DAG). 

XCom is primarily used for **passing small amounts of data** (such as strings, integers, or lists) between tasks.

When tasks are executed in a DAG, **each task can push and pull data to/from XComs**. This is especially useful when one task depends on the output of another.

## How to use XComs:

1. **Pushing data to XCom**
Tasks can push data to XCom using the `xcom_push` method. This can be done within a task's Python function.

```python
def push_data(**kwargs):
    value = 'some data'
    kwargs['ti'].xcom_push(key='my_key', value=value)
```

2. **Pulling data from XCom**
Other tasks can pull the data using the xcom_pull method.

```python
def pull_data(**kwargs):
    ti = kwargs['ti']
    value = ti.xcom_pull(task_ids='task_name', key='my_key')
    print(value)
```

3. **Using XCom in PythonOperator**
XCom can be used seamlessly with PythonOperator. You can define a function that pushes or pulls data from XCom inside the operator.

## Example of Passing Data Between Tasks:

```python
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime


def push_data(**kwargs):
    # 'ti' is the task instance, which allows interaction with XCom and other task-level functions
    # The 'kwargs' argument is passed automatically by Airflow, 
    #   containing contextual information for the task
    kwargs['ti'].xcom_push(key='my_key', value='Hello from task A')

def pull_data(**kwargs):
    # Accessing the task instance 'ti' to pull data from XCom
    ti = kwargs['ti']
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
```

`NOTE`: The XCom mechanism is useful for passing data between tasks that are in the same DAG and that execute sequentially or have dependencies set.

## Big amounts of data

It’s better to **avoid XCom for storing the data directly**. Instead, **use external storage solutions** or databases to store and reference the data, while **keeping XCom to pass small references or metadata**.
