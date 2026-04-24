from hamcrest import assert_that
from hamcrest import equal_to
from hamcrest import has_item
from hamcrest import has_length

from allure_commons_test.result import has_global_attachment_with_content
from allure_commons_test.result import has_global_error
from allure_commons_test.result import with_message_contains

from tests.allure_pytest.pytest_runner import AllurePytestRunner


def test_global_attachment_and_error_from_hook(allure_pytest_bdd_runner: AllurePytestRunner):
    feature_content = (
        """
        Feature: Foo
            Scenario: Bar
                Given noop
        """
    )
    steps_content = (
        """
        from pytest_bdd import scenario, given

        @scenario("sample.feature", "Bar")
        def test_scenario():
            pass

        @given("noop")
        def given_noop():
            pass
        """
    )
    conftest_content = (
        """
        import allure

        def pytest_sessionstart(session):
            allure.global_attach("bdd global attachment", name="bdd global")

        def pytest_sessionfinish(session, exitstatus):
            allure.global_error("bdd global error")
        """
    )

    allure_results = allure_pytest_bdd_runner.run_pytest(
        ("sample.feature", feature_content),
        steps_content,
        conftest_literal=conftest_content,
    )

    assert_that(allure_results.globals, has_length(2))

    assert_that(
        allure_results.globals,
        has_item(
            has_global_attachment_with_content(
                allure_results.attachments,
                equal_to("bdd global attachment"),
                name="bdd global",
            )
        )
    )
    assert_that(
        allure_results.globals,
        has_item(
            has_global_error(
                with_message_contains("bdd global error")
            )
        )
    )
