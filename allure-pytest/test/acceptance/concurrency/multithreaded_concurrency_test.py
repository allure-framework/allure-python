from concurrent.futures import ThreadPoolExecutor
from hamcrest import assert_that, has_entry, has_length, has_property, all_of
from allure_commons.logger import AllureMemoryLogger
import allure_pytest
from ...conftest import fake_logger
import allure_commons
from allure_commons_test.report import has_test_case
from allure_commons_test.result import has_step
from allure_commons_test.result import with_status


def test_concurrent_mt_pytest_runs(allured_testdir, monkeypatch):
    """
    >>> import allure
    >>> import pytest

    >>> @pytest.mark.thread1
    ... def test_multithreaded_concurrency_fn1():
    ...     with allure.step("Step 1 of test 1"):
    ...         pass
    ...     with allure.step("Step 2 of test 1"):
    ...         pass

    >>> @pytest.mark.thread2
    ... def test_multithreaded_concurrency_fn2():
    ...     with allure.step("Step 1 of test 2"):
    ...         pass
    ...     with allure.step("Step 2 of test 2"):
    ...         pass
    """

    thread_pool = ThreadPoolExecutor(max_workers=2)

    allured_testdir.parse_docstring_source()
    allured_testdir.allure_report = AllureMemoryLogger()

    original_register = allure_commons.plugin_manager.register

    def register_nothrow(*args, **kwargs):
        try:
            return original_register(*args, **kwargs)
        except Exception:
            pass

    monkeypatch.setattr(allure_commons.plugin_manager, "register", register_nothrow)

    original_cleanup_factory = allure_pytest.plugin.cleanup_factory

    def cleanup_factory_nothrow(*args, **kwargs):
        cleanup = original_cleanup_factory(*args, **kwargs)

        def wrapped_cleanup():
            try:
                cleanup()
            except Exception:
                pass
        return wrapped_cleanup

    monkeypatch.setattr(allure_pytest.plugin, "cleanup_factory", cleanup_factory_nothrow)

    with fake_logger("allure_pytest.plugin.AllureFileLogger", allured_testdir.allure_report):
        for n in [1, 2]:
            thread_pool.submit(
                allured_testdir.testdir.runpytest,
                "--alluredir",
                allured_testdir.testdir.tmpdir,
                "-m",
                f"thread{n}",
                "--disable-warnings",
                "-q"
            )
        thread_pool.shutdown(True)

    assert_that(
        allured_testdir.allure_report,
        all_of(
            has_property("test_cases", has_length(2)),
            has_test_case(
                "test_multithreaded_concurrency_fn1",
                with_status("passed"),
                has_entry("steps", has_length(2)),
                has_step(
                    "Step 1 of test 1",
                    with_status("passed")
                ),
                has_step(
                    "Step 2 of test 1",
                    with_status("passed")
                )
            ),
            has_test_case(
                "test_multithreaded_concurrency_fn2",
                with_status("passed"),
                has_entry("steps", has_length(2)),
                has_step(
                    "Step 1 of test 2",
                    with_status("passed")
                ),
                has_step(
                    "Step 2 of test 2",
                    with_status("passed")
                )
            )
        ),
        "Should contain two passed tests cases with two steps each"
    )
