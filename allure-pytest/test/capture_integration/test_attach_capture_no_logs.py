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


def test_capture_stdout_no_logs(fix1):
    """
    >>> import os
    >>> allure_report = getfixture('allure_report_with_params')('--log-cli-level=INFO', '-p no:logging')

    >>> attachment_names = []

    >>> test = None
    >>> for item in allure_report.test_cases:
    ...     if item["name"] == "test_capture_stdout_no_logs":
    ...         test = item

    >>> for attachment in test["attachments"]:
    ...     name = attachment["name"]
    ...     source = os.path.join(allure_report.result_dir, attachment["source"])
    ...     attachment_names.append(name)
    ...     if name == "stdout":
    ...         with open(source, "r") as f:
    ...             capstdout = f.read()
    ...         assert "fix setup" in capstdout
    ...         assert "begin test" in capstdout
    ...         assert "end test" in capstdout
    ...         assert "fix teardown" in capstdout
    ...     elif name == "log":
    ...         with open(source, "r") as f:
    ...             caplog = f.read()
    ...         assert caplog == ""

    >>> assert "stdout" in attachment_names
    >>> assert "stderr" in attachment_names
    >>> assert "log" in attachment_names
    """
    print("begin test")
    logger.info("something in test")
    print("end test")

