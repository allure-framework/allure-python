""" ./allure-pytest/examples/label/bdd/bdd_label.rst """

from hamcrest import assert_that
from tests.allure_pytest.pytest_runner import AllurePytestRunner

from allure_commons_test.report import has_test_case
from allure_commons_test.label import has_epic
from allure_commons_test.label import has_feature
from allure_commons_test.label import has_story


def test_single_bdd_label(allure_pytest_runner: AllurePytestRunner):
    allure_results = allure_pytest_runner.run_docpath_examples(cache=True)

    assert_that(
        allure_results,
        has_test_case(
            "test_single_bdd_label",
            has_epic("My epic"),
            has_feature("My feature"),
            has_story("My story")
        )
    )


def test_multiple_bdd_label(allure_pytest_runner: AllurePytestRunner):
    allure_results = allure_pytest_runner.run_docpath_examples(cache=True)

    assert_that(
        allure_results,
        has_test_case(
            "test_multiple_bdd_label",
            has_epic("My epic"),
            has_epic("Another epic"),
            has_feature("My feature"),
            has_feature("Another feature"),
            has_feature("One more feature"),
            has_story("My story"),
            has_story("Alternative story")
        )
    )
