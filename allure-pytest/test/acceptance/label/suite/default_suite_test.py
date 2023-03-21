import pytest
from hamcrest import assert_that, anything, not_
from allure_commons_test.report import has_test_case
from allure_commons_test.label import has_parent_suite
from allure_commons_test.label import has_suite
from allure_commons_test.label import has_sub_suite


@pytest.mark.skip
def test_default_suite(executed_docstring_source):
    """
    >>> def test_default_suite_example():
    ...     pass
    """

    assert_that(executed_docstring_source.allure_report,
                has_test_case("test_default_suite_example",
                              has_parent_suite(anything()),  # path to testdir
                              has_suite("test_default_suite"),  # created file name
                              not_(has_sub_suite(anything()))
                              )
                )


@pytest.mark.skip
def test_default_class_suite(executed_docstring_source):
    """
    >>> class TestSuiteClass(object):
    ...     def test_default_class_suite_example(self):
    ...         pass

    """

    assert_that(executed_docstring_source.allure_report,
                has_test_case("test_default_class_suite_example",
                              has_parent_suite(anything()),  # path to testdir
                              has_suite("test_default_class_suite"),  # created file name
                              has_sub_suite("TestSuiteClass")
                              )
                )
