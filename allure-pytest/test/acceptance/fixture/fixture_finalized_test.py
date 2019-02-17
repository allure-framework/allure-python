import allure
from hamcrest import assert_that
from allure_commons_test.report import has_test_case
from allure_commons_test.container import has_container
from allure_commons_test.container import has_before, has_after


@allure.feature("Fixture")
@allure.story("Fixture finalizer")
def test_fixture_finalizer(executed_docstring_source):
    """
    >>> import pytest

    Let"s define fixture with finalizer:
    >>> @pytest.fixture
    ... def fixture_with_finalizer(request):
    ...     def finalizer():
    ...         pass
    ...     request.addfinalizer(finalizer)

    For next test, allure will report fixture finalizer in TearDown section
    >>> def test_fixture_with_finalizer_example(fixture_with_finalizer):
    ...     pass
    """

    assert_that(executed_docstring_source.allure_report,
                has_test_case("test_fixture_with_finalizer_example",
                              has_container(executed_docstring_source.allure_report,
                                            has_before("fixture_with_finalizer"),
                                            has_after("{fixture}::{finalizer}".format(fixture="fixture_with_finalizer",
                                                                                      finalizer="finalizer")
                                                      )
                                            )
                              )
                )


@allure.feature("Fixture")
@allure.story("Fixture finalizer")
def test_fixture_finalizers(executed_docstring_source):
    """
    >>> import pytest

    In pytest, you can define several finalizers for one fixture, like this:
    >>> @pytest.fixture
    ... def fixture_with_finalizers(request):
    ...     def first_finalizer():
    ...         pass
    ...     request.addfinalizer(first_finalizer)
    ...
    ...     def second_finalizer():
    ...         pass
    ...     request.addfinalizer(second_finalizer)

    Of course, allure will report all of them
    >>> def test_fixture_with_finalizers_example(fixture_with_finalizers):
    ...     pass
    """

    assert_that(executed_docstring_source.allure_report,
                has_test_case("test_fixture_with_finalizers_example",
                              has_container(executed_docstring_source.allure_report,
                                            has_before("fixture_with_finalizers"),
                                            has_after("{fixture}::{finalizer}".format(fixture="fixture_with_finalizers",
                                                                                      finalizer="first_finalizer")
                                                      ),
                                            has_after("{fixture}::{finalizer}".format(fixture="fixture_with_finalizers",
                                                                                      finalizer="second_finalizer"),
                                                      )
                                            )
                              )
                )
