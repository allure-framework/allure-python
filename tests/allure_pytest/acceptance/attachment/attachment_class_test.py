from hamcrest import assert_that
from tests.allure_pytest.pytest_runner import AllurePytestRunner
from allure_commons_test.report import has_test_case
from allure_commons_test.result import has_attachment


def test_class_method_attachment(allure_pytest_runner: AllurePytestRunner):
    """
    >>> import allure

    >>> class TestClass:
    ...     def test_class_method_attachment(self):
    ...         allure.attach("text", "failed", allure.attachment_type.TEXT)
    """

    allure_report = allure_pytest_runner.run_docstring()

    assert_that(
        allure_report,
        has_test_case(
            "test_class_method_attachment",
            has_attachment(name="failed")
        )
    )
