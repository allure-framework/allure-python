# Allure Python Integrations

The repository contains adaptors for python-based test frameworks.
Documentation is available [online](https://docs.qameta.io/allure/2.0/), also you can get help at
[gitter chanel](https://gitter.im/allure-framework/allure-core)


## Pytest
Allure [pytest](http://pytest.org) integration. It's developed as pytest plugin and distributed via
[pypi](https://pypi.python.org/pypi/allure-pytest)


## Behave
Allure [behave](https://behave.readthedocs.io/en/latest/) integration. Just external formatter that produce test results in
allure2 format. This package is available on [pypi](https://pypi.python.org/pypi/allure-behave)

## Robot Framework
Allure [RobotFramework](http://robotframework.org/) integration. This integration is a 
[Listener](http://robotframework.org/robotframework/latest/RobotFrameworkUserGuide.html#listener-interface) 
and does not require changing autotests. Available on [pypi](https://pypi.python.org/pypi/allure-robotframework)

## Allure python commons
Common engine for all modules. It is useful for make integration with your homemade frameworks.


## Allure python commons test
Just pack of hamcrest matchers for validation result in allure2 json format.
