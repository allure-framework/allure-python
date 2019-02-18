import allure
from hamcrest import assert_that, not_
from allure_commons_test.report import has_test_case
from allure_commons_test.result import has_step
from allure_commons_test.container import has_container
from allure_commons_test.container import has_before


def test_step_from_init_py(allured_testdir):
    allured_testdir.testdir.makepyfile(__init__="""
        import allure

        @allure.step("function in __init__ marked as step")
        def step_from__init__():
            pass
    """)

    allured_testdir.testdir.makepyfile("""
        from . import step_from__init__

        def test_step_from_init_py_example():
            step_from__init__()
    """)

    allured_testdir.run_with_allure()

    assert_that(allured_testdir.allure_report,
                has_test_case("test_step_from_init_py_example",
                              has_step("function in __init__ marked as step")
                              )
                )


def test_fixture_with_step_from_conftest(allured_testdir):
    allured_testdir.testdir.makeconftest("""
        import allure
        import pytest

        @allure.step("step in conftest.py")
        def conftest_step():
            pass


        @pytest.fixture
        def fixture_with_conftest_step():
            conftest_step()
    """)

    allured_testdir.testdir.makepyfile("""
        def test_fixture_with_step_from_conftest_example(fixture_with_conftest_step):
            pass
    """)

    allured_testdir.run_with_allure()

    assert_that(allured_testdir.allure_report,
                has_test_case("test_fixture_with_step_from_conftest_example",
                              has_container(allured_testdir.allure_report,
                                            has_before("fixture_with_conftest_step",
                                                       has_step("step in conftest.py")
                                                       )
                                            )
                              )
                )


@allure.issue("232")
def test_call_decorated_as_step_function(executed_docstring_source):
    """
    >>> import allure

    >>> with allure.step("step outside"):
    ...     pass

    >>> def test_call_decorated_as_step_function_example():
    ...     pass
    """

    assert_that(executed_docstring_source.allure_report,
                has_test_case("test_call_decorated_as_step_function_example",
                              not_(has_step("step outside"))
                              )
                )
