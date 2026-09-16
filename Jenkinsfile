pipeline {
    agent any

    environment {
        IMAGE_NAME   = 'backend-django'
        IMAGE_TAG    = "${BUILD_NUMBER}"
        DOCKER_CREDS = 'docker-hub-credentials'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
                sh 'ls -la'
            }
        }

        stage('Testing') {
            steps {
                // pytest devuelve 5 cuando no recolecta ninguna prueba.
                // Ese caso no debe tumbar la tuberia: solo fallan las pruebas rotas.
                sh '
                111
                '
            }
            post {
                always {
                    junit allowEmptyResults: true, testResults: 'reports/junit.xml'
                }
            }
        }

        stage('Build') {
            steps {
                sh 'docker build -t "$IMAGE_NAME:$IMAGE_TAG" -t "$IMAGE_NAME:latest" .'
                sh 'docker images "$IMAGE_NAME"'
            }
        }

        stage('Push') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: "${DOCKER_CREDS}",
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_PASS')]) {
                    sh '''
                        set -e
                        echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin
                        docker tag "$IMAGE_NAME:$IMAGE_TAG" "$DOCKER_USER/$IMAGE_NAME:$IMAGE_TAG"
                        docker tag "$IMAGE_NAME:latest"     "$DOCKER_USER/$IMAGE_NAME:latest"
                        docker push "$DOCKER_USER/$IMAGE_NAME:$IMAGE_TAG"
                        docker push "$DOCKER_USER/$IMAGE_NAME:latest"
                        docker logout
                    '''
                }
            }
        }
    }

    post {
        always {
            cleanWs()
        }
        success {
            echo 'Pipeline completado exitosamente.'
        }
        failure {
            echo 'El pipeline ha fallado.'
        }
    }
}
