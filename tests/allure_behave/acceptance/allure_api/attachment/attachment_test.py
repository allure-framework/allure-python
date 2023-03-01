""" ./allure-behave/examples/attachment.rst """

from tests.allure_behave.behave_runner import AllureBehaveRunner
from hamcrest import assert_that, equal_to
from allure_commons_test.report import has_test_case
from allure_commons_test.result import has_attachment_with_content
from allure_commons_test.result import has_attachment
from allure_commons_test.result import has_step


def test_data_attachment_from_step(behave_runner: AllureBehaveRunner):
    behave_runner.run_behave(
        feature_rst_ids=["data-attachment-feature"],
        step_rst_ids=["data-attachment-steps"]
    )
    assert_that(
        behave_runner.allure_results,
        has_test_case(
            "Data attachment from step definitions",
            has_step(
                "Given a step that adds a named attachment",
                has_attachment_with_content(
                    behave_runner.allure_results.attachments,
                    equal_to("This is the attachment with the name 'step.txt'"),
                    name="step.txt"
                )
            ),
            has_step(
                "And a step that adds a typed named attachment",
                has_attachment_with_content(
                    behave_runner.allure_results.attachments,
                    equal_to(
                        "[DEBUG] This attachment is named 'trace.log' and has "
                        "TEXT document appearance"
                    ),
                    attach_type="text/plain",
                    name="trace.log"
                )
            )
        )
    )


def test_file_attachment_from_step(behave_runner: AllureBehaveRunner):
    behave_runner.run_behave(
        feature_rst_ids=["file-attachment-feature"],
        step_rst_ids=["file-attachment-steps"]
    )
    assert_that(
        behave_runner.allure_results,
        has_test_case(
            "File attachment from a step definition",
            has_step(
                "Given a step that attaches a file",
                has_attachment("text/plain", "web.log")
            )
        )
    )


def test_data_attachment_from_hook(behave_runner: AllureBehaveRunner):
    feature = """
        Feature: Allure attachments in behave tests
            Scenario: Attachment from after_scenario hook
                Given noop
    """
    behave_runner.run_behave(
        feature_literals=[feature],
        step_literals=["given('noop')(lambda _:0)"],
        environment_rst_id="attach-hook"
    )
    assert_that(
        behave_runner.allure_results,
        has_test_case(
            "Attachment from after_scenario hook",
            has_attachment_with_content(
                behave_runner.allure_results.attachments,
                equal_to("This attachment will appear on a scenario level"),
                attach_type="text/plain",
                name="attachment.txt"
            )
        )
    )
