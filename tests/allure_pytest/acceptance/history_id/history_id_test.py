from hamcrest import assert_that
from tests.allure_pytest.pytest_runner import AllurePytestRunner

import allure
from allure_commons_test.report import has_test_case
from allure_commons_test.result import has_history_id


def test_history_id(allure_pytest_runner: AllurePytestRunner):
    """
    >>> def test_history_id_example():
    ...     assert True
    """

    allure_results = allure_pytest_runner.run_docstring()

    assert_that(
        allure_results,
        has_test_case(
            "test_history_id_example",
            has_history_id()
        )
    )


def test_history_id_for_skipped(allure_pytest_runner: AllurePytestRunner):
    """
    >>> import pytest

    >>> @pytest.mark.skip
    ... def test_history_id_for_skipped_example():
    ...     assert True
    """

    allure_results = allure_pytest_runner.run_docstring()

    assert_that(
        allure_results,
        has_test_case(
            "test_history_id_for_skipped_example",
            has_history_id()
        )
    )


@allure.issue("743", name="Issue 743")
def test_history_id_affected_by_allure_parameter(
    allure_pytest_runner: AllurePytestRunner
):
    """
    >>> import allure
    >>> from time import perf_counter

    >>> def test_allure_parameter_with_changing_value():
    ...     allure.dynamic.parameter("time", perf_counter())
    """

    first_run = allure_pytest_runner.run_docstring()
    second_run = allure_pytest_runner.run_docstring()

    assert __get_history_id(first_run) != __get_history_id(second_run)


@allure.issue("743", name="Issue 743")
def test_history_id_not_affected_by_excluded_parameter(
    allure_pytest_runner: AllurePytestRunner
):
    """
    >>> import allure
    >>> from time import perf_counter

    >>> def test_excluded_allure_parameter():
    ...     allure.dynamic.parameter("time", perf_counter(), excluded=True)
    """

    first_run = allure_pytest_runner.run_docstring()
    second_run = allure_pytest_runner.run_docstring()

    assert __get_history_id(first_run) == __get_history_id(second_run)


@allure.issue("744", name="Issue 744")
def test_history_id_not_affected_by_pytest_ids(
    allure_pytest_runner: AllurePytestRunner
):
    # We're using the trick with the same parameter here because it's not easy
    # to run pytester multiple times with different code due to caching of
    # python modules. In reality this change happens between runs
    run_result = allure_pytest_runner.run_pytest(
        """
        import pytest

        @pytest.mark.parametrize("v", [
            pytest.param(1),
            pytest.param(1, id="a")
        ])
        def test_two_allure_parameters(v):
            pass
        """
    )

    assert __get_history_id(run_result, 0) == __get_history_id(run_result, 1)


@allure.issue("743", name="Issue 743")
def test_different_byte_arrays_are_distinguishable(
    allure_pytest_runner: AllurePytestRunner
):
    """
    The 'allure_commons.utils.represent' function used to convert allure
    parameter values to strings makes all byte arrays indistinguishable.
    Some extra effort is required to properly calculate 'historyId' on tests
    that are parametrized with byte arrays.
    """
    run_result = allure_pytest_runner.run_pytest(
        """
        import pytest

        @pytest.mark.parametrize("v", [
            pytest.param(b'a'),
            pytest.param(b'b')
        ])
        def test_two_allure_parameters(v):
            pass
        """
    )

    assert __get_history_id(run_result, 0) != __get_history_id(run_result, 1)


def __get_history_id(run, index=0):
    return run.test_cases[index]["historyId"]
