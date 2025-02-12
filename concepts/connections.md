# Connections

## Benefits
- `Reusability & Maintainability` → Easily reuse the same connection across multiple DAGs, reducing redundancy.
- `Environment Specific` → Define different connections for development, testing, and production environments.
- `Easy to Update` → Changing connection details in one place updates all workflows using it.
- `Security` → Credentials are stored securely in Airflow’s metadata database, avoiding hardcoding sensitive data in DAGs.

```js
{
    "connections" : [
        {
            "conn_id": "my_postpres_conn",
            "conn_type": "postgres",
            "host": "localhost",
            "schema": "my_database",
            "login": "user",
            "password": "password",
            "port": 5432
        }
        {
            "conn_id": "my_api_conn",
            "conn_type": "http",
            "host": "https://api.example.com",
            "extra": '{\"X-API-KEY\": \"...\"}'
        }
    ]
}
```

Connections can be managed via the Airflow UI, CLI, or imported from a JSON file.
