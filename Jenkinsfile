pipeline {
    agent any

    environment {
        REPO_URL = 'https://github.com/alex1436183/tms_test.git'
        BRANCH_NAME = 'main'  
        REPORT_FILE = 'report.html'
    }

    stages {
        stage('Checkout Repository') {
            steps {
            cleanWs() 
                script {
                    checkout scm: [
                        $class: 'GitSCM',
                        userRemoteConfigs: [[url: env.REPO_URL]],
                        branches: [[name: "*/${env.BRANCH_NAME}"]]
                    ]
                }
            }
        }

        stage('Generate File List Report') {
            steps {
                script {
                    def fileList = sh(script: 'ls -lh', returnStdout: true).trim()
                    def reportContent = """
                        <html>
                        <head><title>File List Report</title></head>
                        <body>
                            <h2>Список файлов репозитория:</h2>
                            <pre>${fileList}</pre>
                        </body>
                        </html>
                    """
                    writeFile file: env.REPORT_FILE, text: reportContent
                }
            }
        }

        stage('Archive Report') {
            steps {
                archiveArtifacts artifacts: env.REPORT_FILE, fingerprint: true
            }
        }

        stage('Send Email') {
            steps {
                emailext subject: "Jenkins Report: File List",
                          body: "Прикреплен отчет о файлах в репозитории.",
                          attachmentsPattern: env.REPORT_FILE,
                          to: 'dnsoika@gmail.com'
            }
        }
    }
}
