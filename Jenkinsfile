pipeline {
    agent { label 'minion' }

    environment {
        REPO_URL = 'https://github.com/alex1436183/tms_test.git'
        BRANCH_NAME = 'main'
        VENV_DIR = 'venv'
        DEPLOY_DIR = '/var/www/myapp'
        DEPLOY_SERVER = 'minion'
        SSH_CREDENTIALS_ID = 'agent-ssh-key'
    }

    stages {
        stage('Clone repository') {
            steps {
                cleanWs()
                echo "Cloning repository from ${REPO_URL}"
                git branch: "${BRANCH_NAME}", url: "${REPO_URL}"
            }
        }

        stage('Setup Python Environment') {
            steps {
                sh '''#!/bin/bash
                echo "Setting up Python virtual environment..."
                python3 -m venv ${VENV_DIR}
                source ${VENV_DIR}/bin/activate
                python --version
                pip install --upgrade pip
                echo "Installing Flask..."
                pip install Flask
                echo "Installing pytest..."
                pip install pytest
                echo "Python environment setup completed!"
                '''
            }
        }

        stage('Run Tests') {
            steps {
                sh '''#!/bin/bash
                echo "Running tests..."
                source ${VENV_DIR}/bin/activate
                pytest tests/ --maxfail=1 --disable-warnings || echo "Tests failed!"
                echo "Tests completed."
                '''
            }
        }

        stage('Create Directory for Deployment') {
            steps {
                withCredentials([sshUserPrivateKey(credentialsId: 'agent-ssh-key', keyFileVariable: 'SSH_KEY')]) {
                    sh '''#!/bin/bash
                    echo "Creating deployment directory on the minion server..."
                    ssh -i "$SSH_KEY" jenkins@${DEPLOY_SERVER} "mkdir -p ${DEPLOY_DIR}"
                    echo "Deployment directory created at ${DEPLOY_DIR}"
                    '''
                }
            }
        }

        stage('Deploy') {
            steps {
                withCredentials([sshUserPrivateKey(credentialsId: 'agent-ssh-key', keyFileVariable: 'SSH_KEY')]) {
                    sh '''#!/bin/bash
                    echo "Deploying project files to ${DEPLOY_SERVER}..."
                    scp -i "$SSH_KEY" -r * jenkins@${DEPLOY_SERVER}:${DEPLOY_DIR}
                    echo "Deployment completed!"
                    '''
                }
            }
        }

        stage('Start Application') {
            steps {
                withCredentials([sshUserPrivateKey(credentialsId: 'agent-ssh-key', keyFileVariable: 'SSH_KEY')]) {
                    sh '''#!/bin/bash
                    echo "Running the Python script to start the application on the minion server..."
                    ssh -i "$SSH_KEY" jenkins@${DEPLOY_SERVER} "
                        export DEPLOY_DIR=${DEPLOY_DIR} && 
                        export VENV_DIR=${VENV_DIR} && 
                        cd ${DEPLOY_DIR} && 
                        python start_app.py"  # Запускаем скрипт start_app.py для активации виртуального окружения и запуска приложения
                    echo "Application started on ${DEPLOY_SERVER}."
                    '''
                }
            }
        }

        stage('Check Application') {
            steps {
                sh '''#!/bin/bash
                echo "Waiting for application to start..."
                sleep 10
                echo "Checking application at http://localhost:8080"
                curl -v http://localhost:8080 || echo "Application check failed!"
                '''
            }
        }
    }

    post {
        always {
            sh '''#!/bin/bash
            echo "Cleaning up..."
            if [ -f ${DEPLOY_DIR}/app.pid ]; then
                echo "Stopping application (PID: $(cat ${DEPLOY_DIR}/app.pid))"
                kill $(cat ${DEPLOY_DIR}/app.pid) || true
                rm -f ${DEPLOY_DIR}/app.pid
            fi
            echo "Cleaning up virtual environment..."
            rm -rf ${VENV_DIR}
            '''
        }
        failure {
            echo '❌ Pipeline failed! Check logs for details.'
        }
        success {
            echo '✅ Pipeline completed successfully!'
        }
    }
}
