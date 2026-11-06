import allure
from hamcrest import assert_that
from tests.allure_pytest.pytest_runner import AllurePytestRunner

from allure_commons_test.report import has_test_case
from allure_commons_test.container import has_container
from allure_commons_test.container import has_after


def afters_of(allure_results):
    return [
        after
        for container in allure_results.test_containers
        for after in container.get("afters", [])
    ]


@allure.feature("Fixture")
@allure.story("Fixture finalizer")
def test_pytest_internal_finalizer_is_not_reported(allure_pytest_runner: AllurePytestRunner):
    """
    >>> import pytest

    pytest attaches its own finalizer to every fixture from 9.1 onwards, inside
    ``FixtureDef.execute``. It is machinery, not a teardown anyone wrote:
    >>> @pytest.fixture
    ... def plain_fixture():
    ...     yield

    >>> def test_plain_fixture_example(plain_fixture):
    ...     pass
    """

    allure_results = allure_pytest_runner.run_docstring()

    unreported = [after for after in afters_of(allure_results) if after.get("status") is None]

    assert_that(unreported == [], f"expected no statusless afterStage, got {unreported}")


@allure.feature("Fixture")
@allure.story("Fixture finalizer")
def test_user_lambda_finalizer_is_still_reported(allure_pytest_runner: AllurePytestRunner):
    """
    A finalizer is skipped based on which module owns it, never on its name, so a
    lambda registered by the test author is still a real teardown and is reported.

    >>> import pytest

    >>> @pytest.fixture
    ... def fixture_with_lambda_finalizer(request):
    ...     request.addfinalizer(lambda: None)

    >>> def test_fixture_with_lambda_finalizer_example(fixture_with_lambda_finalizer):
    ...     pass
    """

    allure_results = allure_pytest_runner.run_docstring()

    assert_that(
        allure_results,
        has_test_case(
            "test_fixture_with_lambda_finalizer_example",
            has_container(
                allure_results,
                has_after("fixture_with_lambda_finalizer::<lambda>")
            )
        )
    )
