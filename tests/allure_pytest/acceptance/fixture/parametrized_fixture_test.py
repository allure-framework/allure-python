from hamcrest import assert_that, all_of
from tests.allure_pytest.pytest_runner import AllurePytestRunner

from allure_commons_test.report import has_test_case
from allure_commons_test.container import has_container
from allure_commons_test.container import has_before
from allure_commons_test.result import has_parameter


def params_name(request):
    node_id = request.node.nodeid
    _, name = node_id.rstrip("]").split("[")
    return name


def test_function_scope_parametrized_fixture(allure_pytest_runner: AllurePytestRunner):
    """
    >>> import pytest

    >>> @pytest.fixture(params=[True, False])
    ... def parametrized_fixture(request):
    ...     pass

    >>> def test_function_scope_parametrized_fixture_example(parametrized_fixture):
    ...     pass
    """

    allure_results = allure_pytest_runner.run_docstring()

    assert_that(
        allure_results,
        all_of(
            has_test_case(
                "test_function_scope_parametrized_fixture_example[True]",
                has_parameter(
                    "parametrized_fixture",
                    "True"
                ),
                has_container(
                    allure_results,
                    has_before("parametrized_fixture")
                )
            ),
            has_test_case(
                "test_function_scope_parametrized_fixture_example[False]",
                has_parameter(
                    "parametrized_fixture",
                    "False"
                ),
                has_container(
                    allure_results,
                    has_before("parametrized_fixture")
                )
            )
        )
    )


def test_function_scope_parametrized_fixture_with_ids(
    allure_pytest_runner: AllurePytestRunner
):
    """
    >>> import pytest

    >>> @pytest.fixture(params=[True, False], ids=["param_true", "param_false"])
    ... def parametrized_fixture(request):
    ...     pass

    >>> def test_function(parametrized_fixture):
    ...     pass
    """

    allure_results = allure_pytest_runner.run_docstring()

    assert_that(
        allure_results,
        all_of(
            has_test_case(
                "test_function[param_true]",
                has_parameter("parametrized_fixture", "True"),
                has_container(
                    allure_results,
                    has_before("parametrized_fixture")
                )
            ),
            has_test_case(
                "test_function[param_false]",
                has_parameter("parametrized_fixture", "False"),
                has_container(
                    allure_results,
                    has_before("parametrized_fixture")
                )
            )
        )
    )
