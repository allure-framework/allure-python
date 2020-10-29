import unittest
from hamcrest import assert_that
from allure_commons_test.report import has_test_case
from allure_commons_test.label import has_epic
from allure_commons_test.label import has_feature
from test.example_runner import run_docstring_example


class TestBDDLabel(unittest.TestCase):
    def test_method_label(self):
        """
        >>> import unittest
        >>> import allure

        >>> class TestBDDLabelExample(unittest.TestCase):
        ...     @allure.epic("Label", "Bdd")
        ...     @allure.feature("Method label")
        ...     def test_method_label_example(self):
        ...         pass
        """
        allure_report = run_docstring_example()
        assert_that(allure_report,
                    has_test_case("test_method_label_example",
                                  has_epic("Label"),
                                  has_epic("Bdd"),
                                  has_feature("Method label")
                                  )
                    )

    def test_class_label(self):
        """
        >>> import unittest
        >>> import allure

        >>> @allure.epic("Label", "Bdd")
        ... class TestBDDLabelExample(unittest.TestCase):
        ...     def test_class_label_example(self):
        ...         pass
        """
        allure_report = run_docstring_example()
        assert_that(allure_report,
                    has_test_case("test_class_label_example",
                                  has_epic("Label"),
                                  has_epic("Bdd"),
                                  )
                    )

    def test_class_method_label(self):
        """
        >>> import unittest
        >>> import allure

        >>> @allure.epic("Label", "Bdd")
        ... class TestBDDLabelExample(unittest.TestCase):
        ...     @allure.feature("Method label")
        ...     def test_class_and_method_label_example(self):
        ...         pass
        """
        allure_report = run_docstring_example()
        assert_that(allure_report,
                    has_test_case("test_class_and_method_label_example",
                                  has_epic("Label"),
                                  has_epic("Bdd"),
                                  has_feature("Method label")
                                  )
                    )


def test_func_label():
    """
    >>> import allure

    >>> @allure.epic("Label", "Bdd")
    ... @allure.feature("Function label")
    ... def test_func_label_example():
    ...     pass
    """
    allure_report = run_docstring_example()
    assert_that(allure_report,
                has_test_case("test_func_label_example",
                              has_epic("Label"),
                              has_epic("Bdd"),
                              has_feature("Function label")
                              )
                )
