""" ./allure-pytest/examples/label/bdd/select_tests_by_bdd.rst """

import pytest
from hamcrest import assert_that, only_contains, any_of, ends_with
from tests.allure_pytest.pytest_runner import AllurePytestRunner


@pytest.mark.parametrize(
    ["options", "expected_tests"],
    [
        pytest.param(
            {"epics": ["Another Epic"]},
            ["test_with_another_epic_feature_story"],
            id="epics"
        ),

        pytest.param(
            {"features": ["My Feature"]},
            [
                "test_with_epic_feature_story",
                "test_with_epic_feature"
            ],
            id="features"
        ),

        pytest.param(
            {"stories": ["My Story", "Another Story"]},
            [
                "test_with_epic_feature_story",
                "test_with_another_epic_feature_story"
            ],
            id="stories"
        ),

        pytest.param(
            {"stories": ["My Story"], "epics": ["Another Epic"]},
            [
                "test_with_epic_feature_story",
                "test_with_another_epic_feature_story"
            ],
            id="story-or-epic"
        )

    ]
)
def test_select_by_bdd_label(
    allure_pytest_runner: AllurePytestRunner,
    options,
    expected_tests
):
    bdd_filter_args = (
        f"--allure-{k}=" + ",".join(v) for k, v in options.items()
    )

    allure_results = allure_pytest_runner.run_docpath_examples(*bdd_filter_args)

    test_cases = [test_case["fullName"] for test_case in allure_results.test_cases]
    assert_that(test_cases, only_contains(
        any_of(
            *(ends_with(name) for name in expected_tests)
        )
    ))
