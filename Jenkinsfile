pipeline {
    agent any
    stages {
        stage('Build') {
            steps {
                sh 'pip3 install python3-dev'
                sh 'pip3 install -r docker/jenkins/requirements.txt'                                    
            }
        }
        stage('Test') {
            steps {
                sh 'python3 manage.py makemigrations order'
                sh 'python3 manage.py migrate'
                sh 'python3 manage.py jenkins --enable-coverage'
            }
        }
    }
}
