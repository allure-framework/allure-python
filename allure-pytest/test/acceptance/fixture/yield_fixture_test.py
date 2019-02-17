import allure
from hamcrest import assert_that
from allure_commons_test.report import has_test_case
from allure_commons_test.container import has_container
from allure_commons_test.container import has_before


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
