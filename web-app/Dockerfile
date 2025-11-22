FROM python:3.11-slim

# Set working directory
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
    requests \
    openai
    

# Copy application code
COPY . .

# Expose port
EXPOSE 5050


# Default command (will be overridden by docker-compose) for now
CMD ["python", "web-app/app.py"]
