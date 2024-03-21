# FROM tensorflow/tensorflow:2.10.0

# COPY requirements_prod.txt requirements.txt
# RUN pip install -r requirements.txt

# COPY cardano_crystal_ball cardano_crystal_ball
# COPY setup.py setup.py
# RUN pip install .

# COPY Makefile Makefile

# CMD uvicorn cardano_crystal_ball.api.fast:app --host 0.0.0.0 --port $PORT



# Use a lightweight base image for Python
FROM python:3.10.6-slim AS builder

# Install system dependencies
RUN apt-get update && apt-get install -y build-essential

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements_prod.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the source code
COPY cardano_crystal_ball cardano_crystal_ball
COPY setup.py setup.py

# Install the application
RUN pip install --no-cache-dir .

# Start a new stage to create a smaller final image
FROM python:3.10.6-slim

# Set working directory
WORKDIR /app

# Copy only necessary files from the builder stage
COPY --from=builder /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages
COPY --from=builder /app /app

# Copy Makefile
COPY Makefile Makefile

# Set environment variables
ENV PYTHONPATH=/usr/local/lib/python3.10/site-packages

# CMD
CMD uvicorn cardano_crystal_ball.api.fast:app --host 0.0.0.0 --port $PORT
