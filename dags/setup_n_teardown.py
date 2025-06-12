from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago


def raise_exception(str):
    raise Exception(str)


dag = DAG(
    "setup_teardown_example",
    default_args={"start_date": days_ago(1)},
    schedule_interval="0 12 * * *",
    catchup=False,
)

create_cluster_task = PythonOperator(
    task_id="create_cluster",
    python_callable=lambda: print("Creating Cluster"),
    dag=dag,
)

run_query1_task = PythonOperator(
    task_id="run_query1",
    python_callable=lambda: print("Running Query 1"),
    dag=dag,
)

# run_query2_task = PythonOperator(
#     task_id='run_query2_task',
#     python_callable=lambda: print("Running Query 2"),
#     dag=dag,
# )

run_query2_task = PythonOperator(
    task_id="run_query2",
    python_callable=lambda: raise_exception("Failure in Query 2"),
    dag=dag,
)

run_query3_task = PythonOperator(
    task_id="run_query3",
    python_callable=lambda: print("Running Query 3"),
    dag=dag,
)

delete_cluster_task = PythonOperator(
    task_id="delete_cluster",
    python_callable=lambda: print("Deleting Cluster"),
    dag=dag,
)


# The 'create_cluster_task' task must be executed before 'run_query1_task' and 'run_query2_task'
create_cluster_task >> [run_query1_task, run_query2_task]

# Both 'run_query1_task' and 'run_query2_task' must complete before 'run_query3_task' can start
[run_query1_task, run_query2_task] >> run_query3_task

# 'run_query3_task' must complete before 'delete_cluster_task' starts.
# 'delete_cluster_task' is also marked as a teardown task that depends on the 'create_cluster_task' task
run_query3_task >> delete_cluster_task.as_teardown(setups=create_cluster_task)


# Expected behavior:
# create_cluster_task    -> prints msg 'Creating Cluster'
#
# run_query1_task        -> prints msg 'Running Query 1'
# runs after create_cluster_task
#
# run_query2_task        -> prints msg 'Running Query 2'
# runs after create_cluster_task but will fail (always)
#
# run_query3_task        -> prints msg 'Running Query 3'
# runs after both, run_query1_task and run_query2_task (even if run_query2_task fails)
#
# delete_cluster_task    -> prints msg 'Deleting Cluster'
# runs last after run_query3_task, only if create_cluster_task has run (because it's a teardown)
#
# Flow:
# 1. create_cluster_task starts.
# 2. run_query1_task and run_query2_task run after create_cluster_task (in parallel).
# 3. run_query3_task runs after run_query1_task and run_query2_task (even if run_query2_task fails).
# 4. delete_cluster_task runs after run_query3_task.
