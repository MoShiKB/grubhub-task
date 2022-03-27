pipeline {
    environment {
        imagename = "moshikb/grubhub"
        registryCredential = 'moshikb-dockerhub'
        dockerImage = ''
    }
    agent any
    stages {
        stage('Cloning Git') {
            steps {
                git([url: 'https://github.com/MoShiKB/grubhub-task.git', branch: 'master'])
            }
        }
        stage('Building image') {
            steps{
                script {
                    dir("${env.WORKSPACE}/docker"){
                        dockerImage = docker.build imagename
                    }
                }
            }
        }
        stage('Deploy Image') {
            steps{
                script {
                    docker.withRegistry( '', registryCredential ) {
                        dockerImage.push("$BUILD_NUMBER")
                        dockerImage.push('latest')
                    }
                }
            }
        }
        stage('Remove Unused docker image') {
            steps{
                sh "docker rmi $imagename:$BUILD_NUMBER"
                sh "docker rmi $imagename:latest"
            }
        }
    }
}
