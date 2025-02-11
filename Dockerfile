FROM apache/airflow:2.7.3

USER root

# Atualiza pacotes e instala o Git
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    && rm -rf /var/lib/apt/lists/*

USER airflow
WORKDIR /opt/airflow

# Copia apenas o arquivo de requisitos primeiro (para cache eficiente)
COPY requirements.txt requirements.txt

# Instala os pacotes do Airflow
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo o conteúdo depois (para evitar rebuilds desnecessários)
COPY . /opt/airflow/
