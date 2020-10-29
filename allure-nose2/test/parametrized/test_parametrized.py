from nose2.tools import params
import unittest
from test.example_runner import run_docstring_example
from hamcrest import assert_that
from allure_commons_test.report import has_test_case
from allure_commons_test.result import has_parameter
from allure_commons.utils import represent


@params(
    (("alpha", "hello"), ("betta", 42)),
    (("alpha", "world"), ("betta", 777))
)
def test_parametrized_func(first, second):
    """
    >>> from nose2.tools import params

    >>> @params(("hello", 42), ("world", 777))
    ... def test_parametrized_func_example(alpha, betta):
    ...     pass
    """
    first_param_name, first_param_value = first
    second_param_name, second_param_value = second

    allure_report = run_docstring_example()
    assert_that(allure_report,
                has_test_case("test_parametrized_func_example",
                              has_parameter(first_param_name, represent(first_param_value)),
                              has_parameter(second_param_name, represent(second_param_value))
                              )
                )


class TestParametrized(unittest.TestCase):

    @params(
        (("bravo", {"hello": 4}), ("charlie", [4, 2])),
        (("bravo", {"wold": 2}), ("charlie", [7, 7, 7]))
    )
    def test_parametrized_method(self, first, second):
        """
        >>> import unittest
        >>> from nose2.tools import params

        >>> class TestParametrizedExample(unittest.TestCase):
        ...     @params(({"hello": 4}, [4, 2]), ({"wold": 2}, [7, 7, 7]))
        ...     def test_parametrized_method_example(self, bravo, charlie):
        ...         pass
        """
        first_param_name, first_param_value = first
        second_param_name, second_param_value = second

        allure_report = run_docstring_example()
        assert_that(allure_report,
                    has_test_case("test_parametrized_method_example",
                                  has_parameter(first_param_name, represent(first_param_value)),
                                  has_parameter(second_param_name, represent(second_param_value))
                                  )
                    )