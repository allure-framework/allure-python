import pytest
from hamcrest import assert_that, contains_inanyorder, ends_with
from tests.allure_pytest.pytest_runner import AllurePytestRunner


@pytest.mark.parametrize(
    ["testplan", "expected_tests"],
    [
        pytest.param(
            {"tests": [{"id": 1}, {"id": 2}]},
            ["test_number_one", "test_number_two"],
            id="ids-only"
        ),

        pytest.param(
            {"tests": [{"id": 1}, {"id": 3}, {"id": 4}]},
            ["test_number_one", "test_number_three"],
            id="id-for-test-with-two-ids"
        ),

        pytest.param(
            {"tests": [{"id": 1234}]},
            [],
            id="id-nomatch"
        ),

        pytest.param(
            {"tests": [
                {"selector": "testplan_test#test_number_one"},
                {"selector": "testplan_test#test_number_three"}
            ]},
            ["test_number_one", "test_number_three"],
            id="selectors-only"
        ),

        pytest.param(
            {"tests": [{"selector": "testplan_test#test_without_number"}]},
            ["test_without_number"],
            id="selector-for-test-with-noid"
        ),

        pytest.param(
            {"tests": [{"id": 2, "selector": "testplan_test#test_number_two"}]},
            ["test_number_two"],
            id="id-selector-same-test"
        ),

        pytest.param(
            {"tests": [{"selector": "testplan_test#test_without_never"}]},
            [],
            id="selector-nomatch"
        ),

        pytest.param(
            {"tests": []},
            [
                "test_number_one",
                "test_number_two",
                "test_number_three",
                "test_without_number"
            ],
            id="no-tests-in-plan"
        ),

        pytest.param(
            {},
            [
                "test_number_one",
                "test_number_two",
                "test_number_three",
                "test_without_number"
            ],
            id="empty-plan"
        )
    ]
)
def test_select_by_testcase_id_test(
    allure_pytest_runner: AllurePytestRunner,
    testplan,
    expected_tests
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

    allure_results = allure_pytest_runner.run_docstring(
        filename="testplan_test",
        testplan=testplan
    )

    executed_full_names = [
        tc["fullName"] for tc in allure_results.test_cases
    ]

    assert_that(
        executed_full_names,
        contains_inanyorder(
            * [ends_with(name) for name in expected_tests]
        )
    )
