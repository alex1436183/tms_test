pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                cleanWs()
                checkout scm
            }
        }

        stage('Check Files') {
            steps {
                sh 'ls -la'
            }
        }
    }
}
