from hamcrest import assert_that
from tests.allure_pytest.pytest_runner import AllurePytestRunner

from allure_commons_test.report import has_test_case
from allure_commons_test.result import has_attachment


def test_attach_from_runtest_teardown(allure_pytest_runner: AllurePytestRunner):
    allure_results = allure_pytest_runner.run_pytest(
        """
        def test_attach_from_runtest_teardown():
            pass
        """,
        conftest_literal=(
            """
            import allure


            def pytest_runtest_teardown(*args, **kwargs):
                allure.attach(body="body", name="attachment from teardown")
            """
        )
    )

    assert_that(
        allure_results,
        has_test_case(
            "test_attach_from_runtest_teardown",
            has_attachment(name="attachment from teardown")
        )
    )


def test_attach_from_runtest_logfinish(allure_pytest_runner: AllurePytestRunner):
    allure_results = allure_pytest_runner.run_pytest(
        """
        def test_attach_from_runtest_logfinish():
            pass
        """,
        conftest_literal=(
            """
            import allure


            def pytest_runtest_logfinish(*args, **kwargs):
                allure.attach(body="body", name="attachment from logfinish")
            """
        )
    )

    assert_that(
        allure_results,
        has_test_case(
            "test_attach_from_runtest_logfinish",
            has_attachment(name="attachment from logfinish")
        )
    )
