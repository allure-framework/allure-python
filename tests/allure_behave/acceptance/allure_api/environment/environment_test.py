import textwrap
from tests.allure_behave.behave_runner import AllureBehaveRunner as Runner
from hamcrest import assert_that, has_entries


def test_environment_from_hooks(behave_runner: Runner):
    behave_runner.run_behave(
        feature_literals=[
            """
            Feature: Environment
                Scenario: Environment from hooks
                    Given noop
            """
        ],
        step_literals=["given('noop')(lambda c: None)"],
        environment_literal=textwrap.dedent(
            """
            import allure


            def before_all(context):
                allure.environment(browser="chrome", stand="staging")


            def after_all(context):
                allure.environment({"os.name": "Windows 11"}, browser="firefox")
            """
        ),
    )

    assert_that(
        behave_runner.allure_results.environment,
        has_entries({
            "browser": "firefox",
            "stand": "staging",
            "os.name": "Windows 11",
        }),
    )
