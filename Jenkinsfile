pipeline {
    agent { docker 'xsteadfastx/tox-python' }
    environment {
        HOME = pwd()
        TOX_VERSION = '2.7.0'
    }
    stages {
        stage("Build") {
            steps {
                sh 'tox --version'
                sh 'tox --workdir=/tmp -c allure-python-commons/tox.ini'
                sh 'tox --workdir=/tmp -c allure-python-testing/tox.ini'
                sh 'tox --workdir=/tmp -c allure-pytest/tox.ini'
                sh 'tox --workdir=/tmp -c allure-behave/tox.ini'
            }
        }
    }
}
