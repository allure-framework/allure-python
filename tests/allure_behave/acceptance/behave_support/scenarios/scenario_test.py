import pytest
from hamcrest import assert_that
from tests.allure_behave.behave_runner import AllureBehaveRunner
from allure_commons_test.report import has_test_case
from allure_commons_test.result import with_status
from allure_commons_test.result import has_step


@pytest.mark.parametrize(["step", "status"], [
    pytest.param(
        "given('a step')(lambda c:None)",
        "passed",
        id="passed"
    ),
    pytest.param(
        "@given('a step')\ndef step_impl(_):assert False",
        "failed",
        id="failed"
    ),
    pytest.param(
        "@given('a step')\ndef step_impl(_):raise ValueError",
        "broken",
        id="broken"
    ),
    pytest.param(
        "",
        "broken",
        id="undefined"
    )
])
def test_scenario_with_one_step(
    docstring,
    behave_runner: AllureBehaveRunner,
    step,
    status
):
    """
    Feature: Behave scenario support
        Scenario: Scenario with single step
            Given a step
    """

    behave_runner.run_behave(
        feature_literals=[docstring],
        step_literals=[step]
    )
    assert_that(
        behave_runner.allure_results,
        has_test_case(
            "Scenario with single step",
            with_status(status),
            has_step(
                "Given a step",
                with_status(status)
            )
        )
    )


@pytest.mark.parametrize(["trigger_step", "status"], [
    pytest.param(
        "@given('trigger')\ndef _(_):assert False",
        "failed",
        id="failed"
    ),
    pytest.param(
        "@given('trigger')\ndef _(_):raise ValueError",
        "broken",
        id="broken"
    ),
    pytest.param(
        "",
        "broken",
        id="undefined"
    )
])
def test_when_not_passed_remaining_steps_are_skipped(
    docstring,
    behave_runner: AllureBehaveRunner,
    trigger_step,
    status
):
    """
    Feature: Behave scenario support
        Scenario: Scenario with four steps
            Given step 1
            And trigger
            And step 3
            And step 4
    """

    behave_runner.run_behave(
        feature_literals=[docstring],
        step_literals=[
            "given('step {n}')(lambda c,**_:None)",
            trigger_step
        ]
    )
    assert_that(
        behave_runner.allure_results,
        has_test_case(
            "Scenario with four steps",
            with_status(status),
            has_step(
                "Given step 1",
                with_status("passed")
            ),
            has_step(
                "And trigger",
                with_status(status)
            ),
            has_step(
                "And step 3",
                with_status("skipped")
            ),
            has_step(
                "And step 4",
                with_status("skipped")
            )
        )
    )


def test_nameless_scenario(docstring, behave_runner: AllureBehaveRunner):
    """
    Feature: Behave scenario support
        Scenario:
            Given noop
    """

    behave_runner.run_behave(
        feature_literals=[docstring],
        step_literals=["given('noop')(lambda c:None)"]
    )

    assert_that(
        behave_runner.allure_results,
        has_test_case(
            "Scenario",
            with_status("passed")
        )
    )
