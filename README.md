![Lint-free](https://github.com/nyu-software-engineering/containerized-app-exercise/actions/workflows/lint.yml/badge.svg)

# Containerized App Exercise

Build a containerized app that uses machine learning. See [instructions](./instructions.md) for details.

## Product Vision

> A containarized chatbot that processes audio input from seniors and translate them into helpful instructions related to tech issues

## Team members

- [Kazi Hossain](https://github.com/kazisean)
- [Vaishnavi Suresh](https://github.com/vaishnavi-suresh)
- [sw5556](https://github.com/sw5556)
- [Iced-T](https://github.com/TawhidZGit)
- [Amy Liu](https://github.com/Amyliu2003)

## Task Board

[As projects here](https://github.com/orgs/swe-students-fall2025/projects/96/views/1)

## Configuration

**Prerequisites:** 

- [Docker](https://www.docker.com/products/docker-desktop/)
- [Docker Compose](https://docs.docker.com/compose/)

**Environment Variables:** Download .env file sent in the group discord.
**Running the Application:** From the project root directory, run `docker-compose up --build` to build and start all containers.

**Database Setup:** MongoDB is automatically configured in docker-compose.yml with username `root`, password `example`, and a persistent volume for data storage. No additional setup is required as the database initializes automatically on first run.

**Stopping the Application:** Run `docker-compose down` to stop all containers.