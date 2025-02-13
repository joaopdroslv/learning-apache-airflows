from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago


def raise_exception(str):
    raise Exception(str)


dag = DAG(
    'trigger_rules_example',
    default_args={'start_date': days_ago(1)},
    schedule_interval='0 12 * * *',
    catchup=False
)

task_a = PythonOperator(
    task_id='task_a',
    python_callable=lambda: raise_exception("Failure in Query a"),
    dag=dag,
)

task_b = PythonOperator(
    task_id='task_b',
    python_callable=lambda: raise_exception("Failure in Query b"),
    dag=dag,
)

task_c = PythonOperator(
    task_id='task_c',
    python_callable=lambda: raise_exception("Failure in Query c"),
    dag=dag,
)

task_d = PythonOperator(
    task_id='task_d',
    python_callable=lambda: print("Executing Task D"),
    dag=dag,
    trigger_rule='all_failed',
)

task_e = PythonOperator(
    task_id='task_e',
    python_callable=lambda: print("Executing Task E"),
    dag=dag,
)

# 'task_d' has the 'trigger_rule' attribute set to 'all_failed', 
# this implies that a 'task_d' will only be executed if all previous ones fail

task_a >> task_d
task_b >> task_d
task_c >> task_d
task_d >> task_e
