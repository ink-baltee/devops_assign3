pipeline {
  agent any

  environment {
    REPO = 'https://github.com/<your-username>/assignment3-flask.git' // replace
    APP_IMAGE = "assignment3-flask-app:${env.BUILD_NUMBER}"
    TEST_IMAGE = "assignment3-flask-tests:${env.BUILD_NUMBER}"
  }

  stages {
    stage('Checkout') {
      steps {
        checkout scm
      }
    }

    stage('Code Linting') {
      steps {
        sh 'python3 -m pip install --user flake8 || true'
        sh 'python3 -m pip install -r app/requirements.txt || true'
        sh 'flake8 app || true'  // do not fail pipeline on lint warning; change to fail if required
      }
    }

    stage('Code Build') {
      steps {
        sh 'python3 -m pip install -r app/requirements.txt'
        sh 'echo "Build step: dependencies installed"'
      }
    }

    stage('Unit Testing') {
      steps {
        sh 'pytest -q tests/unit || { echo "Unit tests failed"; exit 1; }'
      }
    }

    stage('Containerized Deployment') {
      steps {
        script {
          // build app image
          sh "docker build -t ${APP_IMAGE} ."
          // run the container in detached mode mapping port
          sh "docker rm -f assignment3_app || true"
          sh "docker run -d --name assignment3_app -p 5000:5000 ${APP_IMAGE}"
          // wait for app to start
          sh 'sleep 5'
        }
      }
    }

    stage('Selenium Testing') {
      steps {
        script {
          // Build & run test image that contains chrome & chromedriver
          sh "docker build -f Dockerfile.tests -t ${TEST_IMAGE} ."
          // Run tests with network so tests can reach host application:
          // We run tests container and point to host.docker.internal (works on many Docker setups).
          sh "docker run --rm --network host ${TEST_IMAGE} pytest -q tests/selenium || { echo 'Selenium tests failed'; docker logs assignment3_app || true; exit 1; }"
        }
      }
    }
  }

  post {
    always {
      sh "docker rm -f assignment3_app || true"
      archiveArtifacts artifacts: 'tests/**/*.py', fingerprint: true
      junit '**/TEST-*.xml' // if pytest junitxml used
    }
    success {
      echo 'Pipeline succeeded'
    }
    failure {
      echo 'Pipeline failed'
    }
  }
}
