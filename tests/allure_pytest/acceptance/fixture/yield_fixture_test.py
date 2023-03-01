
from hamcrest import assert_that, not_, all_of
from tests.allure_pytest.pytest_runner import AllurePytestRunner

import allure
from allure_commons_test.container import has_before
from allure_commons_test.container import has_container
from allure_commons_test.report import has_test_case
from allure_commons_test.result import has_step


@allure.feature("Fixture")
def test_yield_fixture(allure_pytest_runner: AllurePytestRunner):
    """
    >>> import pytest

    >>> @pytest.fixture
    ... def yield_fixture():
    ...     yield

    >>> def test_yield_fixture_example(yield_fixture):
    ...     pass
    """

    allure_results = allure_pytest_runner.run_docstring()

    assert_that(
        allure_results,
        has_test_case(
            "test_yield_fixture_example",
            has_container(
                allure_results,
                has_before("yield_fixture")
            )
        )
    )


def test_opened_step_function(allure_pytest_runner: AllurePytestRunner):
    """
    >>> import allure
    >>> import pytest

    >>> @pytest.fixture()
    ... def yield_fixture():
    ...     with allure.step("Opened step"):
    ...         yield

    >>> def test_opened_step(yield_fixture):
    ...     with allure.step("Body step"):
    ...         pass
    """

    allure_results = allure_pytest_runner.run_docstring()

    assert_that(
        allure_results,
        has_test_case(
            "test_opened_step",
            all_of(
                has_step("Body step"),
                has_container(
                    allure_results,
                    has_before(
                        "yield_fixture",
                        has_step(
                            "Opened step",
                            not_(has_step("Body step"))
                        )
                    )
                )
            )
        )
    )
