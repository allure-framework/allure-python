from hamcrest import assert_that
from allure_commons_test.report import has_test_case
from allure_commons_test.result import has_attachment


def test_class_method_attachment(executed_docstring_source):
    """
    >>> import allure

    >>> class TestClass(object):
    ...     def test_class_method_attachment(self):
    ...         allure.attach("text", "failed", allure.attachment_type.TEXT)
    """

    assert_that(executed_docstring_source.allure_report,
                has_test_case("test_class_method_attachment",
                              has_attachment(name="failed")
                              )
                )
