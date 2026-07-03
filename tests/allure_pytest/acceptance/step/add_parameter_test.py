from hamcrest import assert_that
from tests.allure_pytest.pytest_runner import AllurePytestRunner

from allure_commons_test.report import has_test_case
from allure_commons_test.result import has_step
from allure_commons_test.result import has_parameter
from allure_commons_test.result import get_parameter_matcher
from allure_commons_test.result import with_mode
from allure_commons_test.result import with_excluded
from allure_commons_test.result import with_status


def test_add_parameter_context_manager(allure_pytest_runner: AllurePytestRunner):
    """
    >>> import allure

    >>> def test_add_parameter_context_manager():
    ...     with allure.step("Step 1"):
    ...         allure.add_parameter("env", "production")
    ...         allure.add_parameter("version", "1.0.0")
    """
    allure_results = allure_pytest_runner.run_docstring()

    assert_that(
        allure_results,
        has_test_case(
            "test_add_parameter_context_manager",
            has_step(
                "Step 1",
                has_parameter("env", "'production'"),
                has_parameter("version", "'1.0.0'")
            )
        )
    )


def test_add_parameter_decorator(allure_pytest_runner: AllurePytestRunner):
    """
    >>> import allure

    >>> @allure.step("Step 2")
    ... def decorated_step():
    ...     allure.add_parameter("decorated_param", "decorated_value")

    >>> def test_add_parameter_decorator():
    ...     decorated_step()
    """
    allure_results = allure_pytest_runner.run_docstring()

    assert_that(
        allure_results,
        has_test_case(
            "test_add_parameter_decorator",
            has_step(
                "Step 2",
                has_parameter("decorated_param", "'decorated_value'")
            )
        )
    )


def test_add_parameter_nested(allure_pytest_runner: AllurePytestRunner):
    """
    >>> import allure

    >>> def test_add_parameter_nested():
    ...     with allure.step("Parent Step"):
    ...         with allure.step("Child Step"):
    ...             allure.add_parameter("nested_param", "nested_value")
    """
    allure_results = allure_pytest_runner.run_docstring()

    assert_that(
        allure_results,
        has_test_case(
            "test_add_parameter_nested",
            has_step(
                "Parent Step",
                has_step(
                    "Child Step",
                    has_parameter("nested_param", "'nested_value'")
                )
            )
        )
    )


def test_add_parameter_no_active_step_raises_error(allure_pytest_runner: AllurePytestRunner):
    """
    >>> import allure

    >>> def test_add_parameter_no_active_step_raises_error():
    ...     try:
    ...         allure.add_parameter("test", "value")
    ...         assert False, "Should raise RuntimeError"
    ...     except RuntimeError:
    ...         pass  # Expected error
    """
    allure_results = allure_pytest_runner.run_docstring()

    assert_that(
        allure_results,
        has_test_case(
            "test_add_parameter_no_active_step_raises_error",
            with_status("passed")
        )
    )


def test_add_parameter_with_mode(allure_pytest_runner: AllurePytestRunner):
    """
    >>> import allure

    >>> def test_add_parameter_with_mode():
    ...     with allure.step("Step 1"):
    ...         allure.add_parameter(
    ...             "password", "secret", mode=allure.parameter_mode.MASKED
    ...         )
    """
    allure_results = allure_pytest_runner.run_docstring()

    assert_that(
        allure_results,
        has_test_case(
            "test_add_parameter_with_mode",
            has_step(
                "Step 1",
                get_parameter_matcher(
                    "password",
                    with_mode("masked")
                )
            )
        )
    )


def test_add_parameter_hidden_mode(allure_pytest_runner: AllurePytestRunner):
    """
    >>> import allure

    >>> def test_add_parameter_hidden_mode():
    ...     with allure.step("Step 1"):
    ...         allure.add_parameter(
    ...             "environment", "staging", mode=allure.parameter_mode.HIDDEN
    ...         )
    """
    allure_results = allure_pytest_runner.run_docstring()

    assert_that(
        allure_results,
        has_test_case(
            "test_add_parameter_hidden_mode",
            has_step(
                "Step 1",
                get_parameter_matcher(
                    "environment",
                    with_mode("hidden")
                )
            )
        )
    )


def test_add_parameter_excluded(allure_pytest_runner: AllurePytestRunner):
    """
    >>> import allure

    >>> def test_add_parameter_excluded():
    ...     with allure.step("Step 1"):
    ...         allure.add_parameter("work-dir", "/tmp", excluded=True)
    """
    allure_results = allure_pytest_runner.run_docstring()

    assert_that(
        allure_results,
        has_test_case(
            "test_add_parameter_excluded",
            has_step(
                "Step 1",
                get_parameter_matcher(
                    "work-dir",
                    with_excluded()
                )
            )
        )
    )


def test_add_parameter_multiple(allure_pytest_runner: AllurePytestRunner):
    """
    >>> import allure

    >>> def test_add_parameter_multiple():
    ...     with allure.step("Step 1"):
    ...         allure.add_parameter("env", "staging")
    ...         allure.add_parameter("version", "1.0.0")
    ...         allure.add_parameter("host", "localhost")
    """
    allure_results = allure_pytest_runner.run_docstring()

    assert_that(
        allure_results,
        has_test_case(
            "test_add_parameter_multiple",
            has_step(
                "Step 1",
                has_parameter("env", "'staging'"),
                has_parameter("version", "'1.0.0'"),
                has_parameter("host", "'localhost'")
            )
        )
    )


def test_add_parameter_vs_test_parameter(allure_pytest_runner: AllurePytestRunner):
    """
    >>> import allure

    >>> def test_add_parameter_vs_test_parameter():
    ...     allure.dynamic.parameter("test_param", "test_value")
    ...     with allure.step("Step 1"):
    ...         allure.add_parameter("step_param", "step_value")
    """
    allure_results = allure_pytest_runner.run_docstring()

    assert_that(
        allure_results,
        has_test_case(
            "test_add_parameter_vs_test_parameter",
            has_parameter("test_param", "'test_value'"),
            has_step(
                "Step 1",
                has_parameter("step_param", "'step_value'")
            )
        )
    )
