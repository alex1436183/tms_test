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

                # Активируем виртуальное окружение
                source ${VENV_DIR}/bin/activate

                # Добавляем корневую директорию в PYTHONPATH, чтобы корректно работали импорты
                export PYTHONPATH=$PYTHONPATH:$PWD

                # Проверим, что pytest установлен
                echo "Checking installed packages..."
                pip freeze

                # Запускаем тесты
                pytest tests/ --maxfail=1 --disable-warnings || { echo "Tests failed!"; exit 1; }

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
          
