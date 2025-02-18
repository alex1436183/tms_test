pipeline {
    agent { label 'minion' }

    environment {
        REPO_URL = 'https://github.com/alex1436183/tms_test.git'
        BRANCH_NAME = 'main'
        VENV_DIR = '/var/www/myapp/venv'  // Абсолютный путь к виртуальному окружению
        DEPLOY_DIR = '/var/www/myapp'  // Директория деплоя
        DEPLOY_SERVER = 'minion'  // Сервер деплоя
        SSH_CREDENTIALS_ID = 'agent-ssh-key'  // Jenkins SSH Credentials
    }

    stages {
        stage('Clone Repository') {
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
                pip install --upgrade pip
                pip install -r requirements.txt  # Устанавливаем зависимости из файла
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
                withCredentials([sshUserPrivateKey(credentialsId: SSH_CREDENTIALS_ID, keyFileVariable: 'SSH_KEY')]) {
                    sh '''#!/bin/bash
                    echo "Creating deployment directory on the server..."
                    ssh -i "$SSH_KEY" jenkins@${DEPLOY_SERVER} "mkdir -p ${DEPLOY_DIR}"
                    echo "Deployment directory created at ${DEPLOY_DIR}"
                    '''
                }
            }
        }

        stage('Deploy') {
            steps {
                withCredentials([sshUserPrivateKey(credentialsId: SSH_CREDENTIALS_ID, keyFileVariable: 'SSH_KEY')]) {
                    sh '''#!/bin/bash
                    echo "Deploying project files to ${DEPLOY_SERVER}..."
                    rsync -avz --exclude 'venv' --exclude '__pycache__' -e "ssh -i $SSH_KEY" . jenkins@${DEPLOY_SERVER}:${DEPLOY_DIR}/
                    echo "Deployment completed!"
                    '''
                }
            }
        }

        stage('Start Application') {
            steps {
                withCredentials([sshUserPrivateKey(credentialsId: SSH_CREDENTIALS_ID, keyFileVariable: 'SSH_KEY')]) {
                    sh '''#!/bin/bash
                    echo "Running the Python script to start the application on the server..."
                    ssh -i "$SSH_KEY" jenkins@${DEPLOY_SERVER} "bash -c '
                        export DEPLOY_DIR=${DEPLOY_DIR}
                        export VENV_DIR=${VENV_DIR}
                        cd ${DEPLOY_DIR}
                        source ${VENV_DIR}/bin/activate
                        nohup python3 ${DEPLOY_DIR}/start_app.py > ${DEPLOY_DIR}/app.log 2>&1 &
                        echo $! > ${DEPLOY_DIR}/app.pid
                        echo "Application started with PID $(cat ${DEPLOY_DIR}/app.pid)"
                    '"
                    '''
                }
            }
        }

        stage('Check Application') {
            steps {
                sh '''#!/bin/bash
                echo "Waiting for application to start..."
                sleep 5
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
            echo "Cleanup complete!"
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
