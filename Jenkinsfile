pipeline {
    agent { docker 'xsteadfastx/tox-jenkins-slave' }
    environment { HOME = pwd() }
    stages {
        stage("Build") {
            steps {
                sh 'tox --workdir=/tmp -c allure-python-commons/tox.ini'
                sh 'tox --workdir=/tmp -c allure-python-testing/tox.ini'
                sh 'tox --workdir=/tmp -c allure-pytest/tox.ini'
                sh 'tox --workdir=/tmp -c allure-behave/tox.ini'
            }
        }
    }
}
