import pytest
from hamcrest import assert_that
from hamcrest import all_of, is_, is_not, empty
from hamcrest import has_property, has_value
from hamcrest import contains_string
from tests.allure_pytest.pytest_runner import AllurePytestRunner


@pytest.mark.parametrize("capture", ["sys", "fd", "no"])
def test_capture_stdout(allure_pytest_runner: AllurePytestRunner, capture):
    """
    >>> import pytest
    >>> import allure

    >>> @pytest.fixture
    ... def fixture(request):
    ...     print ("Start fixture")
    ...     def finalizer():
    ...         print ("Stop fixture")
    ...     request.addfinalizer(finalizer)

    >>> def test_capture_stdout_example(fixture):
    ...     print ("Start test")
    ...     with allure.step("Step"):
    ...         print ("Start step")
    """

    allure_results = allure_pytest_runner.run_docstring(f"--capture={capture}")

    if_pytest_capture_ = is_not if capture == "no" else is_

    assert_that(
        allure_results,
        has_property(
            "attachments",
            all_of(
                if_pytest_capture_(has_value(contains_string("Start fixture"))),
                if_pytest_capture_(has_value(contains_string("Stop fixture"))),
                if_pytest_capture_(has_value(contains_string("Start test"))),
                if_pytest_capture_(has_value(contains_string("Start step")))
            )
        )
    )


@pytest.mark.parametrize("capture", ["sys", "fd"])
def test_capture_empty_stdout(allure_pytest_runner: AllurePytestRunner, capture):
    """
    >>> import pytest
    >>> import allure

    >>> @pytest.fixture
    ... def fixture(request):
    ...     def finalizer():
    ...         pass
    ...     request.addfinalizer(finalizer)

    >>> def test_capture_stdout_example(fixture):
    ...     with allure.step("Step"):
    ...         pass
    """

    allure_results = allure_pytest_runner.run_docstring(f"--capture={capture}")

    assert_that(
        allure_results,
        has_property("attachments", empty())
    )


@pytest.mark.parametrize("logging", [True, False])
def test_capture_log(allure_pytest_runner: AllurePytestRunner, logging):
    """
    >>> import logging
    >>> import pytest
    >>> import allure

    >>> logger = logging.getLogger(__name__)

    >>> @pytest.fixture
    ... def fixture(request):
    ...     logger.info("Start fixture")
    ...     def finalizer():
    ...         logger.info("Stop fixture")
    ...     request.addfinalizer(finalizer)

    >>> def test_capture_log_example(fixture):
    ...     logger.info("Start test")
    ...     with allure.step("Step"):
    ...         logger.info("Start step")
    """

    log_level = "INFO" if logging else "WARNING"
    allure_results = allure_pytest_runner.run_docstring(
        f"--log-level={log_level}",
    )

    if_logging_ = is_ if logging else is_not

    assert_that(
        allure_results,
        has_property(
            "attachments",
            all_of(
                if_logging_(has_value(contains_string("Start fixture"))),
                if_logging_(has_value(contains_string("Stop fixture"))),
                if_logging_(has_value(contains_string("Start test"))),
                if_logging_(has_value(contains_string("Start step")))
            )
        )
    )


def test_capture_disabled(allure_pytest_runner: AllurePytestRunner):
    """
    >>> import logging
    >>> logger = logging.getLogger(__name__)

    >>> def test_capture_disabled_example():
    ...     logger.info("Start logging")
    ...     #print ("Start printing")

    """

    allure_results = allure_pytest_runner.run_docstring(
        "--log-level=INFO",
        "--allure-no-capture"
    )

    assert_that(
        allure_results,
        has_property("attachments", empty())
    )
