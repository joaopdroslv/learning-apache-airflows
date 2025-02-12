# Hook

A **hook** in Apache Airflow is a set of **helper functions** or **an abstraction** that **simplifies the interaction with external services or systems** (such as databases, cloud storage, or APIs). Hooks are designed to make it easier to connect to and communicate with these services by handling the low-level details of the connection, authentication, and interaction.

For example, Airflow provides hooks for interacting with services like **AWS** (S3, Redshift), **Google Cloud**, **databases** (PostgreSQL, MySQL), and others. Hooks typically manage the connection setup, data retrieval, and other operations related to the service.

Example:
You might use the `PostgresHook` to connect to a PostgreSQL database:

```python
from airflow.hooks.postgres_hook import PostgresHook

def get_data_from_db():
    hook = PostgresHook(postgres_conn_id='my_postgres_connection')
    # Run a query to fetch data from a table
    records = hook.get_records('SELECT * FROM my_table')
    return records
```

## Most used Hooks

**Database Hooks**
- `PostgresHook` → Used to interact with PostgreSQL databases. Provides methods for executing queries, fetching records, and managing database connections.
- `MySqlHook` → Similar to PostgresHook, but for MySQL databases. Used for executing queries and managing MySQL database connections.
- `SqliteHook` → Used to interact with SQLite databases.
- `MSSQLHook` → Used to interact with Microsoft SQL Server databases.

**Cloud Storage Hooks**
`S3Hook` → Provides an interface for interacting with Amazon S3. Allows you to upload, download, and manage files in S3 buckets.
`GoogleCloudStorageHook` → Used to interact with Google Cloud Storage, providing methods to upload/download files and manage storage resources.

**Cloud Database Hooks**
`BigQueryHook` → Used to interact with Google BigQuery. Provides methods for running SQL queries and managing BigQuery tables.
`CloudSqlHook` → Used to connect to and manage databases in Google Cloud SQL.

**Message Queue/Streaming Hooks**
- `KafkaHook` → Used for interacting with Apache Kafka, typically for sending and receiving messages to/from Kafka topics.
- `RabbitMQHook` → Used to interact with RabbitMQ, a messaging broker that allows you to send and receive messages between systems.

**File System Hooks**
- `FTPHook` → Allows you to interact with FTP servers, enabling file uploads, downloads, and directory management.
- `SFTPHook` → Used for interacting with SFTP servers to upload and download files over secure FTP.
- `FileSensor` → Not exactly a hook itself but an operator that often uses hooks like SFTPHook to check if a file exists in a remote location.

## Difference between Hook & Operator

- `Hooks` → **Are low-level abstractions that simplify interactions with external systems** (databases, cloud services, etc.). They are not responsible for task execution, but for managing connections and executing operations with external systems.
- `Operators` → **Are higher-level abstractions that define tasks in your DAG**. Operators specify what action should be performed (such as executing a function, running a command, or interacting with external services). They can use hooks internally to perform their work.
