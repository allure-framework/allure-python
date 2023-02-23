from hamcrest import assert_that
from tests.allure_pytest.pytest_runner import AllurePytestRunner

from allure_commons_test.report import has_test_case
from allure_commons_test.result import has_step
from allure_commons_test.result import has_parameter


def test_step_parameters(allure_pytest_runner: AllurePytestRunner):
    """
    >>> import pytest
    >>> import allure

    >>> @allure.step
    ... def step(arg, kwarg=None):
    ...     pass

    >>> @pytest.mark.parametrize(
    ...     ["args", "kwargs"],
    ...     [
    ...         ([True], {"kwarg": False}),
    ...         (["hi"], {"kwarg": None}),
    ...         ([None], {"kwarg": 42})
    ...     ]
    ... )
    ... def test_step_parameters(args, kwargs):
    ...     step(*args, **kwargs)
    """

    allure_results = allure_pytest_runner.run_docstring()

    assert_that(
        allure_results,
        has_test_case(
            "test_step_parameters[args0-kwargs0]",
            has_step(
                "step",
                has_parameter("arg", "True"),
                has_parameter("kwarg", "False")
            )
        )
    )
