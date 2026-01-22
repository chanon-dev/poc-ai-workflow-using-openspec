FROM apache/airflow:3.1.6

USER root

# Install Oracle Instant Client dependencies and OpenJDK (for Data Loader)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libaio1 \
    openjdk-17-jre-headless \
    && rm -rf /var/lib/apt/lists/*

# Create Oracle directory
RUN mkdir -p /opt/oracle

# Copy Oracle Instant Client based on architecture
# Supports both x86_64 (amd64) and ARM64 (aarch64)
COPY files/instantclient-basic-linux-x64/instantclient_19_29 /opt/oracle/instantclient-x64
COPY files/instantclient-basic-linux-arm64/instantclient_19_29 /opt/oracle/instantclient-arm64

# Detect architecture and create symlink to appropriate client
RUN ARCH=$(uname -m) && \
    if [ "$ARCH" = "x86_64" ]; then \
    ln -sf /opt/oracle/instantclient-x64 /opt/oracle/instantclient; \
    elif [ "$ARCH" = "aarch64" ]; then \
    ln -sf /opt/oracle/instantclient-arm64 /opt/oracle/instantclient; \
    else \
    echo "Unsupported architecture: $ARCH" && exit 1; \
    fi && \
    echo "Oracle Instant Client configured for $ARCH"

# Set Oracle environment variables
ENV LD_LIBRARY_PATH=/opt/oracle/instantclient
ENV ORACLE_HOME=/opt/oracle/instantclient

# Salesforce Data Loader Setup
# Copy the installer/jar directory
COPY files/dataloader_v64 /opt/dataloader

# Create a process.sh wrapper script to mimic the official CLI behavior
# Usage: process.sh <config_dir> <process_name>
RUN echo '#!/bin/bash' > /opt/dataloader/process.sh && \
    echo 'if [ "$#" -ne 2 ]; then' >> /opt/dataloader/process.sh && \
    echo '    echo "Usage: $0 <config_dir> <process_name>"' >> /opt/dataloader/process.sh && \
    echo '    exit 1' >> /opt/dataloader/process.sh && \
    echo 'fi' >> /opt/dataloader/process.sh && \
    echo 'java --enable-native-access=ALL-UNNAMED -cp /opt/dataloader/dataloader-64.1.0.jar com.salesforce.dataloader.process.DataLoaderRunner run.mode=batch salesforce.config.dir="$1" process.name="$2"' >> /opt/dataloader/process.sh && \
    chmod +x /opt/dataloader/process.sh

USER airflow
ENV PATH="/home/airflow/.local/bin:${PATH}"
COPY requirements.txt /requirements.txt
RUN pip install --no-cache-dir -r /requirements.txt
