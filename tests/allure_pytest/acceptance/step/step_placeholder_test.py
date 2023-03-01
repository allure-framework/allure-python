""" ./allure-pytest/examples/step/step_placeholder.rst """

from hamcrest import assert_that
from tests.allure_pytest.pytest_runner import AllurePytestRunner

from allure_commons_test.report import has_test_case
from allure_commons_test.result import has_step
from allure_commons_test.result import has_status_details
from allure_commons_test.result import with_status
from allure_commons_test.result import with_message_contains


def test_step_with_args_in_placeholder(allure_pytest_runner: AllurePytestRunner):
    allure_results = allure_pytest_runner.run_docpath_examples(cache=True)

    assert_that(
        allure_results,
        has_test_case(
            "test_step_with_args_in_placeholder",
            has_step("Step with two args: 'first' and 'second'")
        )
    )


def test_step_with_kwargs_in_placeholder(allure_pytest_runner: AllurePytestRunner):
    allure_results = allure_pytest_runner.run_docpath_examples(cache=True)

    assert_that(
        allure_results,
        has_test_case(
            "test_step_with_kwargs_in_placeholder",
            has_step("Step with two kwargs: '1' and 'second'")
        )
    )


def test_class_method_as_step(allure_pytest_runner: AllurePytestRunner):
    allure_results = allure_pytest_runner.run_docpath_examples(cache=True)

    assert_that(
        allure_results,
        has_test_case(
            "test_class_method_as_step",
            has_step("Class method step with 'first' and 'second'")
        )
    )


def test_args_less_than_placeholders(allure_pytest_runner: AllurePytestRunner):
    """
    >>> import allure

    >>> @allure.step("{0} and {1}")
    ... def step(arg):
    ...     pass

    >>> def test_args_less_than_placeholders_example():
    ...     step(0)
    """

    allure_results = allure_pytest_runner.run_docstring()

    assert_that(
        allure_results,
        has_test_case(
            "test_args_less_than_placeholders_example",
            with_status("broken"),
            has_status_details(
                with_message_contains("IndexError")
            )
        )
    )
