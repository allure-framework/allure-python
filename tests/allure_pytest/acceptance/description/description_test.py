""" ./allure-pytest/examples/description/description.rst """

from hamcrest import assert_that, contains_string
from tests.allure_pytest.pytest_runner import AllurePytestRunner

from allure_commons_test.report import has_test_case
from allure_commons_test.result import has_description, has_description_html


def test_description(allure_pytest_runner: AllurePytestRunner):
    allure_results = allure_pytest_runner.run_docpath_examples(cache=True)

    assert_that(
        allure_results,
        has_test_case(
            "test_description",
            has_description(
                contains_string("Test description")
            )
        )
    )


def test_description_html(allure_pytest_runner: AllurePytestRunner):
    allure_results = allure_pytest_runner.run_docpath_examples(cache=True)

    assert_that(
        allure_results,
        has_test_case(
            "test_description_html",
            has_description_html(
                contains_string("<h1>Html test description</h1>")
            )
        )
    )


def test_docstring_description(allure_pytest_runner: AllurePytestRunner):
    allure_results = allure_pytest_runner.run_docpath_examples(cache=True)

    assert_that(
        allure_results,
        has_test_case(
            "test_docstring_description",
            has_description(
                contains_string("Docstring")
            )
        )
    )
