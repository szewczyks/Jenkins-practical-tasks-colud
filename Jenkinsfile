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
            post {
                success {
                    script {
                        if (env.BRANCH_NAME != 'main') {
                            sh "docker image rm -f ${DOCKER_IMAGE}:${TAG} || true"
                        }
                    }
                }
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
                script {
                    int attempts   = 2
                    int sleepSec   = 10
                    boolean ok     = false

                    for (int i = 1; i <= attempts; i++) {
                        def status = sh(
                            script: "docker inspect -f '{{.State.Health.Status}}' flask-app 2>/dev/null || echo starting",
                            returnStdout: true
                        ).trim()

                        if (status == 'healthy') {
                            ok = true
                            break
                        }

                        if (i < attempts) { sleep sleepSec }
                    }

                    if (!ok) {
                        echo 'The container did not reach a healthy state — latest logs:'
                        sh  'docker logs --tail=50 flask-app || true'
                        error 'Health-check failed'
                    } else {
                        echo 'Container healthy — Application is running!'
                    }
                }

            }
        }
    }

    post { always { cleanWs() } }
}
