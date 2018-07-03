pip uninstall allure-python-commons-test allure-python-commons allure-pytest
cd allure-python-commons-test
tox
cd ..\allure-python-commons
tox
cd ..\allure-pytest
tox -e py36
cd ..