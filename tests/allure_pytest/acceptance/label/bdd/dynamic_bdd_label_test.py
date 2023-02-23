""" ./allure-pytest/examples/label/bdd/dynamic_bdd_label.rst """

import pytest
from hamcrest import assert_that
from tests.allure_pytest.pytest_runner import AllurePytestRunner

from allure_commons_test.report import has_test_case
from allure_commons_test.label import has_feature, has_epic, has_story


def test_dynamic_labels(allure_pytest_runner: AllurePytestRunner):
    allure_results = allure_pytest_runner.run_docpath_examples(cache=True)

    assert_that(
        allure_results,
        has_test_case(
            "test_dynamic_labels",
            has_feature("first feature"),
            has_feature("second feature"),
            has_epic("first epic"),
            has_epic("second epic"),
            has_story("first story"),
            has_story("second story")
        )
    )


@pytest.mark.parametrize("feature, epic, story", [
    pytest.param("first feature", "first epic", "first story", id="first"),
    pytest.param("second feature", "second epic", "second story", id="second")
])
def test_parametrized_dynamic_labels(
    allure_pytest_runner: AllurePytestRunner,
    feature,
    epic,
    story
):
    allure_results = allure_pytest_runner.run_docpath_examples(cache=True)

    assert_that(
        allure_results,
        has_test_case(
            f"test_parametrized_dynamic_labels[{feature}-{epic}-{story}]",
            has_feature(feature),
            has_epic(epic),
            has_story(story)
        )
    )


def test_multiple_dynamic_labels(allure_pytest_runner: AllurePytestRunner):
    allure_results = allure_pytest_runner.run_docpath_examples(cache=True)

    assert_that(
        allure_results,
        has_test_case(
            "test_multiple_dynamic_labels",
            has_feature("first feature"),
            has_feature("second feature"),
            has_epic("first epic"),
            has_epic("second epic"),
            has_story("first story"),
            has_story("second story")
        )
    )
