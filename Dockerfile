FROM apache/airflow:3.1.6

USER root
# Install Oracle Instant Client dependencies if needed (libaio1)
RUN apt-get update && apt-get install -y libaio1

USER airflow
ENV PATH="/home/airflow/.local/bin:${PATH}"
COPY requirements.txt /requirements.txt
RUN pip install --no-cache-dir -r /requirements.txt
