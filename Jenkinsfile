pipeline {
    agent { docker 'n42org/tox' }
    environment { HOME = pwd() }
    stages {
        stage("Build") {
            steps {
                sh 'tox -c allure-python-commons/tox.ini'
                sh 'tox -c allure-pytest/tox.ini'
            }
        }
    }
}
