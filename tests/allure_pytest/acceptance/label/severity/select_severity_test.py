""" ./allure-pytest/examples/label/severity/select_tests_by_severity.rst """

import pytest
from hamcrest import assert_that, only_contains, any_of, ends_with
from tests.allure_pytest.pytest_runner import AllurePytestRunner


@pytest.mark.parametrize(
    ["severities", "expected_tests"],
    [
        pytest.param(
            ["critical", "minor"],
            ["test_vip", "test_minor"],
            id="critical,minor"
        ),
        pytest.param(
            ["critical"],
            ["test_vip"],
            id="critical"
        ),
        pytest.param(
            ["normal"],
            ["test_with_default_severity"],
            id="normal"
        ),
        pytest.param(
            ["trivial", "minor", "normal", "critical", "blocker"],
            [
                "test_vip",
                "test_with_default_severity",
                "test_minor"
            ],
            id="all"
        )
    ]
)
def test_select_by_severity_level(
    allure_pytest_runner: AllurePytestRunner,
    severities,
    expected_tests
):
    allure_results = allure_pytest_runner.run_docpath_examples(
        "--allure-severities",
        ",".join(severities)
    )

    test_cases = [
        test_case["fullName"] for test_case in allure_results.test_cases
    ]

    assert_that(test_cases, only_contains(
        any_of(
            *[ends_with(name) for name in expected_tests]
        )
    ))
