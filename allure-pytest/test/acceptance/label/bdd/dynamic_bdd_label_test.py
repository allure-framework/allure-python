""" ./examples/label/bdd/dynamic_bdd_label.rst """

import pytest
from hamcrest import assert_that
from allure_commons_test.report import has_test_case
from allure_commons_test.label import has_feature


def test_dynamic_feature(executed_docstring_path):
    assert_that(executed_docstring_path.allure_report,
                has_test_case("test_dynamic_feature",
                              has_feature("first feature"),
                              has_feature("second feature")
                              )
                )


@pytest.mark.parametrize("feature", ["first feature", "second feature"])
def test_parametrized_dynamic_feature(executed_docstring_path, feature):
    assert_that(executed_docstring_path.allure_report,
                has_test_case("test_parametrized_dynamic_feature[{feature}]".format(feature=feature),
                              has_feature(feature),
                              )
                )
