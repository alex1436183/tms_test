pipeline {
    agent { label 'minion' }

    environment {
        REPO_URL = 'https://github.com/alex1436183/tms_test.git'
        BRANCH_NAME = 'main'
        VENV_DIR = 'venv'
        DEPLOY_SERVER = 'your.server.address'  // Укажи свой сервер
        DEPLOY_DIR = '/var/www/myapp'  // Установлен путь к директории деплоя
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

        stage('Deploy to Server') {
            steps {
                withCredentials([sshUserPrivateKey(credentialsId: 'agent-ssh-key', keyFileVariable: 'SSH_KEY')]) {
                    sh '''#!/bin/bash
                    echo "Deploying project files to ${DEPLOY_SERVER}..."
                    ssh -i "$SSH_KEY" jenkins@${DEPLOY_SERVER} "mkdir -p ${DEPLOY_DIR}"
                    rsync -avz -e "ssh -i $SSH_KEY" . jenkins@${DEPLOY_SERVER}:${DEPLOY_DIR}/
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
                    ssh -i "$SSH_KEY" jenkins@${DEPLOY_SERVER} "bash -c '
                        export DEPLOY_DIR=${DEPLOY_DIR} && 
                        export VENV_DIR=${VENV_DIR} && 
                        cd ${DEPLOY_DIR} && 
                        nohup python3 start_app.py > ${DEPLOY_DIR}/app.log 2>&1 & echo $! > ${DEPLOY_DIR}/app.pid
                        echo "Application started with PID $(cat ${DEPLOY_DIR}/app.pid)" '"
                    '''
                }
            }
        }
    }

    post {
        always {
            sh '''#!/bin/bash
            echo "Cleaning up..."
            if [ -f app.pid ]; then
                echo "Stopping application (PID: $(cat app.pid))"
                kill $(cat app.pid) || true
                rm -f app.pid
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
