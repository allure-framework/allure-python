""" ./allure-pytest/examples/label/suite/custom_suite.rst """

from hamcrest import assert_that, not_
from tests.allure_pytest.pytest_runner import AllurePytestRunner

import allure
from allure_commons_test.report import has_test_case
from allure_commons_test.label import has_suite, has_parent_suite, has_sub_suite


def test_custom_suite(allure_pytest_runner: AllurePytestRunner):
    allure_results = allure_pytest_runner.run_docpath_examples(cache=True)

    assert_that(
        allure_results,
        has_test_case(
            "TestCustomSuites#test_custom_suites",
            has_suite("suite name"),
            has_parent_suite("parent suite name"),
            has_sub_suite("sub suite name"),
            not_(
                has_parent_suite(
                    not_("parent suite name")
                )
            ),
            not_(
                has_suite(
                    not_("suite name")
                )
            ),
            not_(
                has_sub_suite(
                    not_("sub suite name")
                )
            )
        )
    )


@allure.issue("586", "Issue 586")
def test_custom_dynamic_suites(allure_pytest_runner: AllurePytestRunner):
    allure_results = allure_pytest_runner.run_docpath_examples(cache=True)

    assert_that(
        allure_results,
        has_test_case(
            "TestCustomDynamicSuites#test_custom_dynamic_suites",
            has_suite("suite name"),
            has_parent_suite("parent suite name"),
            has_sub_suite("sub suite name"),
            not_(
                has_parent_suite(
                    not_("parent suite name")
                )
            ),
            not_(
                has_suite(
                    not_("suite name")
                )
            ),
            not_(
                has_sub_suite(
                    not_("sub suite name")
                )
            )
        )
    )
