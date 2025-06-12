from airflow import DAG
from airflow.operators.latest_only import LatestOnlyOperator
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago


def raise_exception(str):
    raise Exception(str)


dag = DAG(
    "latest_only_example",
    default_args={"start_date": days_ago(3)},
    schedule_interval="0 12 * * *",
    catchup=True,
)

task_a = PythonOperator(
    task_id="task_a",
    python_callable=lambda: print("Executing Task A"),
    dag=dag,
)

task_b = PythonOperator(
    task_id="task_b",
    python_callable=lambda: print("Executing Task B"),
    dag=dag,
)

# Task for LatestOnlyOperator branch
latest_only_task = LatestOnlyOperator(task_id="latest_only", dag=dag)

# Task simulating failure
send_failure_task = PythonOperator(
    task_id="send_failure",
    python_callable=lambda: raise_exception("Task B failed, sending e-mail."),
    dag=dag,
)

# Task for simulating successful completion
send_success_task = PythonOperator(
    task_id="send_success",
    python_callable=lambda: print("Task B succeded, sending e-mail."),
    dag=dag,
)


task_a >> task_b >> send_failure_task
task_b >> latest_only_task >> send_success_task

# Task Execution Flow:
# task_a starts and prints "Executing Task A".
# task_b runs after task_a and prints "Executing Task B".
# send_failure_task runs after task_b, but since it raises an exception (raise_exception),
#   it will fail, and the DAG execution will halt here.
# latest_only_task runs after task_b. However, it will only allow the most
#   recent run of task_b to continue. If task_b succeeds, it allows send_success_task to run. But in this case, since task_b has already failed due to the exception, this task will not proceed either.
#   send_success_task will only run if latest_only_task runs successfully.
#   Since the exception in send_failure_task halts the DAG, this task will not execute in this run.
