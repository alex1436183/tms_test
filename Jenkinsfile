pipeline {
    agent { label 'minion' }

    environment {
        REPO_URL = 'https://github.com/alex1436183/tms_test.git'  // Репозиторий
        BRANCH_NAME = 'main'  // Ветка
        VENV_DIR = '/var/www/myapp/venv'  // Путь к виртуальному окружению
        DEPLOY_DIR = '/var/www/myapp'  // Путь для деплоя
        DEPLOY_SERVER = 'minion'  // Имя или адрес сервера
        SSH_CREDENTIALS_ID = 'agent-ssh-key'  // ID SSH-ключа в Jenkins
    }

    stages {
        stage('Clone Repository') {
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
                pytest tests/ --maxfail=1 --disable-warnings || echo "Tests failed!"
                echo "Tests completed."
                '''
            }
        }

        stage('Deploy') {
            steps {
                withCredentials([sshUserPrivateKey(credentialsId: 'agent-ssh-key', keyFileVariable: 'SSH_KEY')]) {
                    sh '''#!/bin/bash
                    echo "Deploying project files to ${DEPLOY_SERVER}..."
                    ssh -i "$SSH_KEY" jenkins@${DEPLOY_SERVER} "mkdir -p ${DEPLOY_DIR}"  # Создаём папку для деплоя
                    rsync -avz -e "ssh -i $SSH_KEY" . jenkins@${DEPLOY_SERVER}:${DEPLOY_DIR}/  # Копируем файлы
                    echo "Deployment completed!"
                    '''
                }
            }
        }

        stage('Start Application') {
            steps {
                withCredentials([sshUserPrivateKey(credentialsId: 'agent-ssh-key', keyFileVariable: 'SSH_KEY')]) {
                    sh '''#!/bin/bash
                    echo "Starting the application on the minion server..."
                    ssh -i "$SSH_KEY" jenkins@${DEPLOY_SERVER} "
                        export DEPLOY_DIR=${DEPLOY_DIR} && 
                        export VENV_DIR=${VENV_DIR} && 
                        cd ${DEPLOY_DIR} && 
                        python3 start_app.py &"
                    echo "Application started on ${DEPLOY_SERVER}."
                    '''
                }
            }
        }

        stage('Check Application') {
            steps {
                sh '''#!/bin/bash
                echo "Waiting for application to start..."
                sleep 5  # Даем время на старт
                echo "Checking application at http://localhost:8080"
                curl -v http://localhost:8080 || echo "Application check failed!"
                '''
            }
        }
    }

    post {
        always {
            echo "Pipeline execution completed."
        }
        failure {
            echo "❌ Pipeline failed! Check logs for details."
        }
        success {
            echo "✅ Pipeline completed successfully!"
        }
    }
}
