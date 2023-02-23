from hamcrest import assert_that, all_of, not_
from tests.allure_behave.behave_runner import AllureBehaveRunner
from allure_commons_test.report import has_test_case
from allure_commons_test.result import with_status


def test_behave_tags_filter(docstring: str, behave_runner: AllureBehaveRunner):
    """Feature: Behave --tags CLI argument support

        @tag
        Scenario: Scenario with tag
            Given noop

        Scenario: Scenario without tag
            Given noop
    """

    behave_runner.run_behave(
        feature_literals=[docstring],
        step_literals=["given('noop')(lambda c:None)"],
        options=["--tags=tag"]
    )
    assert_that(
        behave_runner.allure_results,
        all_of(
            has_test_case(
                "Scenario with tag",
                with_status("passed")
            ),
            has_test_case(
                "Scenario without tag",
                with_status("skipped")
            )
        )
    )


def test_behave_no_skipped_support(docstring: str, behave_runner: AllureBehaveRunner):
    """Feature: Behave --tags CLI argument support

    @tag
    Scenario: Scenario with tag
        Given noop

    Scenario: Scenario without tag
        Given noop
    """
    behave_runner.run_behave(
        feature_literals=[docstring],
        step_literals=["given('noop')(lambda c:None)"],
        options=["--tags=tag", "--no-skipped"]
    )
    assert_that(
        behave_runner.allure_results,
        all_of(
            has_test_case(
                "Scenario with tag",
                with_status("passed")
            ),
            not_(
                has_test_case("Scenario without tag")
            )
        )
    )
