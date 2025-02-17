from typing import Any, Tuple

import pytest
from allure_commons_test.label import (
    has_epic,
    has_feature,
    has_story,
    has_label,
    has_parent_suite,
    has_suite,
    has_sub_suite,
    has_tag,
    has_severity,
)
from allure_commons_test.report import has_test_case
from allure_commons_test.result import (
    has_history_id,
    has_step,
    with_status,
    has_description,
    has_link,
    has_issue_link,
    has_test_case_link,
)
from hamcrest import assert_that

from tests.allure_pytest.pytest_runner import AllurePytestRunner


@pytest.fixture
def feature_content():
    return (
        """
        Feature: Basic allure-pytest-bdd usage
            Scenario: Simple passed example
                Given the preconditions are satisfied
                When the action is invoked
                Then the postconditions are held
        """
    )


@pytest.mark.parametrize("test_name,decorators,checks", [
    (
        "suites_labels",
        """
        @allure.suite('My Suite')
        @allure.parent_suite('My Parent Suite')
        @allure.sub_suite('My Sub Suite')
        """.strip(),
        (
            has_parent_suite('My Parent Suite'),
            has_suite('My Suite'),
            has_sub_suite('My Sub Suite'),
        ),
    ),
    (
        "bdd_labels",
        """
        @allure.epic('My epic')
        @allure.feature('My feature')
        @allure.story('My story')
        @allure.description('My description')
        """.strip(),
        (
            has_feature("Basic allure-pytest-bdd usage"),  # from the scenario
            has_epic("My epic"),
            has_feature("My feature"),
            has_story("My story"),
            has_description("My description"),
        ),
    ),
    (
        "bdd_multiply_labels",
        """
        @allure.epic('My epic 1')
        @allure.epic('My epic 2')
        @allure.feature('My feature 2')
        @allure.feature('My feature 3')
        @allure.story('My story 1')
        @allure.story('My story 2')
        """.strip(),
        (
            has_epic("My epic 1"),
            has_epic("My epic 2"),
            has_feature("Basic allure-pytest-bdd usage"),
            has_feature("My feature 2"),
            has_feature("My feature 3"),
            has_story("My story 1"),
            has_story("My story 2"),
        ),
    ),
    (
        "id_label",
        """
        @allure.id(123)
        """.strip(),
        (
            has_label("as_id", 123),
        ),
    ),
    (
        "severity_label",
        """
        @allure.severity('critical')
        """.strip(),
        (
            has_severity("critical"),
        ),
    ),
    (
        "manual_label",
        """
        @allure.manual
        """.strip(),
        (
            has_label("ALLURE_MANUAL", True),
        ),
    ),
    (
        "tags",
        """
        @pytest.mark.cool
        @pytest.mark.stuff
        @allure.tag('foo')
        """.strip(),
        (
            has_tag("cool"),
            has_tag("stuff"),
            has_tag("foo"),
        ),
    ),
    (
        "custom_labels",  # !!!
        """
        @allure.label("Application", "desktop", "mobile")
        """.strip(),
        (
            has_label("Application", "desktop"),
            has_label("Application", "mobile"),
        ),
    ),
    (
        "links",
        """
        @allure.link('https://example.org/simple-link')
        @allure.issue('https://example.org/issue')
        @allure.testcase('https://example.org/testcase')
        """.strip(),
        (
            has_link('https://example.org/simple-link'),
            has_issue_link('https://example.org/issue'),
            has_test_case_link('https://example.org/testcase'),
        ),
    ),
])
def test_simple_passed_scenario_with_allure_decorators(
    test_name: str,
    decorators: str,
    checks: Tuple[Any],
    allure_pytest_bdd_runner: AllurePytestRunner,
    feature_content: str,
):
    steps_content = f"""
        import allure
        import pytest
        from pytest_bdd import scenario, given, when, then

        {decorators}
        @scenario("scenario.feature", "Simple passed example")
        def test_scenario_passes():
            pass

        @given("the preconditions are satisfied")
        def given_the_preconditions_are_satisfied():
            pass

        @when("the action is invoked")
        def when_the_action_is_invoked():
            pass

        @then("the postconditions are held")
        def then_the_postconditions_are_held():
            pass
        """

    output = allure_pytest_bdd_runner.run_pytest(
        ("scenario.feature", feature_content),
        steps_content
    )

    assert_that(
        output,
        has_test_case(
            "Simple passed example",
            with_status("passed"),
            has_step("Given the preconditions are satisfied"),
            has_step("When the action is invoked"),
            has_step("Then the postconditions are held"),
            has_history_id(),
            *checks,
        )
    )
