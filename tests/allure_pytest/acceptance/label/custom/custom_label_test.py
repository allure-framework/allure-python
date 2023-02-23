""" ./allure-pytest/examples/label/custom/custom_label.rst """

from hamcrest import assert_that
from tests.allure_pytest.pytest_runner import AllurePytestRunner

from allure_commons_test.report import has_test_case
from allure_commons_test.label import has_label


def test_custom_label(allure_pytest_runner: AllurePytestRunner):
    allure_results = allure_pytest_runner.run_docpath_examples()

    assert_that(
        allure_results,
        has_test_case(
            "test_custom_label",
            has_label("Application", "desktop"),
            has_label("Application", "mobile")
        )
    )
