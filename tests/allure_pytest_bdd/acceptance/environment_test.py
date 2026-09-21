from hamcrest import assert_that
from hamcrest import has_entries

from tests.allure_pytest.pytest_runner import AllurePytestRunner


def test_environment_from_hook_and_step(allure_pytest_bdd_runner: AllurePytestRunner):
    feature_content = (
        """
        Feature: Foo
            Scenario: Bar
                Given noop
        """
    )
    steps_content = (
        """
        import allure

        from pytest_bdd import scenario, given

        @scenario("sample.feature", "Bar")
        def test_scenario():
            pass

        @given("noop")
        def given_noop():
            allure.environment({"os.name": "Windows 11"}, browser="firefox")
        """
    )
    conftest_content = (
        """
        import allure

        def pytest_sessionstart(session):
            allure.environment(browser="chrome", stand="staging")
        """
    )

    allure_results = allure_pytest_bdd_runner.run_pytest(
        ("sample.feature", feature_content),
        steps_content,
        conftest_literal=conftest_content,
    )

    assert_that(
        allure_results.environment,
        has_entries({
            "browser": "firefox",
            "stand": "staging",
            "os.name": "Windows 11",
        }),
    )
