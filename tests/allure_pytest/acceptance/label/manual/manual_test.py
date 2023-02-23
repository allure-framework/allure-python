""" ./allure-pytest/examples/label/manual/allure_manual.rst """

from hamcrest import assert_that
from tests.allure_pytest.pytest_runner import AllurePytestRunner

from allure_commons_test.report import has_test_case
from allure_commons_test.label import has_label


def test_allure_manual_label(allure_pytest_runner: AllurePytestRunner):
    allure_results = allure_pytest_runner.run_docpath_examples(cache=True)

    assert_that(
        allure_results,
        has_test_case(
            "test_manual",
            has_label("ALLURE_MANUAL", True),
        )
    )


def test_allure_manual_label_dynamic(allure_pytest_runner: AllurePytestRunner):
    allure_results = allure_pytest_runner.run_docpath_examples(cache=True)

    assert_that(
        allure_results,
        has_test_case(
            "test_manual_dynamic",
            has_label("ALLURE_MANUAL", True),
        )
    )
