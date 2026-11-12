from hamcrest import assert_that, ends_with, matches_regexp, not_
from allure_commons_test.container import has_after, has_container
from allure_commons_test.report import has_test_case
from allure_commons_test.result import with_status


def test_yield_fixture_has_no_phantom_internal_finalizer(allure_pytest_runner):
    """
    >>> import pytest

    >>> @pytest.fixture
    ... def yield_fixture():
    ...     yield
    ...     pass

    >>> def test_example(yield_fixture):
    ...     pass
    """
    allure_results = allure_pytest_runner.run_docstring()

    assert_that(
        allure_results,
        has_test_case(
            "test_example",
            has_container(
                allure_results,
                has_after(
                    matches_regexp(r"^yield_fixture::\d+$"),
                    with_status("passed")
                ),
                not_(
                    has_after(
                        ends_with("::<lambda>")
                    )
                )
            )
        )
    )


def test_user_lambda_finalizer_is_still_reported(allure_pytest_runner):
    """
    >>> import pytest

    >>> @pytest.fixture
    ... def custom_lambda_fixture(request):
    ...     request.addfinalizer(lambda: None)
    ...     yield

    >>> def test_example(custom_lambda_fixture):
    ...     pass
    """
    allure_results = allure_pytest_runner.run_docstring()

    assert_that(
        allure_results,
        has_test_case(
            "test_example",
            has_container(
                allure_results,
                has_after(
                    matches_regexp(r"^custom_lambda_fixture::\d+$"),
                    with_status("passed")
                ),
                has_after(
                    "custom_lambda_fixture::<lambda>",
                    with_status("passed")
                )
            )
        )
    )
