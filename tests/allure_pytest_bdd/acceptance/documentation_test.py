from hamcrest import assert_that, equal_to

from allure_commons_test.report import has_test_case
from allure_commons_test.result import (
    has_preconditions, has_preconditions_html, has_expected_results, has_expected_results_html, with_status,
)


def test_preconditions_decorator_at_module_level(allure_pytest_bdd_runner):
    results = allure_pytest_bdd_runner.run_pytest(
        ("sample.feature", """
            Feature: Documentation
                Scenario: Documentation
                    Given noop
        """),
        """
            import allure
            from pytest_bdd import scenario, given

            pytestmark = [allure.preconditions("Preconditions")]

            @scenario("sample.feature", "Documentation")
            def test_documentation():
                pass

            @given("noop")
            def given_noop():
                pass
        """,
        cli_args=["--strict-markers"],
    )

    assert_that(
        results,
        has_test_case(
            "sample.feature:Documentation",
            with_status("passed"),
            has_preconditions(equal_to("Preconditions")),
        ),
    )


def test_preconditions_decorator(allure_pytest_bdd_runner):
    results = allure_pytest_bdd_runner.run_pytest(
        ("sample.feature", """
            Feature: Documentation
                Scenario: Documentation
                    Given noop
        """),
        """
            import allure
            from pytest_bdd import scenario, given

            pytestmark = [allure.preconditions("Module Preconditions")]

            @allure.preconditions("Preconditions")
            @scenario("sample.feature", "Documentation")
            def test_documentation():
                pass

            @given("noop")
            def given_noop():
                pass
        """,
        cli_args=["--strict-markers"],
    )

    assert_that(
        results,
        has_test_case(
            "sample.feature:Documentation",
            with_status("passed"),
            has_preconditions(equal_to("Preconditions")),
        ),
    )


def test_dynamic_preconditions(allure_pytest_bdd_runner):
    results = allure_pytest_bdd_runner.run_pytest(
        ("sample.feature", """
            Feature: Documentation
                Scenario: Documentation
                    Given noop
        """),
        """
            import allure
            from pytest_bdd import scenario, given

            pytestmark = [allure.preconditions("Module Preconditions")]

            @allure.preconditions("Function Preconditions")
            @scenario("sample.feature", "Documentation")
            def test_documentation():
                allure.dynamic.preconditions("Preconditions")

            @given("noop")
            def given_noop():
                pass
        """,
        cli_args=["--strict-markers"],
    )

    assert_that(
        results,
        has_test_case(
            "sample.feature:Documentation",
            with_status("passed"),
            has_preconditions(equal_to("Preconditions")),
        ),
    )


def test_preconditions_html_decorator_at_module_level(allure_pytest_bdd_runner):
    results = allure_pytest_bdd_runner.run_pytest(
        ("sample.feature", """
            Feature: Documentation
                Scenario: Documentation
                    Given noop
        """),
        """
            import allure
            from pytest_bdd import scenario, given

            pytestmark = [allure.preconditions_html("<p>Preconditions</p>")]

            @scenario("sample.feature", "Documentation")
            def test_documentation():
                pass

            @given("noop")
            def given_noop():
                pass
        """,
        cli_args=["--strict-markers"],
    )

    assert_that(
        results,
        has_test_case(
            "sample.feature:Documentation",
            with_status("passed"),
            has_preconditions_html(equal_to("<p>Preconditions</p>")),
        ),
    )


def test_preconditions_html_decorator(allure_pytest_bdd_runner):
    results = allure_pytest_bdd_runner.run_pytest(
        ("sample.feature", """
            Feature: Documentation
                Scenario: Documentation
                    Given noop
        """),
        """
            import allure
            from pytest_bdd import scenario, given

            pytestmark = [allure.preconditions_html("<p>Module Preconditions</p>")]

            @allure.preconditions_html("<p>Preconditions</p>")
            @scenario("sample.feature", "Documentation")
            def test_documentation():
                pass

            @given("noop")
            def given_noop():
                pass
        """,
        cli_args=["--strict-markers"],
    )

    assert_that(
        results,
        has_test_case(
            "sample.feature:Documentation",
            with_status("passed"),
            has_preconditions_html(equal_to("<p>Preconditions</p>")),
        ),
    )


def test_dynamic_preconditions_html(allure_pytest_bdd_runner):
    results = allure_pytest_bdd_runner.run_pytest(
        ("sample.feature", """
            Feature: Documentation
                Scenario: Documentation
                    Given noop
        """),
        """
            import allure
            from pytest_bdd import scenario, given

            pytestmark = [allure.preconditions_html("<p>Module Preconditions</p>")]

            @allure.preconditions_html("<p>Function Preconditions</p>")
            @scenario("sample.feature", "Documentation")
            def test_documentation():
                allure.dynamic.preconditions_html("<p>Preconditions</p>")

            @given("noop")
            def given_noop():
                pass
        """,
        cli_args=["--strict-markers"],
    )

    assert_that(
        results,
        has_test_case(
            "sample.feature:Documentation",
            with_status("passed"),
            has_preconditions_html(equal_to("<p>Preconditions</p>")),
        ),
    )


