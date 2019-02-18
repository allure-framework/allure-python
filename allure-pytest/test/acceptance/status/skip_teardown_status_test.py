from hamcrest import assert_that
from allure_commons_test.report import has_test_case
from allure_commons_test.result import with_status
from allure_commons_test.result import has_status_details
from allure_commons_test.result import with_message_contains
from allure_commons_test.result import with_trace_contains
from allure_commons_test.container import has_container
from allure_commons_test.container import has_after


def test_skip_finalizer_fixture(executed_docstring_source):
    """
    >>> import pytest

    >>> @pytest.fixture
    ... def skip_finalizer_fixture(request):
    ...     def fixture_finalizer():
    ...         pytest.skip()
    ...     request.addfinalizer(fixture_finalizer)

    >>> def test_skip_finalizer_fixture_example(skip_finalizer_fixture):
    ...     pass
    """

    assert_that(executed_docstring_source.allure_report,
                has_test_case("test_skip_finalizer_fixture_example",
                              with_status("passed"),
                              has_container(executed_docstring_source.allure_report,
                                            has_after("{fixture}::{finalizer}".format(
                                                fixture="skip_finalizer_fixture",
                                                finalizer="fixture_finalizer"),
                                                with_status("skipped"),
                                                has_status_details(with_message_contains("Skipped: <Skipped instance>"),
                                                                   with_trace_contains("fixture_finalizer")
                                                                   ),
                                            ),
                                            )
                              )
                )
