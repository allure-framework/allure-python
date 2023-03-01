from hamcrest import assert_that
from hamcrest import all_of
from hamcrest import equal_to
from tests.allure_pytest.pytest_runner import AllurePytestRunner

from allure_commons_test.report import has_test_case
from allure_commons_test.result import has_attachment_with_content


def test_parametrized_attachment(allure_pytest_runner: AllurePytestRunner):
    """
    >>> import pytest
    >>> import allure

    >>> @pytest.mark.parametrize("param", ["first", "second"])
    ... def test_parametrized_attachment_example(param):
    ...     allure.attach(param)
    """

    allure_results = allure_pytest_runner.run_docstring()

    assert_that(
        allure_results,
        all_of(
            has_test_case(
                "test_parametrized_attachment_example[first]",
                has_attachment_with_content(
                    allure_results.attachments,
                    content_matcher=equal_to("first")
                )
            ),
            has_test_case(
                "test_parametrized_attachment_example[second]",
                has_attachment_with_content(
                    allure_results.attachments,
                    content_matcher=equal_to("second")
                )
            )
        )
    )
