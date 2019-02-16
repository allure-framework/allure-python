""" ./examples/attachment/attachment_step.rst """

from hamcrest import assert_that
from allure_commons_test.report import has_test_case
from allure_commons_test.result import has_step
from allure_commons_test.result import has_attachment


def test_step_with_attachment(executed_docstring_path):
    assert_that(executed_docstring_path.allure_report,
                has_test_case("test_step_with_attachment",
                              has_step("step_with_attachment",
                                       has_attachment()
                                       ),
                              )
                )
