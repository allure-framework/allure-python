import allure
from allure_commons_test.container import has_before
from allure_commons_test.container import has_container
from allure_commons_test.report import has_test_case
from allure_commons_test.result import has_step
from hamcrest import assert_that, not_, all_of


@allure.feature("Fixture")
def test_yield_fixture(executed_docstring_source):
    """
    >>> import pytest

    >>> @pytest.fixture
    ... def yield_fixture():
    ...     pass

    >>> def test_yield_fixture_example(yield_fixture):
    ...     pass
    """

    assert_that(executed_docstring_source.allure_report,
                has_test_case("test_yield_fixture_example",
                              has_container(executed_docstring_source.allure_report,
                                            has_before("yield_fixture")
                                            ),
                              )
                )


def test_opened_step_function(executed_docstring_source):
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

    assert_that(
        executed_docstring_source.allure_report,
        has_test_case(
            "test_opened_step",
            all_of(
                has_step("Body step"),
                has_container(
                    executed_docstring_source.allure_report,
                    has_before(
                        "yield_fixture",
                        has_step(
                            "Opened step",
                            not_(has_step("Body step"))
                        )
                    )
                ),
            )
        )
    )
