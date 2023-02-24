import pytest
from tests.allure_pytest.pytest_runner import AllurePytestRunner


@pytest.fixture
def allure_pytest_bdd_runner(request, pytester):
    runner = AllurePytestRunner(request, pytester)
    runner.logger_path = "allure_pytest_bdd.plugin.AllureFileLogger"
    runner.select_plugins("pytest-bdd", "allure_pytest_bdd")
    yield runner
