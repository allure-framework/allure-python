import allure
from hamcrest import assert_that
from allure_commons_test.report import has_test_case
from allure_commons_test.container import has_container
from allure_commons_test.container import has_before


@allure.feature("Integration")
def test_lazy_fixture(executed_docstring_source):
    """
    >>> import pytest
    ... from pytest_lazyfixture import lazy_fixture

    >>> @pytest.fixture
    ... def my_lazy_fixture():
    ...     pass

    >>> @pytest.mark.parametrize('param', [lazy_fixture('my_lazy_fixture')])
    ... def test_lazy_fixture_example(param):
    ...     pass
    """

    assert_that(executed_docstring_source.allure_report,
                has_test_case("test_lazy_fixture_example",
                              has_container(executed_docstring_source.allure_report,
                                            has_before("my_lazy_fixture")
                                            ),
                              )
                )


@allure.feature("Integration")
def test_nested_lazy_fixture(executed_docstring_source):
    """
    >>> import pytest
    ... from pytest_lazyfixture import lazy_fixture

    >>> @pytest.fixture
    ... def my_lazy_fixture():
    ...     pass

    >>> @pytest.fixture(params=[lazy_fixture('my_lazy_fixture')])
    ... def my_ordinary_fixture():
    ...     pass

    >>> def test_nested_lazy_fixture_example(my_ordinary_fixture):
    ...     pass
    """

    assert_that(executed_docstring_source.allure_report,
                has_test_case("test_nested_lazy_fixture_example",
                              has_container(executed_docstring_source.allure_report,
                                            has_before("my_lazy_fixture")
                                            ),
                              )
                )
