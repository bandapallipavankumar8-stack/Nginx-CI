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
                // FIXED: Output the zip to the parallel temp folder to avoid self-inclusion
                sh "zip -r ../package-${BUILD_NUMBER}.zip . -x '*.git*' 'Jenkinsfile' 'README.md' '.gitignore'"
                sh "mv ../package-${BUILD_NUMBER}.zip ."
            }
        }

        stage('Upload Package to S3') {
            steps {
                echo "Uploading package-${BUILD_NUMBER}.zip to S3 bucket..."
                // ENHANCEMENT: It is highly recommended to wrap this block using Jenkins AWS steps
                // withAWS(credentials: 'your-aws-credential-id', region: "${env.AWS_REGION}") {
                    sh "aws s3 cp package-${BUILD_NUMBER}.zip ${env.S3_BUCKET}/package-${BUILD_NUMBER}.zip --region ${env.AWS_REGION}"
                // }
            }
        }
    }

    post {
        success {
            echo "CI Complete! Triggering downstream job NGINX_CD with parameter: ${BUILD_NUMBER}"
            // FIXED: Added the mandatory 'parameters: [ ... ]' wrapper block
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
