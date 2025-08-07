# Flask CI/CD Demo

A minimal Flask API with tests, Docker packaging, and Jenkins CI/CD pipeline. 
This project serves as a **self-contained playground** to demonstrate:

* how to package a Python service into a Docker image  
* how to run it locally with `docker-compose`  
* how to build / test / deploy the image from a Jenkins pipeline

## 1 Running the App in Docker

> **Prerequisite:** Docker (Compose v1 or v2).
From the root directory of the project:
```bash
# Build the Docker image
docker build -t flask-ci-cd:latest -f docker/Dockerfile .

# Start the container with Compose
docker compose -f docker/docker-compose.yml up --build -d
```
#### Verifying the App is Running
You can use the following methods to verify that the app is up and healthy:
1. Check container health status:
    ```bash
    docker inspect -f '{{.State.Health.Status}}' flask-app
    # Output should be: healthy
    ```
2. Test API endpoints with curl:
    ```bash
    curl http://localhost:5000/
    # → {"message":"Hello from Flask"}

    curl http://localhost:5000/health
    # → {"status":"healthy"}

    curl http://localhost:5000/random
    # → {"random_number": 42}
    ```
Or open in browser:
- http://localhost:5000
- http://localhost:5000/health
- http://localhost:5000/random

Stop & remove:
```bash
docker compose -f docker/docker-compose.yml down
```

## 2 Running the tests locally
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt pytest
pytest -q
```

## 3 Jenkins pipeline
| Stage                    | What happens                                                                                      |
| ------------------------ |-------------------------------------------------------------------------------------------------- |
| **Source Code Checkout** | cleans workspace, checks out repo, stashes it (`workspace-src`). |
| **Run Tests**            | spins a throw-away `python:3.11` container, installs deps in a venv, runs pytest. |
| **Build Docker Image**   | `docker build -t flask-ci-cd:<branch>`.<br>`main` → tag `latest`|
| **Deploy (Local)**       | *tylko* dla `main`: `docker-compose down && docker-compose up -d --build` inside `docker/`. |
| **post / always**        | `cleanWs()` – keeps the Jenkins workspace tiny. |
