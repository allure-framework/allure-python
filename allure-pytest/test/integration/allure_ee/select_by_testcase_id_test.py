import pytest
import json
import os
from hamcrest import assert_that, only_contains, any_of, ends_with


@pytest.mark.parametrize(
    ["ids", "expected_tests"],
    [
        (
            [{"id": 1}, {"id": 2}],
            ["test_number_one", "test_number_two"]
        ),
        (
            [{"id": 1}, {"id": 3}, {"id": 4}],
            ["test_number_one", "test_number_three"]
        ),
        (
            None,
            ["test_number_one", "test_number_two", "test_number_three", "test_without_number"]
        ),
    ]
)
def test_select_by_testcase_id_test(ids, expected_tests, allured_testdir):
    """
    >>> import allure

    >>> @allure.id("1")
    ... def test_number_one():
    ...     pass

    >>> @allure.id("2")
    ... def test_number_two():
    ...     pass

    >>> @allure.id("3")
    ... @allure.id("4")
    ... def test_number_three():
    ...     pass

    >>> def test_without_number():
    ...     pass
    """
    allured_testdir.parse_docstring_source()

    if ids:
        py_path = allured_testdir.testdir.makefile(".json", json.dumps(ids))
        os.environ["AS_TESTPLAN_PATH"] = py_path.strpath
    else:
        del os.environ["AS_TESTPLAN_PATH"]

    allured_testdir.run_with_allure()
    test_cases = [test_case["fullName"] for test_case in allured_testdir.allure_report.test_cases]
    assert_that(test_cases, only_contains(
        any_of(
            *[ends_with(name) for name in expected_tests]
        )
    ))
