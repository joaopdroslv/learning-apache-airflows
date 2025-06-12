import csv
from datetime import datetime

from airflow import Dataset
from airflow.decorators import dag, task

# import polars as pl


my_dataset = Dataset("/tmp/products.csv")


@dag(start_date=datetime(2025, 1, 1), schedule="@daily", catchup=False)
def producer_dag():
    @task(
        outlets=[my_dataset]
    )  # outlets=[my_dataset]  # Signals that the task updates the dataset
    def generate_data():
        # Simulating data processing and saving to CSV using Polars
        # df = pl.DataFrame({
        #     'name': ['Smart TV', 'Tablet', 'Smartphone'],
        #     'value': [999.99, 296.50, 499.50],
        #     'units_sold': [19, 3, 73],
        #     'processed_at': [datetime.now()] * 3
        # })
        # df.write_csv('/tmp/products.csv')

        data = [
            ["name", "value", "units_sold", "processed_at"],
            ["Smart TV", 999.99, 19, datetime.now()],
            ["Tablet", 296.50, 3, datetime.now()],
            ["Smartphone", 499.50, 73, datetime.now()],
        ]

        with open("/tmp/products.csv", mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerows(data)

    # Generate data task
    generate_data()

    # Mark the dataset as updated after generating the data
    # generate_data() >> my_dataset


producer_dag()


@dag(start_date=datetime(2025, 1, 1), schedule=[my_dataset], catchup=False)
def consumer_dag():
    @task
    def consume_data():
        print("Dataset was updated, processing it...")

        # # Read CSV with Polars
        # df = pl.read_csv('/tmp/products.csv')

        # # Add 'total' column (units_sold * value)
        # df = df.with_columns((pl.col("units_sold") * pl.col("value")).alias("total"))

        # # Print each row after processing
        # for row in df.iter_rows(named=True):
        #     print(row)

        with open("/tmp/products.csv", mode="r") as file:
            reader = csv.reader(file)
            header = next(reader)  # Lê o cabeçalho
            print(f"Cabeçalho: {header}")

            for row in reader:
                name, value, units_sold, processed_at = row
                total = float(value) * int(units_sold)
                print(f"[PRODUCT] {name:<15} [TOTAL] {total:.2f}")

        print("Dataset processed.")

    consume_data()


consumer_dag()
