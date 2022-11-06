""" ./examples/label/bdd/dynamic_bdd_label.rst """

import pytest
from hamcrest import assert_that
from allure_commons_test.report import has_test_case
from allure_commons_test.label import has_feature, has_epic, has_story


def test_dynamic_labels(executed_docstring_path):
    assert_that(executed_docstring_path.allure_report,
                has_test_case("test_dynamic_labels",
                              has_feature("first feature"),
                              has_feature("second feature"),
                              has_epic("first epic"),
                              has_epic("second epic"),
                              has_story("first story"),
                              has_story("second story"),
                              )
                )


@pytest.mark.parametrize("feature, epic, story", [("first feature", "first epic", "first story"),
                                                  ("second feature", "second epic", "second story")])
def test_parametrized_dynamic_labels(executed_docstring_path, feature, epic, story):
    assert_that(executed_docstring_path.allure_report,
                has_test_case("test_parametrized_dynamic_labels[{feature}-{epic}-{story}]".format(feature=feature,
                                                                                                  epic=epic,
                                                                                                  story=story),
                              has_feature(feature),
                              has_epic(epic),
                              has_story(story),
                              )
                )


def test_multiple_dynamic_labels(executed_docstring_path):
    assert_that(executed_docstring_path.allure_report,
                has_test_case("test_multiple_dynamic_labels",
                              has_feature("first feature"),
                              has_feature("second feature"),
                              has_epic("first epic"),
                              has_epic("second epic"),
                              has_story("first story"),
                              has_story("second story"),
                              )
                )
