# Flask CI/CD Demo

Minimal Flask API + pytest suite + Docker + Jenkins.  
Intended as a **self-contained playground** that shows:

* how to package a Python service into a Docker image  
* how to run it locally with `docker-compose`  
* how to build / test / deploy the image from a Jenkins pipeline

## 1 Running locally

> **Prerequisite:** Docker (Compose v1 or v2).

```bash
cd docker
docker-compose up -d
```

Flask API: [http://localhost:5000](http://localhost:5000)
 - `/` → `{"message":"Hello from Flask"}`
 - `/health` → `{"status":"healthy"}`
 - `/random` → `{"random_number": <1-99>}`

Stop & remove:
```bash
docker-compose down
```

## 2 Running the tests
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
