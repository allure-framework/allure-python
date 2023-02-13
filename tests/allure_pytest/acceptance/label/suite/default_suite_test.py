from doctest import script_from_examples
from tests.conftest import AlluredTestdir
from hamcrest import assert_that, anything, not_
from allure_commons_test.report import has_test_case
from allure_commons_test.label import has_parent_suite
from allure_commons_test.label import has_suite
from allure_commons_test.label import has_sub_suite


def test_default_suites_no_parent_module(executed_docstring_source):
    """
    >>> def test_default_suite_example():
    ...     pass
    """

    assert_that(
        executed_docstring_source.allure_report,
        has_test_case(
            "test_default_suite_example",
            not_(has_parent_suite(anything())),
            has_suite("test_default_suites_no_parent_module"),
            not_(has_sub_suite(anything()))
        )
    )


def test_default_suites_class_no_parent_module(executed_docstring_source):
    """
    >>> class TestSuiteClass:
    ...     def test_default_class_suite_example(self):
    ...         pass

    """

    assert_that(
        executed_docstring_source.allure_report,
        has_test_case(
            "test_default_class_suite_example",
            not_(has_parent_suite(anything())),
            has_suite("test_default_suites_class_no_parent_module"),
            has_sub_suite("TestSuiteClass")
        )
    )


def test_default_suites_with_class_and_parent_module(
    docstring: str,
    allured_testdir: AlluredTestdir
):
    """
    >>> class TestSuiteClass:
    ...     def test_default_class_suite_example(self):
    ...         pass

    """

    content = script_from_examples(docstring)
    allured_testdir.testdir.makepyfile(
        **{
            "parent_module/test_default_suites_with_parent_module.py": content
        }
    )
    allured_testdir.run_with_allure()

    assert_that(
        allured_testdir.allure_report,
        has_test_case(
            "test_default_class_suite_example",
            has_parent_suite("parent_module"),
            has_suite("test_default_suites_with_parent_module"),
            has_sub_suite("TestSuiteClass")
        )
    )


def test_default_suites_with_parent_module(
    docstring: str,
    allured_testdir: AlluredTestdir
):
    """
    >>> def test_default_class_suite_example(self):
    ...     pass

    """

    content = script_from_examples(docstring)
    module = "test_default_suites_with_class_and_parent_module"
    filename = module + ".py"
    fullname = "parent_module/" + filename
    allured_testdir.testdir.makefile(
        ".py",
        **{fullname: content }
    )
    allured_testdir.run_with_allure()

    assert_that(
        allured_testdir.allure_report,
        has_test_case(
            "test_default_class_suite_example",
            has_parent_suite("parent_module"),
            has_suite(module),
            not_(has_sub_suite(anything()))
        )
    )


def test_default_suites_with_class_and_parent_module(
    docstring: str,
    allured_testdir: AlluredTestdir
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
    allured_testdir.testdir.makefile(
        ".py",
        **{fullname: content }
    )
    allured_testdir.run_with_allure()

    assert_that(
        allured_testdir.allure_report,
        has_test_case(
            "test_default_class_suite_example",
            has_parent_suite("parent_module"),
            has_suite(module),
            has_sub_suite("TestSuiteClass")
        )
    )
