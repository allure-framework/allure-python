""" ./examples/label/custom/select_tests_by_label.rst """

import pytest
from hamcrest import assert_that, ends_with, contains_inanyorder


@pytest.mark.parametrize(
    ["labels", "expected_tests"],
    [
        (
            {"Application": ["desktop"]},
            [
                "test_custom_label_one",
                "test_custom_label_both"
            ]
        ),
        (
            {"Application": ["mobile"]},
            [
                "test_custom_label_another",
                "test_custom_label_both"
            ]
        ),
        (
            {"Application": ["desktop", "mobile"]},
            [
                "test_custom_label_one",
                "test_custom_label_another",
                "test_custom_label_both"
            ]
        ),
        (
            {"Application": ["mobile"], "layer": ["api"]},
            [
                "test_custom_label_another",
                "test_custom_label_both",
                "test_layer_label"
            ]
        )
    ]
)
def test_select_by_custom_label(allured_testdir, labels, expected_tests):
    allured_testdir.parse_docstring_path()
    allure_labels = []
    for label_name, label_values in labels.items():
        allure_labels.extend(["--allure-label", f"{label_name}={','.join(label_values)}"])
    allured_testdir.run_with_allure(*allure_labels)
    test_cases = [test_case["fullName"] for test_case in allured_testdir.allure_report.test_cases]
    assert_that(test_cases, contains_inanyorder(*[ends_with(name) for name in expected_tests]))
