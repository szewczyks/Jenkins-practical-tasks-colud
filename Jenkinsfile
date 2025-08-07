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
                    // czekamy maks. 90 s aż Docker oznaczy kontener jako healthy
                    def limit = 60
                    def ok = sh(
                        script: """
                        for i in \$(seq 1 ${limit}); do
                            status=\$(docker inspect -f '{{.State.Health.Status}}' flask-app 2>/dev/null || echo starting)
                            [ "\$status" = "healthy" ] && exit 0
                            sleep 1
                        done
                        exit 1
                        """,
                        returnStatus: true
                    ) == 0

                    if (!ok) {
                        echo 'Kontener nie osiągnął stanu healthy — ostatnie logi:'
                        sh 'docker logs --tail=50 flask-app || true'
                        error 'Health-check failed'
                    } else {
                        echo 'Kontener healthy — aplikacja działa'
                    }
                }
            }
        }
    }

    post { always { cleanWs() } }
}
