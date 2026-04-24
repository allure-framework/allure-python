from hamcrest import assert_that, has_item, all_of
from hamcrest import equal_to, ends_with, has_length
from tests.allure_pytest.pytest_runner import AllurePytestRunner

from allure_commons_test.result import has_global_attachment_with_content
from allure_commons_test.result import has_global_error
from allure_commons_test.result import with_message_contains
from allure_commons_test.result import with_trace_contains
from allure_commons_test.result import with_no_trace


def test_globals_from_session_hooks(allure_pytest_runner: AllurePytestRunner):
    allure_results = allure_pytest_runner.run_pytest(
        """
        def test_globals_from_session_hooks():
            pass
        """,
        conftest_literal=(
            """
            import allure


            def pytest_sessionstart(session):
                allure.global_attach(body="global body", name="global attachment")
                allure.global_attach.file(__file__, name="global attachment file")
                allure.global_error("message only error")


            def pytest_sessionfinish(session, exitstatus):
                try:
                    raise ValueError("error from exception")
                except ValueError as error:
                    allure.global_error(error)
                allure.global_error("message with trace", "explicit trace")
            """
        )
    )

    assert_that(
        allure_results.globals,
        has_length(5),
    )

    assert_that(
        allure_results.globals,
        all_of(
            has_item(
                has_global_attachment_with_content(
                    allure_results.attachments,
                    equal_to("global body"),
                    name="global attachment"
                )
            ),
            has_item(
                has_global_attachment_with_content(
                    allure_results.attachments,
                    ends_with("conftest.py"),
                    name="global attachment file"
                )
            ),
            has_item(
                has_global_error(
                    with_message_contains("message only error"),
                    with_no_trace(),
                )
            ),
            has_item(
                has_global_error(
                    with_message_contains("ValueError: error from exception"),
                    with_trace_contains("raise ValueError")
                )
            ),
            has_item(
                has_global_error(
                    with_message_contains("message with trace"),
                    with_trace_contains("explicit trace")
                )
            )
        )
    )
