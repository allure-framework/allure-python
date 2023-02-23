"""./allure-pytest/examples/description/dynamic_description.rst"""

from hamcrest import assert_that, contains_string
from tests.allure_pytest.pytest_runner import AllurePytestRunner

from allure_commons_test.report import has_test_case
from allure_commons_test.result import has_description, has_description_html


def test_dynamic_description(allure_pytest_runner: AllurePytestRunner):
    allure_results = allure_pytest_runner.run_docpath_examples(cache=True)

    assert_that(
        allure_results,
        has_test_case(
            "test_dynamic_description",
            has_description(
                contains_string("Actual description")
            )
        )
    )


def test_dynamic_description_html(allure_pytest_runner: AllurePytestRunner):
    allure_results = allure_pytest_runner.run_docpath_examples(cache=True)

    assert_that(
        allure_results,
        has_test_case(
            "test_dynamic_description_html",
            has_description_html(
                contains_string("<p>Actual HTML description</p>")
            )
        )
    )
