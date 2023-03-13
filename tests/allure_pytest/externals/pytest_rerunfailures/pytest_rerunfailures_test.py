import pytest
from hamcrest import assert_that
from tests.allure_pytest.pytest_runner import AllurePytestRunner

import allure
from allure_commons_test.report import has_test_case
from allure_commons_test.result import with_status


@pytest.fixture
def rerunfailures_runner(allure_pytest_runner: AllurePytestRunner):
    allure_pytest_runner.enable_plugins("rerunfailures")
    yield allure_pytest_runner


@allure.issue("140")
@allure.feature("Integration")
@pytest.mark.parametrize("countdown, status", [(2, "failed"), (4, "passed")])
def test_pytest_rerunfailures(
    rerunfailures_runner: AllurePytestRunner,
    countdown,
    status
):
    testfile_content = (
        f"""
        import pytest

        @pytest.mark.flaky(reruns={countdown})
        def test_pytest_rerunfailures_example(request):
            run = request.node.execution_count
            assert run == 4
        """
    )

    output = rerunfailures_runner.run_pytest(testfile_content)

    assert_that(
        output,
        has_test_case(
            "test_pytest_rerunfailures_example",
            with_status(status)
        )
    )


@allure.issue("735")
@allure.feature("Integration")
def test_separate_result_for_each_rerun(rerunfailures_runner: AllurePytestRunner):
    testfile_content = (
        """
        import pytest

        @pytest.mark.flaky(reruns=1)
        def test_pytest_rerunfailures_example(request):
            assert False
        """
    )

    def __count_labels(tc, name):
        return len(
            [label["value"] for label in tc["labels"] if label["name"] == name]
        )

    output = rerunfailures_runner.run_pytest(testfile_content)

    assert len(output.test_cases) == 2
    assert __count_labels(output.test_cases[0], "suite") == 1
    assert __count_labels(output.test_cases[0], "tag") == 1
    assert __count_labels(output.test_cases[1], "suite") == 1
    assert __count_labels(output.test_cases[1], "tag") == 1
