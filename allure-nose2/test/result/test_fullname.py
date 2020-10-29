import unittest
from hamcrest import assert_that
from test.example_runner import run_docstring_example
from hamcrest import has_entry, has_item, has_property


def test_func_fullname():
    """
    >>> def test_func_fullname_example():
    ...     pass
    """
    allure_report = run_docstring_example()
    assert_that(allure_report,
                has_property("test_cases",
                             has_item(
                                 has_entry("fullName", "example_module.test_func_fullname_example")
                             )
                             )
                )


class TestFullname(unittest.TestCase):
    def test_method_fullname(self):
        """
        >>> import unittest

        >>> class TestFullnameExample(unittest.TestCase):
        ...     def test_method_fullname_example(self):
        ...         pass
        """
        allure_report = run_docstring_example()
        assert_that(allure_report,
                    has_property("test_cases",
                                 has_item(
                                     has_entry("fullName",
                                               "example_module.TestFullnameExample.test_method_fullname_example")
                                 )
                                 )
                    )