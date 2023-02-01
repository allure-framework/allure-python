import pytest
import json
import os
import inspect
from hamcrest import assert_that, contains_inanyorder, ends_with
from tests.conftest import AlluredTestdir
from typing import Sequence


@pytest.mark.parametrize(
    ["planned_tests", "expected_tests"],
    [
        pytest.param(
            [{"id": 1}, {"id": 2}],
            ["test_number_one", "test_number_two"],
            id="ids-only"
        ),

        pytest.param(
            [{"id": 1}, {"id": 3}, {"id": 4}],
            ["test_number_one", "test_number_three"],
            id="id-for-test-with-two-ids"
        ),

        pytest.param(
            [{"id": 1234}],
            [],
            id="id-nomatch"
        ),

        pytest.param(
            [
                {"selector": "test_number_one"},
                {"selector": "test_number_three"}
            ],
            ["test_number_one", "test_number_three"],
            id="selectors-only"
        ),

        pytest.param(
            [{"selector": "test_without_number"}],
            ["test_without_number"],
            id="selector-for-test-with-noid"
        ),

        pytest.param(
            [{"id": 2, "selector": "test_number_two"}],
            ["test_number_two"],
            id="id-selector-same-test"
        ),

        pytest.param(
            [{"selector": "test_without_never"}],
            [],
            id="selector-nomatch"
        ),

        pytest.param(
            None,
            ["test_number_one", "test_number_two", "test_number_three", "test_without_number"],
            id="noplan"
        ),
    ]
)
def test_select_by_testcase_id_test(
    planned_tests: Sequence[dict],
    expected_tests: Sequence[str],
    allured_testdir: AlluredTestdir
):
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

    test_name = inspect.currentframe().f_code.co_name
    if planned_tests:
        for item in planned_tests:
            if "selector" in item:
                selector = item['selector']
                item["selector"] = f"{test_name}#{selector}"

        testplan = {"tests": planned_tests}
        py_path = allured_testdir.testdir.makefile(".json", json.dumps(testplan))
        os.environ["ALLURE_TESTPLAN_PATH"] = str(py_path)
    else:
        os.environ.pop("ALLURE_TESTPLAN_PATH", None)

    allured_testdir.parse_docstring_source()
    allured_testdir.run_with_allure("--rootdir", allured_testdir.testdir.path)

    executed_full_names = [
        tc["fullName"] for tc in allured_testdir.allure_report.test_cases
    ]

    assert_that(
        executed_full_names,
        contains_inanyorder(
            * [ ends_with(name) for name in expected_tests ]
        )
    )
