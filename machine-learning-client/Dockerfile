FROM python:3.10-slim

WORKDIR /app
# Install pipenv
RUN pip install pipenv
COPY Pipfile Pipfile.lock ./
RUN pipenv install

# application code
COPY . .

EXPOSE 5050

# Run the application
CMD ["pipenv", "run", "python", "app.py"]