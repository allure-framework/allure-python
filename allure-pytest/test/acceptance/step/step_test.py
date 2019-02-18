""" ./examples/step/step.rst """

from hamcrest import assert_that
from allure_commons_test.report import has_test_case
from allure_commons_test.result import has_step


def test_inline_step(executed_docstring_path):
    assert_that(executed_docstring_path.allure_report,
                has_test_case("test_inline_step",
                              has_step("inline step")
                              )
                )


def test_reusable_step(executed_docstring_path):
    assert_that(executed_docstring_path.allure_report,
                has_test_case("test_reusable_step",
                              has_step("passed_step")
                              )
                )


def test_nested_steps(executed_docstring_path):
    assert_that(executed_docstring_path.allure_report,
                has_test_case("test_nested_steps",
                              has_step("grand parent step",
                                       has_step("parent step",
                                                has_step("passed_step"
                                                         )
                                                )
                                       )
                              )
                )


def test_class_method_as_step(executed_docstring_path):
    assert_that(executed_docstring_path.allure_report,
                has_test_case("test_class_method_as_step",
                              has_step("class method as step")
                              )
                )
