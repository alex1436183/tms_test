pipeline {
    agent { label 'minion' }

    environment {
        REPO_URL = 'https://github.com/alex1436183/tms_test.git'  // URL репозитория
        BRANCH_NAME = 'main'  // Ветка репозитория
        VENV_DIR = 'venv'  // Путь к виртуальному окружению
        DEPLOY_DIR = '/var/www/myapp'  // Путь для деплоя
        DEPLOY_SERVER = 'minion'  // Имя или адрес сервера
        SSH_CREDENTIALS_ID = 'agent-ssh-key'  // ID SSH-учетных данных в Jenkins
    }

    stages {
        stage('Clone repository') {
            steps {
                cleanWs()  // Очищаем рабочее пространство
                echo "Cloning repository from ${REPO_URL}"
                git branch: "${BRANCH_NAME}", url: "${REPO_URL}"  // Клонируем репозиторий
            }
        }

        stage('Setup Python Environment') {
            steps {
                sh '''#!/bin/bash
                echo "Setting up Python virtual environment..."
                python3 -m venv ${VENV_DIR}  # Создаём виртуальное окружение
                source ${VENV_DIR}/bin/activate  # Активируем виртуальное окружение
                python3 --version  # Проверяем версию Python
                pip install --upgrade pip  # Обновляем pip
                echo "Installing dependencies..."
                pip install -r requirements.txt  # Устанавливаем зависимости
                echo "Python environment setup completed!"
                '''
            }
        }

        stage('Run Tests') {
            steps {
                sh '''#!/bin/bash
                echo "Running tests..."
                source ${VENV_DIR}/bin/activate  # Активируем виртуальное окружение
                pytest tests/ --maxfail=1 --disable-warnings || echo "Tests failed!"  # Запускаем тесты
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

        stage('Check Application') {
            steps {
                sh '''#!/bin/bash
                echo "Waiting for application to start..."
                sleep 10  # Ждем некоторое время для старта приложения
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
            # Убираем виртуальное окружение
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
