import pytest

from hamcrest import assert_that
from hamcrest import equal_to, ends_with

from allure_commons_test.content import csv_equivalent
from allure_commons_test.report import has_test_case
from allure_commons_test.result import has_attachment_with_content
from allure_commons_test.result import has_step
from allure_commons_test.result import doesnt_have_parameter

from tests.allure_pytest.pytest_runner import AllurePytestRunner
from tests.e2e import version_unmet


def test_attach_content_from_scenario_function(allure_pytest_bdd_runner: AllurePytestRunner):
    feature_content = (
        """
        Feature: Foo
            Scenario: Bar
                Given noop
        """
    )
    steps_content = (
        """
        from pytest_bdd import scenario, given
        import allure

        @scenario("sample.feature", "Bar")
        def test_scenario():
            allure.attach("Lorem Ipsum", name="foo")

        @given("noop")
        def given_noop():
            pass
        """
    )

    allure_results = allure_pytest_bdd_runner.run_pytest(
        ("sample.feature", feature_content),
        steps_content,

    )

    assert_that(
        allure_results,
        has_test_case(
            "sample.feature:Bar",
            has_attachment_with_content(
                allure_results.attachments,
                equal_to("Lorem Ipsum"),
                name="foo",
            )
        )
    )


def test_attach_file_from_scenario_function(allure_pytest_bdd_runner: AllurePytestRunner):
    feature_content = (
        """
        Feature: Foo
            Scenario: Bar
                Given noop
        """
    )
    steps_content = (
        """
        from pytest_bdd import scenario, given
        import allure

        @scenario("sample.feature", "Bar")
        def test_scenario():
            allure.attach.file(__file__, name="foo")

        @given("noop")
        def given_noop():
            pass
        """
    )

    allure_results = allure_pytest_bdd_runner.run_pytest(
        ("sample.feature", feature_content),
        steps_content,

    )

    assert_that(
        allure_results,
        has_test_case(
            "sample.feature:Bar",
            has_attachment_with_content(
                allure_results.attachments,
                ends_with("test_attach_file_from_scenario_function.py"),
                name="foo",
            )
        )
    )


def test_attach_content_from_step(allure_pytest_bdd_runner: AllurePytestRunner):
    feature_content = (
        """
        Feature: Foo
            Scenario: Bar
                When data is attached
        """
    )
    steps_content = (
        """
        from pytest_bdd import scenario, when
        import allure

        @scenario("sample.feature", "Bar")
        def test_scenario():
            pass

        @when("data is attached")
        def when_data_is_attached():
            allure.attach("Lorem Ipsum", name="foo")
        """
    )

    allure_results = allure_pytest_bdd_runner.run_pytest(
        ("sample.feature", feature_content),
        steps_content,

    )

    assert_that(
        allure_results,
        has_test_case(
            "sample.feature:Bar",
            has_step(
                "When data is attached",
                has_attachment_with_content(
                    allure_results.attachments,
                    equal_to("Lorem Ipsum"),
                    name="foo",
                ),
            ),
        ),
    )


def test_attach_file_from_step(allure_pytest_bdd_runner: AllurePytestRunner):
    feature_content = (
        """
        Feature: Foo
            Scenario: Bar
                When a file is attached
        """
    )
    steps_content = (
        """
        from pytest_bdd import scenario, when
        import allure

        @scenario("sample.feature", "Bar")
        def test_scenario():
            pass

        @when("a file is attached")
        def when_file_is_attached():
            allure.attach.file(__file__, name="foo")
        """
    )

    allure_results = allure_pytest_bdd_runner.run_pytest(
        ("sample.feature", feature_content),
        steps_content,
    )

    assert_that(
        allure_results,
        has_test_case(
            "sample.feature:Bar",
            has_step(
                "When a file is attached",
                has_attachment_with_content(
                    allure_results.attachments,
                    ends_with("test_attach_file_from_step.py"),
                    name="foo",
                ),
            ),
        ),
    )


@pytest.mark.skipif(version_unmet("pytest-bdd", 8), reason="Data tables support added in 8.0.0")
def test_attach_datatable(allure_pytest_bdd_runner: AllurePytestRunner):
    feature_content = (
        """
        Feature: Foo
            Scenario: Bar
                Given a datatable:
                    | foo | bar |
                    | baz | qux |
        """
    )
    steps_content = (
        """
        from pytest_bdd import scenario, given
        import allure

        @scenario("sample.feature", "Bar")
        def test_scenario():
            pass

        @given("a datatable:")
        def given_datatable(datatable):
            pass
        """
    )

    allure_results = allure_pytest_bdd_runner.run_pytest(
        ("sample.feature", feature_content),
        steps_content,
    )

    assert_that(
        allure_results,
        has_test_case(
            "sample.feature:Bar",
            has_step(
                "Given a datatable:",
                has_attachment_with_content(
                    allure_results.attachments,
                    csv_equivalent([
                        ["foo", "bar"],
                        ["baz", "qux"],
                    ]),
                    name="Data table",
                    attach_type="text/csv",
                ),
                doesnt_have_parameter("datatable"),
            ),
        ),
    )


@pytest.mark.skipif(version_unmet("pytest-bdd", 8), reason="Doc strings support added in 8.0.0")
def test_attach_docstring(allure_pytest_bdd_runner: AllurePytestRunner):
    feature_content = (
        '''
        Feature: Foo
            Scenario: Bar
                Given a docstring:
                    """
                    Lorem ipsum dolor sit amet, consectetur adipiscing elit
                    """
        '''
    )
    steps_content = (
        """
        from pytest_bdd import scenario, given
        import allure

        @scenario("sample.feature", "Bar")
        def test_scenario():
            pass

        @given("a docstring:")
        def given_docstring(docstring):
            pass
        """
    )

    allure_results = allure_pytest_bdd_runner.run_pytest(
        ("sample.feature", feature_content),
        steps_content,
    )

    assert_that(
        allure_results,
        has_test_case(
            "sample.feature:Bar",
            has_step(
                "Given a docstring:",
                has_attachment_with_content(
                    allure_results.attachments,
                    "Lorem ipsum dolor sit amet, consectetur adipiscing elit",
                    name="Doc string",
                    attach_type="text/plain",
                ),
                doesnt_have_parameter("docstring"),
            ),
        ),
    )
