from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator, BranchPythonOperator
from airflow.operators.dummy_operator import DummyOperator
from airflow.utils.dates import days_ago


def get_file_size(file_path, ti):
    # Get file size in bytes
    # with open(file_path, "rb") as f:
    #     file_size_bytes = len(f.read())
    # # Convert bytes to gigabytes
    # file_size_gb = file_size_bytes / (1024 ** 3)

    # Push file size to XCom
    ti.xcom_push(key='file_size', value=100)

def decide_branch(ti):
    """
    Pulls the file size value from XCom and determines the execution path:
    - If the file size is greater than 10GB, it returns 'parallel_transform'.
    - Otherwise, it returns 'serial_transform'.
    """
    file_size = ti.xcom_pull(task_ids='check_file_size', key='file_size')
    return 'parallel_transform' if file_size > 10 else 'serial_transform'

def serial_transform():
    # Add your serial transformation logic here
    print("Executing serial transformation.")

def serial_load():
    # Add your serial load logic here
    print("Executing serial load.")

def parallel_transform():
    # Add your parallel transformation logic here
    print("Executing parallel transformation.")

def parallel_load():
    # Add your parallel load logic here
    print("Executing parallel load.")


dag = DAG(
    'conditional_branching_example',
    default_args={'start_date': days_ago(1)},
    schedule_interval='0 12 * * *',
    catchup=False
)

# Task to check file size
check_file_size_task = PythonOperator(
    task_id='check_file_size',
    python_callable=get_file_size,
    op_args=['/tmp/my_txt.txt'],
    provide_context=True,  # Allows passing Airflow context (e.g., XCom)
    dag=dag,
)

# Task to determine the execution branch
# This task returns the name of the next task to execute.
# The BranchPythonOperator will then decide the next step based on the returned branch name.
decide_branch_task = BranchPythonOperator(
    task_id='decide_branch',
    python_callable=decide_branch,  # Calls function to determine the branch
    provide_context=True,  # Allows pulling the file size from XCom
    dag=dag,
)

# Define tasks for serial execution
serial_transform_task = PythonOperator(
    task_id='serial_transform',
    python_callable=serial_transform,
    dag=dag,
)

serial_load_task = PythonOperator(
    task_id='serial_load',
    python_callable=serial_load,
    dag=dag,
)

# Define tasks for parallel execution
parallel_transform_task = PythonOperator(
    task_id='parallel_transform',
    python_callable=parallel_transform,
    dag=dag,
)

parallel_load_task = PythonOperator(
    task_id='parallel_load',
    python_callable=parallel_load,
    dag=dag,
)


# Check file size before deciding branch
check_file_size_task >> decide_branch_task  

# The result of the 'decide_branch_task' will determine the next step

# Serial branch
decide_branch_task >> serial_transform_task >> serial_load_task

# Parallel branch
decide_branch_task >> parallel_transform_task >> parallel_load_task
