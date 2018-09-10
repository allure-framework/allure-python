import logging
import pytest


logger = logging.getLogger(__name__)


@pytest.fixture
def fix1():
    # Just for checking capture in fixtures
    print("fix setup")
    logger.info("fix setup")
    yield
    logger.info("fix teardown")
    print("fix teardown")


def test_capture_disabled(fix1):
    """
    >>> allure_report = getfixture('allure_report_with_params')('--log-cli-level=INFO', '--allure-no-capture')

    >>> attachment_names = []

    >>> test = None
    >>> for item in allure_report.test_cases:
    ...     if item["name"] == "test_capture_disabled":
    ...         test = item

    >>> assert "attachments" not in test
    """
    print("begin test")
    logger.info("something in test")
    print("end test")
