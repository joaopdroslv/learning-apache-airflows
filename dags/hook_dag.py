from airflow.hooks.mysql_hook import MySqlHook
from airflow.models import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime


def get_products_from_mysql():
    # Initialize the MySqlHook with the connection ID 'mysql_default'
    hook = MySqlHook(mysql_conn_id='mysql_conn')

    # Define the query to retrieve product data from the 'products' table
    query = "SELECT id, name, price FROM products"

    # Execute the query and fetch the results
    results = hook.get_records(query)

    for row in results:
        product_id, product_name, product_price = row
        print(f"[PRODUCT] [ID] {product_id:<5} [Name] {product_name:<35} [Price] $ {product_price}")


with DAG(
    'hook_example',
    start_date=datetime(2025, 1, 1),
    schedule_interval=None,  # The DAG will not be executed automatically, it will only be executed manually.
) as dag:
    # Create a task to run the function 'get_products_from_mysql'
    fetch_products_task = PythonOperator(
        task_id='fetch_products',
        python_callable=get_products_from_mysql,
    )

    fetch_products_task
