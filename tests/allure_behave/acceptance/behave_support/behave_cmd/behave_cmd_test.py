from hamcrest import assert_that, all_of, not_
from tests.allure_behave.behave_runner import AllureBehaveRunner
from allure_commons_test.report import has_test_case
from allure_commons_test.result import has_title, with_status, with_steps


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


def test_hidden_tag_excluded_scenario_steps_are_not_reported(
    docstring: str,
    behave_runner: AllureBehaveRunner
):
    """Feature: Behave hidden tag-excluded scenario support

    Scenario: Scenario without tag
        Given an excluded step

    @tag
    Scenario: Scenario with tag
        Given an included step
    """
    behave_runner.run_behave(
        feature_literals=[docstring],
        step_literals=[
            "given('an excluded step')(lambda c:None)\n"
            "given('an included step')(lambda c:None)"
        ],
        options=["--tags=tag", "-D", "AllureFormatter.hide_excluded=True"]
    )
    assert_that(
        behave_runner.allure_results,
        all_of(
            not_(
                has_test_case("Scenario without tag")
            ),
            has_test_case(
                "Scenario with tag",
                with_status("passed"),
                with_steps(
                    has_title("Given an included step")
                )
            )
        )
    )
