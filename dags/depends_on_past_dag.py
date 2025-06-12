from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago

dag = DAG(
    "depends_on_past_example",
    default_args={"start_date": days_ago(1)},
    schedule_interval="0 12 * * *",
    catchup=False,
)

task_a = PythonOperator(
    task_id="task_a",
    python_callable=lambda: print("Executing Task A"),
    dag=dag,
)

task_b = PythonOperator(
    task_id="task_b",
    python_callable=lambda: print("Executing Task B"),
    depends_on_past=True,
    dag=dag,
)

# 'task_b' will only run if its previous execution was successful.
task_a >> task_b
