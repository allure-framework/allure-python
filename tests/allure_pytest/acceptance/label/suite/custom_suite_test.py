""" ./allure-pytest/examples/label/suite/custom_suite.rst """

from hamcrest import assert_that
from tests.allure_pytest.pytest_runner import AllurePytestRunner

from allure_commons_test.report import has_test_case
from allure_commons_test.label import has_suite, has_parent_suite, has_sub_suite


def test_custom_suite(allure_pytest_runner: AllurePytestRunner):
    allure_results = allure_pytest_runner.run_docpath_examples()

    assert_that(
        allure_results,
        has_test_case(
            "test_custom_suite",
            has_suite("suite name"),
            has_parent_suite("parent suite name"),
            has_sub_suite("sub suite name")
        )
    )
