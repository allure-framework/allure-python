""" ./allure-pytest/examples/label/custom/select_tests_by_label.rst """

import pytest
from hamcrest import assert_that, all_of
from tests.allure_pytest.pytest_runner import AllurePytestRunner

from allure_commons_test.report import has_test_case


@pytest.mark.parametrize(
    ["labels", "expected_tests"],
    [
        pytest.param(
            {"Application": ["desktop"]},
            [
                "test_custom_label_one",
                "test_custom_label_both"
            ],
            id="desktop"
        ),
        pytest.param(
            {"Application": ["mobile"]},
            [
                "test_custom_label_another",
                "test_custom_label_both"
            ],
            id="mobile"
        ),
        pytest.param(
            {"Application": ["desktop", "mobile"]},
            [
                "test_custom_label_one",
                "test_custom_label_another",
                "test_custom_label_both"
            ],
            id="desktop-or-mobile"
        ),
        pytest.param(
            {"Application": ["mobile"], "layer": ["api"]},
            [
                "test_custom_label_another",
                "test_custom_label_both",
                "test_layer_label"
            ],
            id="mobile-or-api"
        )
    ]
)
def test_select_by_custom_label(
    allure_pytest_runner: AllurePytestRunner,
    labels,
    expected_tests
):
    label_filters = (
        f"--allure-label={k}=" + ",".join(v) for k, v in labels.items()
    )
    allure_results = allure_pytest_runner.run_docpath_examples(*label_filters)

    assert_that(
        allure_results,
        all_of(
            *map(has_test_case, expected_tests)
        )
    )
