# Variables

## Variables types

**key:value style variables:**

```
Key:    max_records_to_process
Value:  1000

Key:    support_email
Value:  support@support.com
```

**JSON string variables**

```
Key:    process_interval
Value:  {'start_date': '2025-01-01', 'end_date': '2025-01-31'}
```

##  Benefitis of using varibles

1. **Implementing changes made easy**

Using variables allows you to modify values without changing the DAG code.
```python
from airflow.models import Variable

def fetch_data():
    url = Variable.get("api_url", default_var="https://default-api.com")
    print(f"Fetching data from {url}")
```

2. **Environment specific**

You can define different values for variables based on environments (e.g., dev, staging, production).
```python
env = Variable.get("environment", default_var="dev")
db_name = f"my_database_{env}"  # e.g., "my_database_dev" or "my_database_prod"
print(f"Using database: {db_name}")
```

3. **Security**

Sensitive information (like API keys) can be stored securely as variables instead of hardcoding them.
```python
api_key = Variable.get("api_secret_key", default_var="default_key")
print(f"Using API key: {api_key}")  # Avoid printing sensitive info in logs
```

4. **Makes DAGs more dynamic**

Variables allow DAGs to adapt dynamically based on input values.
```python
batch_size = int(Variable.get("batch_size", default_var="100"))

def process_data():
    print(f"Processing {batch_size} records at a time")

process_data()
```
