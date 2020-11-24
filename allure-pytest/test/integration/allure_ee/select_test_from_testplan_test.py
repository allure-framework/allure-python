import pytest
import json
import os
from hamcrest import assert_that, contains_inanyorder, ends_with


@pytest.mark.parametrize(
    ["planned_tests", "expected_tests"],
    [
        # by ids only
        (
            [{"id": 1}, {"id": 2}],
            ["test_number_one", "test_number_two"]
        ),

        # by ids for multiply decorated test
        (
            [{"id": 1}, {"id": 3}, {"id": 4}],
            ["test_number_one", "test_number_three"]
        ),

        # by wrong id
        (
            [{"id": 1234}],
            []
        ),

        # by selectors only
        (
            [{"selector": "test_number_one"}, {"selector": "test_number_three"}],
            ["test_number_one", "test_number_three"]
        ),

        # by selector for not decorated with id test
        (
            [{"selector": "test_without_number"}],
            ["test_without_number"]
        ),

        # by id and selector for same test
        (
            [{"id": 2, "selector": "test_number_two"}],
            ["test_number_two"]
        ),

        # by wrong selector
        (
            [{"selector": "test_without_never"}],
            []
        ),

        # without plan
        (
            None,
            ["test_number_one", "test_number_two", "test_number_three", "test_without_number"]
        ),
    ]
)
def test_select_by_testcase_id_test(planned_tests, expected_tests, allured_testdir, request):
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

    root_dir = request.config.rootdir.strpath
    test_dir = allured_testdir.testdir.tmpdir.strpath.replace(root_dir, "")
    full_name_base_template = "{base}.test_select_by_testcase_id_test".format(
        base=test_dir.strip(os.sep).replace(os.sep, "."))

    if planned_tests:
        for item in planned_tests:
            if "selector" in item:
                item["selector"] = "{base}#{name}".format(base=full_name_base_template, name=item["selector"])

        testplan = {"tests": planned_tests}
        py_path = allured_testdir.testdir.makefile(".json", json.dumps(testplan))
        os.environ["ALLURE_TESTPLAN_PATH"] = py_path.strpath
    else:
        os.environ.pop("ALLURE_TESTPLAN_PATH", None)

    allured_testdir.parse_docstring_source()
    allured_testdir.run_with_allure()

    executed_full_names = [test_case["fullName"] for test_case in allured_testdir.allure_report.test_cases]

    assert_that(executed_full_names, contains_inanyorder(*[ends_with(name) for name in expected_tests]))
