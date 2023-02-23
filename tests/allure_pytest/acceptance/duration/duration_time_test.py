import allure
import pytest
from hamcrest import assert_that, has_entry, greater_than, all_of, less_than
from tests.allure_pytest.pytest_runner import AllurePytestRunner

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
def test_duration(allure_pytest_runner: AllurePytestRunner, snippet):
    testfile_content = (
        f"""
        def test_duration_example():
            {snippet}
        """
    )

    before = now()
    allure_results = allure_pytest_runner.run_pytest(testfile_content)
    after = now()

    assert_that(
        allure_results,
        has_test_case(
            "test_duration_example",
            all_of(
                has_entry("start", greater_than(before)),
                has_entry("stop", all_of(
                    greater_than(before),
                    less_than(after)
                ))
            )
        )
    )


@allure.issue("244")
@pytest.mark.parametrize("snippet", snippets)
def test_with_fixture_duration(allure_pytest_runner: AllurePytestRunner, snippet):
    testfile_content = (
        f"""
        import pytest

        @pytest.fixture
        def fixture():
            {snippet}

        def test_with_fixture_duration_example(fixture):
            pass
        """
    )

    before = now()
    allure_results = allure_pytest_runner.run_pytest(testfile_content)
    after = now()

    assert_that(
        allure_results,
        has_test_case(
            "test_with_fixture_duration_example",
            all_of(
                has_entry("start", greater_than(before)),
                has_entry("stop", all_of(
                    greater_than(before),
                    less_than(after)
                ))
            )
        )
    )


@allure.issue("244")
@pytest.mark.parametrize("snippet", snippets)
def test_with_fixture_finalizer_duration(
    allure_pytest_runner: AllurePytestRunner,
    snippet
):
    testfile_content = (
        f"""
        import pytest

        @pytest.fixture
        def fixture(request):
            def finalizer():
                {snippet}
            request.addfinalizef(finalizer)

        def test_with_fixture_finalizer_duration(fixture):
            pass
        """
    )

    before = now()
    allure_results = allure_pytest_runner.run_pytest(testfile_content)
    after = now()

    assert_that(
        allure_results,
        has_test_case(
            "test_with_fixture_finalizer_duration",
            all_of(
                has_entry("start", greater_than(before)),
                has_entry("stop", all_of(
                    greater_than(before),
                    less_than(after)
                ))
            )
        )
    )


def test_test_skipped_if_fixture_exits(allure_pytest_runner: AllurePytestRunner):
    """Test should be market as skipped: pytest reports it as 'not run'"""

    testfile_content = (
        """
        import pytest

        @pytest.fixture
        def fixture():
            pytest.exit("Reason")

        def test_with_fixture_duration_example(fixture):
            pass
        """
    )

    allure_results = allure_pytest_runner.run_pytest(testfile_content)

    assert_that(
        allure_results,
        has_test_case(
            "test_with_fixture_duration_example",
            with_status("skipped")
        )
    )
