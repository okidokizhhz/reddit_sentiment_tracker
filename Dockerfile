# official Python runtime as base image
FROM python:3.11-slim

# setting work directory in container
WORKDIR /app

# installing system dependencies required for PostgreSQL and build tools
# psycopg2 requires libpq-dev, build-essential for compiling Python packages
RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# copying requirements first to leverage Docker cache
# 	= when requirements don't change, Docker will use cached layers
COPY requirements.txt .

# installing Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy project code to container
COPY . .

# exposing port 8000 for FastAPI application
EXPOSE 8000

# Command to run the application / FastAPI Server
# --host 0.0.0.0 makes the server accessible from outside the container
CMD sh -c "alembic upgrade head && uvicorn server:app --host 0.0.0.0 --port 8000"
