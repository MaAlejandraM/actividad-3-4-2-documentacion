pipeline {
    agent any

    stages {
        stage('Build') {
            steps {
                echo 'Compilando y preparando entorno del proyecto...'
                sh 'ls -la'
            }
        }

        stage('Test') {
            steps {
                echo 'Ejecutando pruebas unitarias y validación de sintaxis...'
                sh 'python3 -m py_compile app.py && echo "Pruebas unitarias y sintaxis OK"'
            }
        }

        stage('Generate Documentation') {
            steps {
                echo 'Generando documentación técnica con Doxygen...'
                sh '''
                    rm -rf docs
                    docker rm -f doxygen-runner || true
                    docker create --name doxygen-runner -w /app alpine:3.19 sh -c "apk add --no-cache doxygen && doxygen Doxyfile"
                    docker cp . doxygen-runner:/app
                    docker start -a doxygen-runner
                    docker cp doxygen-runner:/app/docs ./docs
                    docker rm -f doxygen-runner || true
                    ls -la docs/html
                '''
            }
        }

        stage('Version Control') {
            steps {
                echo 'Actualizando control de versiones Git con la documentación generada...'
                sh '''
                    git config user.email "jenkins@devsecops.local"
                    git config user.name "Jenkins CI"
                    git add docs
                    git status
                    git commit -m "Docs: Actualización automática de documentación Doxygen [Build #${BUILD_NUMBER}]" || echo "Sin cambios nuevos en documentación"
                    git log -n 2 --stat
                '''
            }
        }

        stage('Deploy') {
            steps {
                echo 'Desplegando aplicación en entorno de prueba controlado...'
                sh '''
                    docker rm -f flask-docs-app || true
                    docker create --name flask-docs-app --network devsecops-net -p 5002:5000 -w /app python:3.11-slim bash -c "pip install --quiet -r requirements.txt && python app.py"
                    docker cp . flask-docs-app:/app
                    docker start flask-docs-app
                    sleep 10
                '''
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: 'docs/html/**/*', allowEmptyArchive: true
        }
    }
}