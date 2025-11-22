![Lint-free](https://github.com/nyu-software-engineering/containerized-app-exercise/actions/workflows/lint.yml/badge.svg)

# Containerized App Exercise

Build a containerized app that uses machine learning. See [instructions](./instructions.md) for details.

## Product Vision

> A containarized chatbot that processes audio input from seniors and translate them into helpful instructions related to tech issues


## Team members

- [Kazi Hossain](https://github.com/kazisean)
- [Vaishnavi Suresh](https://github.com/vaishnavi-suresh)
- [Susan Wang](https://github.com/sw5556)
- [Tawhid Zaman](https://github.com/TawhidZGit)
- [Amy Liu](https://github.com/Amyliu2003)

## Task Board

[As projects here](https://github.com/orgs/swe-students-fall2025/projects/96/views/1)

## Configuration

**Prerequisites:** 

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) (version 20.10 or later)
- [Docker Compose](https://docs.docker.com/compose/) (usually included with Docker Desktop)
- OpenAI API Key from [https://platform.openai.com/api-keys](https://platform.openai.com/api-keys)


### Environment Variables Setup

Create a `.env` file in the **root directory** of the project (same level as `docker-compose.yml`) with the following variables:

# OpenAI API Configuration (REQUIRED)
OPENAI_API_KEY=sk-your-openai-api-key-here

# AI Model Configuration (REQUIRED)
MODEL_NAME=gpt-3.5-turbo

# MongoDB Configuration (REQUIRED)
MONGO_URI=mongodb://root:example@mongodb:27017/
MONGO_DB=wecare_db

# MongoDB Initialization (OPTIONAL - matches docker-compose.yml defaults)
MONGO_INITDB_ROOT_USERNAME=root
MONGO_INITDB_ROOT_PASSWORD=example**Important Notes:**
- Never commit the `.env` file to version control
- The `.env` file must be in the root directory
- Replace `sk-your-openai-api-key-here` with your actual OpenAI API key
- The `MONGO_URI` uses `mongodb` as the hostname (Docker service name, not `localhost`)

See .env.example file.

MongoDB is automatically configured and initialized when containers start. The database:
- Uses credentials: username `root`, password `example`
- Stores data in a persistent Docker volume
- Creates the database specified in `MONGO_DB` environment variable automatically
- Requires no manual setup or data import

## Running the Application

1. **Ensure Docker Desktop is running**

2. **Navigate to the project root directory**

3. **Verify `.env` file exists** with all required variables (see Configuration section above)

4. **Build and start all containers:**
 
   docker-compose up --build
   5. **Access the application:**
   - Web interface: `http://localhost:5050`
   - MongoDB: `localhost:27017`

## Running the Application

1. **Ensure Docker Desktop is running**

2. **Navigate to the project root directory**

3. **Verify `.env` file exists** with all required variables (see Configuration section above)

4. **Build and start all containers:**
 
   docker-compose up --build
   5. **Access the application:**
   - Web interface: `http://localhost:5050`
   - MongoDB: `localhost:27017`

### Running in Background

To run containers in detached mode:h
docker-compose up -d --buildView logs:
docker-compose logs -f### Stopping the Application

Stop all containers:
docker-compose downTo also remove database volume (deletes all data):
docker-compose down -v## License

**Stopping the Application:** Run `docker-compose down` to stop all containers.
