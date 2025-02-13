# Datasets and Data-Aware Scheduling

In Apache Airflow, **datasets** represent logical data assets that can be produced by one DAG and consumed by another. **Data-Aware Scheduling** enables DAGs to be triggered automatically when a specific dataset is updated. This optimizes workflow execution by making DAGs event-driven rather than relying solely on time-based schedules.

**Key Benefits of Data-Aware Scheduling**
1. `Reduced Time-Based Scheduling` → DAGs no longer need to run at fixed intervals.
2. `Optimized Resource Usage` → DAGs execute only when necessary, reducing CPU and memory consumption.
3. `More Dynamic Workflows` → Pipelines become more responsive and efficient.

## Cross DAG Dependencies

Cross DAG Dependencies allow a DAG to trigger another DAG when its execution is complete or when it updates a dataset. This can be managed using **datasets** or the `ExternalTaskSensor`.

**Key Benefits**
1. `Efficient Orchestration` → Large workflows can be broken into smaller, more manageable DAGs.
2. `Improved Modularity` → Independent DAGs make maintenance and scaling easier.
3. `Less Failure and Redundancy` → DAGs run only when the required data is available.

## Producer-Consumer Use Cases

The **Producer-Consumer** pattern is commonly used in data pipelines where:
- A **Producer DAG** generates data.
- A **Consumer DAG** waits for that data before execution.

**Example Use Cases:**
- A DAG downloads and processes raw data, and another DAG analyzes it.
- A DAG loads transformed data into a warehouse, and another triggers a reporting system.

## Cost Reduction
Implementing **Data-Aware Scheduling** and **Cross DAG Dependencies** reduces costs by:
- Avoiding unnecessary executions → DAGs trigger only when new data is available.
- Optimizing infrastructure usage → Less CPU/memory usage in cloud environments.
- Improving operational efficiency → Reduces manual intervention and debugging.

## Example: Cross DAG Dependencies Using Datasets

**Step 1: Producer DAG**
The producer updates a dataset (`my_dataset`) everyday after execution.
```python
from airflow import Dataset
from airflow.decorators import dag, task
from datetime import datetime
import polars as pl

my_dataset = Dataset("/tmp/my_csv.csv")

@dag(start_date=datetime(2024, 1, 1), schedule="@daily", catchup=False)
def producer_dag():
    @task
    def generate_data():
        # Simulating data processing and saving to CSV using Polars
        df = pl.DataFrame({
            "id": [1, 2, 3],
            "value": [100, 200, 300],
            "processed_at": [datetime.now()] * 3
        })
        df.write_csv("/tmp/my_csv.csv")

    generate_data() >> my_dataset  # Mark dataset as updated

producer_dag()
```

**Step 2: Consumer DAG**
The consumer DAG runs **only when the dataset is updated.**
```python
@dag(start_date=datetime(2024, 1, 1), schedule=[my_dataset], catchup=False)
def consumer_dag():
    @task
    def consume_data():
        # Simulate consuming the dataset
        print("Processing updated dataset...")

    consume_data()
s
consumer_dag()
```

This setup ensures that the consumer **DAG runs only when the producer DAG updates the dataset**, avoiding unnecessary executions and improving efficiency.

`NOTE`: One DAG can be triggered by multiple dataset and DAGs can also update multiple datasets.
