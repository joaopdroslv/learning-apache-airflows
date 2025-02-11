# Operators Categories

Apache Airflow provides various types of operators, which define tasks within a workflow. These operators can be categorized based on their functionality. Below are the main categories and their respective operators:

`IMPORTANT`: Not all operators are included on the default installation.

## 1. Action
Action operators are responsible for executing specific actions, such as running scripts, sending emails, or interacting with external systems.

- `BashOperator` – Executes Bash commands or scripts.
- `PythonOperator` – Runs Python functions as tasks.
- `EmailOperator` – Sends emails as part of the workflow.
- `SnowflakeOperator` – Executes SQL queries in Snowflake.
- `KubernetesPodOperator` – Runs tasks inside Kubernetes pods.
- `GitHubOperator` – Interacts with GitHub repositories (e.g., fetching data, creating issues, or triggering workflows).

## 2. Transfer
Transfer operators are used to move data between different storage systems, databases, or services.

- `S3ToRedshiftOperator` – Transfers data from Amazon S3 to Amazon Redshift.
- `LocalFilesystemToGCSOperator` – Uploads files from the local filesystem to Google Cloud Storage (GCS).
- `S3ToGCSOperator` – Moves data from Amazon S3 to Google Cloud Storage.
- `S3ToSnowflakeOperator` – Loads data from Amazon S3 into Snowflake.
- `SFTPToWasbOperator` – Transfers data from an SFTP server to Azure Blob Storage (Wasb).
- `MySqlToHiveOperator` – Moves data from MySQL to Apache Hive.

## 3. Sesor
Sensor operators are used to wait for a specific condition to be met before proceeding to the next task. They continuously monitor external systems, files, or database states.

- `S3KeySensor` – Waits for a specific file (key) to appear in an Amazon S3 bucket.
- `RedshiftClusterSensor` – Monitors the availability status of an Amazon Redshift cluster.
- `ExternalTaskSensor` – Waits for a task in a different DAG to complete.
- `HttpSensorAsync` – Checks for an HTTP response asynchronously.
- `SqlSensor` – Polls a database until a specific query condition is met.
- `RedisPubSubSensor` – Listens for messages on a Redis Pub/Sub channel.
