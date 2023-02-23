""" ./allure-pytest/examples/step/step.rst """

from hamcrest import assert_that
from tests.allure_pytest.pytest_runner import AllurePytestRunner

from allure_commons_test.report import has_test_case
from allure_commons_test.result import has_step


def test_inline_step(allure_pytest_runner: AllurePytestRunner):
    allure_results = allure_pytest_runner.run_docpath_examples(cache=True)

    assert_that(
        allure_results,
        has_test_case(
            "test_inline_step",
            has_step("inline step")
        )
    )


def test_reusable_step(allure_pytest_runner: AllurePytestRunner):
    allure_results = allure_pytest_runner.run_docpath_examples(cache=True)

    assert_that(
        allure_results,
        has_test_case(
            "test_reusable_step",
            has_step("passed_step")
        )
    )


def test_nested_steps(allure_pytest_runner: AllurePytestRunner):
    allure_results = allure_pytest_runner.run_docpath_examples(cache=True)

    assert_that(
        allure_results,
        has_test_case(
            "test_nested_steps",
            has_step(
                "grand parent step",
                has_step(
                    "parent step",
                    has_step("passed_step")
                )
            )
        )
    )


def test_class_method_as_step(allure_pytest_runner: AllurePytestRunner):
    allure_results = allure_pytest_runner.run_docpath_examples(cache=True)

    assert_that(
        allure_results,
        has_test_case(
            "test_class_method_as_step",
            has_step("class method as step")
        )
    )
