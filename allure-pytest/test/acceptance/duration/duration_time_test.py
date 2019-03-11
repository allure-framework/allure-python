import allure
import pytest
from hamcrest import assert_that, has_entry, greater_than, all_of
from allure_commons_test.report import has_test_case
from allure_commons.utils import now


snippets = [
    "pass",
    "assert False",
    "raise(RuntimeError())",
    "pytest.skip()",
    "pytest.fail()",
    "pytest.xfail()",
    pytest.param("pytest.exit('msg')", marks=pytest.mark.skip)
]


@pytest.mark.parametrize("snipped", snippets)
def test_duration(allured_testdir, snipped):
    allured_testdir.testdir.makepyfile("""
        def test_duration_example():
            {snipped}
    """.format(snipped=snipped))

    timestamp = now()
    allured_testdir.run_with_allure()

    assert_that(allured_testdir.allure_report,
                has_test_case("test_duration_example",
                              all_of(
                                  has_entry("start", greater_than(timestamp)),
                                  has_entry("stop", greater_than(timestamp))
                              ))
                )


@allure.issue("244")
@pytest.mark.parametrize("snipped", snippets)
def test_with_fixture_duration(allured_testdir, snipped):
    allured_testdir.testdir.makepyfile("""
        import pytest

        @pytest.fixture
        def fixture():
            {snipped}

        def test_with_fixture_duration_example(fixture):
            pass
    """.format(snipped=snipped))

    timestamp = now()
    allured_testdir.run_with_allure()

    assert_that(allured_testdir.allure_report,
                has_test_case("test_with_fixture_duration_example",
                              all_of(
                                  has_entry("start", greater_than(timestamp)),
                                  has_entry("stop", greater_than(timestamp))
                              ))
                )


@allure.issue("244")
@pytest.mark.parametrize("snipped", snippets)
def test_with_fixture_finalizer_duration(allured_testdir, snipped):
    allured_testdir.testdir.makepyfile("""
        import pytest

        @pytest.fixture
        def fixture(request):
            def finalizer():
                {snipped}
            request.addfinalizef(finalizer)

        def test_with_fixture_finalizer_duration(fixture):
            pass
    """.format(snipped=snipped))

    timestamp = now()
    allured_testdir.run_with_allure()

    assert_that(allured_testdir.allure_report,
                has_test_case("test_with_fixture_finalizer_duration",
                              all_of(
                                  has_entry("start", greater_than(timestamp)),
                                  has_entry("stop", greater_than(timestamp))
                              ))
                )
