import pytest
from hamcrest import assert_that
from hamcrest import all_of, is_, is_not
from hamcrest import has_property, has_value
from hamcrest import contains_string
from tests.allure_pytest.pytest_runner import AllurePytestRunner


@pytest.mark.parametrize("capture", ["sys", "fd", "no"])
def test_capture_stdout_in_bdd(allure_pytest_bdd_runner: AllurePytestRunner, capture):
    feature_content = (
        """
        Feature: Basic allure-pytest-bdd usage
            Scenario: Simple passed example
                Given the preconditions are satisfied
                When the action is invoked
                Then the postconditions are held
        """
    )
    steps_content = (
        """
        from pytest_bdd import scenario, given, when, then
        @scenario("scenario.feature", "Simple passed example")
        def test_scenario_passes():
            pass

        @given("the preconditions are satisfied")
        def given_the_preconditions_are_satisfied():
            print("Print from given step")

        @when("the action is invoked")
        def when_the_action_is_invoked():
            print("Print from when step")

        @then("the postconditions are held")
        def then_the_postconditions_are_held():
            print("Print from then step")
        """
    )

    allure_results = allure_pytest_bdd_runner.run_pytest(
        ("scenario.feature", feature_content),
        steps_content, cli_args=(f"--capture={capture}",)
    )
    if_pytest_capture_ = is_not if capture == "no" else is_

    assert_that(
        allure_results,
        has_property(
            "attachments",
            all_of(
                if_pytest_capture_(has_value(contains_string("Print from given step"))),
                if_pytest_capture_(has_value(contains_string("Print from when step"))),
                if_pytest_capture_(has_value(contains_string("Print from then step")))
            )
        )
    )


# @pytest.mark.parametrize("capture", ["sys", "fd"])
# def test_capture_empty_stdout(allure_pytest_runner: AllurePytestRunner, capture):
#     """
#     >>> import pytest
#     >>> import allure
#
#     >>> @pytest.fixture
#     ... def fixture(request):
#     ...     def finalizer():
#     ...         pass
#     ...     request.addfinalizer(finalizer)
#
#     >>> def test_capture_stdout_example(fixture):
#     ...     with allure.step("Step"):
#     ...         pass
#     """
#
#     allure_results = allure_pytest_runner.run_docstring(f"--capture={capture}")
#
#     assert_that(
#         allure_results,
#         has_property("attachments", empty())
#     )
#
#
# @pytest.mark.parametrize("logging", [True, False])
# def test_capture_log(allure_pytest_runner: AllurePytestRunner, logging):
#     """
#     >>> import logging
#     >>> import pytest
#     >>> import allure
#
#     >>> logger = logging.getLogger(__name__)
#
#     >>> @pytest.fixture
#     ... def fixture(request):
#     ...     logger.info("Start fixture")
#     ...     def finalizer():
#     ...         logger.info("Stop fixture")
#     ...     request.addfinalizer(finalizer)
#
#     >>> def test_capture_log_example(fixture):
#     ...     logger.info("Start test")
#     ...     with allure.step("Step"):
#     ...         logger.info("Start step")
#     """
#
#     params = [] if logging else ["-p", "no:logging"]
#     allure_results = allure_pytest_runner.run_docstring(
#         "--log-level=INFO",
#         *params
#     )
#
#     if_logging_ = is_ if logging else is_not
#
#     assert_that(
#         allure_results,
#         has_property(
#             "attachments",
#             all_of(
#                 if_logging_(has_value(contains_string("Start fixture"))),
#                 if_logging_(has_value(contains_string("Stop fixture"))),
#                 if_logging_(has_value(contains_string("Start test"))),
#                 if_logging_(has_value(contains_string("Start step")))
#             )
#         )
#     )
#
#
# def test_capture_disabled(allure_pytest_runner: AllurePytestRunner):
#     """
#     >>> import logging
#     >>> logger = logging.getLogger(__name__)
#
#     >>> def test_capture_disabled_example():
#     ...     logger.info("Start logging")
#     ...     #print ("Start printing")
#
#     """
#
#     allure_results = allure_pytest_runner.run_docstring(
#         "--log-level=INFO",
#         "--allure-no-capture"
#     )
#
#     assert_that(
#         allure_results,
#         has_property("attachments", empty())
#     )
