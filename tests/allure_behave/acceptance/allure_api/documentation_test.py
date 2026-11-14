from textwrap import dedent

from hamcrest import assert_that, equal_to

from allure_commons_test.report import has_test_case
from allure_commons_test.result import (
    has_preconditions, has_preconditions_html, has_expected_results, has_expected_results_html, with_status,
)


def test_dynamic_preconditions_from_step(behave_runner):
    results = behave_runner.run_behave(
        feature_literals=["""
            Feature: Documentation
                Scenario: Documentation
                    Given documentation
        """],
        step_literals=[dedent("""
            import allure
            from behave import given

            @given("documentation")
            def given_documentation(context):
                allure.dynamic.preconditions("Preconditions")
        """)],
    )

    assert_that(
        results,
        has_test_case(
            "Documentation",
            with_status("passed"),
            has_preconditions(equal_to("Preconditions")),
        ),
    )


def test_dynamic_preconditions_from_before_scenario(behave_runner):
    results = behave_runner.run_behave(
        feature_literals=["""
            Feature: Documentation
                Scenario: Documentation
                    Given documentation
        """],
        step_literals=[dedent("""
            import allure
            from behave import given

            @given("documentation")
            def given_documentation(context):
                pass
        """)],
        environment_literal=dedent("""
            import allure

            def before_scenario(context, scenario):
                allure.dynamic.preconditions("Preconditions")
        """),
    )

    assert_that(
        results,
        has_test_case(
            "Documentation",
            with_status("passed"),
            has_preconditions(equal_to("Preconditions")),
        ),
    )


def test_dynamic_preconditions_from_after_scenario(behave_runner):
    results = behave_runner.run_behave(
        feature_literals=["""
            Feature: Documentation
                Scenario: Documentation
                    Given documentation
        """],
        step_literals=[dedent("""
            import allure
            from behave import given

            @given("documentation")
            def given_documentation(context):
                pass
        """)],
        environment_literal=dedent("""
            import allure

            def after_scenario(context, scenario):
                allure.dynamic.preconditions("Preconditions")
        """),
    )

    assert_that(
        results,
        has_test_case(
            "Documentation",
            with_status("passed"),
            has_preconditions(equal_to("Preconditions")),
        ),
    )


def test_dynamic_preconditions_html_from_step(behave_runner):
    results = behave_runner.run_behave(
        feature_literals=["""
            Feature: Documentation
                Scenario: Documentation
                    Given documentation
        """],
        step_literals=[dedent("""
            import allure
            from behave import given

            @given("documentation")
            def given_documentation(context):
                allure.dynamic.preconditions_html("<p>Preconditions</p>")
        """)],
    )

    assert_that(
        results,
        has_test_case(
            "Documentation",
            with_status("passed"),
            has_preconditions_html(equal_to("<p>Preconditions</p>")),
        ),
    )


def test_dynamic_preconditions_html_from_before_scenario(behave_runner):
    results = behave_runner.run_behave(
        feature_literals=["""
            Feature: Documentation
                Scenario: Documentation
                    Given documentation
        """],
        step_literals=[dedent("""
            import allure
            from behave import given

            @given("documentation")
            def given_documentation(context):
                pass
        """)],
        environment_literal=dedent("""
            import allure

            def before_scenario(context, scenario):
                allure.dynamic.preconditions_html("<p>Preconditions</p>")
        """),
    )

    assert_that(
        results,
        has_test_case(
            "Documentation",
            with_status("passed"),
            has_preconditions_html(equal_to("<p>Preconditions</p>")),
        ),
    )


def test_dynamic_preconditions_html_from_after_scenario(behave_runner):
    results = behave_runner.run_behave(
        feature_literals=["""
            Feature: Documentation
                Scenario: Documentation
                    Given documentation
        """],
        step_literals=[dedent("""
            import allure
            from behave import given

            @given("documentation")
            def given_documentation(context):
                pass
        """)],
        environment_literal=dedent("""
            import allure

            def after_scenario(context, scenario):
                allure.dynamic.preconditions_html("<p>Preconditions</p>")
        """),
    )

    assert_that(
        results,
        has_test_case(
            "Documentation",
            with_status("passed"),
            has_preconditions_html(equal_to("<p>Preconditions</p>")),
        ),
    )


