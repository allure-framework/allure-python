""" ./allure-pytest/examples/label/severity/severity.rst """

from hamcrest import assert_that
from tests.allure_pytest.pytest_runner import AllurePytestRunner

from allure_commons_test.report import has_test_case
from allure_commons_test.label import has_severity


def test_severity(allure_pytest_runner: AllurePytestRunner):
    allure_results = allure_pytest_runner.run_docpath_examples()

    assert_that(
        allure_results,
        has_test_case(
            "test_severity",
            has_severity("minor"),
        )
    )
