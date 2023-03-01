""" ./allure-pytest/examples/attachment/attachment_fixture.rst """

from hamcrest import assert_that
from tests.allure_pytest.pytest_runner import AllurePytestRunner
from allure_commons_test.report import has_test_case
from allure_commons_test.result import has_attachment
from allure_commons_test.container import has_container
from allure_commons_test.container import has_before
from allure_commons_test.container import has_after


def test_fixture_attachment(allure_pytest_runner: AllurePytestRunner):
    allure_results = allure_pytest_runner.run_docpath_examples(cache=True)

    assert_that(
        allure_results,
        has_test_case(
            "test_fixture_attachment",
            has_container(
                allure_results,
                has_before(
                    "fixture_with_attachment",
                    has_attachment()
                )
            )
        )
    )


def test_fixture_finalizer_attachment(allure_pytest_runner: AllurePytestRunner):
    allure_results = allure_pytest_runner.run_docpath_examples(cache=True)

    assert_that(
        allure_results,
        has_test_case(
            "test_fixture_finalizer_attachment",
            has_container(
                allure_results,
                has_after(
                    "fixture_with_attachment_in_finalizer::finalizer",
                    has_attachment()
                )
            )
        )
    )