def test_dynamic_expected_results_from_step(behave_runner):
    results = behave_runner.run_behave(
        feature_literals=["""
            Feature: Documentation
                Scenario: Documentation
                    Given documentation
        """],
        step_literals=[dedent("""
            import allure
            from behave import given

            @given("documentation")
            def given_documentation(context):
                allure.dynamic.expected_results("Expected results")
        """)],
    )

    assert_that(
        results,
        has_test_case(
            "Documentation",
            with_status("passed"),
            has_expected_results(equal_to("Expected results")),
        ),
    )


def test_dynamic_expected_results_from_before_scenario(behave_runner):
    results = behave_runner.run_behave(
        feature_literals=["""
            Feature: Documentation
                Scenario: Documentation
                    Given documentation
        """],
        step_literals=[dedent("""
            import allure
            from behave import given

            @given("documentation")
            def given_documentation(context):
                pass
        """)],
        environment_literal=dedent("""
            import allure

            def before_scenario(context, scenario):
                allure.dynamic.expected_results("Expected results")
        """),
    )

    assert_that(
        results,
        has_test_case(
            "Documentation",
            with_status("passed"),
            has_expected_results(equal_to("Expected results")),
        ),
    )


def test_dynamic_expected_results_from_after_scenario(behave_runner):
    results = behave_runner.run_behave(
        feature_literals=["""
            Feature: Documentation
                Scenario: Documentation
                    Given documentation
        """],
        step_literals=[dedent("""
            import allure
            from behave import given

            @given("documentation")
            def given_documentation(context):
                pass
        """)],
        environment_literal=dedent("""
            import allure

            def after_scenario(context, scenario):
                allure.dynamic.expected_results("Expected results")
        """),
    )

    assert_that(
        results,
        has_test_case(
            "Documentation",
            with_status("passed"),
            has_expected_results(equal_to("Expected results")),
        ),
    )


def test_dynamic_expected_results_html_from_step(behave_runner):
    results = behave_runner.run_behave(
        feature_literals=["""
            Feature: Documentation
                Scenario: Documentation
                    Given documentation
        """],
        step_literals=[dedent("""
            import allure
            from behave import given

            @given("documentation")
            def given_documentation(context):
                allure.dynamic.expected_results_html("<p>Expected results</p>")
        """)],
    )

    assert_that(
        results,
        has_test_case(
            "Documentation",
            with_status("passed"),
            has_expected_results_html(equal_to("<p>Expected results</p>")),
        ),
    )


def test_dynamic_expected_results_html_from_before_scenario(behave_runner):
    results = behave_runner.run_behave(
        feature_literals=["""
            Feature: Documentation
                Scenario: Documentation
                    Given documentation
        """],
        step_literals=[dedent("""
            import allure
            from behave import given

            @given("documentation")
            def given_documentation(context):
                pass
        """)],
        environment_literal=dedent("""
            import allure

            def before_scenario(context, scenario):
                allure.dynamic.expected_results_html("<p>Expected results</p>")
        """),
    )

    assert_that(
        results,
        has_test_case(
            "Documentation",
            with_status("passed"),
            has_expected_results_html(equal_to("<p>Expected results</p>")),
        ),
    )


def test_dynamic_expected_results_html_from_after_scenario(behave_runner):
    results = behave_runner.run_behave(
        feature_literals=["""
            Feature: Documentation
                Scenario: Documentation
                    Given documentation
        """],
        step_literals=[dedent("""
            import allure
            from behave import given

            @given("documentation")
            def given_documentation(context):
                pass
        """)],
        environment_literal=dedent("""
            import allure

            def after_scenario(context, scenario):
                allure.dynamic.expected_results_html("<p>Expected results</p>")
        """),
    )

    assert_that(
        results,
        has_test_case(
            "Documentation",
            with_status("passed"),
            has_expected_results_html(equal_to("<p>Expected results</p>")),
        ),
    )
