from pytest import fixture
from .pytest_runner import AllurePytestRunner


@fixture
def allure_pytest_runner(request, pytester):
    yield AllurePytestRunner(request, pytester)
