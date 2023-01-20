""" ./examples/label/bdd/bdd_label.rst """
import json

from hamcrest import assert_that, calling, is_not, raises
from allure_commons_test.report import has_test_case
from allure_commons_test.label import has_epic
from allure_commons_test.label import has_feature
from allure_commons_test.label import has_story


def test_single_bdd_label(executed_docstring_path):
    assert_that(executed_docstring_path.allure_report,
                has_test_case("test_single_bdd_label",
                              has_epic("My epic"),
                              has_feature("My feature"),
                              has_story("My story")
                              )
                )


def test_multiple_bdd_label(executed_docstring_path):
    assert_that(executed_docstring_path.allure_report,
                has_test_case("test_multiple_bdd_label",
                              has_epic("My epic"),
                              has_epic("Another epic"),
                              has_feature("My feature"),
                              has_feature("Another feature"),
                              has_feature("One more feature"),
                              has_story("My story"),
                              has_story("Alternative story")
                              )
                )


def test_set_bdd_label_as_object(executed_docstring_source):
    """
    >>> import allure

    >>> class SomeClass:
    ...     pass

    >>> @allure.feature(SomeClass())
    ... def test_set_label_as_object_example():
    ...     allure.dynamic.feature(SomeClass)
    """

    assert_that(
        calling(json.dumps).with_args(executed_docstring_source.allure_report.test_cases),
        is_not(raises(TypeError, 'not JSON serializable'))
    )
