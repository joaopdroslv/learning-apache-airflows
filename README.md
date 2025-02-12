# Learning Apache Airflows

Welcome to my Apache Airflows repository!

🚀 This repository is dedicated to learning and experimenting with Apache Airflows.

`⚠️ IMPORTANT`: This repository is still in progress.

## Setup

Start all dockerized services with:
```bash
docker-compose up --build
```

This will start:
- `Apache Airflow Webservice`
- `Apache Airflow Scheduler`
- `Apache Airflow Worker`
- `Redis` used by Apache Airflow
- `Postgre db` used by the Apache Airflow
- `Postgre volume`
- `MySQL` used by some DAGs

## Environment Configuration

The `docker-compose.yml` file sets up the following services:
- **PostgreSQL** (`postgres`): This is the database used by Apache Airflow.
- **MySQL** (`mysql`): Used by some of the DAGs for database operations.
- **Redis** (`redis`): Used as a broker for Celery in Apache Airflow.
- **Apache Airflow Webserver** (`airflow-webserver`): Serves the Airflow UI.
- **Apache Airflow Scheduler** (`airflow-scheduler`): Responsible for scheduling tasks in the DAGs.
- **Apache Airflow Worker** (`airflow-worker`): Executes tasks in the DAGs.
