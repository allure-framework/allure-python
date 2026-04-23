""" ./allure-robotframework/examples/attachment.rst """

from pytest import MonkeyPatch
from hamcrest import assert_that, equal_to
from tests.allure_robotframework.robot_runner import AllureRobotRunner
from allure_commons_test.report import has_test_case
from allure_commons_test.result import has_attachment_with_content
from allure_commons_test.result import has_step
from allure_commons_test.result import with_status


def test_data_attachment_with_default_name_and_type(
    robot_runner: AllureRobotRunner
):
    robot_runner.run_robotframework(
        suite_rst_ids={"attach-data.robot": "data-attachment-default"}
    )

    assert_that(
        robot_runner.allure_results,
        has_test_case(
            "Attach-Data.Data Attachment",
            has_step(
                "AllureLibrary.Attach",
                has_attachment_with_content(
                    robot_runner.allure_results.attachments,
                    equal_to(
                        "This attachment was created using the "
                        "allure_robotframework library"
                    )
                )
            )
        )
    )


def test_data_attachment_with_name_and_type(
    robot_runner: AllureRobotRunner
):
    robot_runner.run_robotframework(
        suite_rst_ids={"attach-data.robot": "data-attachment-name-type"}
    )

    assert_that(
        robot_runner.allure_results,
        has_test_case(
            "Attach-Data.Data Attachment",
            has_step(
                "AllureLibrary.Attach",
                has_attachment_with_content(
                    robot_runner.allure_results.attachments,
                    equal_to(
                        "https://github.com/allure-framework/allure2 "
                        "https://github.com/allure-framework/allure-python"
                    ),
                    "text/uri-list",
                    "links"
                )
            )
        )
    )


def test_file_attachment_with_default_name_and_type(
    robot_runner: AllureRobotRunner
):
    robot_runner.run_robotframework(
        suite_rst_ids={"attach-file.robot": "file-attachment-default"}
    )

    assert_that(
        robot_runner.allure_results,
        has_test_case(
            "Attach-File.File Attachment",
            has_step(
                "AllureLibrary.Attach File",
                has_attachment_with_content(
                    robot_runner.allure_results.attachments,
                    equal_to("./my_file.txt")
                )
            )
        )
    )


def test_file_attachment_with_name_and_type(
    robot_runner: AllureRobotRunner
):
    robot_runner.run_robotframework(
        suite_rst_ids={"attach-file.robot": "file-attachment-name-type"}
    )

    assert_that(
        robot_runner.allure_results,
        has_test_case(
            "Attach-File.File Attachment",
            has_step(
                "AllureLibrary.Attach File",
                has_attachment_with_content(
                    robot_runner.allure_results.attachments,
                    equal_to("./my_file.txt"),
                    "text/plain",
                    "my-file"
                )
            )
        )
    )


def test_autoattach_wrapper(
    robot_runner: AllureRobotRunner,
    monkeypatch: MonkeyPatch
):
    monkeypatch.syspath_prepend(".")

    robot_runner.run_robotframework(
        suite_rst_ids={"selenium-wrapper.robot": "selenium-suite"},
        library_literals={
            "SeleniumLibrary": (
                """
                def open_browser(*_):pass
                def capture_page_screenshot(*_):return "./screenshot.jpg"
                def close_browser(*_):pass
                """
            )
        },
        library_rst_ids={"selenium_wrapper": "selenium-wrapper"}
    )

    assert_that(
        robot_runner.allure_results,
        has_test_case(
            "Selenium-Wrapper.Automatic Screenshot Attachment",
            with_status("passed"),
            has_step(
                "selenium_wrapper.Capture Page Screenshot",
                with_status("passed"),
                has_attachment_with_content(
                    robot_runner.allure_results.attachments,
                    equal_to("./screenshot.jpg"),
                    "image/jpg",
                    "page"
                )
            )
        )
    )
