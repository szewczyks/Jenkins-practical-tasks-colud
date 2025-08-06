pipeline {
    agent any

    options {
        skipDefaultCheckout(true)
        timestamps()
        ansiColor('xterm')
    }

    environment {
        DOCKER_IMAGE = 'flask-ci-cd'
        TAG          = "${env.BRANCH_NAME == 'main' ? 'latest' : env.BRANCH_NAME}"
        CONTAINER    = 'flask-app'
        APP_PORT     = '5000'
    }

    stages {

        stage('Checkout') {
            steps {
                cleanWs()
                checkout scm
            }
        }

        stage('Tests') {
            agent {
                docker {
                    image 'python:3.11'
                    args  '-u root:root'
                    reuseNode true
                }
            }
            steps {
                sh '''
                  python -m venv venv
                  ./venv/bin/pip install -U pip
                  ./venv/bin/pip install -r requirements.txt pytest
                  ./venv/bin/pytest -q
                '''
            }
        }

        stage('Build Image') {
            steps {
                sh "docker build -t ${DOCKER_IMAGE}:${TAG} -f docker/Dockerfile ."
            }
        }

        stage('Deploy on EC2') {
            when { branch 'main' }
            steps {
                sh """
                  # zatrzymaj poprzedni kontener (jeśli jest)
                  docker rm -f ${CONTAINER} 2>/dev/null || true

                  # użyj compose, żeby zachować mapowanie portów i zmienne
                  docker compose -f docker/docker-compose.yml \
                    up -d --no-deps --force-recreate
                """
            }
        }
        stage('Health Check (public)') {
            when { branch 'main' }
            steps {
                // pobierz publiczne IP (metadane EC2) i zapisz do env
                script {
                    env.PUBLIC_IP = sh(
                        script: "curl -s http://169.254.169.254/latest/meta-data/public-ipv4",
                        returnStdout: true
                    ).trim()
                }

                // próbuj do skutku: 6 × co 10 s
                retry(6) {
                    sleep 10
                    sh """
                    echo ">>> Checking http://${PUBLIC_IP}:5000/ ..."
                    curl --fail --silent --show-error http://${PUBLIC_IP}:5000/ >/dev/null
                    """
                }
                echo "✅  Public endpoint http://${PUBLIC_IP}:5000/ is up"
            }
        }
    }

    post { always { cleanWs() } }
}
