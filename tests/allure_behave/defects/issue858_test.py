import allure
import shlex

from tests.allure_behave.behave_runner import AllureBehaveRunner
from ...e2e import allure_file_context

from behave import __main__ as runner


@allure.issue("858")
def test_test_results_leak(behave_runner: AllureBehaveRunner):
    feature_path = behave_runner.pytester.makefile(
        ".feature",
        (
            """
            Feature: Foo
              Scenario: Bar
                Given baz
            """
        ),
    )
    behave_runner.pytester.makefile(
        ".py",
        **{"steps/steps": "given('baz')(lambda *_: None)"},
    )

    args = shlex.join([
        feature_path.name,
        "-f", "allure_behave.formatter:AllureFormatter",
        "-o", "allure-results",
        "--no-summary",
    ])

    with allure_file_context("allure-results") as context:
        runner.main(args)
        runner.main(args)

    assert len(context.allure_results.test_cases) == 2
