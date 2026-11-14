from hamcrest import assert_that, equal_to

from allure_commons_test.report import has_test_case
from allure_commons_test.result import (
    has_preconditions, has_preconditions_html, has_expected_results, has_expected_results_html, with_status,
)


def test_preconditions_decorator_at_module_level(allure_pytest_runner):
    results = allure_pytest_runner.run_pytest("""
        import allure

        pytestmark = [allure.preconditions("Preconditions")]

        class TestDocumentation:
            def test_documentation(self):
                pass
    """, cli_args=["--strict-markers"])

    assert_that(
        results,
        has_test_case(
            "test_documentation",
            with_status("passed"),
            has_preconditions(equal_to("Preconditions")),
        ),
    )


def test_preconditions_decorator_at_class_level(allure_pytest_runner):
    results = allure_pytest_runner.run_pytest("""
        import allure

        pytestmark = [allure.preconditions("Module Preconditions")]

        @allure.preconditions("Preconditions")
        class TestDocumentation:
            def test_documentation(self):
                pass
    """, cli_args=["--strict-markers"])

    assert_that(
        results,
        has_test_case(
            "test_documentation",
            with_status("passed"),
            has_preconditions(equal_to("Preconditions")),
        ),
    )


def test_preconditions_decorator(allure_pytest_runner):
    results = allure_pytest_runner.run_pytest("""
        import allure

        pytestmark = [allure.preconditions("Module Preconditions")]

        @allure.preconditions("Class Preconditions")
        class TestDocumentation:
            @allure.preconditions("Preconditions")
            def test_documentation(self):
                pass
    """, cli_args=["--strict-markers"])

    assert_that(
        results,
        has_test_case(
            "test_documentation",
            with_status("passed"),
            has_preconditions(equal_to("Preconditions")),
        ),
    )


def test_dynamic_preconditions_taking_precedence(allure_pytest_runner):
    results = allure_pytest_runner.run_pytest("""
        import allure

        pytestmark = [allure.preconditions("Module Preconditions")]

        @allure.preconditions("Class Preconditions")
        class TestDocumentation:
            @allure.preconditions("Function Preconditions")
            def test_documentation(self):
                allure.dynamic.preconditions("Preconditions")
    """, cli_args=["--strict-markers"])

    assert_that(
        results,
        has_test_case(
            "test_documentation",
            with_status("passed"),
            has_preconditions(equal_to("Preconditions")),
        ),
    )


def test_preconditions_html_decorator_at_module_level(allure_pytest_runner):
    results = allure_pytest_runner.run_pytest("""
        import allure

        pytestmark = [allure.preconditions_html("<p>Preconditions</p>")]

        class TestDocumentation:
            def test_documentation(self):
                pass
    """, cli_args=["--strict-markers"])

    assert_that(
        results,
        has_test_case(
            "test_documentation",
            with_status("passed"),
            has_preconditions_html(equal_to("<p>Preconditions</p>")),
        ),
    )


def test_preconditions_html_decorator_at_class_level(allure_pytest_runner):
    results = allure_pytest_runner.run_pytest("""
        import allure

        pytestmark = [allure.preconditions_html("<p>Module Preconditions</p>")]

        @allure.preconditions_html("<p>Preconditions</p>")
        class TestDocumentation:
            def test_documentation(self):
                pass
    """, cli_args=["--strict-markers"])

    assert_that(
        results,
        has_test_case(
            "test_documentation",
            with_status("passed"),
            has_preconditions_html(equal_to("<p>Preconditions</p>")),
        ),
    )


def test_preconditions_html_decorator(allure_pytest_runner):
    results = allure_pytest_runner.run_pytest("""
        import allure

        pytestmark = [allure.preconditions_html("<p>Module Preconditions</p>")]

        @allure.preconditions_html("<p>Class Preconditions</p>")
        class TestDocumentation:
            @allure.preconditions_html("<p>Preconditions</p>")
            def test_documentation(self):
                pass
    """, cli_args=["--strict-markers"])

    assert_that(
        results,
        has_test_case(
            "test_documentation",
            with_status("passed"),
            has_preconditions_html(equal_to("<p>Preconditions</p>")),
        ),
    )


def test_dynamic_preconditions_html_taking_precedence(allure_pytest_runner):
    results = allure_pytest_runner.run_pytest("""
        import allure

        pytestmark = [allure.preconditions_html("<p>Module Preconditions</p>")]

        @allure.preconditions_html("<p>Class Preconditions</p>")
        class TestDocumentation:
            @allure.preconditions_html("<p>Function Preconditions</p>")
            def test_documentation(self):
                allure.dynamic.preconditions_html("<p>Preconditions</p>")
    """, cli_args=["--strict-markers"])

    assert_that(
        results,
        has_test_case(
            "test_documentation",
            with_status("passed"),
            has_preconditions_html(equal_to("<p>Preconditions</p>")),
        ),
    )


def test_expected_results_decorator_at_module_level(allure_pytest_runner):
    results = allure_pytest_runner.run_pytest("""
        import allure

        pytestmark = [allure.expected_results("Expected results")]

        class TestDocumentation:
            def test_documentation(self):
                pass
    """, cli_args=["--strict-markers"])

    assert_that(
        results,
        has_test_case(
            "test_documentation",
            with_status("passed"),
            has_expected_results(equal_to("Expected results")),
        ),
    )


