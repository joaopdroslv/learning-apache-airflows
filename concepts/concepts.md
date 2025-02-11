# 🔍 **O que é o Apache Airflow?**

O **Apache Airflow** é uma plataforma de orquestração de workflows que permite definir, agendar e monitorar fluxos de trabalho. 

Ele foi projetado para tarefas de ETL, pipelines de machine learning, automação de processos de dados e execução de jobs distribuídos.

A ideia principal do Airflow é representar um **fluxo de trabalho como um DAG (Directed Acyclic Graph)**.

# 📌 **Conceitos Fundamentais do Airflow**

## 1️. **DAG (Directed Acyclic Graph)**
Uma **DAG** define um fluxo de trabalho e suas dependências. Ela contém **tarefas (Tasks)**, que são organizadas de forma a não criar ciclos (loops infinitos).

💡 **Por que DAGs e não simplesmente scripts sequenciais?**

- DAGs permitem **orquestração** e não apenas execução linear.
- O Airflow **rastrea estado de execução** e **reexecuta tarefas** conforme necessário.
- A DAG é **declarativa**: você define as tarefas e suas dependências, e o Airflow agenda e executa corretamente.

**Estrutura de uma DAG**
```python
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

def tarefa_exemplo():
    print("Executando minha primeira DAG!")

with DAG(
    dag_id="minha_primeira_dag",
    start_date=datetime(2024, 1, 1),
    schedule_interval="0 12 * * *",  # Executa diariamente ao meio-dia
    catchup=False,
) as dag:
    
    tarefa = PythonOperator(
        task_id="executar_script",
        python_callable=tarefa_exemplo,
    )

tarefa
```

**Analisando a DAG acima**
- `dag_id`: Nome da DAG, usado internamente no Airflow.
- `start_date`: Data de início da DAG. O Airflow não executa DAGs antes desta data.
- `schedule_interval`: Intervalo de execução (formato cron).
- `catchup`: Se False, DAGs atrasadas não são executadas retroativamente.
- `PythonOperator`: Um tipo de tarefa que executa funções Python.

## 2. **Operators & Tasks**

Os **operators** são modelos predefinidos de tarefas. Eles são a base das tarefas executadas dentro das DAGs.

📌 Tipos principais de Operators:
✅ `PythonOperator` → Executa uma função Python.
✅ `BashOperator` → Executa comandos no shell.
✅ `PostgresOperator` → Executa queries SQL em bancos de dados PostgreSQL.
✅ `HttpOperator` → Faz requisições HTTP para APIs externas.
✅ `DummyOperator` → Cria tarefas vazias (úteis para organização).

**Exemplo de DAG com múltiplos operadores:**
```python
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator

def processamento():
    print("Processando dados...")

tarefa1 = BashOperator(
    task_id="criar_arquivo",
    bash_command="echo 'Arquivo criado' > /tmp/arquivo.txt"
)

tarefa2 = PythonOperator(
    task_id="processar_dados",
    python_callable=processamento
)

tarefa1 >> tarefa2  # Definição da ordem de execução
```

🛠️ **Observação:**
Cada tarefa dentro de uma DAG pode **rodar em paralelo**, dependendo da configuração do executor e do agendador.

## 3. **Scheduler & Executor**

O **scheduler** (agendador) verifica quais DAGs precisam ser executadas com base no horário agendado e dispara as tarefas.

O **executor** gerencia a execução das tarefas e pode distribuí-las entre múltiplos workers, dependendo da configuração.

### Tipos de Executors
1. `SequentialExecutor` → Apenas uma tarefa por vez (limitado, mas útil para testes).
2. `LocalExecutor` → Execução paralela em um único servidor.
3. `CeleryExecutor` → Distribui tarefas entre múltiplos workers.
4. `KubernetesExecutor` → Cria pods Kubernetes para execução dinâmica de tarefas.

**💡 Por que usar o CeleryExecutor?**
- Permite **escalar** a execução para múltiplos servidores.
- As tarefas podem ser distribuídas em uma fila de mensagens (**Redis**, **RabbitMQ**).

```ini
[core]
executor = CeleryExecutor

[celery]
broker_url = redis://localhost:6379/0
result_backend = db+postgresql://airflow:password@localhost/airflow
```

## 4. **Definição de Dependências**

O Airflow permite definir dependências entre tarefas para criar workflows sofisticados.

**Exemplo de dependências simples**
```python
task1 >> task2  # task2 só executa após task1
task2 << task3  # task3 deve rodar antes de task2
task3 >> [task4, task5]  # task4 e task5 executam após task3
```

## 5. **Execução e Monitoramento**

**Passos para rodar o Airflow**

1. **Iniciar o banco de dados interno**
```sh
airflow db init
```

2. **Criar um usuário administrador**
```sh
airflow users create --username admin --password admin --role Admin --email admin@example.com
```

3. **Rodar o scheduler (agendador)**
```sh
airflow scheduler
```

4. **Rodar o servidor web**
```sh
airflow webserver --port 8080
```

**Acessar a interface** → http://localhost:8080
