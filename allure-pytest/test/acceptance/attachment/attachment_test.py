""" ./examples/attachment/attachment.rst """

from hamcrest import assert_that
from allure_commons_test.report import has_test_case
from allure_commons_test.result import has_attachment


def test_attach_body_with_default_kwargs(executed_docstring_path):
    assert_that(executed_docstring_path.allure_report,
                has_test_case("test_attach_body_with_default_kwargs",
                              has_attachment()
                              )
                )


def test_attach_body(executed_docstring_path):
    assert_that(executed_docstring_path.allure_report,
                has_test_case("test_attach_body",
                              has_attachment(attach_type="application/xml", name="some attachment name")
                              )
                )


def test_attach_file(executed_docstring_path):
    assert_that(executed_docstring_path.allure_report,
                has_test_case("test_attach_file",
                              has_attachment()
                              )
                )
