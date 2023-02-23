from hamcrest import assert_that
from tests.allure_nose2.nose2_runner import AllureNose2Runner
from hamcrest import has_entry, has_item, has_property


def test_func_fullname(nose2_runner: AllureNose2Runner):
    """
    >>> def test_func_fullname_example():
    ...     pass
    """

    allure_report = nose2_runner.run_docstring()

    assert_that(
        allure_report,
        has_property(
            "test_cases",
            has_item(
                has_entry(
                    "fullName",
                    "test_func_fullname.test_func_fullname_example"
                )
            )
        )
    )


def test_method_fullname(nose2_runner: AllureNose2Runner):
    """
    >>> import unittest

    >>> class TestFullnameExample(unittest.TestCase):
    ...     def test_method_fullname_example(self):
    ...         pass
    """

    allure_report = nose2_runner.run_docstring()

    assert_that(
        allure_report,
        has_property(
            "test_cases",
            has_item(
                has_entry(
                    "fullName",
                    "test_method_fullname.TestFullnameExample.test_method_fullname_example"
                )
            )
        )
    )
