""" ./allure-pytest/examples/attachment/attachment.rst """

from hamcrest import assert_that
from tests.allure_pytest.pytest_runner import AllurePytestRunner

from allure_commons_test.report import has_test_case
from allure_commons_test.result import has_attachment


def test_attach_body_with_default_kwargs(allure_pytest_runner: AllurePytestRunner):
    allure_results = allure_pytest_runner.run_docpath_examples(cache=True)

    assert_that(
        allure_results,
        has_test_case(
            "test_attach_body_with_default_kwargs",
            has_attachment()
        )
    )


def test_attach_body(allure_pytest_runner: AllurePytestRunner):
    allure_results = allure_pytest_runner.run_docpath_examples(cache=True)

    assert_that(
        allure_results,
        has_test_case(
            "test_attach_body",
            has_attachment(
                attach_type="application/xml",
                name="some attachment name"
            )
        )
    )


def test_attach_file(allure_pytest_runner: AllurePytestRunner):
    allure_results = allure_pytest_runner.run_docpath_examples(cache=True)

    assert_that(
        allure_results,
        has_test_case(
            "test_attach_file",
            has_attachment()
        )
    )
