""" ./examples/label/severity/module_severity.rst """

from hamcrest import assert_that
from allure_commons_test.report import has_test_case
from allure_commons_test.label import has_severity


def test_not_decorated_function(executed_docstring_path):
    assert_that(executed_docstring_path.allure_report,
                has_test_case("test_not_decorated_function",
                              has_severity("trivial")
                              )
                )


def test_decorated_function(executed_docstring_path):
    assert_that(executed_docstring_path.allure_report,
                has_test_case("test_decorated_function",
                              has_severity("minor")
                              )
                )


def test_method_of_not_decorated_class(executed_docstring_path):
    assert_that(executed_docstring_path.allure_report,
                has_test_case("test_method_of_not_decorated_class",
                              has_severity("trivial")
                              )
                )


def test_method_of_decorated_class(executed_docstring_path):
    assert_that(executed_docstring_path.allure_report,
                has_test_case("test_method_of_decorated_class",
                              has_severity("normal")
                              )
                )
