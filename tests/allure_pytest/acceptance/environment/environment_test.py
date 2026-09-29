""" ./allure-pytest/examples/environment/environment.rst """
from hamcrest import assert_that, has_entries, empty
from tests.allure_pytest.pytest_runner import AllurePytestRunner


def test_environment_from_keywords(allure_pytest_runner: AllurePytestRunner):
    allure_results = allure_pytest_runner.run_docpath_examples(cache=True)

    assert_that(
        allure_results.environment,
        has_entries(browser="chrome", stand="production"),
    )


def test_environment_from_mapping(allure_pytest_runner: AllurePytestRunner):
    allure_results = allure_pytest_runner.run_docpath_examples(cache=True)

    assert_that(
        allure_results.environment,
        has_entries({
            "os.name": "Windows 11",
            "browser version": "125.0",
            "python.version": "3.13.0",
        }),
    )


def test_environment_from_fixture(allure_pytest_runner: AllurePytestRunner):
    allure_results = allure_pytest_runner.run_docpath_examples(cache=True)

    assert_that(
        allure_results.environment,
        has_entries(hostname="my.host.local"),
    )


def test_environment_from_session_hook(allure_pytest_runner: AllurePytestRunner):
    allure_results = allure_pytest_runner.run_pytest(
        """
        def test_environment_from_session_hook():
            pass
        """,
        conftest_literal=(
            """
            import allure


            def pytest_sessionstart(session):
                allure.environment(report="Allure report")
            """
        )
    )

    assert_that(
        allure_results.environment,
        has_entries(report="Allure report"),
    )


def test_empty_environment(allure_pytest_runner: AllurePytestRunner):
    allure_results = allure_pytest_runner.run_pytest(
        """
        import allure


        def test_empty_environment():
            allure.environment()
        """
    )

    assert_that(allure_results.environment, empty())
