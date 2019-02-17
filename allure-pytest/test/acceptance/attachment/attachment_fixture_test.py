""" ./examples/attachment/attachment_fixture.rst """

from hamcrest import assert_that
from allure_commons_test.report import has_test_case
from allure_commons_test.result import has_attachment
from allure_commons_test.container import has_container
from allure_commons_test.container import has_before
from allure_commons_test.container import has_after


def test_fixture_attachment(executed_docstring_path):
    assert_that(executed_docstring_path.allure_report,
                has_test_case("test_fixture_attachment",
                              has_container(executed_docstring_path.allure_report,
                                            has_before("fixture_with_attachment",
                                                       has_attachment()
                                                       )
                                            )
                              )
                )


def test_fixture_finalizer_attachment(executed_docstring_path):
    assert_that(executed_docstring_path.allure_report,
                has_test_case("test_fixture_finalizer_attachment",
                              has_container(executed_docstring_path.allure_report,
                                            has_after("fixture_with_attachment_in_finalizer::finalizer",
                                                      has_attachment()
                                                      )
                                            )
                              )
                )
