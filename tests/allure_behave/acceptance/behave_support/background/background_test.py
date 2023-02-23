import pytest
from hamcrest import assert_that, all_of
from tests.allure_behave.behave_runner import AllureBehaveRunner
from allure_commons_test.report import has_test_case
from allure_commons_test.result import with_status
from allure_commons_test.result import has_step


@pytest.mark.parametrize(
    ["step_outcome", "status", "remained_steps_status"],
    [
        pytest.param("passed", "passed", "passed", id="passed"),
        pytest.param("failed", "failed", "skipped", id="failed"),
        pytest.param("broken", "broken", "skipped", id="broken"),
        pytest.param("undefined", "broken", "skipped", id="undefined"),
    ]
)
def test_background(
    docstring: str,
    behave_runner: AllureBehaveRunner,
    step_outcome: str,
    status: str,
    remained_steps_status: str
):
    """
    Feature: Allure-behave compatibility with feature backgrounds
        Background: A background with {step_outcome} step
            Given the first background step that is {step_outcome}
            And the second background step with no failures

        Scenario: Scenario with background containing {step_outcome} step
            Given the first step with no failures
            And the second step with no failures

        Scenario: Another scenario with background containing {step_outcome} step
            Given the step with no failures
    """
    behave_runner.run_behave(
        feature_literals=[
            docstring.format(step_outcome=step_outcome)
        ],
        step_paths=["./background_steps.py"]
    )
    assert_that(
        behave_runner.allure_results,
        all_of(
            has_test_case(
                f"Scenario with background containing {step_outcome} step",
                with_status(status),
                has_step(
                    f"Given the first background step that is {step_outcome}",
                    with_status(status)
                ),
                has_step(
                    "And the second background step with no failures",
                    with_status(remained_steps_status)
                ),
                has_step(
                    "Given the first step with no failures",
                    with_status(remained_steps_status)
                ),
                has_step(
                    "And the second step with no failures",
                    with_status(remained_steps_status)
                )
            ),
            has_test_case(
                f"Another scenario with background containing {step_outcome} step",
                with_status(status),
                has_step(
                    f"Given the first background step that is {step_outcome}",
                    with_status(status)
                ),
                has_step(
                    "And the second background step with no failures",
                    with_status(remained_steps_status)
                ),
                has_step(
                    "Given the step with no failures",
                    with_status(remained_steps_status)
                )
            )
        )
    )
