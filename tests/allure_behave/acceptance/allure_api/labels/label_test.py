""" ./allure-behave/examples/label.rst """

from tests.allure_behave.behave_runner import AllureBehaveRunner
from hamcrest import assert_that
from allure_commons_test.report import has_test_case
from allure_commons_test.result import with_status
from allure_commons_test.label import has_label


def test_label_from_feature_file(behave_runner: AllureBehaveRunner):
    behave_runner.run_behave(
        feature_rst_ids=["label-feature"],
        step_literals=["given('noop')(lambda c:None)"]
    )
    assert_that(
        behave_runner.allure_results,
        has_test_case(
            "Scenario marked with an author label",
            with_status("passed"),
            has_label("author", "John-Doe")
        )
    )
