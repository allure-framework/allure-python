import os
import pytest
from hamcrest import assert_that, not_

from tests.allure_pytest.pytest_runner import AllurePytestRunner
from allure_commons_test.report import has_test_case
from allure_commons_test.result import has_attachment

pytest.importorskip("playwright", reason="playwright is not installed")

# Capture the real home dir before pytester changes HOME to a tmpdir.
_REAL_HOME = os.path.expanduser("~")
_BROWSERS_PATH = os.path.join(_REAL_HOME, ".cache", "ms-playwright")


@pytest.fixture
def playwright_runner(allure_pytest_runner: AllurePytestRunner, monkeypatch):
    monkeypatch.setenv("PLAYWRIGHT_BROWSERS_PATH", _BROWSERS_PATH)
    allure_pytest_runner.enable_plugins("playwright", "base_url")
    yield allure_pytest_runner


_PAGE_TEST = """
def test_playwright_trace(page):
    page.goto("about:blank")
"""

_PAGE_TEST_FAILING = """
def test_playwright_trace_failing(page):
    page.goto("about:blank")
    assert False
"""


def test_trace_attached_when_tracing_on(playwright_runner: AllurePytestRunner):
    output = playwright_runner.run_pytest(
        _PAGE_TEST,
        cli_args=["--tracing", "on", "--browser", "chromium"],
    )

    assert_that(
        output,
        has_test_case(
            "test_playwright_trace",
            has_attachment(attach_type="application/vnd.allure.playwright-trace"),
        )
    )


def test_trace_attached_on_failure_with_retain_on_failure(playwright_runner: AllurePytestRunner):
    output = playwright_runner.run_pytest(
        _PAGE_TEST_FAILING,
        cli_args=["--tracing", "retain-on-failure", "--browser", "chromium"],
    )

    assert_that(
        output,
        has_test_case(
            "test_playwright_trace_failing",
            has_attachment(attach_type="application/vnd.allure.playwright-trace"),
        )
    )


def test_trace_not_attached_on_pass_with_retain_on_failure(playwright_runner: AllurePytestRunner):
    output = playwright_runner.run_pytest(
        _PAGE_TEST,
        cli_args=["--tracing", "retain-on-failure", "--browser", "chromium"],
    )

    assert_that(
        output,
        has_test_case(
            "test_playwright_trace",
            not_(has_attachment(attach_type="application/vnd.allure.playwright-trace")),
        )
    )


def test_trace_not_attached_when_tracing_off(playwright_runner: AllurePytestRunner):
    output = playwright_runner.run_pytest(
        _PAGE_TEST,
        cli_args=["--tracing", "off", "--browser", "chromium"],
    )

    assert_that(
        output,
        has_test_case(
            "test_playwright_trace",
            not_(has_attachment(attach_type="application/vnd.allure.playwright-trace")),
        )
    )
