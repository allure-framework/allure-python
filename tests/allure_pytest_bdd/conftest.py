import pytest
from tests.conftest import AlluredTestdir

@pytest.fixture
def allured_testdir(allured_testdir: AlluredTestdir):
    allured_testdir.select_plugins("allure_pytest_bdd")
    return allured_testdir