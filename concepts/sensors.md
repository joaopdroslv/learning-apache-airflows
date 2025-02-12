# Sensors

**Sensors** are a special type of operator that waits until a specific condition is met. Once the condition is satisfied, the sensor marks the task as complete and allows downstream tasks to proceed.

## Main types of sensors:

**FileSensor:** Waits for a file or directory to be available in a specific location (local or remote).
`Example:` can use it to check if a file exists or if a file is ready to be processed.

```python
from airflow.sensors.filesystem import FileSensor

file_sensor = FileSensor(
    task_id='check_file',
    filepath='/path/to/file.txt',
    poke_interval=30,
    timeout=600,
    mode='poke',
    dag=dag
)
```

**HttpSensor:** Waits for a response from an HTTP endpoint (like an API or a webpage).
`Example:` can use it to check if an API is up or if a service is responding as expected.

```python
from airflow.sensors.http_sensor import HttpSensor

http_sensor = HttpSensor(
    task_id='check_api',
    http_conn_id='my_api',
    endpoint='status',
    poke_interval=60,
    timeout=600,
    mode='poke',
    dag=dag
)
```

**SqlSensor:** Waits for a condition to be met in a database (based on SQL query results).
`Example:` can use it to wait until a particular record appears in a database or a certain condition is fulfilled.

```python
from airflow.sensors.sql import SqlSensor

sql_sensor = SqlSensor(
    task_id='check_table',
    conn_id='my_db',
    sql='SELECT COUNT(*) FROM my_table WHERE status="READY"',
    poke_interval=60,
    timeout=600,
    mode='poke',
    poke_interval=10,
    dag=dag
)
```

**S3KeySensor:** Waits for a specific object (file) to be available in an S3 bucket.
`Example:` can use it to ensure that a file has been uploaded to S3 before performing downstream tasks.

```python
s3_sensor = S3KeySensor(
    task_id='check_s3_file',
    bucket_name='my_bucket',
    bucket_key='data/file.txt',
    aws_conn_id='aws_default',
    poke_interval=60,
    timeout=600,
    mode='poke',
    dag=dag
)
```

**ExternalTaskSensor:** Waits for the completion of a task from a different DAG.
`Example:` can use it to wait for a task from another DAG to finish before proceeding with the current DAG.

```python
from airflow.sensors.external_task import ExternalTaskSensor

external_task_sensor = ExternalTaskSensor(
    task_id='wait_for_another_dag_task',
    external_dag_id='another_dag',
    external_task_id='task_in_another_dag',
    poke_interval=30,
    timeout=600,
    mode='poke',
    dag=dag
)
```

**TimeSensor:** Waits for a specific time to arrive before proceeding.
`Example:` can use it to wait until a particular time (e.g., the end of the day or a scheduled maintenance window) to start a task.

```python
from airflow.sensors.time import TimeSensor

time_sensor = TimeSensor(
    task_id='wait_for_time',
    target_time='2025-02-12 14:00:00',
    poke_interval=60,
    timeout=600,
    mode='poke',
    dag=dag
)
```

## Sensor Behavior

### Poke

Airflow has two main modes for sensors: `poke mode` and `reschedule mode`. The difference between these modes lies in the behavior of the task while it waits for the defined condition.

- `How It Works` → In poke mode, the sensor periodically checks the desired condition (e.g., the existence of a file or the response of an API) at the defined interval.
- `Behavior` → During this waiting period, the sensor occupies an "execution slot." It keeps checking the condition but does not release resources until the condition is met or the timeout period is reached.
- `When to Use` → Use when you don't mind occupying slots while waiting or when you need continuous checking.

```python
from airflow.sensors.filesystem import FileSensor

wait_for_file = FileSensor(
    task_id="wait_for_file",
    filepath="/path/to/file.txt",
    poke_interval=30,  # Checks every 30 seconds
    timeout=600,       # Waits for a maximum of 10 minutes
    mode="poke",       # Poke mode
    dag=dag
)
```

### Reschedule

- `How It Works` → In reschedule mode, the sensor still checks the condition periodically, but instead of occupying an execution slot during the waiting period, it "suspends" the task and only resumes when the next check is made.
- `Behavior` → This mode is more efficient because it frees up slots for other tasks while waiting, allowing Airflow to execute other tasks while the condition is being met.
- `When to Use` → Use in production environments where efficiency and optimal resource utilization are important, especially when continuous checks with occupied slots are unnecessary.

```python
wait_for_file_reschedule = FileSensor(
    task_id="wait_for_file_reschedule",
    filepath="/path/to/file.txt",
    poke_interval=30,  # Checks every 30 seconds
    timeout=600,       # Waits for a maximum of 10 minutes
    mode="reschedule", # Reschedule mode
    dag=dag
)
```

## Soft Fail

A soft fail is a feature that allows a task to fail "softly" without stopping the execution of downstream tasks.

- If a task fails in **soft fail**, it is marked as "failed," but Airflow does not consider this a critical failure that would block downstream tasks from running.
- The soft fail behavior is controlled by setting `soft_fail=True` in the operator.

```python
from airflow.operators.dummy_operator import DummyOperator

soft_fail_task = DummyOperator(
    task_id='soft_fail_task',
    dag=dag,
    retries=0,      # No retry attempts
    soft_fail=True  # Indicates the failure is soft
)

downstream_task = DummyOperator(
    task_id='downstream_task',
    dag=dag
)

soft_fail_task >> downstream_task
```

In this example, if `soft_fail_task` fails, it will not stop the execution of `downstream_task`, allowing the DAG to continue running.
