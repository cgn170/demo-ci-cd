pipeline {

  agent {
    kubernetes {
      yamlFile 'kaniko-builder.yaml'
    }
  }

  options {
      buildDiscarder logRotator( 
                  daysToKeepStr: '16', 
                  numToKeepStr: '10'
          )
      disableConcurrentBuilds()
  }

  environment {
    APP_NAME = "demo-ci-cd"
    DOCKER_REGISTRY = "harbor-portal.harbor-system.svc.cluster.local:80/public"
    IMAGE_NAME = "${DOCKER_REGISTRY}" + "/" + "${APP_NAME}"
    DOCKERFILE_PATH = "Dockerfile"
    APP_NAME_LABEL = "${APP_NAME}"
    CONTAINER_NAME = "${APP_NAME}"
  }

  stages {

    stage("Cleanup Workspace") {
      steps {
        cleanWs()
      }
    }

    stage("Checkout from SCM"){
      steps {
        script {
            sh """
              echo "Cloning repo with branch: ${GIT_BRANCH}"
            """
            checkout([
              $class: 'GitSCM',
              branches: scm.branches,
              extensions: scm.extensions + [[$class: 'CloneOption', noTags: false, reference: '', shallow: false]],
              userRemoteConfigs: scm.userRemoteConfigs
            ])
          }
        
      }
    }

    stage('Unit Testing') {
      steps {
        container(name: 'node', shell: '/bin/sh') {
          sh '''#!/bin/sh
            echo "Running Unit Tests"
          '''
        }
      }
    }

    stage('Code Analysis') {
        steps {
            sh """
            echo "Running Code Analysis"
            """
        }
    }

    stage("Get Version"){
      steps {
        script {
          env.VERSION = sh(returnStdout: true, script: 'git describe --tags --abbrev=0').trim()
          echo "Branch: ${env.GIT_BRANCH}"
          echo "Git tag version: ${VERSION}"
          echo "Creating ${IMAGE_NAME}:${VERSION} container image"
        }
      }
    }

    stage('Build & Push with Kaniko') {
      steps {
        script {
            container(name: 'kaniko', shell: '/busybox/sh') {
                    sh '''#!/busybox/sh
                      /kaniko/executor --dockerfile `pwd`/${DOCKERFILE_PATH} \
                                      --context `pwd` \
                                      --destination=${IMAGE_NAME}:${VERSION}
                    '''
            }
        }
    }

    stage('Deploy in K8s') {
      steps {
        script {
            withKubeConfig([namespace: "staging"]) {
                sh 'curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/arm64/kubectl"'  
                sh 'chmod u+x ./kubectl'
                sh './kubectl set image deployment/demo-ci-cd ${CONTAINER_NAME}=${IMAGE_NAME}:${VERSION} demo-ci-cd=${IMAGE_NAME}:${VERSION}'
            }
        }
      }
    }

  }
  post {
      success {
          slackSend message: "Job: ${env.JOB_NAME} - Build: ${env.BUILD_NUMBER} - was successful  (<${env.BUILD_URL}| Link>)"
      }
      failure {
          slackSend message: "Job: ${env.JOB_NAME} - Build: ${env.BUILD_NUMBER} - failed  (<${env.BUILD_URL}| Link>)", failOnError: true
      }
  }
}
