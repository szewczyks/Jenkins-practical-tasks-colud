// pipeline {
//     agent any

//     options {
//         skipDefaultCheckout(true)       // blocks default Source Control Management checkout
//         timestamps()                    // add timestamps to console output
//         ansiColor('xterm')              // colorize console output
//     }

//     environment {
//         DOCKER_IMAGE = 'flask-ci-cd'
//     }

//     stages {

//         stage('Source Code Checkout') {
//             steps {
//                 cleanWs()               // clean workspace before checkout
//                 checkout scm
//                 stash name: 'workspace-src', includes: '**/*'
//             }
//         }

//         stage('Run Tests') {
//             agent {
//                 docker {
//                     image 'python:3.11'
//                     args  '-u root:root'
//                     reuseNode true      // use the same workspace
//                 }
//             }
//             steps {
//                 unstash 'workspace-src'
//                 sh '''
//                     python -m venv venv
//                     ./venv/bin/pip install --upgrade pip
//                     ./venv/bin/pip install -r requirements.txt pytest
//                     ./venv/bin/pytest -q
//                 '''
//             }
//         }

//         stage('Build Docker Image') {
//             steps {
//                 // unstash 'workspace-src'
//                 script {
//                     env.TAG = (env.BRANCH_NAME == 'main') ? 'latest' : env.BRANCH_NAME
//                     sh "docker build -t ${DOCKER_IMAGE}:${TAG} -f docker/Dockerfile ."
//                 }
//             }
//         }

//         stage('Deploy (Local)') {
//             when { branch 'main' }
//             steps {
//                 sh '''
//                     cd docker
//                     docker-compose down || true
//                     docker-compose up -d --build
//                 '''
//             }
//         }
//     }

//     post {
//         always {
//             cleanWs()
//         }
//     }
// }


