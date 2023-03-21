""" ./examples/label/severity/select_tests_by_severity.rst """

import pytest
from hamcrest import assert_that, only_contains, any_of, ends_with


@pytest.mark.parametrize(
    ["severities", "expected_tests"],
    [
        (["critical", "minor"],
         [
             "test_vip",
             "test_minor"
         ]),
        (["critical"],
         [
             "test_vip",
         ]),
    ]
)
def test_select_by_severity_level(allured_testdir, severities, expected_tests):
    allured_testdir.parse_docstring_path()

    allured_testdir.run_with_allure("--allure-severities", ",".join(severities))
    test_cases = [test_case["fullName"] for test_case in allured_testdir.allure_report.test_cases]

    assert_that(test_cases, only_contains(
        any_of(
            *[ends_with(name) for name in expected_tests]
        )
    ))
