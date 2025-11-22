FROM python:3.11-slim

# set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies directly
RUN pip install --no-cache-dir \
    flask \
    flask-cors \
    pymongo \
    python-dotenv \
    requests
    

# Copy application code
COPY . .

# open port
EXPOSE 5050

# Default command
CMD ["python", "app.py"]