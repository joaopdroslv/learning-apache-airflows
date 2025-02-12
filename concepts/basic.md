# Apache Airflow, DAGs (Directed Acyclic Graphs)

São a estrutura fundamental para orquestrar tarefas de forma organizada e controlada. Elas representam um **fluxo de trabalho (workflow)** como um grafo direcionado e acíclico, onde **cada nó é uma task (tarefa)** e as **arestas representam dependências entre elas**.

## 🚀 Conceitos Principais

1. **DAG (Direct Acyclic Graph)**
    - Define a sequência e a dependência entre tarefas.
    - Não pode contner ciclos (loops), pois isso causaria exceções infinitas.
    - Especificada via código Python.

2. **Tasks (Tarefas)**
    - São as unidades de trabalho dentro da DAG
    - Cada tarefa executa uma ação específica, como rodar script Python,
    chama uma API, ou interagir com um banco de dados.
    - Podem ser de diferentes tipo (Operators).

3. **Operators (Operadores)**
    - São modelos pré-definidos de tarefas no **Airflow**.
    - Exemplos:
        - `PythonOperator` → Executa uma função Python.
        - `BashOperator` → Executa comandos no shell.
        - `PostgresOperator` → Executa queries em um banco de dados PostgreSQL

4. **Scheduler (Agendador)**
    - Responsável por disparar a execução das DAGs conforme o cronograma definido.
    - Trabalha em conjunto com o *Executor* para distribuir a carga de trabalho.

5. **Executor**
    - Gerencia a execução das tarefas.
    - Tipos comuns:
        - `SequentialExecutor` → Execução serial, uma task por vez.
        - `LocalExecutor` → Execução paralela em uma única máquina.
        - `CeleryExecutor` → Distribui tarefas em vários workers.
        - `KubernetesExecutor` → Cria pods dinâmicos para execução.

## 🛠️ Criando uma DAG no Airflow

Uma DAG é um script Python que define um fluxo de trabalho. Exemplo básico:

```python
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

# Função que será executada na DAG
def hello_world():
    print("Hello, Apache Airflow!")

# Definição da DAG
with DAG(
    dag_id="hello_world_dag",
    start_date=datetime(2024, 1, 1),
    schedule_interval="@daily",  # Executa diariamente
    catchup=False,
) as dag:
    
    task1 = PythonOperator(
        task_id="print_hello",
        python_callable=hello_world,  # Função a ser executada
    )

# Definição do fluxo
task1  # DAG com apenas uma tarefa
```

## 🔗 Definição de Dependências

As tarefas podem depender umas das outras, formando um fluxo de execução:

```python
task1 >> task2  # task2 depende de task1 (task1 -> task2)
task2 << task3  # task3 executa antes de task2 (task3 -> task2)
task3 >> [task4, task5]  # task4 e task5 só executam após task3
```

## 📊 Monitoramento

O Apache Airflow possui uma UI web onde podemos:
- Ver DAGs ativas e suas execuções.
- Monitorar logs de tarefas.
- Modificar e pausar DAGs conforme necessário.

Para iniciar a UI:

```sh
airflow webserver --port 8080
```

E para iniciar o scheduler:

```sh
airflow scheduler
```
