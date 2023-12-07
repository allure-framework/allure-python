from allure_commons_test.report import AllureReport

from tests.allure_pytest.pytest_runner import AllurePytestRunner


FEATURE_CONTENT = (
    """
    Feature: Basic allure-pytest-bdd usage
        Scenario: Simple passed example
            Given the preconditions are satisfied
            When the action is invoked
            Then the postconditions are held
    """
)
STEPS_CONTENT = (
    """
    from pytest_bdd import scenario, given, when, then

    @scenario("scenario.feature", "Simple passed example")
    def test_scenario_passes():
        pass

    @given("the preconditions are satisfied")
    def given_the_preconditions_are_satisfied():
        pass

    @when("the action is invoked")
    def when_the_action_is_invoked():
        pass

    @then("the postconditions are held")
    def then_the_postconditions_are_held():
        pass
    """
)


def test_custom_alluredir(allure_pytest_bdd_runner: AllurePytestRunner):
    alluredir = allure_pytest_bdd_runner.pytester.path
    allure_pytest_bdd_runner.in_memory = False

    # run test twice
    # results of all runs must be in the results directory
    for _ in range(2):
        allure_pytest_bdd_runner.run_pytest(
            ("scenario.feature", FEATURE_CONTENT),
            STEPS_CONTENT,
            cli_args=["--alluredir", "allure_results"]
        )
    assert (alluredir / 'allure_results').exists()
    results = AllureReport(alluredir / 'allure_results')
    assert len(results.test_cases) == 2


def test_clean_alluredir(allure_pytest_bdd_runner: AllurePytestRunner):
    alluredir = allure_pytest_bdd_runner.pytester.path
    allure_pytest_bdd_runner.in_memory = False

    # run test twice
    # results of only last runs must be in the results directory
    for _ in range(2):
        allure_pytest_bdd_runner.run_pytest(
            ("scenario.feature", FEATURE_CONTENT),
            STEPS_CONTENT,
            cli_args=["--alluredir", "allure_results", "--clean-alluredir"]
        )
    results = AllureReport(alluredir / 'allure_results')
    assert len(results.test_cases) == 1


def test_clean_alluredir_with_collectonly(allure_pytest_bdd_runner: AllurePytestRunner):
    alluredir = allure_pytest_bdd_runner.pytester.path
    allure_pytest_bdd_runner.in_memory = False

    # run test
    allure_pytest_bdd_runner.run_pytest(
        ("scenario.feature", FEATURE_CONTENT),
        STEPS_CONTENT,
        cli_args=["--alluredir", "allure_results"]
    )
    results_before_clean = AllureReport(alluredir / 'allure_results')
    # run test with --collectonly
    allure_pytest_bdd_runner.run_pytest(
        ("scenario.feature", FEATURE_CONTENT),
        STEPS_CONTENT,
        cli_args=["--alluredir", "allure_results", "--clean-alluredir", "--collectonly"]
    )
    # results should be the same
    results_after_clean = AllureReport(alluredir / 'allure_results')
    assert results_before_clean.test_cases == results_after_clean.test_cases
