from hamcrest import assert_that
from tests.allure_nose2.nose2_runner import AllureNose2Runner

from allure_commons_test.report import has_test_case
from allure_commons_test.label import has_epic
from allure_commons_test.label import has_feature


def test_method_label(nose2_runner: AllureNose2Runner):
    """
    >>> import unittest
    >>> import allure

    >>> class TestBDDLabelExample(unittest.TestCase):
    ...     @allure.epic("Label", "Bdd")
    ...     @allure.feature("Method label")
    ...     def test_method_label_example(self):
    ...         pass
    """

    allure_report = nose2_runner.run_docstring()

    assert_that(
        allure_report,
        has_test_case(
            "test_method_label_example",
            has_epic("Label"),
            has_epic("Bdd"),
            has_feature("Method label")
        )
    )


def test_class_label(nose2_runner: AllureNose2Runner):
    """
    >>> import unittest
    >>> import allure

    >>> @allure.epic("Label", "Bdd")
    ... class TestBDDLabelExample(unittest.TestCase):
    ...     def test_class_label_example(self):
    ...         pass
    """

    allure_report = nose2_runner.run_docstring()

    assert_that(
        allure_report,
        has_test_case(
            "test_class_label_example",
            has_epic("Label"),
            has_epic("Bdd"),
        )
    )


def test_class_method_label(nose2_runner: AllureNose2Runner):
    """
    >>> import unittest
    >>> import allure

    >>> @allure.epic("Label", "Bdd")
    ... class TestBDDLabelExample(unittest.TestCase):
    ...     @allure.feature("Method label")
    ...     def test_class_and_method_label_example(self):
    ...         pass
    """

    allure_report = nose2_runner.run_docstring()

    assert_that(
        allure_report,
        has_test_case(
            "test_class_and_method_label_example",
            has_epic("Label"),
            has_epic("Bdd"),
            has_feature("Method label")
        )
    )


def test_func_label(nose2_runner: AllureNose2Runner):
    """
    >>> import allure

    >>> @allure.epic("Label", "Bdd")
    ... @allure.feature("Function label")
    ... def test_func_label_example():
    ...     pass
    """

    allure_report = nose2_runner.run_docstring()

    assert_that(
        allure_report,
        has_test_case(
            "test_func_label_example",
            has_epic("Label"),
            has_epic("Bdd"),
            has_feature("Function label")
        )
    )
