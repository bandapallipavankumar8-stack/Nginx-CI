pipeline {
    agent any

    environment {
        // Your exact AWS S3 Bucket layout path
        S3_BUCKET = 's3://nginx-ci/packages'
        AWS_REGION = 'ap-south-1'
    }

    stages {
        stage('Checkout Source') {
            steps {
                echo "Cloning the source code from GitHub repository..."
                // This command explicitly clones your repository files into the Jenkins workspace
                checkout scm
            }
        }

        stage('Package Code') {
            steps {
                echo "Packaging project files and index.html into a zip archive..."
                // Creates the zip package safely
                sh "zip -r ../package-${BUILD_NUMBER}.zip . -x '*.git*' 'Jenkinsfile' 'README.md' '.gitignore'"
                sh "mv ../package-${BUILD_NUMBER}.zip ."
            }
        }

        stage('Upload Package to S3 Repository') {
            steps {
                echo "Uploading package-${BUILD_NUMBER}.zip to S3 bucket repository..."
                // Standard double quotes allow perfect variable interpolation without breaking
                sh "aws s3 cp package-${BUILD_NUMBER}.zip ${env.S3_BUCKET}/package-${BUILD_NUMBER}.zip --region ${env.AWS_REGION}"
            }
        }
    }

    post {
        success {
            echo "CI Complete! Triggering downstream job NGINX_CD with parameter: ${BUILD_NUMBER}"
            // Automatically kicks off your deployment pipeline with the precise build number
            build job: 'NGINX_CD', 
                  wait: false, 
                  parameters: [
                      string(name: 'CI_BUILD_NUMBER', value: "${BUILD_NUMBER}")
                  ]
        }
        always {
            echo "Cleaning up workspace zip files..."
            sh "rm -f package-${BUILD_NUMBER}.zip"
        }
    }
}
