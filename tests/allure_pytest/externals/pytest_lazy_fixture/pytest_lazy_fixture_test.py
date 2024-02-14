import pytest
from hamcrest import assert_that
from tests.allure_pytest.pytest_runner import AllurePytestRunner

import allure
from allure_commons_test.report import has_test_case
from allure_commons_test.container import has_container
from allure_commons_test.container import has_before

from packaging import version

pytestmark = pytest.mark.xfail(
    version.parse(pytest.__version__) >= version.parse("8"),
    reason=(
        "Lazy-fixture is incompatible with pytest 8 "
        "(see TvoroG/pytest-lazy-fixture#65)"
    ),
)


@pytest.fixture
def lazy_fixture_runner(allure_pytest_runner: AllurePytestRunner):
    allure_pytest_runner.enable_plugins("lazy-fixture")
    yield allure_pytest_runner


@allure.feature("Integration")
def test_lazy_fixture(lazy_fixture_runner: AllurePytestRunner):
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

    output = lazy_fixture_runner.run_docstring()

    assert_that(
        output,
        has_test_case(
            "test_lazy_fixture_example",
            has_container(
                output,
                has_before("my_lazy_fixture")
            )
        )
    )


@allure.feature("Integration")
def test_nested_lazy_fixture(lazy_fixture_runner: AllurePytestRunner):
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

    output = lazy_fixture_runner.run_docstring()

    assert_that(
        output,
        has_test_case(
            "test_nested_lazy_fixture_example",
            has_container(
                output,
                has_before("my_lazy_fixture")
            )
        )
    )
