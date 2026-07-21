pipeline {
    agent any

    environment {
        // Target AWS S3 Bucket Name
        S3_BUCKET = 's3://code-version/packages'
        // Target AWS Region (Mumbai)
        AWS_REGION = 'ap-south-1'
    }

    stages {
        stage('Checkout Source') {
            steps {
                // Pulls code automatically from your GitHub repository
                checkout scm
            }
        }

        stage('Package Code') {
            steps {
                echo 'Packaging project files and index.html into a zip archive...'
                // Zips all root files while ignoring configuration and metadata files
                sh "zip -r package-${BUILD_NUMBER}.zip . -x '*.git*' 'Jenkinsfile' 'README.md' '.gitignore'"
                
                echo 'Verifying package contents:'
                // Lists the contents inside the zip to verify index.html is included
                sh "unzip -l package-${BUILD_NUMBER}.zip"
            }
        }

        stage('Upload Package to S3') {
            steps {
                echo "Uploading package-${BUILD_NUMBER}.zip to S3 bucket in Mumbai..."
                // Copies the packaged file utilizing the local EC2 instance profile role
                sh "aws s3 cp package-${BUILD_NUMBER}.zip ${env.S3_BUCKET}/package-${BUILD_NUMBER}.zip --region ${env.AWS_REGION}"
            }
        }
    }

    post {
        always {
            echo 'Cleaning up workspace zip files...'
            // Clean up workspace memory to prevent disk fill-ups on the agent
            sh "rm -f package-${BUILD_NUMBER}.zip"
        }
    }
}
