from allure_commons_test.report import AllureReport

from tests.allure_pytest.pytest_runner import AllurePytestRunner


TEST_FUNC = "def test_first_func(): pass"


def test_custom_alluredir(allure_pytest_runner: AllurePytestRunner):
    alluredir = allure_pytest_runner.pytester.path
    allure_pytest_runner.in_memory = False

    # run test twice
    # results of all runs must be in the results directory
    for _ in range(2):
        allure_pytest_runner.run_pytest(
            TEST_FUNC,
            cli_args=["--alluredir", "allure_results"]
        )
    assert (alluredir / 'allure_results').exists()
    results = AllureReport(alluredir / 'allure_results')
    assert len(results.test_cases) == 2


def test_clean_alluredir(allure_pytest_runner: AllurePytestRunner):
    alluredir = allure_pytest_runner.pytester.path
    allure_pytest_runner.in_memory = False

    # run test twice
    # results of only last runs must be in the results directory
    for _ in range(2):
        allure_pytest_runner.run_pytest(
            TEST_FUNC,
            cli_args=["--alluredir", "allure_results", "--clean-alluredir"]
        )
    results = AllureReport(alluredir / 'allure_results')
    assert len(results.test_cases) == 1


def test_clean_alluredir_with_collectonly(allure_pytest_runner: AllurePytestRunner):
    alluredir = allure_pytest_runner.pytester.path
    allure_pytest_runner.in_memory = False

    # run test
    allure_pytest_runner.run_pytest(
        TEST_FUNC,
        cli_args=["--alluredir", "allure_results"]
    )
    results_before_clean = AllureReport(alluredir / 'allure_results')
    # run test with --collectonly
    allure_pytest_runner.run_pytest(
        TEST_FUNC,
        cli_args=["--alluredir", "allure_results", "--clean-alluredir", "--collectonly"]
    )
    # results should be the same
    results_after_clean = AllureReport(alluredir / 'allure_results')
    assert results_before_clean.test_cases == results_after_clean.test_cases