def test_expected_results_decorator_at_class_level(allure_pytest_runner):
    results = allure_pytest_runner.run_pytest("""
        import allure

        pytestmark = [allure.expected_results("Module expected results")]

        @allure.expected_results("Expected results")
        class TestDocumentation:
            def test_documentation(self):
                pass
    """, cli_args=["--strict-markers"])

    assert_that(
        results,
        has_test_case(
            "test_documentation",
            with_status("passed"),
            has_expected_results(equal_to("Expected results")),
        ),
    )


def test_expected_results_decorator(allure_pytest_runner):
    results = allure_pytest_runner.run_pytest("""
        import allure

        pytestmark = [allure.expected_results("Module expected results")]

        @allure.expected_results("Class expected results")
        class TestDocumentation:
            @allure.expected_results("Expected results")
            def test_documentation(self):
                pass
    """, cli_args=["--strict-markers"])

    assert_that(
        results,
        has_test_case(
            "test_documentation",
            with_status("passed"),
            has_expected_results(equal_to("Expected results")),
        ),
    )


def test_dynamic_expected_results_taking_precedence(allure_pytest_runner):
    results = allure_pytest_runner.run_pytest("""
        import allure

        pytestmark = [allure.expected_results("Module expected results")]

        @allure.expected_results("Class expected results")
        class TestDocumentation:
            @allure.expected_results("Function expected results")
            def test_documentation(self):
                allure.dynamic.expected_results("Expected results")
    """, cli_args=["--strict-markers"])

    assert_that(
        results,
        has_test_case(
            "test_documentation",
            with_status("passed"),
            has_expected_results(equal_to("Expected results")),
        ),
    )


def test_expected_results_html_decorator_at_module_level(allure_pytest_runner):
    results = allure_pytest_runner.run_pytest("""
        import allure

        pytestmark = [allure.expected_results_html("<p>Expected results</p>")]

        class TestDocumentation:
            def test_documentation(self):
                pass
    """, cli_args=["--strict-markers"])

    assert_that(
        results,
        has_test_case(
            "test_documentation",
            with_status("passed"),
            has_expected_results_html(equal_to("<p>Expected results</p>")),
        ),
    )


def test_expected_results_html_decorator_at_class_level(allure_pytest_runner):
    results = allure_pytest_runner.run_pytest("""
        import allure

        pytestmark = [allure.expected_results_html("<p>Module expected results</p>")]

        @allure.expected_results_html("<p>Expected results</p>")
        class TestDocumentation:
            def test_documentation(self):
                pass
    """, cli_args=["--strict-markers"])

    assert_that(
        results,
        has_test_case(
            "test_documentation",
            with_status("passed"),
            has_expected_results_html(equal_to("<p>Expected results</p>")),
        ),
    )


def test_expected_results_html_decorator(allure_pytest_runner):
    results = allure_pytest_runner.run_pytest("""
        import allure

        pytestmark = [allure.expected_results_html("<p>Module expected results</p>")]

        @allure.expected_results_html("<p>Class expected results</p>")
        class TestDocumentation:
            @allure.expected_results_html("<p>Expected results</p>")
            def test_documentation(self):
                pass
    """, cli_args=["--strict-markers"])

    assert_that(
        results,
        has_test_case(
            "test_documentation",
            with_status("passed"),
            has_expected_results_html(equal_to("<p>Expected results</p>")),
        ),
    )


def test_dynamic_expected_results_html_taking_precedence(allure_pytest_runner):
    results = allure_pytest_runner.run_pytest("""
        import allure

        pytestmark = [allure.expected_results_html("<p>Module expected results</p>")]

        @allure.expected_results_html("<p>Class expected results</p>")
        class TestDocumentation:
            @allure.expected_results_html("<p>Function expected results</p>")
            def test_documentation(self):
                allure.dynamic.expected_results_html("<p>Expected results</p>")
    """, cli_args=["--strict-markers"])

    assert_that(
        results,
        has_test_case(
            "test_documentation",
            with_status("passed"),
            has_expected_results_html(equal_to("<p>Expected results</p>")),
        ),
    )


def test_documentation_fields_are_independent(allure_pytest_runner):
    results = allure_pytest_runner.run_pytest("""
        import allure

        @allure.description("Description")
        @allure.description_html("<p>Description</p>")
        @allure.preconditions("Preconditions")
        @allure.preconditions_html("<p>Preconditions</p>")
        @allure.expected_results("Expected results")
        @allure.expected_results_html("<p>Expected results</p>")
        def test_documentation():
            allure.dynamic.preconditions("Updated preconditions")
            allure.dynamic.preconditions("Final preconditions")

        def test_without_documentation():
            pass
    """)

    documented, undocumented = results.test_cases
    assert documented["description"] == "Description"
    assert documented["descriptionHtml"] == "<p>Description</p>"
    assert documented["precondition"] == "Final preconditions"
    assert documented["preconditionHtml"] == "<p>Preconditions</p>"
    assert documented["expectedResult"] == "Expected results"
    assert documented["expectedResultHtml"] == "<p>Expected results</p>"
    for field in ("precondition", "preconditionHtml", "expectedResult", "expectedResultHtml"):
        assert field not in undocumented
