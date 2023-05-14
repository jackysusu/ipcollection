pipeline {
    agent any
    environment {
       DOCKERHUB_CREDENTIALS = credentials('DockerHub_Login')
       DOCKER_IMAGE = 'jackysusu/fwbase2204:roger'
    }

    stages {

        stage('Pull Project') {
            steps {
                // git branch: 'main', credentialsId: 'jenkins_rsa', url: 'ssh://git@tpe-gitlab.amigo.com.tw:8022/devops/cicd.git'
                sh 'mkdir -p apps/openwrt'
                dir('apps/openwrt') {
                    git branch: 'main', credentialsId: 'amigo_rsa', url: 'ssh://git@gitlab.amigo.ga:2222/amigo/mtk/openwrt.git'

                }

            }
        }

        stage('Docker Hub Login') {
            steps {
                sh 'echo $DOCKERHUB_CREDENTIALS_PSW | docker login -u $DOCKERHUB_CREDENTIALS_USR --password-stdin'
            }
        }

        stage('Docker Pull fwbase:01') {
            steps {
                script {
                    sh 'docker pull $DOCKER_IMAGE'
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    def containerExists = sh(script: 'docker ps -aqf "name=fwbuilder"', returnStatus: true) == 0
                    if (containerExists) {
                        sh 'docker rm -f fwbuilder'
                    }
                    sh 'docker rmi -f fwbuilder:01'
                    sh 'docker build -t fwbuilder:01 .'
                }
            }
        }

        stage('Build FW') {
            steps {
                sh 'docker run --name fwbuilder fwbuilder:01 sh -c "./scripts/feeds update -a && ./scripts/feeds install -a && ./scripts/feeds install -a luci && make defconfig oldconfig && make download -j 10 && make -j 10"'
            }
        }

        stage('Deploy') {
            when {
                expression { currentBuild.result == null || currentBuild.result == 'SUCCESS' }
            }
            steps {
                sh 'rm -rf /tmp/fw'
                sh 'docker cp fwbuilder:/home/doagent/openwrt/bin/targets /tmp/fw'
                sh 'docker rm -f fwbuilder'
                sh 'docker rmi -f jackysusu/fwbuilder:ubuntu2004'
            }
        }

        // stage ("Ansible Copy FW to NAS") {
        //     steps {
        //         sh "pwd"
        //         dir('./ansible') {
        //         sh "ansible all -m ping"
        //         sh "ansible-playbook all.yml"
        //         }
        //     }
        // }

    }
}
