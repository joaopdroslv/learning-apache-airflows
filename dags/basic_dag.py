from datetime import datetime

from airflow import DAG
from airflow.models import Variable
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago


def print_welcome():
    greeting = Variable.get("greeting")
    print(f"\n{greeting}")


def print_hello_world():
    print("\nHello, world!")


def print_date():
    print("\nToday is {}".format(datetime.today().date()))


dag = DAG(
    "basic_dags_example",
    default_args={"start_date": days_ago(1)},
    schedule_interval="0 12 * * *",
    catchup=False,
)

print_welcome_task = PythonOperator(
    task_id="print_welcome", python_callable=print_welcome, dag=dag
)

print_hello_world_task = PythonOperator(
    task_id="print_hello_world", python_callable=print_hello_world, dag=dag
)

print_date_task = PythonOperator(
    task_id="print_date", python_callable=print_date, dag=dag
)


# Define task dependencies
print_welcome_task >> print_hello_world_task >> print_date_task
