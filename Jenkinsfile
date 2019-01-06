pipeline {
    agent any
    stages {
        stage('Build') {
            steps {
                sh 'pip3 install -r docker/jenkins/requirements.txt'                                    
            }
        }
        stage('Test') {
            steps {
                sh 'python3 manage.py makemigrations --merge'
                sh 'python3 manage.py makemigrations order'
                sh 'python3 manage.py migrate'
                sh 'python3 manage.py jenkins --enable-coverage'
            }
        }
        
    }
    post {
        always {
            junit 'reports/junit.xml'
             // publish coverage html
            //publishHTML target: [
            //    allowMissing: false,
            //    alwaysLinkToLastBuild: false,
            //    keepAll: true,
            //    reportDir: 'reports/coverage',
            //    reportFiles: 'index.html',
            //    reportName: 'Coverage Test Report'
            //]
        }
        success {
            cobertura coberturaReportFile: 'reports/coverage.xml' 
        }
    }
}
