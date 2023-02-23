""" ./allure-pytest/examples/attachment/attachment_step.rst """

from hamcrest import assert_that
from tests.allure_pytest.pytest_runner import AllurePytestRunner

from allure_commons_test.report import has_test_case
from allure_commons_test.result import has_step
from allure_commons_test.result import has_attachment


def test_step_with_attachment(allure_pytest_runner: AllurePytestRunner):
    allure_results = allure_pytest_runner.run_docpath_examples()

    assert_that(
        allure_results,
        has_test_case(
            "test_step_with_attachment",
            has_step(
                "step_with_attachment",
                has_attachment()
            ),
        )
    )


def test_step_with_thread_and_attachment(allure_pytest_runner: AllurePytestRunner):
    testfile_content = (
        """
        from concurrent.futures import ThreadPoolExecutor

        import allure
        import pytest

        @allure.step("thread {x}")
        def parallel_step(x=1):
            allure.attach("text", str(x), allure.attachment_type.TEXT)


        def test_thread():
            with allure.step("Start in thread"):
                with ThreadPoolExecutor(max_workers=2) as executor:
                    f_result = executor.map(parallel_step, [1, 2])
        """
    )

    allure_results = allure_pytest_runner.run_pytest(testfile_content)

    assert_that(
        allure_results,
        has_test_case(
            "test_thread",
            has_step(
                "Start in thread",
                has_step(
                    "thread 1",
                    has_attachment(name="1")
                ),
                has_step(
                    "thread 2",
                    has_attachment(name="2")
                )
            )
        )
    )
