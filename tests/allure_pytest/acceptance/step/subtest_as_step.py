from hamcrest import assert_that
from tests.allure_pytest.pytest_runner import AllurePytestRunner

from allure_commons_test.report import has_test_case
from allure_commons_test.result import has_step
from allure_commons_test.result import with_status
from allure_commons_test.result import with_message_contains
from allure_commons_test.result import has_status_details


def test_with_subtest(allure_pytest_runner: AllurePytestRunner):
    """
    >>> import allure
    >>> import pytest
    >>> @pytest.mark.skipif("pytest.__version__[0] < '9'")
    >>> def test_with_subtest(subtests):
    ...    with subtests.test(msg='Some failed subtest'):
    ...        assert False, 'Some error'
    ...    with allure.step('Next step'):
    ...        pass
    """

    allure_results = allure_pytest_runner.run_docstring()

    assert_that(
        allure_results,
        has_test_case(
            "test_with_subtest",
            has_step(
                "Some failed subtest",
                with_status("failed"),
                has_status_details(
                    with_message_contains("Some error")
                )
            ),
            has_step(
                "Next step",
                with_status("passed")
            ),
            with_status("failed")
        )
    )


def test_with_subtest_without_msg(allure_pytest_runner: AllurePytestRunner):
    """
    >>> import allure
    >>> import pytest
    >>> @pytest.mark.skipif("pytest.__version__[0] < '9'")
    >>> def test_with_subtest_without_msg(subtests):
    ...    with subtests.test():
    ...        pass
    """

    allure_results = allure_pytest_runner.run_docstring()

    assert_that(
        allure_results,
        has_test_case(
            "test_with_subtest_without_msg",
            has_step(
                "test_with_subtest_without_msg (<subtest>)",
            ),
        )
    )
