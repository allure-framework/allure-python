""" ./examples/step/step_placeholder.rst """

from hamcrest import assert_that
from allure_commons_test.report import has_test_case
from allure_commons_test.result import has_step
from allure_commons_test.result import has_status_details
from allure_commons_test.result import with_message_contains


def test_step_with_args_in_placeholder(executed_docstring_path):
    assert_that(executed_docstring_path.allure_report,
                has_test_case("test_step_with_args_in_placeholder",
                              has_step("Step with two args: 'first' and 'second'")
                              )
                )


def test_step_with_kwargs_in_placeholder(executed_docstring_path):
    assert_that(executed_docstring_path.allure_report,
                has_test_case("test_step_with_kwargs_in_placeholder",
                              has_step("Step with two kwargs: '1' and 'second'")
                              )
                )


def test_class_method_as_step(executed_docstring_path):
    assert_that(executed_docstring_path.allure_report,
                has_test_case("test_class_method_as_step",
                              has_step("Class method step with 'first' and 'second'")
                              )
                )


def test_args_less_than_placeholders(executed_docstring_source):
    """
    >>> import allure

    >>> @allure.step("{0} and {1}")
    ... def step(arg):
    ...     pass

    >>> def test_args_less_than_placeholders_example():
    ...     step(0)
    """

    assert_that(executed_docstring_source.allure_report,
                has_test_case("test_args_less_than_placeholders_example",
                              has_status_details(with_message_contains("IndexError: tuple index out of range"))
                              )
                )