def test_expected_results_decorator_at_module_level(allure_pytest_bdd_runner):
    results = allure_pytest_bdd_runner.run_pytest(
        ("sample.feature", """
            Feature: Documentation
                Scenario: Documentation
                    Given noop
        """),
        """
            import allure
            from pytest_bdd import scenario, given

            pytestmark = [allure.expected_results("Expected results")]

            @scenario("sample.feature", "Documentation")
            def test_documentation():
                pass

            @given("noop")
            def given_noop():
                pass
        """,
        cli_args=["--strict-markers"],
    )

    assert_that(
        results,
        has_test_case(
            "sample.feature:Documentation",
            with_status("passed"),
            has_expected_results(equal_to("Expected results")),
        ),
    )


def test_expected_results_decorator(allure_pytest_bdd_runner):
    results = allure_pytest_bdd_runner.run_pytest(
        ("sample.feature", """
            Feature: Documentation
                Scenario: Documentation
                    Given noop
        """),
        """
            import allure
            from pytest_bdd import scenario, given

            pytestmark = [allure.expected_results("Module Expected results")]

            @allure.expected_results("Expected results")
            @scenario("sample.feature", "Documentation")
            def test_documentation():
                pass

            @given("noop")
            def given_noop():
                pass
        """,
        cli_args=["--strict-markers"],
    )

    assert_that(
        results,
        has_test_case(
            "sample.feature:Documentation",
            with_status("passed"),
            has_expected_results(equal_to("Expected results")),
        ),
    )


def test_dynamic_expected_results(allure_pytest_bdd_runner):
    results = allure_pytest_bdd_runner.run_pytest(
        ("sample.feature", """
            Feature: Documentation
                Scenario: Documentation
                    Given noop
        """),
        """
            import allure
            from pytest_bdd import scenario, given

            pytestmark = [allure.expected_results("Module Expected results")]

            @allure.expected_results("Function Expected results")
            @scenario("sample.feature", "Documentation")
            def test_documentation():
                allure.dynamic.expected_results("Expected results")

            @given("noop")
            def given_noop():
                pass
        """,
        cli_args=["--strict-markers"],
    )

    assert_that(
        results,
        has_test_case(
            "sample.feature:Documentation",
            with_status("passed"),
            has_expected_results(equal_to("Expected results")),
        ),
    )


def test_expected_results_html_decorator_at_module_level(allure_pytest_bdd_runner):
    results = allure_pytest_bdd_runner.run_pytest(
        ("sample.feature", """
            Feature: Documentation
                Scenario: Documentation
                    Given noop
        """),
        """
            import allure
            from pytest_bdd import scenario, given

            pytestmark = [allure.expected_results_html("<p>Expected results</p>")]

            @scenario("sample.feature", "Documentation")
            def test_documentation():
                pass

            @given("noop")
            def given_noop():
                pass
        """,
        cli_args=["--strict-markers"],
    )

    assert_that(
        results,
        has_test_case(
            "sample.feature:Documentation",
            with_status("passed"),
            has_expected_results_html(equal_to("<p>Expected results</p>")),
        ),
    )


def test_expected_results_html_decorator(allure_pytest_bdd_runner):
    results = allure_pytest_bdd_runner.run_pytest(
        ("sample.feature", """
            Feature: Documentation
                Scenario: Documentation
                    Given noop
        """),
        """
            import allure
            from pytest_bdd import scenario, given

            pytestmark = [allure.expected_results_html("<p>Module Expected results</p>")]

            @allure.expected_results_html("<p>Expected results</p>")
            @scenario("sample.feature", "Documentation")
            def test_documentation():
                pass

            @given("noop")
            def given_noop():
                pass
        """,
        cli_args=["--strict-markers"],
    )

    assert_that(
        results,
        has_test_case(
            "sample.feature:Documentation",
            with_status("passed"),
            has_expected_results_html(equal_to("<p>Expected results</p>")),
        ),
    )


def test_dynamic_expected_results_html(allure_pytest_bdd_runner):
    results = allure_pytest_bdd_runner.run_pytest(
        ("sample.feature", """
            Feature: Documentation
                Scenario: Documentation
                    Given noop
        """),
        """
            import allure
            from pytest_bdd import scenario, given

            pytestmark = [allure.expected_results_html("<p>Module Expected results</p>")]

            @allure.expected_results_html("<p>Function Expected results</p>")
            @scenario("sample.feature", "Documentation")
            def test_documentation():
                allure.dynamic.expected_results_html("<p>Expected results</p>")

            @given("noop")
            def given_noop():
                pass
        """,
        cli_args=["--strict-markers"],
    )

    assert_that(
        results,
        has_test_case(
            "sample.feature:Documentation",
            with_status("passed"),
            has_expected_results_html(equal_to("<p>Expected results</p>")),
        ),
    )
