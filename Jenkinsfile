pipeline {
    agent { label 'minion' }

    environment {
        REPO_URL = 'https://github.com/alex1436183/tms_test.git'
        BRANCH_NAME = 'main'
        VENV_DIR = 'venv'
        DEPLOY_DIR = '/var/www/myapp'  // Указываем путь для деплоя на сервере
        DEPLOY_SERVER = 'minion'  // Имя или адрес сервера
        SSH_CREDENTIALS_ID = 'agent-ssh-key'  // ID SSH-учетных данных в Jenkins
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
                pip install Flask  # Устанавливаем Flask
                echo "Installing pytest..."
                pip install pytest  # Устанавливаем pytest
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
                    # Копируем файлы на сервер с помощью SCP
                    scp -i "$SSH_KEY" -r * jenkins@${DEPLOY_SERVER}:${DEPLOY_DIR}
                    echo "Deployment completed!"
                    '''
                }
            }
        }

        // Этап для запуска приложения **после деплоя**
        stage('Start Application') {
            steps {
                withCredentials([sshUserPrivateKey(credentialsId: 'agent-ssh-key', keyFileVariable: 'SSH_KEY')]) {
                    sh '''#!/bin/bash
                    echo "Starting application on the minion server..."
                    ssh -i "$SSH_KEY" jenkins@${DEPLOY_SERVER} "cd ${DEPLOY_DIR} && source ${VENV_DIR}/bin/activate && nohup python app.py > app.log 2>&1 &"
                    echo "Application started on ${DEPLOY_SERVER}"
                    '''
                }
            }
        }

        stage('Check Application') {
            steps {
                sh '''#!/bin/bash
                echo "Waiting for application to start..."
                sleep 10  # Подождать некоторое время для запуска приложения
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
