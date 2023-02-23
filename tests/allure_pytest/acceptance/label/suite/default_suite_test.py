from doctest import script_from_examples
from hamcrest import assert_that, anything, not_
from tests.allure_pytest.pytest_runner import AllurePytestRunner

from allure_commons_test.report import has_test_case
from allure_commons_test.label import has_parent_suite
from allure_commons_test.label import has_suite
from allure_commons_test.label import has_sub_suite


def test_no_parent_module(
    allure_pytest_runner: AllurePytestRunner
):
    """
    >>> def test_default_suite_example():
    ...     pass
    """

    allure_results = allure_pytest_runner.run_docstring()

    assert_that(
        allure_results,
        has_test_case(
            "test_default_suite_example",
            not_(has_parent_suite(anything())),
            has_suite("test_no_parent_module"),
            not_(has_sub_suite(anything()))
        )
    )


def test_class_no_parent_module(
    allure_pytest_runner: AllurePytestRunner
):
    """
    >>> class TestSuiteClass:
    ...     def test_default_class_suite_example(self):
    ...         pass

    """

    allure_results = allure_pytest_runner.run_docstring()

    assert_that(
        allure_results,
        has_test_case(
            "test_default_class_suite_example",
            not_(has_parent_suite(anything())),
            has_suite("test_class_no_parent_module"),
            has_sub_suite("TestSuiteClass")
        )
    )


def test_with_parent_module(
    allure_pytest_runner: AllurePytestRunner,
    docstring
):
    """
    >>> def test_default_suite_example():
    ...     pass

    """

    content = script_from_examples(docstring)
    module = "test_default_suites_with_parent_module"
    filename = module + ".py"
    fullname = "parent_module/" + filename
    allure_pytest_runner.pytester.makepyfile(**{fullname: content})

    allure_results = allure_pytest_runner.run_pytest()

    assert_that(
        allure_results,
        has_test_case(
            "test_default_suite_example",
            has_parent_suite("parent_module"),
            has_suite(module),
            not_(has_sub_suite(anything()))
        )
    )


def test_with_class_and_parent_module(
    allure_pytest_runner: AllurePytestRunner,
    docstring
):
    """
    >>> class TestSuiteClass:
    ...     def test_default_class_suite_example(self):
    ...         pass

    """

    content = script_from_examples(docstring)
    module = "test_default_suites_with_class_and_parent_module"
    filename = module + ".py"
    fullname = "parent_module/" + filename
    allure_pytest_runner.pytester.makepyfile(**{fullname: content})

    allure_results = allure_pytest_runner.run_pytest()

    assert_that(
        allure_results,
        has_test_case(
            "test_default_class_suite_example",
            has_parent_suite("parent_module"),
            has_suite(module),
            has_sub_suite("TestSuiteClass")
        )
    )
