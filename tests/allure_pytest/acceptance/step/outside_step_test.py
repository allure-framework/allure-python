import allure
from hamcrest import assert_that, not_
from tests.allure_pytest.pytest_runner import AllurePytestRunner

from allure_commons_test.report import has_test_case
from allure_commons_test.result import has_step
from allure_commons_test.container import has_container
from allure_commons_test.container import has_before


def test_step_from_init_py(allure_pytest_runner: AllurePytestRunner):
    allure_pytest_runner.pytester.makepyfile(__init__=(
        """
        import allure

        @allure.step("function in __init__ marked as step")
        def step_from__init__():
            pass
        """
    ))

    allure_results = allure_pytest_runner.run_pytest(
        """
        from . import step_from__init__

        def test_step_from_init_py_example():
            step_from__init__()
        """
    )

    assert_that(
        allure_results,
        has_test_case(
            "test_step_from_init_py_example",
            has_step("function in __init__ marked as step")
        )
    )


def test_fixture_with_step_from_conftest(allure_pytest_runner: AllurePytestRunner):
    conftest_content = (
        """
        import allure
        import pytest

        @allure.step("step in conftest.py")
        def conftest_step():
            pass


        @pytest.fixture
        def fixture_with_conftest_step():
            conftest_step()
        """
    )

    testfile_content = (
        """
        def test_fixture_with_step_from_conftest_example(fixture_with_conftest_step):
            pass
        """
    )

    allure_results = allure_pytest_runner.run_pytest(
        testfile_content,
        conftest_literal=conftest_content
    )

    assert_that(
        allure_results,
        has_test_case(
            "test_fixture_with_step_from_conftest_example",
            has_container(
                allure_results,
                has_before(
                    "fixture_with_conftest_step",
                    has_step("step in conftest.py")
                )
            )
        )
    )


@allure.issue("232")
def test_call_decorated_as_step_function(allure_pytest_runner: AllurePytestRunner):
    """
    >>> import allure

    >>> with allure.step("step outside"):
    ...     pass

    >>> def test_call_decorated_as_step_function_example():
    ...     pass
    """

    allure_results = allure_pytest_runner.run_docstring()

    assert_that(
        allure_results,
        has_test_case(
            "test_call_decorated_as_step_function_example",
            not_(
                has_step("step outside")
            )
        )
    )
