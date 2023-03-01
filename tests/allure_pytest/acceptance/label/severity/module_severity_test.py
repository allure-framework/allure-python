""" ./allure-pytest/examples/label/severity/module_severity.rst """

from hamcrest import assert_that
from tests.allure_pytest.pytest_runner import AllurePytestRunner

from allure_commons_test.report import has_test_case
from allure_commons_test.label import has_severity


def test_not_decorated_function(allure_pytest_runner: AllurePytestRunner):
    allure_results = allure_pytest_runner.run_docpath_examples(cache=True)

    assert_that(
        allure_results,
        has_test_case(
            "test_not_decorated_function",
            has_severity("trivial")
        )
    )


def test_decorated_function(allure_pytest_runner: AllurePytestRunner):
    allure_results = allure_pytest_runner.run_docpath_examples(cache=True)

    assert_that(
        allure_results,
        has_test_case(
            "test_decorated_function",
            has_severity("minor")
        )
    )


def test_method_of_not_decorated_class(allure_pytest_runner: AllurePytestRunner):
    allure_results = allure_pytest_runner.run_docpath_examples(cache=True)

    assert_that(
        allure_results,
        has_test_case(
            "test_method_of_not_decorated_class",
            has_severity("trivial")
        )
    )


def test_method_of_decorated_class(allure_pytest_runner: AllurePytestRunner):
    allure_results = allure_pytest_runner.run_docpath_examples(cache=True)

    assert_that(
        allure_results,
        has_test_case(
            "test_method_of_decorated_class",
            has_severity("normal")
        )
    )
