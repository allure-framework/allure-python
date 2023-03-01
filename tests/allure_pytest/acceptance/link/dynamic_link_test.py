""" ./allure-pytest/examples/link/dynamic_link.rst """

from hamcrest import assert_that, equal_to, all_of
from tests.allure_pytest.pytest_runner import AllurePytestRunner

from allure_commons_test.report import has_test_case
from allure_commons_test.result import has_link
from allure_commons_test.result import has_issue_link


def test_dynamic_link(allure_pytest_runner: AllurePytestRunner):
    allure_results = allure_pytest_runner.run_docpath_examples(cache=True)

    assert_that(
        allure_results,
        has_test_case(
            "test_dynamic_link",
            has_issue_link("issues/24")
        )
    )


def test_parametrize_dynamic_link(allure_pytest_runner: AllurePytestRunner):
    allure_results = allure_pytest_runner.run_docpath_examples(cache=True)

    assert_that(
        allure_results,
        all_of(
            has_test_case(
                "test_parametrize_dynamic_link[issues/24]",
                has_issue_link("issues/24"),
            ),
            has_test_case(
                "test_parametrize_dynamic_link[issues/132]",
                has_issue_link("issues/132"),
            )
        )
    )


def test_all_links_together(allure_pytest_runner: AllurePytestRunner):
    allure_results = allure_pytest_runner.run_docpath_examples(cache=True)

    assert_that(
        allure_results,
        has_test_case(
            "test_all_links_together",
            has_issue_link("issues/24"),
            has_issue_link("issues/132"),
            has_link("allure", name="QAMETA", link_type="docs")
        )
    )


def test_unique_dynamic_links(allure_pytest_runner: AllurePytestRunner):
    """
    >>> import allure

    >>> def test_unique_dynamic_links_example():
    ...     allure.dynamic.link("some/unique/dynamic/link")
    ...     allure.dynamic.link("some/unique/dynamic/link")
    """

    allure_results = allure_pytest_runner.run_docstring()

    assert_that(
        allure_results.test_cases[0]['links'],
        equal_to([{
            'url': 'some/unique/dynamic/link',
            'type': 'link',
            'name': 'some/unique/dynamic/link'
        }])
    )
