import allure
from hamcrest import assert_that, is_not
from tests.allure_pytest.pytest_runner import AllurePytestRunner

from allure_commons_test.report import has_test_case
from allure_commons_test.result import has_full_name
from allure_commons_test.label import has_sub_suite


@allure.issue("868", name="Issue 868")
def test_nested_class_affects_fullname_and_subsuite(allure_pytest_runner: AllurePytestRunner):
    """
    >>> class TestFoo:
    ...     class TestBar:
    ...         def test_bar(self):
    ...             pass
    """

    allure_results = allure_pytest_runner.run_docstring(filename="foo_test.py")

    assert_that(
        allure_results,
        has_test_case(
            "test_bar",
            has_full_name("foo_test.TestFoo.TestBar#test_bar"),
            has_sub_suite("TestFoo > TestBar"),
        ),
    )


@allure.issue("868", name="Issue 868")
def test_nested_class_affects_testcaseid_and_historyid(allure_pytest_runner: AllurePytestRunner):
    """
    >>> class TestFoo:
    ...     class TestFoo:
    ...         def test_foo(self):
    ...             pass
    ...     def test_foo(self):
    ...         pass
    """

    allure_results = allure_pytest_runner.run_docstring(filename="foo_test.py")
    test_case_id1, test_case_id2 = [tc["testCaseId"] for tc in allure_results.test_cases]
    history_id1, history_id2 = [tc["historyId"] for tc in allure_results.test_cases]

    assert_that(test_case_id1, is_not(test_case_id2))
    assert_that(history_id1, is_not(history_id2))
