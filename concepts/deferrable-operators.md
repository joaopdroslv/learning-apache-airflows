# Deferrable Operators

In Apache Airflow, **deferrable operators** and **triggers** provide an efficient way to manage long-running tasks or tasks that require waiting for some external event or condition to be met, without consuming resources (like worker slots) during the wait time.

Deferrable operators are a type of operator that `can be deferred`. When a task is deferred, it doesn't occupy an execution slot for the entire duration it is waiting for an external event or condition. Instead, the task can be paused and then resumed when the event happens or after a specified condition is met.

**Key Characteristics of Deferrable Operators:**

- `Non-blocking` → They don't hold up resources while waiting.
- `Efficient` → Helps in reducing the overall load on the system, especially in cases where tasks may need to wait for external systems, such as databases, APIs, or file systems.
- `State management` → Airflow tracks the state of deferred tasks, and these tasks are resumed once the required conditions are met.

**How Deferrable Operators Work:**

- `Defer` → When the operator's execution logic is deferred, the task is paused.
- `Trigger` → A trigger will eventually be executed (either via an event or an external system) to resume the task, which will complete its execution.

**Example:**
Here’s an example of a deferrable operator, specifically the `HttpSensor`, which is used to wait for a response from an HTTP endpoint.

```python
from airflow.sensors.http import HttpSensor
from airflow.utils.dates import days_ago

def check_api_response(**kwargs):
    print("Checking API response...")

http_sensor = HttpSensor(
    task_id='wait_for_api_response',
    http_conn_id='my_api',
    endpoint='status',
    poke_interval=30,
    timeout=600,
    mode='reschedule',  # Deferrable mode
    deferrable=True,    # Set deferrable mode
    poke_interval=60,
    timeout=600,
    dag=dag
)
```

In this case, the `HttpSensor` will check the status of the API. If the condition isn't met, it will defer, freeing up the worker slot until the next scheduled check. Once the condition is met, the task will proceed.

# Triggers

A **trigger** is a mechanism that controls the execution of deferred tasks in Airflow. When a task is deferred, it will stay in a deferred state until it is triggered. A trigger is responsible for notifying Airflow that the task should resume.

**Key Concepts of Triggers:**

- `Triggers are event-driven` → They respond to specific events or conditions, such as the availability of data, an external system responding, or a time-based event.
- `Custom Triggers` → You can create custom triggers to respond to various external conditions (e.g., waiting for a file to be available in a cloud storage system, or waiting for a response from an API).
- `Built-in Triggers` → Airflow provides a set of 
built-in triggers like `TimeDeltaTrigger` (which waits for a certain time delta to pass) or `ExternalTaskTrigger` (which waits for an external task to complete).

**How Triggers Work:**

1. When a deferrable task reaches a state where it cannot proceed (like waiting for a condition or external signal), it is deferred.
2. The task enters a "waiting" state until a trigger is fired.
3. Once the trigger is activated, it signals the task to proceed with its execution.

**Example:**
Here’s an example of using a `TimeDeltaTrigger` to trigger a task after a specific delay:

```python
from airflow.triggers.delay import TimeDeltaTrigger
from datetime import timedelta

def wait_for_time_trigger(**kwargs):
    print("Waiting for time to pass...")

time_trigger = TimeDeltaTrigger(
    task_id='wait_for_10_minutes',
    delta=timedelta(minutes=10),
    trigger_rule='all_success',  # Trigger when all upstream tasks succeed
    dag=dag
)
```

In this example, the `TimeDeltaTrigger` will trigger the task to run after 10 minutes have passed, allowing the task to "wait" without holding up a worker slot.
