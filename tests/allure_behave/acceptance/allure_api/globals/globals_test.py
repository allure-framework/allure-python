import textwrap
from tests.allure_behave.behave_runner import AllureBehaveRunner as Runner
from hamcrest import assert_that, equal_to, has_item, has_length
from allure_commons_test.result import has_global_attachment_with_content
from allure_commons_test.result import has_global_error
from allure_commons_test.result import with_message_contains


def test_global_attachment_and_error_hooks(behave_runner: Runner):
    behave_runner.run_behave(
        feature_literals=[
            """
            Feature: Global attachments and errors
                Scenario: Global hooks
                    Given noop
            """
        ],
        step_literals=["given('noop')(lambda c: None)"],
        environment_literal=textwrap.dedent(
            """
            import allure


            def before_all(context):
                allure.global_attach("behave global attachment", name="behave global")


            def after_all(context):
                allure.global_error("behave global error")
            """
        ),
    )

    assert_that(
        behave_runner.allure_results.globals,
        has_length(2),
    )

    assert_that(
        behave_runner.allure_results.globals,
        has_item(
            has_global_attachment_with_content(
                behave_runner.allure_results.attachments,
                equal_to("behave global attachment"),
                name="behave global"
            )
        )
    )
    assert_that(
        behave_runner.allure_results.globals,
        has_item(
            has_global_error(
                with_message_contains("behave global error")
            )
        )
    )
