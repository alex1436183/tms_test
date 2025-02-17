pipeline {
    agent { label 'minion' }  // Выполняем на агенте с меткой 'minion'

    environment {
        REPO_URL = 'https://github.com/alex1436183/tms_test.git'
        BRANCH_NAME = 'main'
        VENV_DIR = 'venv'
    }

    stages {
        stage('Clone repository') {
            steps {
                git branch: "${BRANCH_NAME}", url: "${REPO_URL}"
            }
        }
        
        stage('Setup Python Environment') {
            steps {
                sh '''
                python3 -m venv ${VENV_DIR}
                source ${VENV_DIR}/bin/activate
                pip install --upgrade pip
                pip install -r requirements.txt
                '''
            }
        }

        stage('Run Tests') {
            steps {
                sh '''
                source ${VENV_DIR}/bin/activate
                pytest tests/ --maxfail=1 --disable-warnings
                '''
            }
        }

        stage('Start Application') {
            steps {
                sh '''
                source ${VENV_DIR}/bin/activate
                nohup python app.py > app.log 2>&1 &
                echo $! > app.pid
                '''
            }
        }

        stage('Check Application') {
            steps {
                sh '''
                sleep 5
                curl -v http://localhost:8080
                '''
            }
        }
    }

    post {
        always {
            sh '''
            if [ -f app.pid ]; then
                kill $(cat app.pid) || true
                rm -f app.pid
            fi
            '''
        }
        failure {
            echo 'Pipeline failed!'
        }
        success {
            echo 'Pipeline completed successfully!'
        }
    }
}
