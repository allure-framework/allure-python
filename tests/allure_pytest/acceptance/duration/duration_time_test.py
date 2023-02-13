import allure
import pytest
from hamcrest import assert_that, has_entry, greater_than, all_of
from allure_commons_test.report import has_test_case
from allure_commons_test.result import with_status
from allure_commons.utils import now


snippets = [
    "pass",
    pytest.param("assert False", id="assert-fail"),
    pytest.param("raise RuntimeError()", id="break"),
    pytest.param("pytest.skip()", id="skip"),
    pytest.param("pytest.fail()", id="pytest-fail"),
    pytest.param("pytest.xfail()", id="xfail"),
    pytest.param("pytest.exit('msg')", id="exit"),
]


@pytest.mark.parametrize("snippet", snippets)
def test_duration(allured_testdir, snippet):
    allured_testdir.testdir.makepyfile(f"""
        def test_duration_example():
            {snippet}
    """)

    timestamp = now()
    allured_testdir.run_with_allure()

    assert_that(
        allured_testdir.allure_report,
        has_test_case(
            "test_duration_example",
            all_of(
                has_entry("start", greater_than(timestamp)),
                has_entry("stop", greater_than(timestamp))
            )
        )
    )


@allure.issue("244")
@pytest.mark.parametrize("snippet", snippets)
def test_with_fixture_duration(allured_testdir, snippet):
    allured_testdir.testdir.makepyfile(f"""
        import pytest

        @pytest.fixture
        def fixture():
            {snippet}

        def test_with_fixture_duration_example(fixture):
            pass
    """)

    timestamp = now()
    allured_testdir.run_with_allure()

    assert_that(
        allured_testdir.allure_report,
        has_test_case(
            "test_with_fixture_duration_example",
            all_of(
                has_entry("start", greater_than(timestamp)),
                has_entry("stop", greater_than(timestamp))
            )
        )
    )


@allure.issue("244")
@pytest.mark.parametrize("snippet", snippets)
def test_with_fixture_finalizer_duration(allured_testdir, snippet):
    allured_testdir.testdir.makepyfile(f"""
        import pytest

        @pytest.fixture
        def fixture(request):
            def finalizer():
                {snippet}
            request.addfinalizef(finalizer)

        def test_with_fixture_finalizer_duration(fixture):
            pass
    """)

    timestamp = now()
    allured_testdir.run_with_allure()

    assert_that(allured_testdir.allure_report,
                has_test_case("test_with_fixture_finalizer_duration",
                              all_of(
                                  has_entry("start", greater_than(timestamp)),
                                  has_entry("stop", greater_than(timestamp))
                              ))
                )


def test_test_skipped_if_fixture_exits(allured_testdir):
    """Test should be market as skipped: pytest reports it as 'not run'"""

    allured_testdir.testdir.makepyfile(f"""
        import pytest

        @pytest.fixture
        def fixture():
            pytest.exit("Reason")

        def test_with_fixture_duration_example(fixture):
            pass
    """)

    timestamp = now()
    allured_testdir.run_with_allure()

    assert_that(
        allured_testdir.allure_report,
        has_test_case(
            "test_with_fixture_duration_example",
            with_status("skipped")
        )
    )
