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
                  docker rm -f ${CONTAINER} 2>/dev/null || true
                  docker compose -f docker/docker-compose.yml \
                    up -d --no-deps --force-recreate
                """
            }
        }
        stage('Health Check') {
            when { branch 'main' }
            steps {
                retry(6) {
                    sleep 10
                    sh '''
                    echo ">>> Checking http://localhost:5000/ ..."
                    curl --fail --silent http://localhost:5000/ > /dev/null
                    '''
                }
                echo '✅  Flask works on port 5000'
            }
        }
    }

    post { always { cleanWs() } }
}
