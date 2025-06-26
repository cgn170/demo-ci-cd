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
    DOCKER_REGISTRY = "harbor.devops.svc:8080/library"
    IMAGE_NAME = "${DOCKER_REGISTRY}" + "/" + "${APP_NAME}"
    DOCKERFILE_PATH = "Dockerfile"
    APP_NAME_LABEL = "${APP_NAME}"
    CONTAINER_NAME = "${APP_NAME}"
  }

  stages {

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
      //when {
      //  branch 'main'
      //}
      steps {
            script {
                container(name: 'kaniko', shell: '/busybox/sh') {
                        sh '''#!/busybox/sh
                        /kaniko/executor --dockerfile `pwd`/${DOCKERFILE_PATH} \
                                        --context `pwd` \
                                        --destination=${IMAGE_NAME}:${VERSION} \
                                        --insecure \
                                        --skip-tls-verify
                        '''
                }
            }
        }
    }

    stage('Deploy in K8s: Staging') {
    //when {
    //  branch 'main'
    //}
      steps {
        script {
            container(name: 'kaniko', shell: '/busybox/sh') {
                sh '''#!/busybox/sh
                    set -x  # Print all commands before executing
                    set -e  # Exit on any error
                    
                    echo "=== Starting Kubernetes Deployment ==="
                    echo "Container Name: ${CONTAINER_NAME}"
                    echo "Image Name: ${IMAGE_NAME}"
                    echo "Version: ${VERSION}"
                    echo "Namespace: staging"
                    
                    echo "=== Downloading kubectl ==="
                    wget -O kubectl "https://dl.k8s.io/release/$(wget -qO- https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
                    chmod +x kubectl
                    
                    echo "=== Executing kubectl command ==="
                    ./kubectl set image deployment/demo-ci-cd ${CONTAINER_NAME}=${IMAGE_NAME}:${VERSION} -n staging
                    
                    echo "=== Deployment command completed ==="
                '''
            }
        }
      }
    }

  }
  
}
