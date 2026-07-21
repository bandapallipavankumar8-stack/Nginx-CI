pipeline {
    agent any

    environment {
        S3_BUCKET = 's3://nginx-ci/packages'
        AWS_REGION = 'ap-south-1'
    }

    stages {
        stage('Checkout Source') {
            steps {
                checkout scm
            }
        }

        stage('Package Code') {
            steps {
                echo 'Packaging project files and index.html into a zip archive...'
                // FIXED: Creates the zip outside the root directory to prevent a recursive loop, then brings it back
                sh "zip -r ../package-${BUILD_NUMBER}.zip . -x '*.git*' 'Jenkinsfile' 'README.md' '.gitignore'"
                sh "mv ../package-${BUILD_NUMBER}.zip ."
            }
        }

        stage('Upload Package to S3') {
            steps {
                echo "Uploading package-${BUILD_NUMBER}.zip to S3 bucket..."
                sh "aws s3 cp package-${BUILD_NUMBER}.zip ${env.S3_BUCKET}/package-${BUILD_NUMBER}.zip --region ${env.AWS_REGION}"
            }
        }
    }

    post {
        success {
            echo "CI Complete! Triggering downstream job NGINX_CD with parameter: ${BUILD_NUMBER}"
            // FIXED: Structural wrapper block correctly passes the build parameter to the CD pipeline
            build job: 'NGINX_CD', 
                  wait: false, 
                  parameters: [
                      string(name: 'CI_BUILD_NUMBER', value: "${BUILD_NUMBER}")
                  ]
        }
        always {
            echo 'Cleaning up workspace zip files...'
            sh "rm -f package-${BUILD_NUMBER}.zip"
        }
    }
}
