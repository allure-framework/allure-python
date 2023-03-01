from hamcrest import assert_that, all_of
from tests.allure_nose2.nose2_runner import AllureNose2Runner

from allure_commons_test.report import has_test_case
from allure_commons_test.result import has_parameter


def test_parametrized_func(nose2_runner: AllureNose2Runner):
    """
    >>> from nose2.tools import params

    >>> @params(("hello", 42), ("world", 777))
    ... def test_parametrized_func_example(alpha, betta):
    ...     pass
    """

    allure_report = nose2_runner.run_docstring()

    assert_that(
        allure_report,
        all_of(
            has_test_case(
                "test_parametrized_func_example",
                has_parameter("alpha", "'hello'"),
                has_parameter("betta", "42")
            ),
            has_test_case(
                "test_parametrized_func_example",
                has_parameter("alpha", "'world'"),
                has_parameter("betta", "777")
            )
        )
    )


def test_parametrized_method(nose2_runner: AllureNose2Runner):
    """
    >>> import unittest
    >>> from nose2.tools import params

    >>> class TestParametrizedExample(unittest.TestCase):
    ...     @params(({"hello": 4}, [4, 2]), ({"wold": 2}, [7, 7, 7]))
    ...     def test_parametrized_method_example(self, bravo, charlie):
    ...         pass
    """

    allure_report = nose2_runner.run_docstring()

    assert_that(
        allure_report,
        all_of(
            has_test_case(
                "test_parametrized_method_example",
                has_parameter("bravo", "{'hello': 4}"),
                has_parameter("charlie", "[4, 2]")
            )
        )
    )
