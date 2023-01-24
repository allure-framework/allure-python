""" ./examples/parameter/dynamic_parameter.rst """

from hamcrest import assert_that
from allure_commons_test.report import has_test_case
from allure_commons_test.result import (
    has_parameter,
    get_parameter_matcher,
    with_excluded,
    with_mode
)


def test_dynamic_parameter(executed_docstring_path):
    assert_that(
        executed_docstring_path.allure_report,
        has_test_case(
            "test_dynamic_parameter",
            has_parameter("username", "'John Doe'")
        )
    )


def test_masked_dynamic_parameter(executed_docstring_path):
    assert_that(
        executed_docstring_path.allure_report,
        has_test_case(
            "test_masked_dynamic_parameter",
            has_parameter(
                "password",
                "'qwerty'",
                with_mode("masked")
            )
        )
    )


def test_hidden_dynamic_parameter(executed_docstring_path):
    assert_that(
        executed_docstring_path.allure_report,
        has_test_case(
            "test_hidden_dynamic_parameter",
            get_parameter_matcher(
                "hostname",
                with_mode("hidden")
            )
        )
    )


def test_excluded_dynamic_parameter(executed_docstring_path):
    assert_that(
        executed_docstring_path.allure_report,
        has_test_case(
            "test_excluded_dynamic_parameter",
            get_parameter_matcher(
                "work-dir",
                with_excluded()
            )
        )
    )
