pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                git 'https://github.com/alex1436183/MyRepository.git'  // Репозиторий, из которого будет загружаться код
            }
        }
        stage('Run Script') {
            steps {
                script {
                    // Запуск твоего Python скрипта
                    sh 'python tiner.py'
                }
            }
        }
    }

    post {
        always {
            // Это всегда будет выполняться после выполнения пайплайна (например, для очистки)
            echo 'Build finished'
        }
        success {
            // Сообщение при успешной сборке
            echo 'Build was successful!'
        }
        failure {
            // Сообщение при ошибке сборки
            echo 'Build failed!'
        }
    }
}
