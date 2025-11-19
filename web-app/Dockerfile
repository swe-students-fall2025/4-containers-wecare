# Use Python 3.11 slim image
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
    transformers \
    torch

# Copy application code (entire repo, since build context is ..)
COPY . .

# Expose port
EXPOSE 5050

# No need to set FLASK_APP here since we're using python directly
ENV PYTHONUNBUFFERED=1

# Default command (will be overridden by docker-compose)
CMD ["python", "web-app/app.py"]
