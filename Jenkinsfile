pipeline {
    agent { label 'minion' }

    environment {
        REPO_URL = 'https://github.com/alex1436183/tms_test.git'
        BRANCH_NAME = 'main'
        VENV_DIR = 'venv'
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
                pip install -r requirements.txt  # Установка зависимостей из файла, если он есть
                echo "Installing Flask..."
                pip install Flask  # Устанавливаем Flask, если он не в requirements.txt
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

        stage('Start Application') {
            steps {
                sh '''#!/bin/bash
                echo "Starting application..."
                source ${VENV_DIR}/bin/activate
                nohup python app.py > app.log 2>&1 &
                echo $! > app.pid
                echo "Application started with PID: $(cat app.pid)"
                '''
            }
        }

        stage('Check Application') {
            steps {
                sh '''#!/bin/bash
                echo "Waiting for application to start..."
                sleep 10  # Увеличиваем время ожидания для запуска приложения
                echo "Checking application at http://localhost:8080"
                curl -v http://localhost:8080 || echo "Application check failed!"
                '''
            }
        }

        stage('Keep Application Running') {
            steps {
                echo "Application should now be running, waiting for manual intervention to end pipeline."
                input message: 'Press "Proceed" to stop the pipeline and leave the app running.'
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
