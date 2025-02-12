pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                
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
