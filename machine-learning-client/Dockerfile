FROM python:3.10-slim

WORKDIR /app
# Install pipenv
RUN pip install pipenv
COPY Pipfile Pipfile.lock ./
RUN pipenv install
RUN pipenv install flask flask-cors python-dotenv openai pymongo requests

# application code
COPY . .

EXPOSE 5050

# Run the Flask application
CMD ["pipenv", "run", "python", "app.py"]