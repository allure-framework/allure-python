pipeline {
    agent { docker 'xsteadfastx/tox-jenkins-slave' }
    environment { HOME = pwd() }
    stages {
        stage("Build") {
            steps {
                sh 'tox -c allure-python-commons/tox.ini'
                sh 'tox -c allure-python-testing/tox.ini'
                sh 'tox -c allure-pytest/tox.ini'
                sh 'tox -c allure-behave/tox.ini'
            }
        }
    }
}
