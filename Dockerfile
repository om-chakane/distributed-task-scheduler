# Use official Python slim image as base
FROM python:3.11-slim

# Set working directory inside the container
WORKDIR /app

# Copy requirements first (so Docker caches this layer)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the project into the container
COPY . .

# Default command — can be overridden in docker-compose
CMD ["python", "-m", "worker.worker", "worker-1"]