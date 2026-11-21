import pytest
from hamcrest import assert_that
from tests.allure_pytest.pytest_runner import AllurePytestRunner

from allure_commons_test.report import has_test_case
from allure_commons_test.result import with_status
from allure_commons_test.result import has_status_details
from allure_commons_test.result import with_message_contains
from allure_commons_test.result import with_trace_contains


def test_xfail(allure_pytest_runner: AllurePytestRunner):
    """
    >>> import pytest

    >>> @pytest.mark.xfail()
    ... def test_xfail_example():
    ...     assert False

    """

    allure_results = allure_pytest_runner.run_docstring()

    assert_that(
        allure_results,
        has_test_case(
            "test_xfail_example",
            with_status("skipped"),
            has_status_details(
                with_message_contains("XFAIL"),
                with_message_contains("AssertionError"),
                with_trace_contains("def test_xfail_example():")
            )
        )
    )


def test_xfail_with_reason_raise_mentioned_exception(
    allure_pytest_runner: AllurePytestRunner
):
    """
    >>> import pytest

    >>> @pytest.mark.xfail(raises=AssertionError, reason='Some reason')
    ... def test_xfail_with_reason_raise_mentioned_exception_example():
    ...     assert False

    """

    allure_results = allure_pytest_runner.run_docstring()

    assert_that(
        allure_results,
        has_test_case(
            "test_xfail_with_reason_raise_mentioned_exception_example",
            with_status("skipped"),
            has_status_details(
                with_message_contains("XFAIL Some reason"),
                with_message_contains("AssertionError"),
                with_trace_contains(
                    "def test_xfail_with_reason_raise_mentioned_exception_example():"
                )
            )
        )
    )


def test_xfail_raise_not_mentioned_exception(
    allure_pytest_runner: AllurePytestRunner
):
    """
    >>> import pytest

    >>> @pytest.mark.xfail(raises=AssertionError)
    ... def test_xfail_raise_not_mentioned_exception_example():
    ...     raise ZeroDivisionError
    """

    allure_results = allure_pytest_runner.run_docstring()

    assert_that(
        allure_results,
        has_test_case(
            "test_xfail_raise_not_mentioned_exception_example",
            with_status("broken"),
            has_status_details(
                with_message_contains("ZeroDivisionError"),
                with_trace_contains(
                    "def test_xfail_raise_not_mentioned_exception_example():"
                )
            )
        )
    )


def test_xfail_do_not_raise_mentioned_exception(
    allure_pytest_runner: AllurePytestRunner
):
    """
    >>> import pytest

    >>> @pytest.mark.xfail(raises=AssertionError)
    ... def test_xfail_do_not_raise_mentioned_exception_example():
    ...     pass
    """

    allure_results = allure_pytest_runner.run_docstring()

    assert_that(
        allure_results,
        has_test_case(
            "test_xfail_do_not_raise_mentioned_exception_example",
            with_status("passed"),
            has_status_details(
                with_message_contains("XPASS"),
            )
        )
    )


def test_xfail_with_reason_do_not_raise_mentioned_exception(
    allure_pytest_runner: AllurePytestRunner
):
    """
    >>> import pytest

    >>> @pytest.mark.xfail(raises=AssertionError, reason="Some reason")
    ... def test_xfail_with_reason_do_not_raise_mentioned_exception_example():
    ...     pass
    """

    allure_results = allure_pytest_runner.run_docstring()

    assert_that(
        allure_results,
        has_test_case(
            "test_xfail_with_reason_do_not_raise_mentioned_exception_example",
            with_status("passed"),
            has_status_details(
                with_message_contains("XPASS Some reason"),
            )
        )
    )


@pytest.mark.parametrize("reason", [None, "Some reason"])
@pytest.mark.parametrize("strict_from_config", [False, True])
def test_xfail_mark_strict(allure_pytest_runner: AllurePytestRunner, reason, strict_from_config):
    marker_args = []
    if reason is not None:
        marker_args.append(f"reason={reason!r}")
    if not strict_from_config:
        marker_args.append("strict=True")
    marker_args = ", ".join(marker_args)
    cli_args = ("-o", "xfail_strict=true") if strict_from_config else ()
    allure_results = allure_pytest_runner.run_pytest(
        f"""
        import pytest

        @pytest.mark.xfail({marker_args})
        def test_xfail_mark_strict_example():
            pass
        """,
        cli_args=cli_args
    )

    message = f"[XPASS(strict)] {reason}" if reason else "[XPASS(strict)]"
    assert_that(
        allure_results,
        has_test_case(
            "test_xfail_mark_strict_example",
            with_status("failed"),
            has_status_details(with_message_contains(message))
        )
    )


def test_xfail_mark_strict_expected_failure(allure_pytest_runner: AllurePytestRunner):
    """
    >>> import pytest

    >>> @pytest.mark.xfail(reason="Some reason", strict=True)
    ... def test_xfail_mark_strict_expected_failure_example():
    ...     assert False
    """
    allure_results = allure_pytest_runner.run_docstring()

    assert_that(
        allure_results,
        has_test_case(
            "test_xfail_mark_strict_expected_failure_example",
            with_status("skipped"),
            has_status_details(
                with_message_contains("XFAIL Some reason"),
                with_message_contains("AssertionError"),
                with_trace_contains("def test_xfail_mark_strict_expected_failure_example():")
            )
        )
    )


def test_failure_mentioning_strict_xpass(allure_pytest_runner: AllurePytestRunner):
    """
    >>> def test_failure_mentioning_strict_xpass_example():
    ...     assert False, "[XPASS(strict)] is just an assertion message"
    """
    allure_results = allure_pytest_runner.run_docstring()

    assert_that(
        allure_results,
        has_test_case(
            "test_failure_mentioning_strict_xpass_example",
            with_status("failed"),
            has_status_details(
                with_message_contains("AssertionError: [XPASS(strict)] is just an assertion message"),
                with_trace_contains("def test_failure_mentioning_strict_xpass_example():")
            )
        )
    )
