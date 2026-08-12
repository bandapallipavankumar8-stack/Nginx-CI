pipeline {
    agent any

    environment {
        // Your exact AWS S3 Bucket storage path
        S3_BUCKET = 's3://nginx-ci/packages'
        AWS_REGION = 'ap-south-1'
    }

    stages {
        stage('Checkout Source') {
            steps {
                echo "Cloning the source code from GitHub repository..."
                // This command securely pulls your latest code down into the Jenkins workspace
                checkout scm
            }
        }

        stage('Package Code') {
            steps {
                echo "Packaging project files and index.html into a zip archive..."
                // Creates the zip archive safely outside the root folder to avoid loop issues
                sh "zip -r ../package-${BUILD_NUMBER}.zip . -x '*.git*' 'Jenkinsfile' 'README.md' '.gitignore'"
                sh "mv ../package-${BUILD_NUMBER}.zip ."
            }
        }

        stage('Upload Package to S3') {
            steps {
                echo "Uploading package-${BUILD_NUMBER}.zip to S3 bucket repository..."
                // Plain double quotes allow Jenkins to substitute variables cleanly without errors
                sh "aws s3 cp package-${BUILD_NUMBER}.zip ${env.S3_BUCKET}/package-${BUILD_NUMBER}.zip --region ${env.AWS_REGION}"
            }
        }
    }

    post {
        success {
            echo "CI Complete! Triggering downstream job NGINX_CD with parameter: ${BUILD_NUMBER}"
            // This block automatically triggers your CD pipeline and passes the exact build number
            build job: 'NGINX_CD', 
                  wait: false, 
                  parameters: [
                      string(name: 'CI_BUILD_NUMBER', value: "${BUILD_NUMBER}")
                  ]
        }
        always {
            echo "Cleaning up workspace zip files..."
            // Deletes the temporary zip file from the Jenkins workspace to keep the server clean
            sh "rm -f package-${BUILD_NUMBER}.zip"
        }
    }
}
