FROM python:3.10-bullseye

ENV DEBIAN_FRONTEND=noninteractive
WORKDIR /work

# System deps for building CityFlow
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    git \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip tooling
RUN python -m pip install --upgrade pip setuptools wheel

# TensorFlow (includes MultiHeadAttention)
# 2.13.1 supports Python 3.10 and has tf.keras.layers.MultiHeadAttention
RUN pip install --no-cache-dir tensorflow==2.13.1

# CityFlow build from source
RUN git clone https://github.com/cityflow-project/CityFlow.git /opt/CityFlow
WORKDIR /opt/CityFlow
RUN pip install --no-cache-dir .

# Back to workspace
WORKDIR /work
