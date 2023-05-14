pipeline {
    agent any
        environment {
        CONTINER = "ipreg"
        }

    stages {

        stage('Build Docker Image') {
            steps {
                script {
                    def containerExists = sh(script: 'docker ps -aqf "name=$CONTINER"', returnStatus: true) == 0
                    if (containerExists) {
                        sh 'docker rm -f $CONTINER'
                    }
                    sh 'docker rmi -f $CONTINER:latest'
                    sh 'docker build -t $CONTINER .'
                }
            }
        }

        stage('Deploy') {
            steps {
                sh 'docker run --restart=always -d -p 1080:5000 --name $CONTINER $CONTINER:latest'
            }
        }

    }
}
