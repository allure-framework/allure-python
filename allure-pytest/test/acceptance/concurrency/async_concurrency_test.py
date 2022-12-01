from hamcrest import assert_that, has_entry, has_length, all_of, has_property
from allure_commons_test.report import has_test_case
from allure_commons_test.report import has_only_n_test_cases
from allure_commons_test.result import has_step
from allure_commons_test.result import with_status

def test_asyncio_concurrent_steps(executed_docstring_source):
    """
    >>> import allure
    >>> import asyncio

    >>> async def run_steps(name, to_set, to_wait):
    ...     with allure.step(f"{name}-step"):
    ...         to_set.set()
    ...         await to_wait.wait()

    >>> async def run_tasks():
    ...     task1_fence = asyncio.Event()
    ...     task2_fence = asyncio.Event()
    ...     await asyncio.gather(
    ...         run_steps("task1", task2_fence, task1_fence),
    ...         run_steps("task2", task1_fence, task2_fence)
    ...     )

    >>> def test_asyncio_concurrency():
    ...     asyncio.get_event_loop().run_until_complete(
    ...         run_tasks()
    ...     )
    """

    assert_that(
        executed_docstring_source.allure_report,
        has_only_n_test_cases(
            "test_asyncio_concurrency",
            1,
            with_status("passed"),
            has_entry("steps", has_length(2)),
            has_step(
                "task1-step",
                with_status("passed")
            ),
            has_step(
                "task2-step",
                with_status("passed")
            )
        ),
        "Should contain a single test with two non-nested steps"
    )


def test_async_concurrent_tests(allured_testdir):
    """
    >>> import allure
    >>> import pytest
    ... import asyncio

    >>> @pytest.fixture(scope="module")
    ... async def event():
    ...     return asyncio.Event()

    >>> @pytest.mark.asyncio_cooperative
    >>> async def test_async_concurrency_fn1(event):
    ...     with allure.step("Step of fn1"):
    ...         await event.wait()

    >>> @pytest.mark.asyncio_cooperative
    >>> async def test_async_concurrency_fn2(event):
    ...     with allure.step("Step of fn2"):
    ...         event.set()
    """

    allured_testdir.parse_docstring_source()
    allured_testdir.run_with_allure("-q", "-p", "asyncio-cooperative")

    assert_that(
        allured_testdir.allure_report,
        all_of(
            has_property("test_cases", has_length(2)),
            has_test_case(
                "test_async_concurrency_fn1",
                with_status("passed"),
                has_entry("steps", has_length(1)),
                has_step(
                    "Step of fn1",
                    with_status("passed")
                )
            ),
            has_test_case(
                "test_async_concurrency_fn2",
                with_status("passed"),
                has_entry("steps", has_length(1)),
                has_step(
                    "Step of fn2",
                    with_status("passed")
                )
            )
        ),
        "Should contain two passed tests cases with two steps each"
    )